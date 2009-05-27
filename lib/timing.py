import time

def timing_print_args(func):
	def wrapper(*arg):
		t0 = time.time()
		r = func(*arg)
		elapsed = time.time() - t0
		print '%s%s => %0.3f ms' % (func.func_name, arg, elapsed*1000.00)
		return r
	return wrapper

def timing(func):
	def wrapper(*arg):
		t0 = time.time()
		r = func(*arg)
		elapsed = time.time() - t0
		print '%s => %0.3f ms' % (func.func_name, elapsed*1000.00)
		return r
	return wrapper


# arigato.
@timing	
def f():
	pass

if __name__ == '__main__':
	print 'the what?'
	f()
