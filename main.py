import os
import re
from tkinter import messagebox
from typing import Callable


class Subject:

    def __init__(self, name: str = '<unknown>', credit: int = None, score: float = None):
        self.name = name
        if (credit is None) | (score is None):
            handler(ValueError(
                f'Require input for {'|credit|' if (credit is None) else ''} {'|score|' if (score is None) else ''}'))
        if credit < 0:
            handler(ValueError('Requires a non-negative number for credit'))
        if not 0 <= score <= 10:
            handler(ValueError('Score must be >= 0 and <= 10'))
        self.credit = credit
        self.score = score

    def __str__(self):
        return f'Subject({self.name}, credit:{self.credit}, score:{self.score:.01f})'


class Student:
    def __init__(self, name: str = '<unknown>', subjects=None):
        if subjects is None:
            subjects = []
        self.name = name
        self.subjects: list[Subject] = subjects

    def __str__(self):
        output = f'Student name: {self.name}'
        tableHeader = f'|{'Subject':^20}|{'Credit':^10}|{'Score':^10}|'
        output += f'\n+{'-' * 20}+{'-' * 10}+{'-' * 10}+'
        output += f'\n{tableHeader}'
        output += f'\n+{'-' * 20}+{'-' * 10}+{'-' * 10}+'
        if len(self.subjects) <= 0:
            output += f'\n|{'Empty':^42}|'
        else:
            for subject in self.subjects:
                output += f'\n| {subject.name:<19}|{subject.credit:^10}|{subject.score:^10}|'
            output += f'\n+{'-' * 20}+{'-' * 10}+{'-' * 10}+'
            output += f'\n|{f'GPA: {calculate_gpa(self):.1f}':^42}|'
        output += f'\n+{'-' * 20}+{'-' * 10}+{'-' * 10}+\n'
        return output


def calculate_gpa(student: Student = None) -> float:
    checkNone(student, 'Provide a student!')
    total_credit = 0
    total_score = 0
    for subject in student.subjects:
        total_credit += subject.credit
        total_score += subject.score * subject.credit
    return 0 if total_credit == 0 else total_score / total_credit


def print_gpa(student: Student = None):
    checkNone(student, 'Provide a student!')
    print(str(student))


def checkNone(any, errorMessage: str = ''):
    if any is None:
        handler(ValueError(errorMessage))


def writer(any: Student):
    file = f'{any.name}.txt'
    if not bool(file):
        handler(ValueError('File not choose'))
    checkNone(any, "Input can not be None")
    with open(file, 'wt') as file:
        file.writelines(str(any))
        print(f'\nFile saved to {os.path.abspath(file.name)}\n')


def handler(exception: BaseException):
    messagebox.showerror(type(exception).__name__, str(exception))
    raise exception


def getTypedInput(prompt: str = '', desireType: type = str,
                  condition: Callable[[()], bool] = lambda o: True,
                  conditionErrorMessage: str = 'Conditions are not met'):
    raw = input(f'({desireType.__name__}) {prompt}: ')
    raw = raw.strip()
    try:
        processed = desireType(raw)
        if not condition(processed):
            print(conditionErrorMessage)
            return getTypedInput(prompt, desireType, condition, conditionErrorMessage)
    except ValueError as e:
        print(f'Type mismatch. Require <{desireType.__name__}> but received "{raw}"')
        return getTypedInput(prompt, desireType, condition, conditionErrorMessage)
    return processed


def studentDataCollector() -> Student:
    namePattern = re.compile('^[A-Za-z ]+$')
    student: Student = Student()
    nameInput: str = getTypedInput('Enter your name', str, lambda name: not namePattern.fullmatch(name) is None,
                                   'Name must match a-z | A-Z | \' \'')

    student.name = '<unknown>' if (nameInput is None) | (len(nameInput) <= 0) else nameInput

    subjectList = []
    while True:
        print(f'Current subject list: {subjectList}')
        newSubject: str = getTypedInput('New subject name (Enter without type anything to finish)', str,
                                        lambda name: len(name) <= 20, 'Subject name must less than 20')
        if len(newSubject) <= 0 | newSubject.isspace():
            print()
            break
        else:
            if [subjectName.lower() for subjectName in subjectList].__contains__(newSubject.lower().strip()):
                print(f'Duplicate {newSubject}')
            else:
                subjectList.append(newSubject)

    for sName in subjectList:
        sCredit = getTypedInput(f'{sName} credit', int, lambda credit: credit >= 0, 'Credit must not negative')
        sScore = getTypedInput(f'{sName} score', float, lambda score: 0 <= score <= 10, 'Score must be >= 0 and <= 10')
        subject = Subject(sName, sCredit, sScore)
        student.subjects.append(subject)
        print()

    saveToFile: str = getTypedInput('Save student data to file? (Y/N)', str,
                                    lambda action: action in ['Y', 'y', 'N', 'n'],
                                    'Y or N only')
    if saveToFile.lower() == 'y':
        writer(student)
    print_gpa(student)
    return student


if __name__ == '__main__':
    studentDataCollector()
