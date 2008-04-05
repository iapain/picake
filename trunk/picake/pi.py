import math
import cmath
import time

try:
	import gmpy
except:
	raise ImportError, 'Please install gmpy'

try:
	import psyco
	psyco.full()
except ImportError:
	pass

class NotConvergentError:
	pass

def factorial(n):
	"""calculates factorial"""
	return gmpy.fac(n)

def f(n):
	""" Alias for factorial function """
	return gmpy.fac(n)


class pi:
	""" compute pi computes value of pi based on various alrogithms """
	def __init__(self, percision=100, time=-1, n=2):
		self.percision = percision
		self.n = n
		self.time = time
		self.time_took = -1
		self.convergence = -1

	def compute_chudnovsky(self):
		gmpy.set_minprec(self.percision)
		sum = gmpy.mpf(0)
		k = gmpy.mpf(0)
		i = 0
		term = 0
		last_sum = 0
		while True:
			i += 1
			n = (((-1) ** k) * f(6 * k) * (13591409 + 545140134 * k))
			d = (f(3 * k) * ((f(k)) ** 3) * gmpy.fsqrt(gmpy.mpf(640320) ** (6 * k + gmpy.mpf(3))))
			term = n/d
			sum += term
			if sum == last_sum:
				fp = open('pi.txt', 'w')
				fp.write(str(1 / (12 * sum)))
				fp.close()
				self.iterations = i
				return self
			last_sum = sum
			k += 1
			if i > 2000:
				raise NotConvergentError