import RPi.GPIO as GPIO
import curses
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pins you are using
relay_2 = 20
speed_1 = 19
relay_1 = 26
speed_2 = 16


GPIO.setup(relay_1, GPIO.OUT)
GPIO.setup(relay_2, GPIO.OUT)
GPIO.setup(speed_1, GPIO.OUT)
GPIO.setup(speed_2, GPIO.OUT)

def forward():
    GPIO.output(speed_1, GPIO.HIGH)
    GPIO.output(speed_2, GPIO.HIGH)
    GPIO.output(relay_1, GPIO.LOW)
    GPIO.output(relay_2, GPIO.LOW)
    time.sleep(1)  # Adjust sleep time as needed

def backward():
    GPIO.output(speed_1, GPIO.HIGH)
    GPIO.output(speed_2, GPIO.HIGH)
    GPIO.output(relay_1, GPIO.HIGH)
    GPIO.output(relay_2, GPIO.HIGH)
    time.sleep(1)  # Adjust sleep time as needed

def right():
    GPIO.output(speed_1, GPIO.HIGH)
    GPIO.output(speed_2, GPIO.HIGH)
    GPIO.output(relay_1, GPIO.HIGH)
    GPIO.output(relay_2, GPIO.LOW)
    time.sleep(1)  # Adjust sleep time as needed

def left():
    GPIO.output(speed_1, GPIO.HIGH)
    GPIO.output(speed_2, GPIO.HIGH)
    GPIO.output(relay_1, GPIO.LOW)
    GPIO.output(relay_2, GPIO.HIGH)
    time.sleep(1)  # Adjust sleep time as needed

def stop():
    GPIO.output(speed_1, GPIO.LOW)
    GPIO.output(speed_2, GPIO.LOW)
    GPIO.output(relay_1, GPIO.LOW)
    GPIO.output(relay_2, GPIO.LOW)

try:
    screen = curses.initscr()
    curses.cbreak()
    screen.keypad(1)
    key = ''
    while key != ord('q'):  # press <Q> to exit the program
        key = screen.getch()  # get the key
        screen.addch(0, 0, key)  # display it on the screen
        screen.refresh()

        # Check the pressed key and take action accordingly
        if key == curses.KEY_UP:
            screen.addstr(0, 0, "Up")
            forward()
        elif key == curses.KEY_DOWN:
            screen.addstr(0, 0, "Down")
            backward()
        elif key == curses.KEY_LEFT:
            screen.addstr(0, 0, "Left")
            left()
        elif key == curses.KEY_RIGHT:
            screen.addstr(0, 0, "Right")
            right()
        elif key == ord('s'):  # Press 's' to stop
            screen.addstr(0, 0, "Stop")
            stop()

finally:
    curses.endwin()  # Clean up curses on exit
    GPIO.cleanup()  # Clean up GPIO on exit
