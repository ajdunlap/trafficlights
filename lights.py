#.i lights.py
# Implements the traffic light logic.
from collections import deque
import math
import copy
import random
#import numpy as np
from vec2 import Vec2

RED = 0
GREEN = 2

#def Vec2(x,y):
#  return (x,y)

NORTH = Vec2(-1,0)
SOUTH = Vec2(1,0)
EAST = Vec2(0,1)
WEST = Vec2(0,-1)

class Grid (object):
  def __init__(self,ewsize,nssize):
    self.ewsize = ewsize
    self.nssize = nssize
    self._lst = [None for x in range(0,ewsize) for y in range(0,nssize)]

  def __getitem__(self,co):
    return (self._lst[co[0]*self.ewsize+co[1]])[1]

  def __setitem__(self,co,val):
    self._lst[co[0]*self.ewsize+co[1]] = (co,val)

  def __contains__(self,co):
    return self.inRange(co) and self._lst[co[0]*self.ewsize+co[1]] != None

  def __iter__(self):
    return iter([y[0] for y in self._lst if y])

  def inRange(self,co):
    return co[0] >= 0 and co[1] >= 0 and co[0] <= self.nssize - 1 and co[1] <= self.ewsize - 1

class StreetMap (object):
  def isOpen(self,co):
    return co not in self.cars
  
  def hasRedLight(self,co,direction):
    if co in self.lights:
      return self.lights[co].state == RED and self.lights[co].direction == direction
    else:
      return False

  def canMoveFrom(self,co,direction):
    #if co in self.movables[direction]:
      #return self.movables[direction][co]
    #else:
      #return self.isOpen(Vec2(co[0]+direction[0],co[1]+direction[1])) and not self.hasRedLight(co,direction)
      return self.isOpen(direction+co) and not self.hasRedLight(co,direction)
      #self.movables[direction][co] = ok
      #return ok
    #ok = self.movables[direction][co] if co in self.movables[direction] else self.isOpen(co+direction) and not self.hsaRedLight(co,direction)
    #if ok:
      #self.movables[direction].add(co)
      #return True
    #else:
      #return False
    # return self.isOpen(co+direction) and not self.hasRedLight(co,direction)

  def canMoveFromFor(self,co,direction,sqs):
    #print (len(self.movables[direction]))
    for d in range(0,sqs):
      if not self.canMoveFrom(d*direction+co,direction):
      #if not self.canMoveFrom((co[0]+d*direction[0],co[1]+d*direction[1]),direction):
        return d
    return sqs

  #def buildSetOfMovements(self):
    #self.movables = {}
    #for direction in [NORTH,SOUTH,EAST,WEST]:
      #self.movables[direction] = set([])
      #for co in self.coords:
        #if self.canMoveFrom(co,direction):
          #self.movables[direction].add(co)

  def queueVehicleAtInroad(self,veh,inroad):
    veh.direction = inroad.direction
    inroad.queue.append(veh) 

  def enterVehicleFromInroad(self,inroad):
    co = inroad.coord
    if self.isOpen(co): #self.cars[co] == None:
      self.cars[co] = inroad.queue.popleft()

  def advanceCars(self):
    #print ("                                                                       >>> " + str(len(self.cars)))
    self.iteration += 1
    carsupd = Grid (self.eastwestsize, self.northsouthsize) # { co : None for co in self.cars.keys() }
    self.movables = {d : {} for d in [NORTH,SOUTH,EAST,WEST]}
    for co in self.cars:
      self.advanceCar(co,self.cars[co],carsupd)
    self.cars = carsupd
    if self.timesSquared:
      self.rmsTime = math.sqrt(sum(self.timesSquared)/len(self.timesSquared))

  def coordIsAtEnd(self,nextco):
    return nextco in self.outroadcoords or not self.cars.inRange(nextco) #  nextco[0] < 0 or nextco[0] >= self.northsouthsize-1 or nextco[1] < 0 or nextco[1] >= self.eastwestsize-1 #  next not in self.coords

  def advanceCar(self,co,car,carsupd):
    car = self.cars[co]
      #car = self.cars[co]
      #if car:
    car.time += 1
        #if co in self.lights.keys():
          #light = self.lights[co]
          #if light.direction == self.cars[co].direction and light.state == RED:
            #print("stopped",light.ident,self.cars[co].direction)
            #continue
        #moved = False
        #topspeed = random.choice([0,1])
    v = self.canMoveFromFor(co,car.direction, min(car.velocity+1,car.maxvelocity))
        #for v in range(min(car.velocity+1,car.maxvelocity - topspeed),0,-1):
    nextco = (co[0] + v*self.cars[co].direction[0],co[1]+v*self.cars[co].direction[1])
        #nextr = r + carstmp[r][c].direction[0]
        #nextc = c + carstmp[r][c].direction[1]
        #if self.canMoveFromFor(co,car.direction,v):
    if not self.coordIsAtEnd(nextco):
      carsupd[nextco] = car
      car.velocity = v
          #self.cars[nextco] = car
          #self.cars[co] = None
    else:
      self.timesSquared.append(car.time**2)
      if len(self.timesSquared) >= 100:
          self.timesSquared.pop(0)
      #if self.iteration % 25 == 0:
        #self.timeSquared = 0
        #self.numCars = 0
      self.lastTime = car.time
      #self.rmsTime = math.sqrt(sum(self.timesSquared))
      #self.timeSquared += car.time**2
      #self.numCars += 1
      #self.rmsTime = math.sqrt(self.timeSquared/self.numCars)

  def __init__(self,northsouthsize,eastwestsize,inroads,outroadcoords,lights):
    self.iteration = 0
    self.numCars = 0
    self.timeSquared = 0
    self.rmsTime = 0
    self.timesSquared = []
    self.lastTime = 0
    self.lights = lights
    #self.lightidents = { v.ident : v for v in lights.values() }
    # self.lightdirs = lightdirs
    # self.lightstates = { v : RED for v in lights.values() }
    self.inroads = inroads #coords = inroadcoords
    self.outroadcoords = outroadcoords
    #self.inroaddirs = inroaddirs
    self.queues = dict([(ir,deque([])) for ir in inroads.keys()])
    self.northsouthsize = northsouthsize
    self.eastwestsize = eastwestsize
    self.coords = [Vec2(r,c) for c in range(0,self.eastwestsize) for r in range(0,self.northsouthsize)]
    #for row in grid:
      #print(type(row))
      #if len(row) != self.eastwestsize:
        #raise ValueError("Inconsistent row lengths")
    # self.grid = grid
    self.cars = Grid(self.eastwestsize,self.northsouthsize) # {} # co : None for co in self.coords } #[[None for x in range(0,self.eastwestsize)] for x in range(0,self.northsouthsize)]
    self.decider = LightDecider()

  #def showGrid(self):
    #for r in range(-1,self.northsouthsize+1):
      #for c in range(-1,self.eastwestsize+1):
        #if r == -1 or r == self.northsouthsize:
          #if c == -1 or c == self.eastwestsize:
            #print('+',end='')
            #pass
          #else:
            #print('-',end='')
        #elif c == -1 or c == self.eastwestsize:
          #print('|',end='')
        #else:
          #if Vec2(r,c) in self.cars: #[Vec2(r,c)] != None:
            #print('O',end='')
          #else:
            #print(' ',end='')
      #print()

  def update(self):
    for inr in self.inroads.values():
      if random.uniform(0,1) < inr.probability:
        self.queueVehicleAtInroad(Vehicle(inr,self),inr)
        self.enterVehicleFromInroad(inr)
    self.advanceCars()
    #newlightstates = self.decider.changeStates()
    for l in self.lights.values():
      l.change(self.iteration) # state = newlightstates[l.ident]

  def addLightsAtIntersection(self,ident,co,redtime,greentime,nsfirst):
    iSouth = co - SOUTH # (co[0]-SOUTH[0],co[1]-SOUTH[1])
    iNorth = co + EAST - 2*NORTH #(co[0]+EAST[0]-2*NORTH[0],co[1]+EAST[1]-2*NORTH[1])
    iEast = co + SOUTH - EAST # (co[0]+SOUTH[0]-EAST[0],co[1]+SOUTH[1]-EAST[1])
    iWest = co - 2*WEST # (co[0]-2*WEST[0],co[1]-2*WEST[1])
    k = { iSouth : Light(ident+1,SOUTH,iSouth,redtime if nsfirst else 0,redtime,greentime),
          iNorth : Light(ident+3,NORTH,iNorth,redtime if nsfirst else 0,redtime,greentime),
          iEast : Light(ident+2,EAST,iEast,0 if nsfirst else redtime,redtime,greentime),
          iWest : Light(ident+4,WEST,iWest,0 if nsfirst else redtime,redtime,greentime)
          }
    self.lights.update(k)
      
