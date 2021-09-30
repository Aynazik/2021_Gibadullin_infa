import turtle
from random import randint

number_of_turtles = 10

# рамка
turtle.penup()
turtle.goto(-300, -300)
turtle.pendown()
turtle.left(90)
for _ in range(4):
    turtle.forward(600)
    turtle.right(90)
turtle.penup()
turtle.goto(0, 0)

# разброс черепашек
pool = [turtle.Turtle(shape='circle') for i in range(20)]
for unit in pool:
    unit.penup()
    unit.speed()
    unit.goto(randint(-292, 292), randint(-292, 292))

turtle.shape('circle')

# поворот черепашек
for unit in pool:
    unit.left(randint(0, 360))

# Движение + условие разворота от стенки
for _ in range(20000):
    for unit in pool:
        unit.speed(0)
        x = unit.xcor()
        y = unit.ycor()
        if abs(-300 - y) <= 12:
            unit.left((360 - unit.heading()) * 2)
        if abs(300 - y) <= 12:
            unit.right(unit.heading() * 2)
        if abs(-300 - x) <= 12:
            unit.right(2 * unit.heading() - 180)
        if abs(300 - x) <= 12:
            unit.left(180 - 2 * unit.heading())
        unit.forward(4)
