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
    # draw_text('Pub Quiz', (50, 30))
    # draw_text('Pick a category', (50, 60))
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

        draw_text(text, (90, y), 'red')
        y += 50


def draw_quiz():
    questbg.draw()
    question = quiz.get_question()
    draw_text(quiz.currentCategory, (620, 30))
    draw_text(question.question, (50, 70))
    draw_score()
    y = 380
    for idx, answer in enumerate(question.answers):
        if idx == selectedAnswerIdx:
            draw_text('>', (160, y), 'blue')
            draw_text(answer, (180, y), 'blue')
        else:
            draw_text(answer, (160, y), 'blue')
        y += 80


def draw_answer_screen():
    questbg.draw()
    question = quiz.get_question()
    draw_text(quiz.currentCategory, (620, 30))
    draw_text(question.question, (50, 70))
    y = 380
    for idx, answer in enumerate(question.answers):
        if question.answer == idx:
            draw_symbol('\u2714', (160, y), 'blue')
        else:
            draw_symbol('\u2718', (160, y), 'blue')

        draw_text(answer, (180, y), 'blue')
        y += 30
    if quiz.mark_question(selectedAnswerIdx):
        draw_text('Correct!', (160, 200))
    else:
        draw_text('Incorrect!', (160, 200))
    draw_score()


def draw_score():
    draw_text('Score: ' + str(quiz.score), (620, 400), 'black')
    draw_text(str(quiz.score), (620, 450), 'black')


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


def draw_text(text, position, colour='white'):
    screen.draw.text(text, position, color=colour, fontname='pressstart2p')


def draw_symbol(text, position, colour):
    position = (position[0], position[1] + 5)
    screen.draw.text(text, position, color=colour, fontname='symbol')