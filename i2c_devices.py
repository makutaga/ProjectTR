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
		reg1 は上位
		"""
		dat = (self.bus.read_byte_data(self.dev_addr, reg1) << 8) + self.bus.read_byte_data(self.dev_addr, reg1 + 1)
		if dat > 0x8000:
			dat = dat - 0xffff
		return dat
	def read_word2(self, reg1):
		"""
		1ワード（2バイト）読み込み．
		reg で指定されるレジスタから 1ワード（2バイト）読みこむ．
		符号付き2バイト整数を仮定．
		reg1 は下位
		"""
		dat = self.bus.read_byte_data(self.dev_addr, reg1) + self.bus.read_byte_data(self.dev_addr, reg1 + 1) << 8
		if dat > 0x8000:
			dat = dat - 0xffff
		return dat

class MagSensor(I2CDevice):
	"""
	磁気センサ HMC5883L
	"""
	DEV_ADDR = 0x1e
	REG_CRA = 0x00
	REG_CRB = 0x01
	REG_MODE = 0x02
	REG_X_H = 0x03
	REG_X_L = 0x04
	REG_Y_H = 0x05
	REG_Y_L = 0x06
	REG_Z_H = 0x07
	REG_Z_L = 0x08
	REG_STATUS = 0x09

	def __init__(self, bus, dev_addr=DEV_ADDR):
		super(MagSensor, self).__init__(bus, dev_addr)
		self.write_byte(self.REG_CRA, 0x70)
		self.write_byte(self.REG_CRB, 0xa0)
	def isLocked(self):
		ret = True
		if self.read_byte(self.REG_STATUS) & 0x02 == 0:
			ret = False
		return ret
	def isReady(self):
		ret = True
		if self.read_byte(self.REG_STATUS) & 0x01 == 0:
			ret = False
		return ret
	def measSingle(self):
		self.write_byte(self.REG_MODE, 0x01)
		time.sleep(0.01)
		bx = self.read_word(self.REG_X_H)
		by = self.read_word(self.REG_Y_H)
		bz = self.read_word(self.REG_Z_H)
		return list([bx, by, bz])

class AccSensor(I2CDevice):
	"""
	加速度センサ STMicroelectronics LIS3DH
	"""
	DEV_ADDR=0x18
	STATUS_REG_AUX = 0x07
	OUT_ADC1_L = 0x08
	OUT_ADC1_H = 0x09
	OUT_ADC2_L = 0x0a
	OUT_ADC2_H = 0x0b
	OUT_ADC3_L = 0x0c
	OUT_ADC3_H = 0x0d
	INT_COUNTER_REG = 0x0e
	WHO_AM_I = 0x0f
	TEMP_CFG_REG = 0x1f
	CTRL_REG1 = 0x20
	CTRL_REG2 = 0x21
	CTRL_REG3 = 0x22
	CTRL_REG4 = 0x23
	CTRL_REG5 = 0x24
	CTRL_REG6 = 0x25
	CTRL_REFERENCE = 0x26
	STATUS_REG2 = 0x27
	OUT_X_L = 0x28
	OUT_X_H = 0x29
	OUT_Y_L = 0x2a
	OUT_Y_H = 0x2b
	OUT_Z_L = 0x2c
	OUT_Z_H = 0x2d
	FIFO_CTRL_REG = 0x2e
	FIFO_SRC_REG = 0x2f
	INT1_CFG = 0x30
	INT1_SOURCE = 0x31
	INT1_THS = 0x32
	INT1_DURATION = 0x33
	CLICK_CFG = 0x38
	CLICK_SRC = 0x39
	CLICK_THS = 0x3a
	TIME_LIMIT = 0x3b
	TIME_LATENCY = 0x3c
	TIME_WINDOW = 0x3d

	def __init__(self, bus, dev_addr=DEV_ADDR):
		super(AccSensor, self).__init__(bus, dev_addr)
		
		if self.read_byte(self.WHO_AM_I) != 0x33:
			print "AccSensor: Failed to communicate"

	def measSingle(self):
		self.write_byte(self.CTRL_REG1, 0x7f)
		time.sleep(0.001)
		ax = self.read_word2(self.OUT_X_L)
		ay = self.read_word2(self.OUT_Y_L)
		az = self.read_word2(self.OUT_Z_L)
		time.sleep(0.001)
		self.write_byte(self.CTRL_REG1, 0x0f)
		return list([ax, ay, az])
		
if __name__ == "__main__":
	bus = smbus.SMBus(1)
	mag = MagSensor(bus)
	acc = AccSensor(bus)

	while True:
		try:
			b = mag.measSingle()
			bb = math.sqrt(b[0]**2 + b[1]**2 + b[2]**2)

			a = acc.measSingle()
			aa = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
			
			print '[{0[0]:6d} {0[1]:6d} {0[2]:6d}] {1} [{2[0]:6d} {2[1]:6d} {2[2]:6d}] {3}'.format(b, bb, a, aa)

		except KeyboardInterrupt:
			break


		time.sleep(0.05)
