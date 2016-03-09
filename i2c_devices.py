#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import smbus

mag_dev_addr = 0x1e

mag_f_cra = 0x00
mag_f_crb = 0x01
mag_f_mode = 0x02
mag_f_x_h = 0x03
mag_f_x_l = 0x04
mag_f_y_h = 0x05
mag_f_y_l = 0x06
mag_f_z_h = 0x07
mag_f_z_l = 0x08
mag_f_status = 0x09

class I2CDevice(object):
	def __init__(self, bus, dev_addr):
		self.bus = bus
		self.dev_addr = dev_addr
	def write_byte(self, reg, dat):
		self.bus.write_byte_data(self.dev_addr, reg, dat)
	def read_byte(self, reg):
		return self.bus.read_byte_data(self.dev_addr, reg)
	def read_word(self, reg1):
		dat = (self.bus.read_byte_data(self.dev_addr, reg1) << 8) + self.bus.read_byte_data(self.dev_addr, reg1 + 1)
		if dat > 0x8000:
			dat = dat - 0xffff
		return dat

class MagSensor(I2CDevice):
	def __init__(self, bus, dev_addr):
		super(MagSensor, self).__init__(bus, dev_addr)
		super(MagSensor, self).write_byte(mag_f_cra, 0x70)
		super(MagSensor, self).write_byte(mag_f_crb, 0xa0)
	def meas_single(self):
		super(MagSensor, self).write_byte(mag_f_mode, 0x01)
		time.sleep(0.05)
		bx = super(MagSensor, self).read_word(mag_f_x_h)
		by = super(MagSensor, self).read_word(mag_f_y_h)
		bz = super(MagSensor, self).read_word(mag_f_z_h)
		return list([bx, by, bz])

if __name__ == "__main__":
	bus = smbus.SMBus(1)
	mag = MagSensor(bus, mag_dev_addr)

	while True:
		try:
			print mag.meas_single()

		except KeyboardInterrupt:
			break


		time.sleep(0.1)
