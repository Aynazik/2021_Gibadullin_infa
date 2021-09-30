import turtle as t

dt = 0
x = 0
y = 0
x0 = 0
vy = 70
vx = 35

t.shape('circle')

while vy != 0:
    while y >= 0:
        dt += 0.05
        x = x0 + vx * dt
        y = vy * dt - 10 * (dt ** 2)
        t.goto(x, y)
    x0 = x
    y = 0
    dt = 0
    vy -= 10
    vx -= 5

t.exitonclick()
