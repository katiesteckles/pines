from quiz import Quiz

WIDTH = 400
HEIGHT = 300
quiz = Quiz()
selectedCategoryIdx = 0
selectedAnswerIdx = 0
MENU = 'menu'
QUIZ = 'quiz'
ANSWER = 'answer'
currentScreen = MENU
questionNo = 0


def draw():
    screen.fill((0, 0, 0))
    if currentScreen == MENU:
        draw_menu()

    elif currentScreen == QUIZ:
        draw_quiz()

    elif currentScreen == ANSWER:
        draw_answer_screen()


def draw_menu():
    screen.draw.text('Pub Quiz', (50, 30), color='white', fontname='font')
    screen.draw.text('Pick a category', (50, 60), color='white', fontname='font')
    draw_categories()


def draw_categories():
    global selectedCategoryIdx, quiz
    y = 90
    for idx, category in enumerate(quiz.categories):
        if selectedCategoryIdx == idx:
            text = '> ' + category
        else:
            text = category

        screen.draw.text(text, (50, y), color='white', fontname='font')
        y += 30


def draw_quiz():
    question = quiz.get_question()
    screen.draw.text(quiz.currentCategory, (50, 30), color='white', fontname='font')
    screen.draw.text(question.question, (50, 70), color='white', fontname='font')
    draw_score()
    y = 100
    for idx, answer in enumerate(question.answers):
        if idx == selectedAnswerIdx:
            screen.draw.text('>', (80, y), color='white', fontname='font')
            screen.draw.text(answer, (100, y), color='white', fontname='font')
        else:
            screen.draw.text(answer, (80, y), color='white', fontname='font')
        y += 30


def draw_answer_screen():
    question = quiz.get_question()
    screen.draw.text(quiz.currentCategory, (50, 30), color='white', fontname='font')
    screen.draw.text(question.question, (50, 70), color='white', fontname='font')
    y = 100
    for idx, answer in enumerate(question.answers):
        if question.answer == idx:
            screen.draw.text('\u2714', (80, y+5), color='green', fontname='symbol')
        else:
            screen.draw.text('\u2718', (80, y+5), color='red', fontname='symbol')

        screen.draw.text(answer, (100, y), color='white', fontname='font')
        y += 30
    if quiz.mark_question(selectedAnswerIdx):
        screen.draw.text('Correct!', (50, 200), color='white', fontname='font')
    else:
        screen.draw.text('Incorrect!', (50,200), color='white', fontname='font')
    draw_score()


def draw_score():
    screen.draw.text('Score: ' + str(quiz.score), (50, 250), color='white', fontname='font')


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