class Vehicle:
  def __init__(self,inroad,grid):
    self.time = 0
    self.grid = grid
    self.inroad = inroad
    redandgreen = ''.join((chr(random.choice(list(range(ord('4'),ord('9')+1))+list(range(ord('A'),ord('B')+1)))) for x in range(2)))
    blue = ''.join((chr(random.choice(list(range(ord('4'),ord('9')+1))+list(range(ord('A'),ord('F')+1)))) for x in range(2)))
    self.color = redandgreen*2 + blue
    self.velocity = 0
    self.maxvelocity = 3

class Light:
  def __init__(self,ident,direction,coord,offset,redtime,greentime):
    self.coord = coord
    self.ident = ident
    self.direction = direction
    self.offset = offset
    self.redtime = redtime
    self.greentime = greentime
    self.change(0)
  def change(self,time):
    self.state = ((time + self.offset) % (self.redtime+self.greentime) < self.redtime)*2

class Inroad:
  def __init__(self,coord,direction,probability):
    self.coord = coord
    self.direction = direction
    self.probability = probability
    self.queue = deque([])

class LightDecider:
  def __init__(self):
    self.count = 0

  def changeStates(self):
    which = math.floor(self.count/10) % 2
    self.count += 1
    #r = { i : random.choice([0,2]) for i in range (1,9) }
    r = { i : which * 2 for i in range(1,16,2)}
    print (r.values())
    r.update({ i : (not which)*2 for i in range (2,17,2) })
    #r = { 'Light1' : which * 2 , 'Light2' : (not which)*2 }
    return r
  
sm = StreetMap(
            150,
            150,
            { 'A' : Inroad(Vec2(125,0),EAST,0.4),
              'B' : Inroad(Vec2(124,149),WEST,0.4),

              'C' : Inroad(Vec2(0, 124),SOUTH,0.4),
              'D' : Inroad(Vec2(149, 125),NORTH,0.4),

              'E' : Inroad(Vec2(56, 0),EAST,0.4),
              'F' : Inroad(Vec2(55, 149),WEST,0.4),

              'G' : Inroad(Vec2(0, 55),SOUTH,0.4),
              'H' : Inroad(Vec2(149, 56),NORTH,0.4),
              },
            {},
            {}
            )

sm.addLightsAtIntersection(0,Vec2(55,55),15,15,True)
sm.addLightsAtIntersection(4,Vec2(124,55),15,15,True)
sm.addLightsAtIntersection(8,Vec2(55,124),15,15,False)
sm.addLightsAtIntersection(12,Vec2(124,124),15,15,False)
