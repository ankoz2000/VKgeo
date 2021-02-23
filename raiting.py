from operator import itemgetter


class Raiting:
    def __init__(self):
        self.USERS = {}
        self.USERS_HARD = {
            '138437140': {
                'data': {
                    'name': 'Андрей', 'last_name': 'Козлов'
                }, 'hard_points': 14, 'time': 41.279115438461304},
            '221749260': {
                'data': {
                    'name': 'Арина', 'last_name': 'Белокрыльцева'
                }, 'hard_points': 8, 'time': 139.67671012878418},
            '236673429': {
                'data': {
                    'name': 'Сергей', 'last_name': 'Быстров'
                }, 'hard_points': 8, 'time': 87.47103905677795},
            '59428300': {
                'data': {
                    'name': 'Андрей', 'last_name': 'Жуйков'
                }, 'hard_points': 6, 'time': 237.07635712623596}
        }

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

    def add_user_hard(self, user_id, user_name, user_last_name, points, time):
        self.USERS_HARD[user_id] = {
            'data': {
                'name': user_name,
                'last_name': user_last_name
            },
            'hard_points': points,
            'time': time
        }
        return

    def get_raiting(self):
        users = self.sort_users()
        return users

    def get_hard_rating(self):
        users = self.sort_users_hard()
        return users

    def sort_users_hard(self):
        users = self.USERS_HARD
        users_list = list(users.items())
        print(users_list)
        users_list.sort(key=lambda user: [user[1]['hard_points'], -int(user[1]['time'])], reverse=True)

        diction = {}
        for user in users_list:
            diction[user[0]] = {
                'data': {
                    'name': user[1]['data']['name'],
                    'last_name': user[1]['data']['last_name']
                },
                'hard_points': user[1]['hard_points'],
                'time': user[1]['time']
            }
        return diction

    def sort_users(self):
        users = self.USERS
        users_list = list(users.items())
        # users_list.sort(key=lambda user: user[1]['points'], reverse=True)
        users_list.sort(key=lambda user: [user[1]['points'], -int(user[1]['time'])], reverse=True)
        # users_list = sorted(users.items(), key=itemgetter('points', 'time'), reverse=True)

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
