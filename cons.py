import random
from vk_api.keyboard import VkKeyboard



end = 0  # количество вопросов


class Test:

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._QUESTIONS = {
            0: {
                'question': "Ты тут?",
                'is_elected': False
            }}
        self._ANSWERS = {0: "Да"}
        self.POINTS = 0
        self.ERRORS = 0
        self.current_question = ''
        self.current_answer = ''

    def reset(self):
        self.POINTS = 0
        self.ERRORS = 0
        self.current_question = ''
        self.current_answer = ''
        self.reset_questions()

    def save_questions(self):
        question = 'Ты тут?'
        doc = '0'
        for number in doc:
            self._QUESTIONS[number] = {
                'question': question,
                'is_elected': False
            }

    def reset_questions(self):
        questions = self._QUESTIONS
        for num in questions:
            if questions[num]['is_elected']:
                questions[num]['is_elected'] = False
        return

    def elect_question(self):
        questions = self._QUESTIONS
        for question in questions:
            n = random.randint(0, end)
            if not questions[n]['is_elected']:
                questions[n]['is_elected'] = True
                return {'question': questions[n]['question'], 'number': n}
        return False

    def check(self, received):
        print(self.current_answer.upper() + ' CUR ANS UP')
        if received.upper() == self.current_answer.upper():
            self.POINTS += 1
            print(self.POINTS)
            return True
        else:
            self.ERRORS += 1
        return False

    def get_question(self):
        diction = self.elect_question()
        print(diction)
        if not diction:
            return False
        number = diction['number']
        question = diction['question']
        answer = self._ANSWERS[number]
        self.current_question = question
        self.current_answer = answer
        return question

    def start(self):
        self.reset()
        self.save_questions()
        return self
