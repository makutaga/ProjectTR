#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

pin_a1 = 19
pin_a2 = 15
pin_b1 = 13
pin_b2 = 11
pinb_a1 = 37
pinb_a2 = 35
pinb_b1 = 33
pinb_b2 = 31
pins = [pin_a1, pin_a2, pin_b1, pin_b2, pinb_a1, pinb_a2, pinb_b1, pinb_b2]

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
		self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def motor_rotate(pin1, pin2, vel):
	if vel > 0:
		GPIO.output(pin1, GPIO.HIGH)
		GPIO.output(pin2, GPIO.LOW)
	elif vel < 0:
		GPIO.output(pin1, GPIO.LOW)
		GPIO.output(pin2, GPIO.HIGH)
	else:
		GPIO.output(pin1, GPIO.LOW)
		GPIO.output(pin2, GPIO.LOW)

def move_forward():
	motor_rotate(pin_a1, pin_a2, 1)
	motor_rotate(pin_b1, pin_b2, 1)

def move_back():
	motor_rotate(pin_a1, pin_a2, -1)
	motor_rotate(pin_b1, pin_b2, -1)

def move_stop():
	motor_rotate(pin_a1, pin_a2, 0)
	motor_rotate(pin_b1, pin_b2, 0)

def turn_right():
	motor_rotate(pin_a1, pin_a2, 1)
	motor_rotate(pin_b1, pin_b2, -1)

def turn_left():
	motor_rotate(pin_a1, pin_a2, -1)
	motor_rotate(pin_b1, pin_b2, 1)

def aux_up():
	motor_rotate(pinb_b1, pinb_b2, 1)

def aux_down():
	motor_rotate(pinb_b1, pinb_b2, -1)

def aux_stop():
	motor_rotate(pinb_b1, pinb_b2, 0)

if __name__ == "__main__":
	getch = _Getch()
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

	try:
		while 1:

			key = getch()
			print key

			if key == "w":
				print "Forward"
				move_forward()
			elif key == "z":
				print "Back"
				move_back()
			elif key == "a":
				print "Left"
				turn_left()
			elif key == "s":
				print "Right"
				turn_right()
			elif key == "e":
				print "Up"
				aux_up()
			elif key == "x":
				print "Down"
				aux_down()
			elif key == "q":
				break
			else:
				move_stop()
				aux_stop()

			time.sleep(0.2)


	except KeyboardInterrupt:
		pass

	GPIO.cleanup()
