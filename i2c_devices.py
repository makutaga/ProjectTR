#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raspberry Pi 2 でI2Cを使うためのクラスの定義
"""

__author__ = "M. Akutagawa"

import RPi.GPIO as GPIO
import time
import smbus
import math

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
	"""汎用I2Cデバイスクラス"""
	def __init__(self, bus, dev_addr):
		"""
		コンストラクタ．
		bus には smbus.SMBus(1) をつかう．
		dev_addr はデバイスのI2Cアドレス
		"""
		self.bus = bus
		self.dev_addr = dev_addr

	def write_byte(self, reg, dat):
		"""
		1バイト書き込み．
		reg で指定されるレジスタに dat を書き込む．
		"""
		self.bus.write_byte_data(self.dev_addr, reg, dat)

	def read_byte(self, reg):
		"""
		1バイト読み込み．
		reg で指定されるレジスタから 1バイト読みこむ．
		"""
		return self.bus.read_byte_data(self.dev_addr, reg)
	def read_word(self, reg1):
		"""
		1ワード（2バイト）読み込み．
		reg で指定されるレジスタから 1ワード（2バイト）読みこむ．
		符号付き2バイト整数を仮定．
		"""
		dat = (self.bus.read_byte_data(self.dev_addr, reg1) << 8) + self.bus.read_byte_data(self.dev_addr, reg1 + 1)
		if dat > 0x8000:
			dat = dat - 0xffff
		return dat

class MagSensor(I2CDevice):
	def __init__(self, bus, dev_addr):
		super(MagSensor, self).__init__(bus, dev_addr)
		self.write_byte(mag_f_cra, 0x70)
		self.write_byte(mag_f_crb, 0xa0)
	def meas_single(self):
		self.write_byte(mag_f_mode, 0x01)
		time.sleep(0.05)
		bx = self.read_word(mag_f_x_h)
		by = self.read_word(mag_f_y_h)
		bz = self.read_word(mag_f_z_h)
		return list([bx, by, bz])

if __name__ == "__main__":
	bus = smbus.SMBus(1)
	mag = MagSensor(bus, mag_dev_addr)

	while True:
		try:
			b = mag.meas_single()
			bb = math.sqrt(b[0]**2 + b[1]**2 + b[2]**2)
			
			print mag.meas_single(), bb

		except KeyboardInterrupt:
			break


		time.sleep(0.1)
