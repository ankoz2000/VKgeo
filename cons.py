import random
import time

from vk_api.keyboard import VkKeyboard
from answers import Questions, Answers

end = 5  # количество вопросов 1
end2 = 14 # количество правильных ответов 2

qts = Questions()
qts.parse_questions().parse_hard_questions()
answ = Answers()
answ.add_answers()\
    .parse_answers()\
    .write_right()
answ.add_hard_answers()\
    .parse_hard_answers()\
    .get_right_hard_answers()

class Test:

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._QUESTIONS = qts.questions.copy()
        self._HARD_QUESTIONS = qts.hard_questions.copy()
        self._ANSWERS = answ.answers
        self._HARD_ANSWERS = answ.hard_answers
        self.POINTS = 0
        self.HARD_POINTS = 0
        self.points_buff = 0
        self.ERRORS = 0
        self.current_question = ''
        self.current_answers = ''
        self.right_answer = ''
        self.right_hard_answer = answ.right_hard_answers
        self.counter = end
        self.counter2 = end2
        self.timer = time
        self.current_time_result = 0

    def reset(self):
        self.POINTS = 0
        self.ERRORS = 0
        self.current_time_result = 0
        self.current_question = ''
        self.current_answers = ''
        self.reset_questions()
        self.timer = time
        return self

    def reset_hard(self):
        self.HARD_POINTS = 0
        self.current_time_result = 0
        self.current_question = ''
        self.current_answers = ''
        self.reset_questions()
        self.timer = time
        return self

    def reset_questions(self):
        self._QUESTIONS = qts.questions.copy()
        self._HARD_QUESTIONS = qts.hard_questions.copy()
        print("Q: ", self._QUESTIONS)
        print("HQ: ", self._HARD_QUESTIONS)
        return

    def check_hard(self, answer):  # Проверка если ответ соответствует любому множественному ответу
        hard = self._HARD_ANSWERS
        for ans in hard:
            for item in hard[ans]:
                if answer == self.cleaning(item):
                    return True
        return False

    def cleaning(self, string):
        result = ''
        word = list('&quot;')
        for item in list(string):
            if item == '"':
                for s in word:
                    result += s
            else:
                result += item
        return result

    def check_hard_right_answer(self, answer):
        current_right_answers = self.right_hard_answer
        for item in current_right_answers:
            if self.cleaning(answer) in self.cleaning(item):
                return True
        return False

    def elect_question(self):
        questions = self._QUESTIONS
        try:
            quest = questions.popitem()
            return quest
        except KeyError as err:
            print(err)
            qts.parse_questions()
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

    def elect_hard_question(self):
        questions = self._HARD_QUESTIONS
        try:
            quest = questions.popitem()
            return quest
        except KeyError as err:
            print(err)
            qts.parse_hard_questions()
            self._HARD_QUESTIONS = qts.hard_questions
            return False

    def isFit(self, message):
        for ans in self._ANSWERS:
            for answer in self._ANSWERS[ans]:
                if message == answer:
                    return True
        return False

    def check(self, received):
        difference = time.time() - float(self.timer)
        self.current_time_result += difference
        if received.upper() == self.right_answer.upper() and difference <= 25:
            return True
        return False

    def check_time(self):
        difference = time.time() - float(self.timer)
        self.current_time_result += difference
        if difference <= 35.00:
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
        self.current_question = question
        self.current_answers = answer
        self.right_answer = right
        return question

    def get_hard_question(self):
        diction = self.elect_hard_question()
        if not diction:
            return False
        number = diction[0]
        question = diction[1]['question']
        answer = self._HARD_ANSWERS[number]
        right = answ.right_hard_answers[number]
        self.current_question = question
        self.current_answers = answer
        self.right_hard_answer = right
        return question
