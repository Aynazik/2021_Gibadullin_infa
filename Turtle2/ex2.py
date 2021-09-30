import turtle as t


def draw0():
    t.forward(25)
    t.backward(25)


def draw1():
    t.penup()
    t.forward(25)
    t.right(90)
    t.pendown()
    t.forward(25)
    t.penup()
    t.backward(25)
    t.left(90)
    t.backward(25)
    t.pendown()


def draw2():
    t.right(90)
    t.forward(25)
    t.backward(25)
    t.left(90)


def draw3():
    t.penup()
    t.forward(25)
    t.right(90)
    t.forward(25)
    t.pendown()
    t.forward(25)
    t.penup()
    t.backward(50)
    t.left(90)
    t.backward(25)
    t.pendown()


def draw4():
    t.penup()
    t.right(90)
    t.forward(50)
    t.left(90)
    t.pendown()
    t.forward(25)
    t.penup()
    t.backward(25)
    t.left(90)
    t.forward(50)
    t.right(90)
    t.pendown()


def draw5():
    t.right(90)
    t.penup()
    t.forward(25)
    t.pendown()
    t.forward(25)
    t.penup()
    t.backward(50)
    t.left(90)
    t.pendown()


def draw6():
    t.right(90)
    t.penup()
    t.forward(25)
    t.left(90)
    t.pendown()
    t.forward(25)
    t.backward(25)
    t.penup()
    t.right(90)
    t.backward(25)
    t.left(90)
    t.pendown()


def draw7():
    t.penup()
    t.right(90)
    t.forward(25)
    t.left(135)
    t.pendown()
    t.forward(25 * (2 ** 0.5))
    t.right(45)
    t.penup()
    t.backward(25)
    t.pendown()


def draw8():
    t.penup()
    t.right(90)
    t.forward(50)
    t.left(135)
    t.pendown()
    t.forward(25 * (2 ** 0.5))
    t.penup()
    t.left(45)
    t.forward(25)
    t.right(90)
    t.backward(25)
    t.pendown()


def placechange():
    t.penup()
    t.forward(35)
    t.pendown()


B = str(input("Ведите число"))
A = [int(y) for y in B]
t.speed(0)
for x in A:
    if x == 0:
        draw0()
        draw1()
        draw2()
        draw3()
        draw4()
        draw5()
    elif x == 1:
        draw1()
        draw3()
        draw7()
    elif x == 2:
        draw0()
        draw1()
        draw4()
        draw8()
    elif x == 3:
        draw0()
        draw6()
        draw7()
        draw8()
    elif x == 4:
        draw1()
        draw2()
        draw3()
        draw6()
    elif x == 5:
        draw0()
        draw2()
        draw3()
        draw4()
        draw6()
    elif x == 6:
        draw3()
        draw4()
        draw5()
        draw6()
        draw7()
    elif x == 7:
        draw0()
        draw5()
        draw7()
    elif x == 8:
        draw0()
        draw1()
        draw2()
        draw3()
        draw4()
        draw5()
        draw6()
    else:
        draw0()
        draw1()
        draw2()
        draw6()
        draw8()
    placechange()

t.exitonclick()
