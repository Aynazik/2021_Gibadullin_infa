from random import random, randint
import turtle as t

t.speed(0)
for i in range(200):
    p = randint(0, 1)
    t.forward(random()*randint(0, 50))
    if p == 0:
        t.left(random()*randint(0, 360))
    else:
        t.right(random()*randint(0, 360))

t.exitonclick()