import csv
import os
from question import Question
from random import shuffle


class Quiz:

    def __init__(self):
        self.questions = self.load_questions()
        self.categories = [k for k in self.questions.keys()]
        self.score = 0
        self.currentCategory = ''
        self.currentQuestion = 0
        self.roundEnded = False
        self.score = 0
        self.givenAnswer = None

    def load_questions(self):
        questions = {}
        for filename in os.listdir('questions'):
            with open('questions/' + filename) as csvfile:
                category_questions = []
                rows = csv.reader(csvfile)
                for row in rows:
                    category_questions.append(Question(row[0], row[1], row[2], row[3], row[4], row[5]))
                category = filename.replace('-', ' ').replace('.csv', '').title()
                questions[category] = category_questions

        return questions

    def get_questions(self):
        category_questions = self.questions[self.currentCategory]
        shuffle(category_questions)
        return category_questions[:10]

    def get_question(self):
        return self.get_questions()[self.currentQuestion]

    def set_category(self, categoryIdx):
        self.currentCategory = self.categories[categoryIdx]

    def next_question(self):
        if len(self.get_questions()) >= self.currentQuestion + 2:
            self.roundEnded = True
        else:
            self.currentQuestion += 1
            self.givenAnswer = None

    def mark_question(self, answerIdx):
        self.givenAnswer = answerIdx
        if self.answered_correctly():
            self.score += 1
            return True

        return False

    def answered_correctly(self):
        return self.givenAnswer == self.get_question().answer
