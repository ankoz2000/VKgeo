from operator import itemgetter


class Raiting:
    def __init__(self):
        self.USERS = {}

    def add_user(self, user_id, user_name, user_last_name, points, errors, time):
        self.USERS[user_id] = {
            'data': {
                'name': user_name,
                'last_name': user_last_name
            },
            'points': points,
            'errors': errors,
            'time': time
        }
        return

    def get_raiting(self):
        users = self.sort_users()
        return users

    def sort_users(self):
        users = self.USERS
        users_list = list(users.items())
        #users_list.sort(key=lambda user: user[1]['points'], reverse=True)
        users_list.sort(key=lambda user: [user[1]['points'], -int(user[1]['time'])], reverse=True)
        #users_list = sorted(users.items(), key=itemgetter('points', 'time'), reverse=True)

        diction = {}
        for user in users_list:
            diction[user[0]] = {
                'data': {
                    'name': user[1]['data']['name'],
                    'last_name': user[1]['data']['last_name']
                },
                'points': user[1]['points'],
                'errors': user[1]['errors'],
                'time': user[1]['time']
            }
        return diction
