import csv
import os
from question import Question
from random import shuffle
from pgzero import clock
from config import QUESTION_TIME_LIMIT, NUMBER_OF_QUESTIONS_IN_ROUND


class Quiz:

    def __init__(self):
        self.questions = self.load_questions()
        self.categories = [k for k in self.questions.keys()]
        self.score = 0
        self.currentCategory = ''
        self.currentQuestion = 0
        self.givenAnswer = None
        self.tryAgainUsed = False
        self.time_remaining = QUESTION_TIME_LIMIT
        self.timer_running = False

    def load_questions(self):
        questions = {}
        for filename in os.listdir('questions'):
            if filename.endswith('.csv'):
                with open('questions/' + filename) as csvfile:
                    category_questions = []
                    rows = csv.reader(csvfile)
                    for row in rows:
                        category_questions.append(Question(row[0], row[1], row[2], row[3], row[4], row[5]))
                    category = filename.replace('-', ' ').replace('.csv', '').title()
                    shuffle(category_questions)
                    round_questions = category_questions[:NUMBER_OF_QUESTIONS_IN_ROUND]
                    round_questions.sort(key=lambda q: q.difficulty)
                    questions[category] = round_questions
        return questions

    def reset(self):
        self.questions = self.load_questions()
        self.categories = [k for k in self.questions.keys()]
        self.score = 0
        self.currentCategory = ''
        self.currentQuestion = 0
        self.givenAnswer = None
        self.tryAgainUsed = False
        self.time_remaining = QUESTION_TIME_LIMIT
        self.timer_running = False

    def get_questions(self):
        return self.questions[self.currentCategory]

    def get_question(self):
        return self.get_questions()[self.currentQuestion]

    def set_category(self, categoryidx):
        self.currentCategory = self.categories[categoryidx]

    def next_question(self):
        if len(self.get_questions()) <= self.currentQuestion + 1:
            return False
        else:
            self.currentQuestion += 1
            self.time_remaining = QUESTION_TIME_LIMIT
            self.givenAnswer = None
            return True

    def mark_question(self, answerIdx):
        self.givenAnswer = answerIdx
        if self.answered_correctly():
            self.score += 1
            return True

        return False

    def answered_correctly(self):
        return self.givenAnswer == self.get_question().answer

    def start_timer(self):
        self.timer_running = True
        clock.schedule_unique(self.increment_timer, 1)

    def increment_timer(self):
        if self.time_remaining > 0 and self.timer_running:
            self.time_remaining -= 1

        clock.schedule_unique(self.increment_timer, 1)

    def pause_timer(self):
        self.timer_running = False

    def use_try_again(self):
        self.tryAgainUsed = True
        self.time_remaining = QUESTION_TIME_LIMIT
        self.get_question().answers[self.givenAnswer] = ''