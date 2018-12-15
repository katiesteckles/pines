from quiz import Quiz
from config import QUESTION_TIME_LIMIT

WIDTH = 800
HEIGHT = 600
quiz = Quiz()
selectedCategoryIdx = 0
selectedAnswerIdx = 0

MENU = 'menu'
QUIZ = 'quiz'
ANSWER = 'answer'
GAME_OVER = 'game_over'
WIN_SCREEN = 'win_screen'

currentScreen = MENU
questionNo = 0
menubg = Actor('menu-bg')
clockhand = Actor('clockhand', anchor=(14, 59))
clockhand.pos = (680, 190)
menubg.pos = (400, 300)
questbg = Actor('background')
questbg.pos = (400, 300)
gameoverbg = Actor('gameover')
gameoverbg.pos = (400, 300)

win_frames = [Actor('win_f1'), Actor('win_f2'), Actor('win_f3'), Actor('win_f4'), Actor('win_f5'), Actor('win_f6'),
              Actor('win_b5'), Actor('win_b4'), Actor('win_b3'), Actor('win_b2'), Actor('win_b1'), Actor('win_b0')]
win_frame_dir_fwd = True
current_win_frame = 0


def draw():
    screen.fill((0, 0, 0))

    if currentScreen == MENU:
        draw_menu()

    elif currentScreen == QUIZ:
        draw_quiz()

    elif currentScreen == ANSWER:
        draw_answer_screen()

    elif currentScreen == GAME_OVER:
        draw_game_over_screen()

    if currentScreen == WIN_SCREEN:
        draw_win_screen()


def draw_menu():
    menubg.draw()
    draw_categories()


def draw_categories():
    global selectedCategoryIdx, quiz
    y = 190
    for idx, category in enumerate(quiz.categories):
        if selectedCategoryIdx == idx:
            text = '> ' + category
        else:
            text = category

        draw_category(text, (90, y), 'red')
        y += 30


def draw_quiz_header(question):
    questbg.draw()
    screen.draw.textbox(quiz.currentCategory, (570, 20, 230, 60), align='center', fontname='pressstart2p')
    screen.draw.textbox(question.question, (40, 40, 490, 230), align='left', fontname='pressstart2p', lineheight=1.2)
    draw_score()
    draw_text(str(quiz.time_remaining), (190, 680))
    if not quiz.tryAgainUsed:
        draw_text('try again', (530, 450))


def draw_quiz():
    question = quiz.get_question()
    draw_quiz_header(question)
    draw_clock()
    y = 360
    for idx, answer in enumerate(question.answers):
        if idx == selectedAnswerIdx:
            draw_text('<', (500, y + 25), 'blue')
        screen.draw.textbox(answer, (130, y, 350, 60), align='left', fontname='pressstart2p', color='blue',
                            lineheight=1.2)
        y += 80


def draw_clock():
    global currentScreen, quiz
    clockhand.angle = -((QUESTION_TIME_LIMIT - quiz.time_remaining) * (360 / QUESTION_TIME_LIMIT))
    clockhand.draw()
    if quiz.time_remaining <= 5:
        colour = 'red'
    else:
        colour = 'blue'
    screen.draw.textbox(str(quiz.time_remaining), (660, 200, 40, 40), align='center', color=colour, fontname='pressstart2p')

    if quiz.time_remaining == 0:
        currentScreen = GAME_OVER
        clock.schedule_unique(return_to_menu, 5)


def draw_answer_screen():
    question = quiz.get_question()
    draw_quiz_header(question)
    y = 360
    if quiz.answered_correctly():
        symbol = '\u2714'
        colour = 'blue'
    else:
        symbol = '\u2718'
        colour = 'red'
    for idx, answer in enumerate(question.answers):
        if question.answer == idx:
            draw_symbol(symbol, (500, y), colour)

        screen.draw.textbox(answer, (130, y, 350, 60), align='left', fontname='pressstart2p', color='blue',
                            lineheight=1.2)
        y += 80
    draw_score()


def draw_score():
    draw_text('Score: ' + str(quiz.score), (540, 400), 'black')


def draw_game_over_screen():
    gameoverbg.draw()


def return_to_menu():
    global currentScreen, quiz
    currentScreen = MENU
    quiz.reset()


def draw_win_screen():
    global current_win_frame, win_frames, win_frame_dir_fwd
    win_frames[current_win_frame].draw()

    if win_frame_dir_fwd:
        next_frame = current_win_frame + 1
        if next_frame >= len(win_frames):
            win_frame_dir_fwd = False
            next_frame = len(win_frames) - 1

    else:
        next_frame = current_win_frame - 1
        if next_frame < 0:
            win_frame_dir_fwd = True
            next_frame = 1

    current_win_frame = next_frame
    clock.schedule_unique(draw, 0.25)


def on_key_down(key):
    global selectedCategoryIdx, quiz, currentScreen, MENU, QUIZ, selectedAnswerIdx
    if currentScreen == MENU:
        if key == keys.UP:
            if selectedCategoryIdx == 0:
                selectedCategoryIdx = len(quiz.categories) - 1
            else:
                selectedCategoryIdx -= 1
        elif key == key.DOWN:
            if selectedCategoryIdx > len(quiz.categories) - 1:
                selectedCategoryIdx = 0
            else:
                selectedCategoryIdx += 1
        elif key == keys.A:
            quiz.set_category(selectedCategoryIdx)
            currentScreen = QUIZ
            quiz.start_timer()

    elif currentScreen == QUIZ:
        if key == keys.UP:
            if selectedAnswerIdx != 0:
                selectedAnswerIdx -= 1
        elif key == keys.DOWN:
            if selectedAnswerIdx != 2:
                selectedAnswerIdx += 1
        elif key == keys.A:
            if quiz.mark_question(selectedAnswerIdx):
                currentScreen = ANSWER
                clock.schedule_unique(next_question, 3)
            elif quiz.tryAgainUsed:
                currentScreen = GAME_OVER
                clock.schedule_unique(return_to_menu, 5)
            else:
                quiz.use_try_again()


def next_question():
    global currentScreen
    if quiz.next_question():
        currentScreen = QUIZ
    else:
        currentScreen = WIN_SCREEN
        clock.schedule_unique(return_to_menu, 5)


def draw_text(text, position, colour='white', fontsize=30):
    screen.draw.text(text, position, color=colour, fontname='pressstart2p', width=500, fontsize=fontsize)


def draw_category(text, position, colour='white', fontsize=15):
    screen.draw.text(text, position, color=colour, fontname='pressstart2p', width=250, fontsize=fontsize)


def draw_symbol(text, position, colour):
    position = (position[0], position[1] + 5)
    screen.draw.text(text, position, color=colour, fontname='symbol', fontsize=30)
