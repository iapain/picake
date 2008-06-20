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
		self.n = n+60
		self.time = time
		self.time_took = -1
		self.convergence = -1
		
	def fast_cal(self):
		from popen2 import popen2
		cmd = 'lib32\\lib.pyd %d pi -fancy:100,100,0,0,none' % self.percision
		output, input = popen2(cmd)
		ans = output.readlines()
		try:
			fp = open('pi', 'r')
		except IOError:
			print "Computation uses file IO. Couldn't create file for dumping values."
			return
		op = fp.readlines()[23:]
		
		fp.close()
		try:
			fp = open('pi', 'w')
		except IOError:
			print "Computation uses file IO. Couldn't create file for dumping values."
			return
		obb = '3.'
		for line in op:
			obb += line.replace('\n', '')
		fp.write(obb)
		fp.close()
		
		
		

	def gmp_arch_tan(self):
		self.method = "ArcTan"
		ts = time.time()
		dat =  str(gmpy.pi(self.percision*3 + int(self.percision/10) + int(4*self.percision/100) + int(5*self.percision/10)))[:self.percision]
		self.time_took = time.time() - ts
		try:
			fp = open('pi', 'w')
		except IOError:
			print "Computation uses file IO. Couldn't create file for dumping values."
		fp.write(dat)
		fp.close()
		print self.time_took
		return;
		
	def compute_chudnovsky(self):
		self.method = "Chudnovsky"
		ts = time.time()
		gmpy.set_minprec(self.percision*3 + int(self.percision/10) + int(4*self.percision/100) + int(5*self.percision/10))
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
				fp = open('pi', 'w')
				fp.write(str(1 / (12 * sum)))
				fp.close()
				self.iterations = i
				self.time_took = time.time() - ts
				return self
			last_sum = sum
			k += 1
			if i > 10000:
				raise NotConvergentError
