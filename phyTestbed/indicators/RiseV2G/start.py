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
import sys

START_COMMAND = b"ChargingStatusRes"  # this is the command that it is used to start the charging
STOP_COMMAND = b"SessionStopRes"  # this for stopping
RASPBERRY = True  # if you are working on a Raspberry you can set this parameters to trigger a LED
if RASPBERRY:
    import RPi.GPIO as GPIO
    LED_GPIO_PIN = 26  # set the GPIO number (not the PIN number). See here: https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GPIO_PIN, GPIO.OUT)

is_charging = False  # global GPIO.setmode(GPIO.BCM)variable for maintain the charging status

def processLine(line, verbose):
    global is_charging
    if verbose:
        print(line.decode('utf-8'), end="", flush=True)

    # catch start of charging
    if not is_charging and START_COMMAND in line:
        is_charging = True
        print("************* START CHARGING **************")
        if RASPBERRY: GPIO.output(LED_GPIO_PIN, GPIO.HIGH)
    # catch stop charging
    elif is_charging and STOP_COMMAND in line:
        is_charging = False
        print("************* STOP CHARGING **************")
        if RASPBERRY: GPIO.output(LED_GPIO_PIN, GPIO.LOW)


def processErrorLine(line, verbose):
    global is_charging
    if verbose:
        print(f"STDERR: {line.decode('utf-8')}", end="", flush=True)

    # if error during charging, stop it
    if is_charging:
        print("************* ERROR: STOP CHARGING **************")
        if RASPBERRY:  # if error, the led blinks and the stops
            GPIO.output(LED_GPIO_PIN, GPIO.LOW)
            time.sleep(1)
            GPIO.output(LED_GPIO_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_GPIO_PIN, GPIO.LOW)
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
    if is_charging:
        print("************* FORCED EXIT: STOP CHARGING **************")
        if RASPBERRY:  # if error, the led blinks and the stops
            GPIO.output(LED_GPIO_PIN, GPIO.LOW)
            time.sleep(1)
            GPIO.output(LED_GPIO_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_GPIO_PIN, GPIO.LOW)
    if RASPBERRY:  # clean GPIO if rpi is used
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

    COMMAND = f"java -jar ./rise-v2g-{args.type}cc-1.2.6.jar"

    execute(
        COMMAND.split(),
        lambda x: processLine(x, verbose=verbose),
        lambda x: processErrorLine(x, verbose=verbose),
    )

    if RASPBERRY:  # clean GPIO if rpi is used
        GPIO.cleanup()
