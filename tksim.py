# from tkinter import *
import cProfile
import tkinter as tk
import lights
from vec2 import Vec2
# from lights import StreetMap

pxpercoord = 4
carlength = 3
carwidth = 2
waittime = 1

class App ():
  def __init__(self,sm):
    self.sm = sm
    self.root = tk.Tk()
    # tk.wm_geometry("600x600+20+40")
    self.canvas = tk.Canvas(self.root, width=900, height=900,background="black")
    self.canvas.pack()
    self.updateTraffic()

  def drawSm (self):
    self.canvas.delete(tk.ALL)
    for co in self.sm.cars:
    #for co in self.sm.coords:
      #if co in self.sm.cars:
        c_co = self.canvasCoord(co)
        self.drawCar(c_co,self.sm.cars[co].direction,self.sm.cars[co].color)
    for l in self.sm.lights.values():
      c_co = self.canvasCoord(l.coord)
      self.drawLight(c_co,l.direction,l.state)
    #self.text.text = "foobar"
    self.text = self.canvas.create_text((100,100),text="RMS Time: " + ("{0:0.1f}".format(self.sm.rmsTime)),fill="white")
    self.text = self.canvas.create_text((100,120),text="Last Time: " + ("{0:d}".format(self.sm.lastTime)),fill="white")
    self.text = self.canvas.create_text((100,140),text="Iteration: " + ("{0}".format(self.sm.iteration)),fill="white")

  def canvasCoord(self,co):
    return Vec2(co[1]*pxpercoord,co[0]*pxpercoord)

  def drawCar(self,co,direction,color):
    startco = (co[0]+(pxpercoord/2)-direction[1]*carlength/2,co[1]+(pxpercoord/2)-direction[0]*carlength/2)
    self.canvas.create_line(startco,(startco[0]+direction[1]*carlength,startco[1]+direction[0]*carlength),width=carwidth,fill='#'+color)

  def drawLight(self,co,direction,color):
    linecos = ()
    if direction == lights.SOUTH:
      linecos = ((co[0],co[1]+pxpercoord),(co[0]+pxpercoord,co[1]+pxpercoord))
    elif direction == lights.EAST:
      linecos = ((co[0]+pxpercoord,co[1]),(co[0]+pxpercoord,co[1]+pxpercoord))
    elif direction == lights.NORTH:
      linecos = ((co[0],co[1]),(co[0]+pxpercoord,co[1]))
    elif direction == lights.WEST:
      linecos = ((co[0],co[1]),(co[0],co[1]+pxpercoord))
    if color == lights.RED:
      color = "#ff5555"
    elif color == lights.GREEN:
      color = "lightgreen"
    self.canvas.create_line(linecos[0],linecos[1],fill=color,width=2)

  def lineFrom(self,co,direction):
    return (co,(co[0] + direction[0]*pxpercoord,co[1]+direction[1]*pxpercoord))

  def updateTraffic(self):
    self.sm.update()
    # self.updateMap()
    self.drawSm()
    self.root.after(waittime,self.updateTraffic)

app = App (lights.sm)
cProfile.run("app.root.mainloop ()")
