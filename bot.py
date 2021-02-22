import bs4 as bs4
import requests
import random
import time

from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
from vk_api.execute import VkFunction
from cons import Test, end, end2

empty = VkKeyboard()


class VkBot:

    def __init__(self, event, test, users, photo):
        self._EVENT = event
        self._USER_ID = self._EVENT.user_id
        self._USERNAME = self._get_user_name_from_vk_id(self._USER_ID)['user_name']
        self._LAST_NAME = self._get_user_name_from_vk_id(self._USER_ID)['last_name']
        self._GREETINGS = {1: "Привет", 2: "Здравствуй", 3: "Приветствую"}
        self._COMMANDS = ["ПОКА", "НАЧАТЬ ОБУЧЕНИЕ", "ПРОЙТИ ТЕСТИРОВАНИЕ", "ПРОВЕРИТЬ", "ДАЛЕЕ"]
        self.test = test
        self.users = users
        self.counter = 0
        self.photo = photo
        self.wall = 1
        self.gid = 202039114

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        last_name = self._clean_all_tag_from_str(bs.find_all("title")[0])
        return {'user_name': user_name.split()[0], 'last_name': last_name.split()[1]}

    def write_msg(self, session, message, board=empty):
        return session.method('messages.send', {
            'user_id': self._USER_ID, 'message': message,
            'random_id': get_random_id(), 'peer_id': self._USER_ID, 'keyboard': board.get_keyboard()
        })

    def hard(self, session):
        question = self.test.get_hard_question()
        check = self.check_hard(question)
        if check:
            message = check['message']
            points = check['hard_points']
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': 'Тест закончен. \n'
                                                     f'Правильных ответов: {points}\n'
                                                     f'Время: {round(self.test.current_time_result)} сек.\n\n'
                                                     'Рейтинг:\n'
                                                     f'{message}',
                'random_id': get_random_id(), 'peer_id': self._USER_ID, 'keyboard': empty.get_empty_keyboard()
            })
            wall = session.method('groups.edit', {'group_id': self.gid, 'description': message})
            print(wall)
            '''self.wall = session.method('wall.edit', {'owner_id': -self.gid, 'post_id': wall, 'message': message})
            else:
                self.wall = session.method('wall.post', {'owner_id': -self.gid, 'message': message})'''
            return False
        answers = self.test.current_answers
        keyboard = self.create_keyboard(position=False)
        i = 0
        n = 0
        for answer in answers:
            if i % 2 == 0 and i != 0:
                keyboard.add_line()
            keyboard.add_button(label=f'{answers[n]}', color=VkKeyboardColor.SECONDARY)
            i += 1
            n += 1
        keyboard.add_line()
        keyboard.add_button(label='Далее', color=VkKeyboardColor.POSITIVE)
        session.method('messages.send', {
            'user_id': self._USER_ID, 'message': question,
            'random_id': get_random_id(), 'peer_id': self._USER_ID,
            'keyboard': keyboard.get_keyboard()
        })
        self.test.timer = self.test.timer.time()

    def new_message(self, message, session):

        '''if message.upper() == 'GO':
            i = random.randint(1, 3)
            keyboard = self.create_keyboard(position=True)
            keyboard.add_button(label='Начать', color=VkKeyboardColor.POSITIVE)
            self.write_msg(
                session=session,
                message=f'{self._GREETINGS[i]}, {self._USERNAME}!',  Написать вступительное сообщение
                board=keyboard)
            return'''
        if message.upper() == 'GO':
            i = random.randint(1, 3)
            keyboard = self.create_keyboard(position=True)
            keyboard.add_button(label='Начать', color=VkKeyboardColor.POSITIVE)
            return

        if message.upper() == 'ПРИВЕТ' or message.upper() == 'ХАЙ' or message.upper() == 'HELLO' \
                or message.upper() == 'НАЧАТЬ':
            i = random.randint(1, 3)
            keyboard = self.create_keyboard(position=True)
            keyboard.add_button(label='Начать обучение', color=VkKeyboardColor.POSITIVE)
            self.write_msg(
                session=session,
                message=f'{self._GREETINGS[i]}, {self._USERNAME}!',
                board=keyboard)
            return

        elif message.upper() == self._COMMANDS[0]:
            return f"Пока-пока, {self._USERNAME}!"

        elif message.upper() == self._COMMANDS[1]:
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': 'Посмотри это видео:',
                'random_id': get_random_id(), 'peer_id': self._USER_ID,
                'attachment': 'video490797033_456239056',
            })
            keyboard = self.create_keyboard(position=True)
            keyboard.add_button(label='Пройти тестирование', color=VkKeyboardColor.POSITIVE)
            self.write_msg(
                session=session,
                message='После просмотра видео предлагаю тебе пройти небольшой тест.\nОбрати внимание, тест на время '
                        '(для каждого ответа отводится 15 секунд). '
                        '\nЖми кнопку по готовности ;-)',
                board=keyboard
                           )

        elif message.upper() == self._COMMANDS[2] or message.upper() == 'ТЕСТ 1':
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': 'Начнём',
                'random_id': get_random_id(), 'peer_id': self._USER_ID
            })
            self.test.reset()
            question = self.test.get_question()
            answers = self.test.current_answers
            keyboard = self.create_hidden_keyboard(position=False)
            i = 0
            n = 0
            #for answer in answers:
            #    if i % 2 == 0 and i != 0:
            #        keyboard.add_line()
            #    keyboard.add_button(label=f'{answers[n]}', color=VkKeyboardColor.SECONDARY)
            for answer in answers:
                if i % 3 == 0 and i != 0:
                    keyboard.add_line()
                keyboard.add_button(label=f'{answers[n]}', color=VkKeyboardColor.SECONDARY)
                i += 1
                n += 1
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': question,
                'random_id': get_random_id(), 'peer_id': self._USER_ID,
                'keyboard': keyboard.get_keyboard()
            })
            self.test.timer = self.test.timer.time()
            return

        elif message.upper() == self._COMMANDS[3] or message.upper() == 'ТЕСТ 2':
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': 'Начинаем!',
                'random_id': get_random_id(), 'peer_id': self._USER_ID
            })
            self.test.reset_hard()
            self.hard(session)
            return
        #  Game
        elif message.upper() == self._COMMANDS[4]:
            if self.test.check_time():
                if self.test.points_buff < 0:
                    self.test.points_buff = 0
                self.test.HARD_POINTS += self.test.points_buff
                self.test.points_buff = 0
            # Continue
                self.test.timer = time
                self.hard(session)
            else:
                self.test.timer = time
                self.test.points_buff = 0
                self.hard(session)

        elif self.test.check_hard(message):
            check = self.test.check_hard_right_answer(message)
            if check:
                self.test.points_buff += 1
            else:
                if self.test.points_buff >= 0:
                    self.test.points_buff -= 1
            return

        elif self.test.check(message) and self.test.isFit(message):
            self.test.POINTS += 1
            question = self.test.get_question()
            check = self.check(question)
            if check:
                message = check['message']
                points = check['points']
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': 'Поздравляю, тест закончен. \n'
                                                         f'Правильных ответов: {points}'
                                                         f'Время: {round(self.test.current_time_result)} сек.\n\n'
                                                         'Рейтинг:\n'
                                                         f'{message}',
                    'random_id': get_random_id(), 'peer_id': self._USER_ID, 'keyboard': empty.get_empty_keyboard()
                })
                self.test.timer = time
                self.next_task(session)
                return
            answers = self.test.current_answers
            keyboard = self.create_hidden_keyboard(position=False)
            i = 0
            m = 0
            #for answer in answers:
            #    if i % 2 == 0 and i != 0:
            #        keyboard.add_line()
            #    keyboard.add_button(label=f'{answers[m]}', color=VkKeyboardColor.SECONDARY)
            for answer in answers:
                if i % 3 == 0 and i != 0:
                    keyboard.add_line()
                keyboard.add_button(label=f'{answers[m]}', color=VkKeyboardColor.SECONDARY)
                i += 1
                m += 1
            if self.isNeedPhoto(question):
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': question,
                    'random_id': get_random_id(), 'peer_id': self._USER_ID,
                    'keyboard': keyboard.get_keyboard(), 'attachment': self.photo
                })
            else:
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': question,
                    'random_id': get_random_id(), 'peer_id': self._USER_ID,
                    'keyboard': keyboard.get_keyboard()
                })
            self.test.timer = time.time()
            return

        elif not self.test.check(message) and self.test.isFit(message):
            self.test.ERRORS += 1
            question = self.test.get_question()
            check = self.check(question)
            is_need_photo = self.isNeedPhoto(question)
            if check:
                message = check['message']
                points = check['points']
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': 'Тест закончен. \n'
                                                         f'Правильных ответов: {points}'
                                                         f'Время: {round(self.test.current_time_result)} сек.\n\n'
                                                         'Рейтинг:\n'
                                                         f'{message}',
                    'random_id': get_random_id(), 'peer_id': self._USER_ID, 'keyboard': empty.get_empty_keyboard()
                })
                self.test.timer = time
                self.next_task(session)
                return
            answers = self.test.current_answers
            keyboard = self.create_hidden_keyboard(position=False)
            i = 0
            m = 0
            for answer in answers:
                if i % 2 == 0 and i != 0:
                    keyboard.add_line()
                keyboard.add_button(label=f'{answers[m]}', color=VkKeyboardColor.SECONDARY)
                i += 1
                m += 1
            photo = None
            if self.isNeedPhoto(question):
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': question,
                    'random_id': get_random_id(), 'peer_id': self._USER_ID,
                    'keyboard': keyboard.get_keyboard(), 'attachment': self.photo
                })
            else:
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': question,
                    'random_id': get_random_id(), 'peer_id': self._USER_ID,
                    'keyboard': keyboard.get_keyboard()
                })
            self.test.timer = time.time()
            return

        elif not self.test.isFit(message) and not self.test.check_hard(message):
            keyboard = self.create_hidden_keyboard(position=False)
            keyboard.add_button(label='Тест 1', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(label='Тест 2', color=VkKeyboardColor.POSITIVE)
            self.write_msg(
                session=session,
                message='Попробуй заново.',
                board=keyboard.get_keyboard()
                           )
            return

    def create_keyboard(self, position=True):
        return VkKeyboard(inline=position)

    def create_hidden_keyboard(self, position=True):
        return VkKeyboard(inline=position, one_time=True)

    def next_task(self, session):
        keyboard = self.create_keyboard(position=True)
        keyboard.add_button(label='Проверить', color=VkKeyboardColor.POSITIVE)
        self.write_msg(
            session=session,
            message='Проверь себя! Можешь ли ты считаться знатоком по географии Костромской области?'
                    '\nЧтобы ответить правильно на вопросы, нужно изучить 1 и 2 разделы книги '
                    '"География Костромской области".\n\nПравила те же, на ответ - 15 секунд,'
                    ' но вариантов ответов может быть несколько!\n Обязательно нажми кнопку "Далее" '
                    'после выбора варианта(-ов) ответа.\n\nЖми кнопку ниже, чтобы начать.',
            board=keyboard
        )
        self.test.reset_hard()

    def check_hard(self, question):
        if not question:
            h_points = self.test.HARD_POINTS
            tm = self.test.current_time_result  # test-time
            self.users.add_user_hard(self._USER_ID, self._USERNAME, self._LAST_NAME, h_points, tm)
            rating = self.users.get_hard_rating()
            message = ''
            n = 1
            for i in rating:
                name = rating[i]['data']['name']
                last_name = rating[i]['data']['last_name']
                pnt = rating[i]['hard_points']
                self_time = round(rating[i]['time'])
                point_frase = 'Правильных ответов'
                if pnt < 5:
                    point_frase = 'Правильных ответа'
                if pnt == 0:
                    point_frase = 'Правильных ответов'
                if pnt == 1:
                    point_frase = 'Правильный ответ'
                message += f'{n}. {name} {last_name}:\n{pnt} {point_frase} из {end2}.\n\n' \
                           f'Время: {self_time} сек.\n\n\n'
                n += 1
            return {'message': message, 'hard_points': h_points}
        return False

    def check(self, question):
        if not question:
            points = self.test.POINTS
            errors = self.test.ERRORS
            tm = self.test.current_time_result  # test-time
            self.users.add_user(self._USER_ID, self._USERNAME, self._LAST_NAME,
                                points, errors, tm)
            raiting = self.users.get_raiting()
            message = ''
            n = 1
            for i in raiting:
                name = raiting[i]['data']['name']
                last_name = raiting[i]['data']['last_name']
                pnt = raiting[i]['points']
                err = raiting[i]['errors']
                self_time = round(raiting[i]['time'])
                end_frase = 'Ошибки'
                point_frase = 'Правильных ответов'
                if pnt < 5:
                    point_frase = 'Правильных ответа'
                if pnt == 0:
                    point_frase = 'Правильных ответов'
                if pnt == 1:
                    point_frase = 'Правильный ответ'
                if err == 0 or err == 5:
                    end_frase = 'Ошибок'
                if err == 1:
                    end_frase = 'Ошибка'
                message += f'{n}. {name} {last_name}:\n{pnt} {point_frase} из {end}.\n{err} {end_frase}.\n' \
                           f'Время: {self_time} сек.\n\n\n'
                n += 1
            return {'message': message, 'points': points}
        return False

    def isNeedPhoto(self, question):
        if question == 'В каком населённом пункте Костромской области была написана картина?':
            return True
        return False


    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result
