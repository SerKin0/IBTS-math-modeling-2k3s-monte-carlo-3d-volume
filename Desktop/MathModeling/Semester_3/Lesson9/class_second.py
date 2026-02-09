# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 11:26:58 2025

@author: user
"""

import tkinter as tk
import numpy as np

root=tk.Tk() #объявляем объект главного окна
cs=tk.Canvas(root,width=1000,height=1000) #создание холста
cs.pack() #размещаем в окне

dt=0.01
GM=4*np.pi**2

#рисуем центральный шар
x_scr0=500 #координаты центрального шара
y_scr0=500
rads=10 #радиус центрального шара
cs.create_oval(x_scr0-rads,y_scr0-rads, \
x_scr0+rads,y_scr0+rads,fill='yellow')
        
#начальные условия
x=1
y=-1
r=np.sqrt(x**2+y**2) #
v=np.sqrt(GM/r)

#vx=v# если запускаем горизонтально
#vy=0#

vx=np.abs(v*y/r)
vy=np.abs(v*x/r)

#рисуем двигающийся шар
radp=5 #радиус двигающегося шара
coef=100 #множитель 
x_scr=x_scr0+x*coef #сдвинули нач.сост двигающегося шара от-но центр-го
y_scr=y_scr0+y*coef
ball=cs.create_oval(x_scr-radp,y_scr-radp, \
    x_scr+radp,y_scr+radp,fill='lightblue')

x_line=x_scr
y_line=y_scr
def motion():
    global x,y,vx,vy,r,x_line,y_line #не создаем новые переменные
    ax=-GM/r/r/r*x
    ay=-GM/r/r/r*y
    vx+=ax*dt
    vy+=ay*dt
    dx=vx*dt
    dy=vy*dt
    x+=dx
    y+=dy
    cs.move(ball,dx*coef,dy*coef) #сдвинуть шар
    cs.create_line(x_line, y_line, x_line+dx*coef,y_line+dy*coef, fill="silver",width=1) #рисование линии
    root.after(20,motion) #вызов функции с задержкой; задержка в миллисекундах, функция, кот выз после задержки 
    
    r=np.sqrt(x**2+y**2)
    x_line=x_line+dx*coef
    y_line=y_line+dy*coef
    
    
motion()    
root.mainloop() #запускаем цикл приема сообщений от ОС