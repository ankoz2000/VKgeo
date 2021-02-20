import random
import time

from vk_api.keyboard import VkKeyboard
from answers import Questions, Answers

end = 5  # количество вопросов

qts = Questions()
qts.parse_questions()
answ = Answers()
answ.add_answers(answ.file_answers)\
    .parse_answers(answ.lines)\
    .get_right_answers(answ.file_right_answers, answ.lines, answ.right_answers)
answ.add_answers(answ.file_hard_answers)\
    .parse_answers(answ.hard_answers_lines)\
    .get_right_hard_answers(answ.file_right_hard_answers, answ.hard_answes_lines, answ.right_hard_answers)

class Test:

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._QUESTIONS = qts.questions
        self._ANSWERS = answ.answers
        self.POINTS = 0
        self.ERRORS = 0
        self.current_question = ''
        self.current_answers = ''
        self.right_answer = ''
        self.not_elected = self.start()
        self.counter = end
        self.timer = time
        self.current_time_result = 0

    def reset(self):
        self.POINTS = 0
        self.ERRORS = 0
        self.current_question = ''
        self.current_answers = ''
        self.reset_questions()
        self.timer = time

    def reset_questions(self):
        questions = self._QUESTIONS
        for num in questions:
            if questions[num]['is_elected']:
                questions[num]['is_elected'] = False
        self._QUESTIONS = qts.parse_questions().questions
        return

    def elect_question(self):
        questions = self._QUESTIONS
        try:
            quest = questions.popitem()
            return quest
        except KeyError as err:
            print(err)
            self._QUESTIONS = qts.questions
            return False
        #if not questions[n]['is_elected']:
        #    questions[n]['is_elected'] = True
        #    quest = questions[n]['question']
        #    self.not_elected.remove(n)
        #    del questions[n]
        #    return {'question': quest, 'number': n}
        #i += 1
        #return False

    def check(self, received):
        difference = time.time() - float(self.timer)
        self.current_time_result += difference
        if received.upper() == self.right_answer.upper() and difference <= 15:
            return True
        return False

    def get_question(self):
        diction = self.elect_question()
        if not diction:
            return False
        number = diction[0]
        question = diction[1]['question']
        answer = self._ANSWERS[number]
        right = answ.right_answers[number][0]
        print(question, ' - que')
        print(right, ' - right')
        print(answer)
        self.current_question = question
        self.current_answers = answer
        self.right_answer = right
        return question

    def start(self):
        i = 1
        lst = []
        while i < end:
            lst.append(i)
            i += 1
        return lst

