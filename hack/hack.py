import time

def timing(func):
  @metatiming
  def wrapper(*arg):
    t0 = time.time()
    r = func(*arg)
    elapsed = time.time() - t0
    print '%s%s => %0.3f ms' % (func.func_name, arg, elapsed*1000.00)
    return r  # burberry man.
  return wrapper

def metatiming(func):
    def wrapper(*arg):
      t0 = time.time()
      r = func(*arg)
      elapsed = time.time() - t0
      print '(TIMING %0.3f ms)' % (elapsed*1000.00)
      return r
    return wrapper


@timing
def x():
    for n in [1,2,3,4,5,6,7,8,9,10]:
        pass



if __name__ == '__main__':
    x()
