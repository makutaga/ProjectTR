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

pwm_freq = 100
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
	def __init__(self, pin_phase, pin_enable, freq=60):
		self.p_phase = pin_phase
		self.p_enable = pin_enable
		self.pwm_freq = freq
		self.pwm_limit = 100
		self.duty = 0.0
		self.pwm = GPIO.PWM(self.p_phase, self.pwm_freq)
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
		self.pwm.ChangeDutyCycle(dc)

class Locomotor:
    def __init__self(self, mt_left, mt_right):
        self.motor_left = mt_left
        self.motor_right = mt_right

def motor_rotate(pin_phase, pwm, vel):
	if vel >= 0:
		GPIO.output(pin_phase, GPIO.LOW)
	elif vel < 0:
		GPIO.output(pin_phase, GPIO.HIGH)
		vel = -vel
	dc = vel
	if (dc > pwm_limit):
		dc = pwm_limit
	pwm.ChangeDutyCycle(dc)

def move_forward(phasea, pwma, phaseb, pwmb, vel):
	motor_rotate(phasea, pwma, vel)
	motor_rotate(phaseb, pwmb, vel)

def move_back(phasea, pwma, phaseb, pwmb, vel):
	motor_rotate(phasea, pwma, -vel)
	motor_rotate(phaseb, pwmb, -vel)

def move_stop(phasea, pwma, phaseb, pwmb):
	move_forward(phasea, pwma, phaseb, pwmb, 0)

def turn_right(phasea, pwma, phaseb, pwmb, vel):
	motor_rotate(phasea, pwma, vel)
	motor_rotate(phaseb, pwmb, -vel)

def turn_left(phasea, pwma, phaseb, pwmb, vel):
	motor_rotate(phasea, pwma, -vel)
	motor_rotate(phaseb, pwmb, vel)

def aux_up(phase, pwm, vel):
	motor_rotate(phase, pwm, vel)

def aux_down(phase, pwm, vel):
	motor_rotate(phase, pwm, -vel)

def aux_stop(phase, pwm):
	aux_up(phase, pwm, 0)

if __name__ == "__main__":
	getch = _Getch()
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

#	pwmA_a = GPIO.PWM(pinA_a_enable, pwm_freq)
#	pwmA_b = GPIO.PWM(pinA_b_enable, pwm_freq)
#	pwmB_a = GPIO.PWM(pinB_a_enable, pwm_freq)
#	pwmB_b = GPIO.PWM(pinB_b_enable, pwm_freq)
#	pwmA_a.start(0)
#	pwmA_b.start(0)
#	pwmB_a.start(0)
#	pwmB_b.start(0)

	mt_left = PWMMotor(pinA_a_phase, pinA_a_enable)
	mt_right = PWMMotor(pinA_b_phase, pinA_b_enable)
	mt_dummy = PWMMotor(pinB_a_phase, pinB_a_enable)
	mt_arm = PWMMotor(pinB_b_phase, pinB_b_enable)

	try:
		while 1:

			key = getch()
			print key

			if key == "w":
				print "Forward"
				move_forward(pinA_a_phase, pwmA_a, pinA_b_phase, pwmA_b, pwm_limit)
			elif key == "z":
				print "Back"
				move_back(pinA_a_phase, pwmA_a, pinA_b_phase, pwmA_b, pwm_limit)
			elif key == "a":
				print "Left"
				turn_left(pinA_a_phase, pwmA_a, pinA_b_phase, pwmA_b, pwm_limit)
			elif key == "s":
				print "Right"
				turn_right(pinA_a_phase, pwmA_a, pinA_b_phase, pwmA_b, pwm_limit)
			elif key == "e":
				print "Up"
				aux_up(pinB_b_phase, pwmB_b, pwm_limit * 0.7)
			elif key == "x":
				print "Down"
				aux_down(pinB_b_phase, pwmB_b, pwm_limit * 0.7)
			elif key == "q":
				break
			else:
				move_stop(pinA_a_phase, pwmA_a, pinA_b_phase, pwmA_b)
				aux_stop(pinB_b_phase, pwmB_b)

			time.sleep(0.2)


	except KeyboardInterrupt:
		pass

	GPIO.cleanup()
