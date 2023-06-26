from time import sleep
import RPi.GPIO as GPIO
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)

print('Initialization Completed')

i = 0
while i<20:

    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to LOW - Controller Enabled')
    sleep(2)
    GPIO.output(ENA, GPIO.HIGH)
    print('ENA set to HIGH - Controller Disabled')
    sleep(2) # pause for possible change direction
    i += 1


