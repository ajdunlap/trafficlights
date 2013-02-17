class Vec2 (tuple):
  def __new__(cls,*args):
    if len(args) == 1:
      return tuple.__new__(cls,args[0])
    elif len(args) == 2:
      return tuple.__new__(cls,(args[0],args[1]))
  def __len__(self):
    return 2
  def __getItem__(self,tuple):
    if type(key) != int:
      raise TypeError("index of Vec2 must be int")
    elif key == 0:
      return self.r
    elif key == 1:
      return self.c
    else:
      raise IndexError("index of Vec2 must be 1 or 2")
  def __add__(self,vec):
    return Vec2(self[0]+vec[0],self[1]+vec[1])
  def __sub__(self,vec):
    return Vec2(self[0]-vec[0],self[1]-vec[1])
  def __neg__(self,vec):
    return Vec2(-self[0],-self[1])
  def __sub__(self,vec):
    return Vec2(self[0]-vec[0],self[1]-vec[1])
  def __mul__(self,i):
    return Vec2(self[0]*i,self[1]*i)
  def __rmul__(self,i):
    return Vec2(self[0]*i,self[1]*i)
