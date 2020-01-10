import turtle
import base
import random
path = turtle.Turtle(visible=False)
turtle.bgcolor("Black")
potty = base.vector(0, 0)
ir = base.vector(0, 5)
potty2 = base.vector(4, 0)
ir2 = base.vector(5, 0)
map = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def world():
    path.color("Blue")
    for index in range(len(map)):
        tile = map[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')
def inside(objektum):
    return -200 < objektum.x < 200 and -200 < objektum.y < 200  # összehasonlítás

def valtozik(x, y):
    ir.x = x
    ir.y = y

def valtozik2(x, y):
    ir2.x = x
    ir2.y = y

def move():
    turtle.clear()
    if potty.x < -180 or potty.x > 180:
        ir.x = ir.x * -1
    if potty.y < -180 or potty.y > 180:
        ir.y = ir.y * -1
    if inside(potty + ir):
        potty.move(ir)

    if potty2.x < -180 or potty2.x > 180:
        ir2.x = ir2.x * -1
    if potty2.y < -180 or potty2.y > 180:
        ir2.y = ir2.y * -1
    if inside(potty2 + ir2):
        potty2.move(ir2)

    turtle.up()
    turtle.goto(potty.x, potty.y)
    turtle.dot(20, "Red")

    turtle.goto(potty2.x, potty2.y)
    turtle.dot(20, "Yellow")

    turtle.update()
    print("potty = " + str(potty) + " irany:" + str(ir))  # ez mutatja a háttérben lévő irányt
    turtle.ontimer(move, 100)


def move2():
    turtle.clear()

    turtle.up()

    turtle.update()
    print("potty2 = " + str(potty2) + " irany:" + str(ir2))  # ez mutatja a háttérben lévő irányt
    turtle.ontimer(move2, 100)




turtle.hideturtle()
turtle.tracer(False)
turtle.up()
world()
move()


turtle.listen()
turtle.onkey(lambda: valtozik(0, 5), " w ")
turtle.onkey(lambda: valtozik(5, 0), " d ")
turtle.onkey(lambda: valtozik(-5, 0), " a ")
turtle.onkey(lambda: valtozik(0, -5), "s")
turtle.setup(420, 420, 300, 200)

turtle.done()