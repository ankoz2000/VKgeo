import re


class Questions:
    def __init__(self):
        self.questions = {}
        self.hard_questions = {}
        self.file_questions = './bot_questions/q.txt'
        self.file_hard_questions = './bot_questions/q2.txt'

    def parse_questions(self):
        with open(self.file_questions, 'r', encoding='utf-8') as read_file:
            i = 1
            for line in read_file:
                self.questions[i] = {
                    'question': line.strip('\n')
                }
                i += 1
        return self

    def parse_hard_questions(self):
        with open(self.file_hard_questions, 'r', encoding='utf-8') as read_file:
            i = 1
            for line in read_file:
                self.hard_questions[i] = {
                    'question': line.strip('\n')
                }
                i += 1
        return self


class Answers:

    def __init__(self):
        self.answers = {}
        self.hard_answers = {}
        self.hard_answers_lines = {}
        self.lines = {}
        self.right_answers = {}
        self.right_hard_answers = {}
        self.file_answers = './bot_answers/a.txt'
        self.file_right_answers = './bot_answers/r.txt'
        self.file_hard_answers = './bot_answers/a2.txt'
        self.file_right_hard_answers = './bot_answers/r2.txt'

    def add_answers(self):
        with open(self.file_answers, 'r', encoding='utf-8') as read_file:
            i = 1
            for line in read_file:
                self.lines[i] = line.strip('\n')
                i += 1
        return self

    def add_hard_answers(self):
        with open(self.file_hard_answers, 'r', encoding='utf-8') as read_file:
            i = 1
            for line in read_file:
                self.hard_answers_lines[i] = line.strip('\n')
                i += 1
        return self

    def parse_answers(self):
        lines = self.lines
        parsed = {}
        for line in lines:
            parsed[line] = re.split(r'[;]', lines[line])
        self.answers = parsed
        return self

    def parse_hard_answers(self):
        lines = self.hard_answers_lines
        parsed = {}
        for line in lines:
            parsed[line] = re.split(r'[;]', lines[line])
        self.hard_answers = parsed
        return self

    def get_right_answers(self, path, line_stack):
        with open(path, 'r', encoding='utf-8') as read_file:
            i = 1
            for line in read_file:
                line_stack[i] = line.strip('\n')
                i += 1
        lines = line_stack
        parsed = {}
        for line in lines:
            parsed[line] = re.split(r'\n', lines[line])
        return parsed

    def write_right(self):
        self.right_answers = self.get_right_answers(self.file_right_answers, self.lines,)

    def get_right_hard_answers(self):
        self.hard_answers_lines = self.get_right_answers(self.file_right_hard_answers, self.hard_answers_lines)
        parsed = {}
        lines = self.hard_answers_lines
        for line in lines:
            parsed[line] = re.split(r'[;]', str(lines[line]))
            self.right_hard_answers = parsed
        return self

    def cleaning(self, string):
        result = ''
        for i in list(string):
            if i == '"':
                result += ''
            else:
                result += str(i)
        return result
