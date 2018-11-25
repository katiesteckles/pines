from set import SetCard, SetGame
from math import floor
import time

WIDTH = 1200
HEIGHT = 800

border = 150
hgap = 250
vgap = 180
game = SetGame(cards=12)
arrow = Actor('arrow2')
arrowx = 150
arrowy = 60
arrow.pos=(arrowx,arrowy)
arrowrow = 0
arrowcol = 0
print(arrowrow)

def draw_table():
    for i, card in game.table.items():
        if card is None:
            continue
        col = hgap * floor(i / 3) + border
        row = vgap * (i % 3) + border
        card.sprite.pos = (col, row)
        card.sprite.draw()
        if i in game.selected:
            #print('outlining card ' + str(i))
            outline = Actor('outline')
            outline.pos = card.sprite.pos
            outline.draw()
    
def clearanddraw():
    screen.clear()
    screen.fill((0, 0, 0))
    draw_table()   
    
def reset():
    print('resetting')
    game.selected = []
    clearanddraw
    game.is_a_set = False
    game.not_a_set = False

def update():
    global arrowrow, arrowcol, game
    clearanddraw()
    print(game.is_a_set or game.not_a_set)
    if game.is_over:
        text = 'End of game!'
    elif game.is_a_set:
        text = "It's a SET!"
    elif game.not_a_set:
        text = "That's not a SET"
    else:
        text = 'Available sets: {}'.format(len(game.available_sets))
    screen.draw.text(text, (50, 650), fontname="pressstart2p", fontsize=30, color='white')
    text = 'Player points: {}'.format(len(game.player))
    screen.draw.text(text, (50, 700), fontname="pressstart2p", fontsize=30, color='white')
    arrow.draw()
    
def on_key_up(key):
    global arrowrow
    global arrowcol
    global itisaset
    global itisntaset
    if key == keys.LEFT:
        print(arrowcol)
        arrowcol = arrowcol - 1
        if arrowcol < 0:
            arrowcol = 3
        arrow.pos=(arrowx+(arrowcol*hgap),arrowy+(arrowrow*vgap))
    elif key == keys.RIGHT:
        arrowcol = arrowcol + 1
        if arrowcol > 3:
            arrowcol = 0
        arrow.pos=(arrowx+(arrowcol*hgap),arrowy+(arrowrow*vgap))
    elif key == keys.DOWN:
        arrowrow = arrowrow + 1
        if arrowrow > 2:
            arrowrow = 0
        arrow.pos=(arrowx+(arrowcol*hgap),arrowy+(arrowrow*vgap))
    elif key == keys.UP:
        arrowrow = arrowrow - 1
        if arrowrow < 0:
            arrowrow = 2
        arrow.pos=(arrowx+(arrowcol*hgap),arrowy+(arrowrow*vgap))
    #elif key == keys.B:
    #    game.is_a_set = True
    #elif key == keys.C:
    #    game.is_a_set = False
    elif key == keys.A:
        if game.is_over:
            return
        table_index = arrowrow + (3*arrowcol)
        if table_index not in game.selected:
            game.selected.append(table_index)
            print('Added:', game.selected)
            if len(game.selected) == 3:
                try:
                    game.take(*game.selected)
                    game.is_a_set = True
                    clock.schedule_unique(reset, 2)
                except ValueError:
                    print('Not a valid set')
                    game.not_a_set = True
                    clock.schedule_unique(reset, 2)
        else:
            selected_index = game.selected.index(table_index)
            game.selected.pop(selected_index)
            print('Removed:', game.selected)

def on_mouse_down(pos):
    if game.is_over:
        return
    for table_index, card in game.table.items():
        if card and card.sprite.collidepoint(pos):
            if table_index not in game.selected:
                game.selected.append(table_index)
                print('Added:', game.selected)
                if len(game.selected) == 3:
                    try:
                        game.take(*game.selected)
                        game.is_a_set = True
                        clock.schedule_unique(reset, 2)
                    except ValueError:
                        print('Not a valid set')
                        game.not_a_set = True
                        clock.schedule_unique(reset, 2)
            
            else:
                selected_index = game.selected.index(table_index)
                game.selected.pop(selected_index)
                print('Removed:', game.selected)