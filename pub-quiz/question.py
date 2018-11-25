class Question:

    def __init__(self, question, answer1, answer2, answer3, correctAnswerNo):
        self.question = question
        self.answers = [answer1, answer2, answer3]
        self.answer = int(correctAnswerNo)

    def is_correct(self, index):
        return index == self.answer