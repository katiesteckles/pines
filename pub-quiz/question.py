class Question:

    def __init__(self, question, answer1, answer2, answer3, correct_answer_no, difficulty):
        self.question = question
        self.answers = [answer1, answer2, answer3]
        self.answer = int(correct_answer_no)
        self.difficulty = int(difficulty)

    def is_correct(self, index):
        return index == self.answer