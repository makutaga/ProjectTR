#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib

if __name__ == "__main__":
	s = xmlrpclib.ServerProxy('http://raspberrypi.local:18080')
	print s.system.listMethods()

	print s.measMag()
	print s.measAcc()
