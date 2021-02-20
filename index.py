import vk_api
import random

from bot import VkBot
from config import tkn
from cons import Test
from raiting import Raiting

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def main():

    group_id = 202039114
    token = tkn

    vk_session = vk_api.VkApi(token=token)

    tests = {}
    users = Raiting()

    longpoll = VkLongPoll(vk_session)
    print("Started")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if not tests.get(f'{event.user_id}', False):
                test = Test(event.user_id)
                test.reset()
                tests[f'{event.user_id}'] = test
            else:
                test = tests.get(f'{event.user_id}')
            received_message = event.text
            addresser = event.user_id
            bot = VkBot(event, tests.get(f'{event.user_id}'), users)
            bot.new_message(received_message, vk_session)
            tests[f'{event.user_id}'] = test
            print('Текст:', received_message)
            print()

        #elif event.type == VkEventType.GROUP_JOIN:
         #   print(event.obj.user_id, end=' ')

         #   print('Вступил в группу!')
         #   print()

        else:
            print(event.type)
            print()


if __name__ == '__main__':
    main()
