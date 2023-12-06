from gpiozero import Motor
from time import sleep

# Definieren Sie die Pins für die Steuerung des ersten Motors (M1)
motor1 = Motor(forward=19, backward=16)

# Definieren Sie die Pins für die Steuerung des zweiten Motors (M2)
motor2 = Motor(forward=26, backward=20)

def move_forward():
    print("Vorwärts")
    motor1.forward()
    motor2.forward()
    sleep(2)
    motor1.stop()
    motor2.stop()

def move_backward():
    print("Rückwärts")
    motor1.backward()
    #otor2.backward()
    sleep(2)
    motor1.stop()
    motor2.stop()

def turn_left():
    print("Links drehen")
    motor1.forward()
    motor2.backward()
    sleep(2)
    motor1.stop()
    motor2.stop()

def turn_right():
    print("Rechts drehen")
    motor1.backward()
    motor2.forward()
    sleep(2)
    motor1.stop()
    motor2.stop()

try:
    while True:
        move_forward()
        move_backward()
        turn_left()
        turn_right()

except KeyboardInterrupt:
    motor1.stop()
    motor2.stop()
