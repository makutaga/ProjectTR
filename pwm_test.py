#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

pinA_a1 = 19
pinA_a2 = 15
pinA_b1 = 13
pinA_b2 = 11
pinB_a1 = 37
pinB_a2 = 35
pinB_b1 = 33
pinB_b2 = 31
pins = [pinA_a1, pinA_a2, pinA_b1, pinA_b2, pinB_a1, pinB_a2, pinB_b1, pinB_b2]
pinA_a_enable = pinA_a2
pinA_a_phase  = pinA_a1
pinA_b_enable = pinA_b2
pinA_b_phase  = pinA_b1
pinB_a_enable = pinB_a2
pinB_a_phase  = pinB_a1
pinB_b_enable = pinB_b2
pinB_b_phase  = pinB_b1

pwm_freq = 1000
pwm_limit = 95

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

class PWMMotor:
	def __init__(self, pin_phase, pin_enable, freq=1000):
		self.p_phase = pin_phase
		self.p_enable = pin_enable
		self.pwm_freq = freq
		self.pwm_limit = 100
		self.duty = 0.0
		self.pwm = GPIO.PWM(self.p_enable, self.pwm_freq)
		self.pwm.start(self.duty)
	def rotate(self, vel):
		if vel >= 0:
			GPIO.output(self.p_phase, GPIO.LOW)
		elif vel < 0:
			GPIO.output(self.p_phase, GPIO.HIGH)
			vel = -vel
		self.duty = vel
		if (self.duty > self.pwm_limit):
			self.duty =self.pwm_limit
		self.pwm.ChangeDutyCycle(self.duty)

class Locomotor:
	def __init__(self, mt_left, mt_right):
		self.motor_left = mt_left
		self.motor_right = mt_right
	def move(self, vel_l, vel_r):
		self.motor_left.rotate(vel_l)
		self.motor_right.rotate(vel_r)
	def move_forward(self, vel):
		self.move(vel, vel)
	def move_back(self, vel):
		self.move(-vel, -vel)
	def stop(self):
		self.move(0, 0)
	def move_circle(self, vel):
		self.move(vel, vel * 0.4)
	def move_eight(self, vel):
		self.move(vel, vel * 0.4)
		time.sleep(8)
		self.move(vel * 0.4, vel)
		time.sleep(8)
		self.stop()
		

if __name__ == "__main__":
	getch = _Getch()
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

	mt_left = PWMMotor(pinA_a_phase, pinA_a_enable, pwm_freq)
	mt_right = PWMMotor(pinA_b_phase, pinA_b_enable, pwm_freq)
	mt_dummy = PWMMotor(pinB_a_phase, pinB_a_enable, pwm_freq)
	mt_arm = PWMMotor(pinB_b_phase, pinB_b_enable, pwm_freq)

	loc = Locomotor(mt_left, mt_right)
	vel_normal = pwm_limit * 0.5
	vel_high = pwm_limit * 0.8
	vel_arm = pwm_limit * 0.4

	try:
		while 1:

			key = getch()
			print key

			mt_arm.rotate(0)
			if key == "W":
				print "Forward (Fast)"
				loc.move_forward(vel_high)
			elif key == "w":
				print "Forward"
				loc.move_forward(vel_normal)
			elif key == "Z":
				print "Back (Fast)"
				loc.move_back(vel_high)
			elif key == "z":
				print "Back"
				loc.move_back(vel_normal)
			elif key == "A":
				print "Left"
				loc.move(-vel_normal, vel_normal)
			elif key == "a":
				print "Left"
				loc.move(0, vel_normal)
			elif key == "S":
				print "Right"
				loc.move(vel_normal, -vel_normal)
			elif key == "s":
				print "Right"
				loc.move(vel_normal, 0)
			elif key == "e":
				print "Up"
				loc.stop()
				mt_arm.rotate(vel_arm)
			elif key == "x":
				print "Down"
				loc.stop()
				mt_arm.rotate(-vel_arm)
			elif key == "c":
				loc.move_circle(vel_high)
			elif key == "8":
				loc.move_eight(vel_high)
			elif key == "q":
				break
			else:
				loc.stop()
				mt_arm.rotate(0)

			time.sleep(0.2)


	except KeyboardInterrupt:
		pass

	GPIO.cleanup()
