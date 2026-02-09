import tkinter as tk
import numpy as np

# Размеры поля по ширине и высоте (штук)
x_size, y_size = 100, 100

# Масштаб полотна и прямоугольников в нем
scale = 10

# Оступы по осям от краёв поля (px)
x_pad, y_pad = 10, 10

# Цвета прямоугольников
colors = [
    "white",
    "black"
]

# Два списка для хранения состояния "сейчас" и нового, основанного на первом
now_map = np.zeros(shape=[y_size, x_size], dtype=bool)
new_map = np.zeros(shape=[y_size, x_size], dtype=bool)

# Размеры полотна (px)
width_canvas = x_size * scale + 2 * x_pad
height_canvas = y_size * scale + 2 * y_pad

root = tk.Tk()
root.title("Игра Жизнь (by SerKin0)")
cs = tk.Canvas(root, width=width_canvas, height=height_canvas)
cs.pack()

# Создаем список с клетками поля для их отрисовки
rect = [[None] * x_size for _ in range(y_size)]
for i in range(y_size):
    for j in range(x_size):
        # ИСПРАВЛЕННЫЕ координаты:
        # j - координата X (столбец), i - координата Y (строка)
        x1 = x_pad + j * scale
        y1 = y_pad + i * scale
        x2 = x1 + scale
        y2 = y1 + scale
        
        rect[i][j] = cs.create_rectangle(
            x1, y1, x2, y2,
            fill="white", outline="white"
        )

# ИСПРАВЛЕННАЯ инициализация начального состояния
# Центральный прямоугольник должен быть в центре canvas
center_x_start = x_size // 3
center_x_end = 2 * x_size // 3
center_y_start = y_size // 3
center_y_end = 2 * y_size // 3

for i in range(y_size):
    for j in range(x_size):
        if center_x_start < j < center_x_end and center_y_start < i < center_y_end:
            now_map[i][j] = True
            cs.itemconfig(rect[i][j], fill="black", outline="black")
                
def update_screen(screen_now, screen_new) -> None:
    for i in range(y_size):
        for j in range(x_size):
            if screen_now[i][j] != screen_new[i][j]:
                col = colors[int(screen_new[i][j])]
                cs.itemconfig(rect[i][j], fill=col, outline=col)
                
def game_of_life() -> None:
    global now_map, new_map
    new_map = np.zeros(shape=[y_size, x_size], dtype=bool)
    
    for i in range(y_size):
        for j in range(x_size):
            left = j - 1
            right = j + 1
            top = i - 1
            bottom = i + 1
            
            if i == 0:          top = y_size - 1
            if i == y_size - 1: bottom = 0
            if j == 0:          left = x_size - 1
            if j == x_size - 1: right = 0
            
            sum_cell = (bool(now_map[top][left])  + bool(now_map[i][left])  + bool(now_map[bottom][left]) + 
                        bool(now_map[top][j])     + 0                       + bool(now_map[bottom][j])  + 
                        bool(now_map[top][right]) + bool(now_map[i][right]) + bool(now_map[bottom][right]))
            
            if now_map[i][j]:
                new_map[i][j] = (sum_cell == 2 or sum_cell == 3)
            else:
                new_map[i][j] = (sum_cell == 3)
                
    update_screen(now_map, new_map)
    now_map = new_map.copy()
    
    root.after(10, game_of_life)
    
game_of_life()
root.mainloop()