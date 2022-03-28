#!/bin/env python
# python3 --version = 3.8.5
# GCC -v = 9.3.0 on linux
# author Kindane

from datetime import datetime
from json import load as json_load
from platform import system as get_os_type
from os import system as system_command
from os import getcwd as pwd


def clear_console():
    if get_os_type() == "Windows":
        system_command("cls")
    else:
        system_command("clear")
    return True

def convert_day(string):
    tmp = {
            "monday": "понедельник",
            "tuesday": "вторник",
            "wednesday": "среда",
            "thursday": "четверг",
            "friday": "пятница",
    }
    return tmp[string]


time_format = "%H:%M"


print("""Что ты хочешь узнать?
1 - Расписание уроков на неделю
2 - Расписание уроков на сегодня
3 - Расписание звонков
4 - Когда закончится этот урок/перерыв и какой следующий урок? """)
choice = int(input(": "))


try:
    with open("config.json") as file:
        config = json_load(file)
    if choice == 2 or choice == 4:
        today = config["уроки"][convert_day(datetime.now().strftime("%A").lower())]
        #today = config["уроки"]["понедельник"] # DEBUG
        if today != config["уроки"]["пятница"]:
            callShedule = config["звонки"]
        else:
            callShedule = config["звонкиПт"]
except FileNotFoundError:
    print(pwd())
    print("Я не могу найти config.json.\nПожалуйста, прочитайте файл README.md")
    exit(-1)
except KeyError:
    print("Сегодня выходной")
    exit(0)




if choice == 1:
    clear_console()
    daynames = ("понедельник", "вторник", "среда", "четверг", "пятница")
    # Print the names of the columns.
    print ("   {:<20} {:<20} {:<20} {:<20} {:<20}\n".format(*daynames))
    tmp = list()
    num_of_lesson = 0
    for i in range(8):
        for day in daynames:
            try:
                tmp.append(config["уроки"][day][num_of_lesson])
            except IndexError:
                tmp.append("")
        print(num_of_lesson+1, ". ", end="", sep="")
        print ("{:<20} {:<20} {:<20} {:<20} {:<20}".format(*tmp))
        tmp = list()
        num_of_lesson += 1


if choice == 2:
    clear_console()
    for i in range(len(today)):
        lesson = today[i]
        print(f"{i+1}. {lesson}", end="")
        # i don't know how, but this works pretty good :D
        print(f"{callShedule[i]}".rjust(30-len(lesson)))

elif choice == 3:
    clear_console()
    x = zip(config["звонки"], config["звонкиПт"])
    print ("   {:<20} {:<20}".format("Пн-Чт", "Пт"))
    for num, i in enumerate(tuple(x), 1):
        print(num, ". ", sep="", end="")
        print ("{:<20} {:<20}".format(i[0], i[1]))
    

elif choice == 4:
    clear_console()
    now = datetime.strptime(datetime.now().strftime(time_format), time_format)
    if now > datetime.strptime(callShedule[-1].split("-")[1], time_format):
        print("Уроки уже закончились, отдыхай!")
        exit()
    if now < datetime.strptime(callShedule[0].split("-")[0], time_format):
        print("{0} начнётся через {1} минут(ы)".format(
            today[0], int((datetime.strptime(callShedule[0].split("-")[0],
                time_format) - now).seconds/60)))
        exit()
    lesson_number = -1
    is_coffe_break = False
    for i in range(len(today)):
        tuple_time = callShedule[i].split("-")
        start_lesson = datetime.strptime(tuple_time[0], time_format)
        end_lesson = datetime.strptime(tuple_time[1], time_format)
        next_start_lesson = datetime.strptime(callShedule[i+1].split("-")[0], time_format)
        if now >= start_lesson and now < end_lesson:
            lesson_number = i
            print("У тебя сейчас: {}".format(today[i]))
            break

        if now >= end_lesson and now < next_start_lesson:
            is_coffe_break = True
            lesson_number = i
            break
    
    # on the lesson
    if not is_coffe_break:
        current_lesson = today[lesson_number]
        left = end_lesson-now
        print("Потерпи ещё немного, до конца урока осталось: {} минут(ы)".format(int(left.seconds/60)))
        try:
            print("Следующий урок: {}".format(today[lesson_number+1]))
        except IndexError:
            print("Дальше уроков нет")

    # on the break
    else:
        print("Следующий урок: {}".format(today[lesson_number+1]))
        print("Начало урока через: {} минут(ы)".format(int((next_start_lesson-now).seconds/60)))
