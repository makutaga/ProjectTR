#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://blanktar.jp/blog/2013/09/python-xml-rpc.html
#http://docs.python.jp/2/library/simplexmlrpcserver.html#SimpleXMLRPCServer.SimpleXMLRPCRequestHandler

from SimpleXMLRPCServer import SimpleXMLRPCServer

import numpy as np
import i2c_devices as i2c

server = SimpleXMLRPCServer(("raspberrypi.local", 18080))
server.register_introspection_functions() 

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

# Register a function under a different name
def adder_function(x, y):
	return x + y
server.register_function(adder_function, 'add')

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class MyFuncs:
	def div(self, x, y):
		return x // y

server.register_instance(MyFuncs())

def Hello():
	''' 外部に公開するための関数。
	なんと普通の関数である。びっくり。
	'''
	return 'Hello World.'

def Add(x, y):
	return x + y

server.register_function(Hello)  # 関数を外部に公開する。
server.register_function(Add)


def values(dim):
	v = np.random.rand(dim)
	return v.tolist()

server.register_function(values)

def arrays(dim):
	v1 = np.array(range(0, dim))
	v2 = np.random.rand(dim)
	return [v1.tolist(), v2.tolist()]

server.register_function(arrays)

def goForward():
	print 'forward'
	return True

server.register_function(goForward)

bus = i2c.smbus.SMBus(1)
mag = i2c.MagSensor(bus, i2c.mag_dev_addr)
acc = i2c.AccSensor(bus)

def measMag():
	return mag.measSingle()
server.register_function(measMag)

def measAcc():
	return acc.measSingle()
server.register_function(measAcc)

server.serve_forever()
#server.handle_request()

