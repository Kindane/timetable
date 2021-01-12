# usr/bin/python3.8
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


time_format = "%H:%M"

try:
    with open("config.json") as file:
        config = json_load(file)
    today = config["timetable"][datetime.now().strftime("%A").lower()]
except FileNotFoundError:
    print(pwd())
    print("Я не могу найти config.json.\nПожалуйста, прочитайте файл README.md")
    print("I can't find config.json.\nPlease, read README.md file")
    input()
    exit(-1)
except KeyError:
    print("Сегодня выходной (today is day off)") 
    input()
    exit(-2)
except Exception as e:
    print(f"Exception: {e}")
    input()
    exit(-3)

print("Что ты хочешь узнать?\n1 - расписание уроков на сегодня\n2 - Когда закончится этот урок/перерыв и какой следующий урок?")
choice = input(": ")


if today != config["timetable"]["friday"]:
    callShedule = config["callSchedule"]
else:
    callShedule = config["callScheduleFriday"]

if choice == '1':
    clear_console()
    for i in range(len(today)):
        lesson = today[i]
        print(f"{lesson}", end="")
        # i don't know how, but this works pretty good :D
        print(f"{callShedule[i]}".rjust(30-len(lesson)))

elif choice == '2':
    clear_console()
    now = datetime.strptime(datetime.now().strftime(time_format), time_format)
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

input("\nPress Enter to exit")
