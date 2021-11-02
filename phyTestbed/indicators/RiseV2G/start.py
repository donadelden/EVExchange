"""
This script is a wrapper for RiseV2G.
It adds the chance to perform an action when starting and stopping the energy delivery.
This script must be placed in the same folder as RiseV2G.
@author Denis Donadel
"""
import argparse
import asyncio
import atexit
import time

START_COMMAND = b"ChargingStatusRes"  # this is the command that it is used to start the charging
STOP_COMMAND = b"SessionStopRes"  # this for stopping
WAITING_START_COMMAND = b"TCPServer: TCP server initialized at link-local address"
RASPBERRY = True  # if you are working on a Raspberry you can set this parameters to trigger a LED
if RASPBERRY:
    import RPi.GPIO as GPIO
    # set the GPIO number (not the PIN number).
    # See here: https://www.theengineeringprojects.com/wp-content/uploads/2021/03/raspberry-pi-4.png
    CHARGING_LED_GPIO_PIN = 26  # pin for Yellow (SE) and Green (EV) LEDs
    SE_READY_LED_GPIO_PIN = 19  # pin for Blue LED on SE
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHARGING_LED_GPIO_PIN, GPIO.OUT)
    GPIO.setup(SE_READY_LED_GPIO_PIN, GPIO.OUT)

device_type = ""  # global variable to get the type of device (ev or se)
is_charging = False  # global variable for maintain the charging status


def processLine(line, verbose):
    global is_charging, device_type
    if verbose:
        print(line.decode('utf-8'), end="", flush=True)

    # catch start of waiting
    if WAITING_START_COMMAND in line and device_type == "se":
        print("************* START WAITING **************")
        if RASPBERRY: GPIO.output(SE_READY_LED_GPIO_PIN, GPIO.HIGH)

    # catch start of charging
    if not is_charging and START_COMMAND in line:
        is_charging = True
        print("************* START CHARGING **************")
        if RASPBERRY: GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.HIGH)
    # catch stop charging
    elif is_charging and STOP_COMMAND in line:
        is_charging = False
        if RASPBERRY:
            time.sleep(10)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
        print("************* STOP CHARGING **************")


def processErrorLine(line, verbose):
    global is_charging
    if verbose:
        print(f"STDERR: {line.decode('utf-8')}", end="", flush=True)

    # if error during charging, stop it
    if is_charging:
        print("************* ERROR: STOP CHARGING **************")
        if RASPBERRY:  # if error, the led blinks and the stops
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
            time.sleep(1)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
        is_charging = False


async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    process = await asyncio.create_subprocess_exec(*cmd,
                                                   stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb)
    ])
    return await process.wait()


def execute(cmd, stdout_cb, stderr_cb):
    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(
        _stream_subprocess(
            cmd,
            stdout_cb,
            stderr_cb,
        ))
    loop.close()
    return rc


def exit_handler():
    """
    Handle a premature (i.e., CTRL+C) exit
    """
    global device_type
    if is_charging:
        print("************* FORCED EXIT: STOP CHARGING **************")
        if RASPBERRY:  # if error, the LED blinks and then stops
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
            time.sleep(.8)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.HIGH)
            time.sleep(.8)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
            time.sleep(.8)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.HIGH)
            time.sleep(.8)
            GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
    if device_type == "se": print("************* STOP WAITING **************")
    if RASPBERRY:  # clean GPIO if rpi is used
        if device_type == "se": GPIO.output(SE_READY_LED_GPIO_PIN, GPIO.LOW)
        GPIO.output(CHARGING_LED_GPIO_PIN, GPIO.LOW)
        GPIO.cleanup()


# Set the atexit handler
atexit.register(exit_handler)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Wrapper for starting EV or SE.')
    parser.add_argument('type', type=str, choices=["ev", "se"],
                        help='ev or se based on what you want to start')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_const',
                        const=True, default=False,
                        help='Print the log of RiseV2G (default: False')

    args = parser.parse_args()
    verbose = args.verbose
    device_type = args.type

    COMMAND = f"java -jar ./rise-v2g-{device_type}cc-1.2.6.jar"

    execute(
        COMMAND.split(),
        lambda x: processLine(x, verbose=verbose),
        lambda x: processErrorLine(x, verbose=verbose),
    )

    #if RASPBERRY:  # clean GPIO if rpi is used (it will be done by atexit handler anyway)
    #    GPIO.cleanup()
