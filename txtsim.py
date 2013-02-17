import lights
import cProfile
import pstats

def simulate():
  sm = lights.sm
  while sm.iteration < 1000:
    sm.update()
    print (sm.rmsTime)

if __name__ == '__main__':
  cProfile.run('simulate()')
  # p = pstats.Stats('simprof')
