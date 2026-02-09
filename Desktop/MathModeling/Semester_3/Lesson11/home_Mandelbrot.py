import tkinter as tk

w, h = 600, 600
max_iter = 50
scale = 200

root = tk.Tk()
canvas = tk.Canvas(root, width=w, height=h, bg='black')
canvas.pack()

class Complex:
    def __init__(self, re: float, im: float) -> None:
        self.re = re
        self.im = im
        
    def __add__(self, other: Complex) -> Complex:
        return Complex(self.re + other.re, self.im + other.im)
    
    def __mul__(self, other: Complex) -> Complex:
        return Complex(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re
        )
        
    def __str__(self) -> None:
        return f"Complex: re={self.re}, im={self.im}"
        

for x in range(w):
    for y in range(h):
        c = Complex((x - w / 2) / scale, (y - h / 2) / scale)
        z = Complex(0, 0)
        for k in range(max_iter):
            z = z*z + c
            if z.re**2 + z.im**2 > 2**2:
                color = f'#{k*5%255:02x}{k*10%255:02x}{k*15%255:02x}'
                canvas.create_line(x, y, x+1, y, fill=color)
                break
            

root.mainloop()