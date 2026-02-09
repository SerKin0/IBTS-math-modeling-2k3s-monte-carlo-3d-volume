import numpy as np
import matplotlib.pyplot as plt

dt=0.01
GM=4*np.pi**2 
    
#начальные условия
x=1
y=-1
r=np.sqrt(x**2+y**2) #
v=np.sqrt(GM/r)

#vx=v# если запускаем горизонтально
#vy=0#

vx=np.abs(v*y/r)
vy=np.abs(v*x/r)

N=200
for i in range(N):
    r=np.sqrt(x**2+y**2)
    ax=-GM/r/r/r*x
    ay=-GM/r/r/r*y
    vx+=ax*dt
    vy+=ay*dt
    dx=vx*dt
    dy=vy*dt
    x+=dx
    y+=dy
    
    plt.plot(x,y,'bo')

plt.plot(0,0,'yo',markersize=30)
plt.axis('equal')
plt.show()
