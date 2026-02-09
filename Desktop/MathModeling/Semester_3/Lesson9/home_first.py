import tkinter as tk
import numpy as np

class Point:
    def __init__(self, x: float, y: float, 
                 vx: float = None, vy: float = None,
                 ax: float = 0, ay: float = 0,
                 r: float = 1, color: str = 'black', mass: float = 1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.r = r
        self.color = color
        self.mass = mass
        self.canvas_id = None
    
    def data_to_oval(self, offset_x: float = 0, offset_y: float = 0, scale: float = 1) -> tuple:
        return (
            offset_x + self.x * scale - self.r, offset_y + self.y * scale - self.r,
            offset_x + self.x * scale + self.r, offset_y + self.y * scale + self.r
        )
        
def calculate_all_forces(bodies: list[Point]) -> None:
    # Сбрасываем ускорения всех тел
    for body in bodies:
        body.ax = 0
        body.ay = 0
    
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            R = np.sqrt(dx**2 + dy**2)
            
            if R == 0: 
                continue
                
            F = GM * bodies[i].mass * bodies[j].mass / R**2
            
            fx = F * (dx / R)
            fy = F * (dy / R)
            
            bodies[i].ax += fx / bodies[i].mass
            bodies[i].ay += fy / bodies[i].mass
            bodies[j].ax -= fx / bodies[j].mass
            bodies[j].ay -= fy / bodies[j].mass

def update_all_positions(bodies: list) -> None:
    for body in bodies:
        body.vx += body.ax * dt
        body.vy += body.ay * dt
        
        body.x += body.vx * dt
        body.y += body.vy * dt

def dist(first_point: Point, second_point: Point) -> float:
    return np.sqrt(
        (first_point.x - second_point.x)**2 + (first_point.y - second_point.y)**2
        )


w, h = 1000, 1000
scale = 100  # масштаб для отображения

root = tk.Tk()
cs = tk.Canvas(root, width=w, height=h)
cs.pack()

# Время тика
dt = 10e-4
GM = 4 * np.pi**2

# Создаем все небесные тела
bodies = [
    Point(0, 0, vx=0, vy=0,r=15, color='yellow', mass=200),  
    Point(0, 2, vx=50, r=6, color='lightblue', mass=1),   
    Point(-1.5, -1.5, vx=10, vy=50, r=8, color='red', mass=20),      
    # Point(0, 2, r=5, color='green', mass=0.5),   
    # Point(0, -1.8, r=7, color='orange', mass=1.5)
]

for planet in bodies[1:]: 
    R = dist(planet, bodies[0])
    v = np.sqrt(GM * bodies[0].mass / R)
    
    dx = planet.x - bodies[0].x
    dy = planet.y - bodies[0].y
    if planet.vx is None:
        planet.vx = v * dy / R
    if planet.vy is None:
        planet.vy = v * dx / R
    
prev_positions = [{'x': body.x, 'y': body.y} for body in bodies]

for body in bodies:
    body.canvas_id = cs.create_oval(*body.data_to_oval(w/2, h/2, scale), fill=body.color)



def motion():
    global prev_positions
    
    calculate_all_forces(bodies)
    
    current_positions = [{'x': body.x, 'y': body.y} for body in bodies]
    
    update_all_positions(bodies)
    
    for i, body in enumerate(bodies):
        new_coords = body.data_to_oval(w/2, h/2, scale)
        cs.coords(body.canvas_id, *new_coords)
        
        cs.create_line(
            prev_positions[i]['x'] * scale + w/2, 
            prev_positions[i]['y'] * scale + h/2, 
            current_positions[i]['x'] * scale + w/2,
            current_positions[i]['y'] * scale + h/2,
            fill=body.color)    
        
    prev_positions = current_positions
    root.after(20, motion)
    
motion()
root.mainloop()