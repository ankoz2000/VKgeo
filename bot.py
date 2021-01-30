import bs4 as bs4
import requests
import random

from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
from cons import Test, end

empty = VkKeyboard()


class VkBot:

    def __init__(self, event, test, users):
        print("Created")
        self._EVENT = event
        self._USER_ID = self._EVENT.user_id
        self._USERNAME = self._get_user_name_from_vk_id(self._USER_ID)['user_name']
        self._LAST_NAME = self._get_user_name_from_vk_id(self._USER_ID)['last_name']
        self._GREETINGS = {1: "Привет", 2: "Здравствуй", 3: "Приветствую"}
        self._COMMANDS = ["ПОКА", "НАЧАТЬ ОБУЧЕНИЕ", "ПРОЙТИ ТЕСТИРОВАНИЕ"]
        self.test = test
        self.users = users

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

    def new_message(self, message, session):

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
                message='После просмотра видео предлагаю тебе пройти небольшой тест.\n Обрати внимание, тест на время '
                        '(для каждого ответа отводится 15 секунд). '
                        '\nЖми кнопку по готовности ;-)',
                board=keyboard
                           )

        elif message.upper() == self._COMMANDS[2]:
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': 'Начнём',
                'random_id': get_random_id(), 'peer_id': self._USER_ID
            })
            self.test.reset()
            question = self.test.get_question()
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': question,
                'random_id': get_random_id(), 'peer_id': self._USER_ID
            })
            return

        #  Game

        elif self.test.check(message):
            question = self.test.get_question()
            if not question:
                points = self.test.POINTS
                errors = self.test.ERRORS
                self.users.add_user(self._USER_ID, self._USERNAME, self._LAST_NAME, points, errors)
                raiting = self.users.get_raiting()
                message = ''
                n = 1
                for i in raiting:
                    name = raiting[i]['data']['name']
                    last_name = raiting[i]['data']['last_name']
                    pnt = raiting[i]['points']
                    err = raiting[i]['errors']
                    end_frase = 'Ошибок'
                    point_frase = 'Правильных ответов'
                    if pnt < 5:
                        point_frase = 'Правильных ответа'
                    if pnt == 0:
                        point_frase = 'Правильных ответов'
                    if pnt == 1:
                        point_frase = 'Правильный ответ'
                    if err == 1:
                        endfrase = 'Ошибка'
                    if err < 5:
                        endfrase = 'Ошибки'
                    message += f'{n}. {name} {last_name}:\n{pnt} {point_frase} из {end + 1}.\n{err} {end_frase}\n\n\n'
                    n += 1
                session.method('messages.send', {
                    'user_id': self._USER_ID, 'message': 'Поздравляю, тест закончен. \n'
                                                         f'Правильных ответов: {points}\n\n'
                                                         'Рейтинг:\n'
                                                         f'{message}',
                    'random_id': get_random_id(), 'peer_id': self._USER_ID
                })

                return
            session.method('messages.send', {
                'user_id': self._USER_ID, 'message': question,
                'random_id': get_random_id(), 'peer_id': self._USER_ID
            })
            return

        else:
            keyboard = self.create_keyboard(position=False)
            keyboard.add_button(label='Пройти тестирование', color=VkKeyboardColor.POSITIVE)
            self.write_msg(
                session=session,
                message='Попробуй заново(',
                board=keyboard
                           )
            return

    def create_keyboard(self, position=True):
        return VkKeyboard(inline=position)

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
