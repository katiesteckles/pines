from quiz import Quiz

WIDTH = 800
HEIGHT = 600
quiz = Quiz()
selectedCategoryIdx = 0
selectedAnswerIdx = 0
MENU = 'menu'
QUIZ = 'quiz'
ANSWER = 'answer'
currentScreen = MENU
questionNo = 0
menubg = Actor('menu-bg')
menubg.pos=(400,300)
questbg = Actor('background')
questbg.pos=(400,300)

def draw():
    screen.fill((0, 0, 0))
    if currentScreen == MENU:
        draw_menu()

    elif currentScreen == QUIZ:
        draw_quiz()

    elif currentScreen == ANSWER:
        draw_answer_screen()


def draw_menu():
    # screen.draw.text('Pub Quiz', (50, 30), color='white', fontname='pressstart2p')
    # screen.draw.text('Pick a category', (50, 60), color='white', fontname='pressstart2p')
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

        screen.draw.text(text, (90, y), color='red', fontname='pressstart2p')
        y +=50


def draw_quiz():
    questbg.draw()
    question = quiz.get_question()
    screen.draw.text(quiz.currentCategory, (620, 30), color='white', fontname='pressstart2p')
    screen.draw.text(question.question, (50, 70), color='white', fontname='pressstart2p')
    y = 380
    for idx, answer in enumerate(question.answers):
        if idx == selectedAnswerIdx:
            screen.draw.text('>', (160, y), color='blue', fontname='pressstart2p')
            screen.draw.text(answer, (180, y), color='blue', fontname='pressstart2p')
        else:
            screen.draw.text(answer, (160, y), color='blue', fontname='pressstart2p')
        y += 80


def draw_answer_screen():
    questbg.draw()
    question = quiz.get_question()
    screen.draw.text(quiz.currentCategory, (620, 30), color='white', fontname='pressstart2p')
    screen.draw.text(question.question, (50, 70), color='white', fontname='pressstart2p')
    y = 380
    for idx, answer in enumerate(question.answers):
        if question.answer == idx:
            screen.draw.text('\u2714', (160, y+5), color='blue', fontname='symbol')
        else:
            screen.draw.text('\u2718', (160, y+5), color='blue', fontname='symbol')

        screen.draw.text(answer, (180, y), color='blue', fontname='pressstart2p')
        y += 80
    if quiz.mark_question(selectedAnswerIdx):
        screen.draw.text('Correct!', (160, 200), color='white', fontname='pressstart2p')
    else:
        screen.draw.text('Incorrect!', (160, 200), color='white', fontname='pressstart2p')
    draw_score()


def draw_score():
    screen.draw.text('Score:', (620, 400), color='black', fontname='pressstart2p')
    screen.draw.text(str(quiz.score), (620, 450), color='black', fontname='pressstart2p')


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

    elif currentScreen == QUIZ:
        if key == keys.UP:
            selectedAnswerIdx -= 1
        elif key == keys.DOWN:
            selectedAnswerIdx +=1
        elif key == keys.A:
            currentScreen = ANSWER
            clock.schedule_unique(quiz.next_question(), 3)

        