
beermat1 = Actor('beermat')
beermat1.pos = (250, 150)
beermat2 = Actor('beermat')
beermat2.pos = (550, 150)
beermat3 = Actor('beermat')
beermat3.pos = (250, 450)
beermat4 = Actor('beermat')
beermat4.pos = (550, 450)

def draw():
    screen.fill((85, 47, 0))
    beermat1.draw()
    beermat2.draw()
    beermat3.draw()
    beermat4.draw()
    
def swap12():
    global beermat1, beermat2
    for i in range(0, 100):
        beermat1.x += 1
        beermat2.x -= 1
        clock.schedule_unique(draw, 0.1) # this does not work
    beermat1, beermat2 = beermat2, beermat1

def on_key_up(key):
    if key == keys.LEFT:
        swap12()