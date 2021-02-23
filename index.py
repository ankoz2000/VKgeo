import vk_api
import random

from bot import VkBot
from config import tkn
from cons import Test
from raiting import Raiting

from vk_api.requests_pool import VkRequestsPool, RequestResult
from vk_api.upload import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def photo_messages(session):
    url = session.method('photos.getMessagesUploadServer', {'peer_id': 0})['upload_url']
    photo_files = './pics/G.jpg'
    response = session.http.post(url, files={'photo': open(photo_files, 'rb')})
    response = session.method('photos.saveMessagesPhoto', {
        'photo': response.json()['photo'], 'server': response.json()['server'], 'hash': response.json()['hash']
    })[0]
    return f'photo{response["owner_id"]}_{response["id"]}'

def main():

    group_id = 202039114
    token = tkn

    vk_session = vk_api.VkApi(token=token)


    tests = {}
    users = Raiting()

    longpoll = VkLongPoll(vk_session)

    photo = photo_messages(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            test = tests.get(f'{event.user_id}', False)
            if not test:
                test = Test(event.user_id)
                test.reset()
                test.reset_hard()
                tests[f'{event.user_id}'] = test
            received_message = event.text
            addresser = event.user_id
            bot = VkBot(event, test, users, photo)
            bot.new_message(received_message, vk_session)
            tests[f'{event.user_id}'] = test


if __name__ == '__main__':
    main()
