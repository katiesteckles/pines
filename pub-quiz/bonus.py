
beermat1 = Actor('beermat')
beermat1.pos = (250, 150)
beermat2 = Actor('beermat')
beermat2.pos = (550, 150)
beermat3 = Actor('beermat')
beermat3.pos = (250, 450)
beermat4 = Actor('beermat')
beermat4.pos = (550, 450)
global moving_12, moving_13
moving_12 = 0
moving_13 = 0

def draw():
    screen.fill((85, 47, 0))
    beermat1.draw()
    beermat2.draw()
    beermat3.draw()
    beermat4.draw()
    
def update():
    draw()
    move_beermats()
    
def move_beermats():
    global moving_12, moving_13, beermat1, beermat2, beermat3
    if moving_12 > 0:
        if moving_12 < 50:
            beermat1.x += 6
            beermat2.x -= 6
            moving_12 += 1
        elif moving_12 == 50:
            beermat1, beermat2 = beermat2, beermat1
            moving_12 = 0
    if moving_13 > 0:
        if moving_13 < 50:
            beermat1.y += 6
            beermat3.y -= 6
            moving_13 += 1
        elif moving_13 == 50:
            beermat1, beermat3 = beermat3, beermat1
            moving_13 = 0

def on_key_down(key):
    global moving_12, moving_13
    if key == keys.A:
        moving_12 = 1
    if key == keys.B:
        moving_13 = 1