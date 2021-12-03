# Program     : TODO List (TUD - Tallaght Edition)
# Language    : Python
# Version     : 3.9
# Author      : Ken
# Created     : 10/09/2020
# Modified    : 30/11/2021

from datetime import datetime
from datetime import date
from pathlib import Path
import os
import re
import sys

title = "TODO List: Technological University Dublin - Tallaght | Computing Semester 1 [2021/2022]"
border = ("=" * 145)
# Course modules
SDEV = "Software Development"
CSD = "Critical Skills Development"
CA = "Computer Architecture"
MATHS = "Discrete Mathematics"
BIS = "Business & Information Systems"
VDUE = "Visual Design & User Experience"
MISC = "Miscellaneous"
# Command list
CMD_CANCEL = "!cancel"
CMD_HELP = "help"
CMD_DEL = "del"
CMD_ADD = "add"
CMD_SCHEDULE = "sched"
CMD_EXIT = "exit"

path = Path(r"Path\todo.txt")  # Path to todo.txt


def create_file():
    """
    Initialises text file creation used to store the data.
    If text file does not exist, it will be created.
    """
    if not os.path.exists(path):
        with open(path, "w+") as file_create:
            file_create.close()

    if os.stat(path).st_size == 0:
        header = "[Task #]\t[Days Left]\t[Due Date]\t[Module]\t\t\t\t[Type]\t\t[Description]\n"
        with open(path, "a") as todo_header:
            todo_header.write(header.upper())
            todo_header.close()


def task_list(get_task):
    """
    Displays enumerated list of task sorted from furthest to nearest due. The timedelta measured
    by the number of days left is updated if applicable and the data in the text file is overwritten
    for every instance this function is called.

    :argument get_task integer representing the task number to retrieve information from.
    :return string containing task subject, type and description only.
    """
    task_info = list()
    header = ""

    with open(path, "r") as file:
        lines = file.readlines()
        file.close()
        todo_list = list()
        overdue = list()

    for num, line in enumerate(lines):
        if num == 0:
            header = line
        else:
            date_pattern = re.compile(r"\d\d/\d\d/\d\d\d\d")
            get_date = date_pattern.search(line).group()
            entry_date = get_date.split("/")
            day = int(entry_date[0])
            month = int(entry_date[1])
            year = int(entry_date[2])
            due_date = date(year, month, day)
            delta = due_date - date.today()

            line_split = line.split("\t")
            if not line_split[2].isdigit() and line_split[2] != "Overdue".upper() and \
                    not line_split[2].startswith("-"):
                if delta.days < 0:
                    todo_list.append("\t\tOverdue\t".upper() + line)
                else:
                    todo_list.append(f"\t\t{delta.days}\t" + line)
            elif line_split[2].isdigit() and delta.days >= 0:
                line_split[2] = str(delta.days)
                todo_list.append("\t".join(line_split))
            elif delta.days < 0 or line_split[2].startswith("-"):
                line_split[2] = "Overdue".upper()
                todo_list.append("\t".join(line_split))

    with open(path, "w") as todo_sorted:
        todo_sorted.write(header)
        for new in sorted(todo_list, key=lambda x: list(map(int, re.findall(r"\d+", x))), reverse=True):
            if "Overdue".upper() in new:
                overdue.append(new)
            else:
                todo_sorted.write(new)

        for od in overdue:
            todo_sorted.write(od)

        todo_sorted.close()

    with open(path, "r") as todo:
        print()
        lines = todo.readlines()
        todo.close()
        for num, line in enumerate(lines):
            if num == 0:
                print(line)
            elif num == get_task:
                print(num, line, end='')
                split_line = line.split("\t")
                for element in split_line:
                    for e in element.split():
                        if e[0].isalpha():
                            task_info.append(element)
                            break
            else:
                print(num, line, end='')

    print("\n")
    return task_info


def add_task():
    """Adds a new task entry."""
    adding_task = True
    while adding_task:
        cancel_operation = False
        subject_list = {
            0: "Cancel",
            1: f"{SDEV}\t",
            2: CSD,
            3: f"{CA}\t",
            4: f"{MATHS}\t",
            5: BIS,
            6: VDUE,
            7: f"{MISC}\t\t",
        }

        with open(path, "a") as task_add:
            print("\nSelect the task subject\n".upper())

            for key, value in subject_list.items():
                print(f"[{key}]", value)

            adding_subject = True
            while adding_subject:
                try:
                    subject = int(input("\nSubject: "))
                    if subject < 0 or subject > 9:
                        print("ERROR! Input out of range.")
                        continue

                    if subject == 0:
                        os.system("cls")
                        print(border)
                        print("No changes has been made.".upper())
                        print(border)
                        adding_subject = False
                        cancel_operation = True
                        continue

                    for key, value in subject_list.items():
                        if subject == key:
                            subject = f"\t{value}"
                    adding_subject = False
                except ValueError:
                    print("Please input the number of the corresponding subject.")

            if cancel_operation:
                adding_task = False
                continue

            os.system("cls")
            type_list = {
                0: "Cancel",
                1: "Lab\t",
                2: "C.A.\t",
                3: "Quiz\t",
                4: "Exam\t",
                5: "Others\t",
            }
            print("\nSelect the task type\n".upper())

            for key, value in type_list.items():
                print(f"[{key}]", value)

            selecting_type = True
            while selecting_type:
                try:
                    task_type = int(input("\nTask type: "))
                    if task_type < 0 or task_type > len(type_list):
                        print("ERROR! Input out of range.")
                        continue

                    if task_type == 0:
                        os.system("cls")
                        print(border)
                        print("No changes has been made.".upper())
                        print(border)
                        selecting_type = False
                        cancel_operation = True
                        continue

                    for key, value in type_list.items():
                        if task_type == key:
                            task_type = f"\t\t{value}"
                    selecting_type = False
                except ValueError:
                    print("Please input the number of the corresponding task type.")

            if cancel_operation:
                adding_task = False
                continue

            os.system("cls")
            print("\nInput task due date or '{}' to cancel".upper().format(CMD_CANCEL))
            selecting_date = True
            while selecting_date:
                try:
                    due_date = input("\nDue date (DD/MM/YYYY): ")
                    date_split = due_date.split("/")

                    if due_date == f"{CMD_CANCEL}":
                        os.system("cls")
                        print(border)
                        print("No changes has been made.".upper())
                        print(border)
                        selecting_date = False
                        cancel_operation = True
                        continue

                    if list(due_date)[2] and list(due_date)[5] != "/":
                        print("ERROR! Invalid date format.")
                        continue

                    if int(date_split[0]) < 1 or int(date_split[0]) > 31:
                        print("ERROR! Date day value out of range.")
                        continue

                    if int(date_split[1]) < 1 or int(date_split[1]) > 12:
                        print("ERROR! Date month value out of range.")
                        continue

                    if int(date_split[2]) < 2020 or int(date_split[2]) > 9999:
                        print("ERROR! Date year value out of range.")
                        continue

                    if 1 <= int(date_split[0]) <= 31 \
                            and 1 <= int(date_split[1]) <= 12 \
                            and 2020 <= int(date_split[2]) <= 9999:
                        day = int(date_split[0])
                        month = int(date_split[1])
                        year = int(date_split[2])
                        date_due = date(year, month, day)
                        delta = date_due - date.today()
                        if delta.days < 0:
                            print("ERROR! Please input present or later date.")
                            continue

                        due_date = f"\t{date_due.strftime('%d/%m/%Y')}"
                        selecting_date = False
                except (ValueError, IndexError):
                    print("ERROR! Invalid date.")

            if cancel_operation:
                adding_task = False
                continue

            os.system("cls")
            min_desc = 4
            max_desc = 40
            print("\nInput Task description ({}-{} characters) or '{}' to cancel".upper().format(min_desc,
                                                                                                 max_desc,
                                                                                                 CMD_CANCEL))
            adding_desc = True
            while adding_desc:
                try:
                    desc = input("\nTask description: ")
                    if desc == f"{CMD_CANCEL}":
                        os.system("cls")
                        print(border)
                        print("No changes has been made.".upper())
                        print(border)
                        adding_desc = False
                        cancel_operation = True
                        continue

                    if not desc[0].isalpha():
                        print("Description must start with a letter.")
                        continue

                    if min_desc <= len(desc) <= max_desc:
                        desc = f"\t{desc}\r"
                        adding_desc = False
                    else:
                        print(f"Min {min_desc} to Max {max_desc} characters only.")
                        continue
                except IndexError:
                    print("Invalid description.")

            if cancel_operation:
                adding_task = False
                continue

            task_add.write(due_date)
            task_add.write(subject)
            task_add.write(task_type)
            task_add.write(desc)
            task_add.close()
            os.system("cls")
        print(border)
        print("Task successfully created!".upper())
        print(border)
        adding_task = False


def delete_task():
    """Removes a task from the list."""
    print(border)
    print("Deleting a task from the list. Input '0' to cancel.".upper())
    print(border)
    task_list(None)
    deleting_task = True
    while deleting_task:
        try:
            task_del = int(input("Enter task number to delete: "))
            if task_del > ((len(open(path).readlines())) - 1):
                print("ERROR! Input out of range.\n")
                continue

            if task_del == 0:
                os.system("cls")
                print(border)
                print("No changes has been made.".upper())
                print(border)
                deleting_task = False
                continue

            os.system("cls")
            print(border)
            print("Confirm action.".upper())
            print(border)
            delete_line = task_list(task_del)
            print("Permanently deleting: {}".upper().format(' | '.join(delete_line).strip()))

            confirm_action = input("Are you sure you want to continue? (Y/N): ").lower()
            if confirm_action == "y":
                with open(path, "r") as todo:
                    lines = todo.readlines()
                    del lines[task_del]
                    todo.close()

                with open(path, "w") as todo:
                    for line in lines:
                        todo.write(line)
                    todo.close()

                os.system("cls")
                print(border)
                print("Task successfully deleted!".upper())
                print(border)
                deleting_task = False
            elif confirm_action == "n":
                os.system("cls")
                print(border)
                print("No changes has been made.".upper())
                print(border)
                deleting_task = False
            else:
                os.system("cls")
                print(border)
                print("ERROR! Invalid input. No changes has been made. Enter '0' to cancel".upper())
                print(border)
                task_list(None)
        except (ValueError, IndexError):
            print("ERROR! Invalid input.\n")


def schedule():
    guide = f"""
    =============================================================================================================
    COURSE/GROUP: Computing (TU859) - Group 1A(1) | CLASS TUTOR: Tutor Name - tutor@email.ie
    =============================================================================================================
    
    [MODULE CODE]       [MODULE NAME]                       [LECTURER]              [CONTACT]                          
       
    SDev                Software Development                Lecturer Name           lecturer@email.ie        
    CSD                 Critical Skills Development         Lecturer Name           lecturer@email.ie        
    Comp Arch           Computer Architecture               Lecturer Name           lecturer@email.ie      
    Maths               Discrete Mathematics                Lecturer Name           lecturer@email.ie          
    BIS                 Business & Information Systems      Lecturer Name           lecturer@email.ie           
    VDUE                Visual Design & User Experience     Lecturer Name           lecturer@email.ie             
    
    
    Current Date/Time: {datetime.now().strftime("%A | %d %B %Y | %H:%M")}
    """

    monday = """
    ===================================================================================
                                    MONDAY Timetable
    ===================================================================================
    
    [MODULE]                [TIME]              [LOCATION]      [DURATION]      [GROUP]
           
    Comp Arch               09:00 - 11:00       Online          2 Hours         1A          
    BIS Lab                 11:00 - 12:00       Online          1 Hour          1A(1)      
    SDev                    12:00 - 13:00       Online          1 Hour          1A          
    <FREE TIME>             13:00 - 14:00       -               1 Hour          -           
    Maths                   14:00 - 16:00       Online          2 Hours         1A          
    VDUE                    16:00 - 17:00       Online          1 Hour          1A       
    """

    tuesday = """
    ===================================================================================
                                    TUESDAY Timetable
    ===================================================================================
    
    [MODULE]                [TIME]              [LOCATION]      [DURATION]      [GROUP]
         
    Comp Arch Lab           09:00 - 10:00       Online          1 Hour          1A(1)       
    <FREE TIME>             10:00 - 11:00       -               1 Hour          -           
    CSD                     11:00 - 12:00       Online          1 Hour          1A(1)       
    <FREE TIME>             12:00 - 14:00       -               2 Hours         -          
    BIS (Week 8 & 9 ONLY)   14:00 - 15:00       229             1 Hour          1A(1)       
    <FREE TIME>             15:00 - 17:00       -               2 Hours         -           
    CSD Support (Optional)  17:00 - 18:00       Online          1 Hour          1A          
    """

    wednesday = """
    ===================================================================================
                                    WEDNESDAY Timetable
    ===================================================================================
    
    [MODULE]                [TIME]              [LOCATION]      [DURATION]      [GROUP]
         
    SDev                    09:00 - 10:00       Online          1 Hour          1A          
    BIS                     10:00 - 11:00       Online          1 Hour          1A       
    <FREE TIME>             11:00 - 12:00       -               1 Hour          -           
    Maths                   12:00 - 13:00       Online          1 Hour          1A          
    <FREE TIME>             13:00 - 14:00       -               1 Hour          -           
    VDUE                    14:00 - 15:00       Online          1 Hour          1A          
    CSD (Self Access)       15:00 - 16:00       Online          1 Hour          1A          
    BIS                     16:00 - 17:00       Online          1 Hour          1A + 1B
    BIS Support (Optional)  17:00 - 18:00       Online          1 Hour          1A          
    """

    thursday = """
    ===================================================================================
                                    THURSDAY Timetable
    ===================================================================================
    
    [MODULE]                [TIME]              [LOCATION]      [DURATION]      [GROUP]
         
    SDev                    10:00 - 11:00       025             1 Hour          1A(1)       
    VDUE Lab                11:00 - 13:00       150/152         2 Hours         1A(1)       
    <FREE TIME>             13:00 - 14:00       -               1 Hour          -           
    SDev Lab                14:00 - 16:00       150/152         2 Hours         1A(1)       
    Maths Support (Opt.)    16:00 - 17:00       023             1 Hour          1A          
    """

    friday = """
    ===================================================================================
                                    FRIDAY Timetable
    ===================================================================================
    
    [MODULE]                [TIME]              [LOCATION]      [DURATION]      [GROUP]
         
    SDev Lab                09:00 - 11:00       216             2 Hours         1A(1)       
    <FREE TIME>             11:00 - 14:00       -               3 Hours         -           
    Comp Arch Lab           14:00 - 15:00       Online          1 Hour          1A(1)       
    CSD (Self Access)       15:00 - 16:00       Online          1 Hour          1A(1)                        
    """

    weekend = """
    ===================================================================================
                                    WEEKEND Timetable
    ===================================================================================
    
    There are no classes scheduled on the weekend. Get a life!
    """

    print(guide)
    if datetime.now().strftime("%A") == "Monday":
        print(monday)
    elif datetime.now().strftime("%A") == "Tuesday":
        print(tuesday)
    elif datetime.now().strftime("%A") == "Wednesday":
        print(wednesday)
    elif datetime.now().strftime("%A") == "Thursday":
        print(thursday)
    elif datetime.now().strftime("%A") == "Friday":
        print(friday)
    else:
        print(weekend)

    selecting_schedule = True
    while selecting_schedule:
        print("\n    Input 'x' to close or select another timetable 'mon', 'tue', 'wed', 'thu' or 'fri'")
        schedule_input = input("    TODO: ")
        os.system("cls")

        print(guide)
        if schedule_input == "x":
            os.system("cls")
            selecting_schedule = False
        elif schedule_input == "mon":
            print(monday)
        elif schedule_input == "tue":
            print(tuesday)
        elif schedule_input == "wed":
            print(wednesday)
        elif schedule_input == "thu":
            print(thursday)
        elif schedule_input == "fri":
            print(friday)
        elif schedule_input == "sat" or schedule_input == "sun":
            print(weekend)
        else:
            print("    ERROR! Invalid user input.")
            continue

    print(border)
    print(f"{title}".upper())
    print(border)


def command():
    print("[Program Command List]\n".upper())
    print(f"{CMD_ADD}\t\t-\tAdd task")
    print(f"{CMD_DEL}\t\t-\tDelete task")
    print(f"{CMD_EXIT}\t\t-\tExit program")
    print(f"{CMD_SCHEDULE}\t\t-\tDisplay timetables")

    show_help = True
    while show_help:
        input("\nPress ENTER to continue")
        os.system("cls")
        show_help = False

        print(border)
        print(f"{title}".upper())
        print(border)


def main():
    """Program main function."""
    os.system("cls")
    create_file()
    print(border)
    print(f"{title}".upper())
    print(border)
    running_main = True
    while running_main:
        task_list(None)
        cmd_list = [CMD_ADD, CMD_DEL, CMD_SCHEDULE, CMD_EXIT, CMD_HELP]
        print(" | ".join(cmd_list))

        todo = input("TODO: ")
        if todo == CMD_ADD:
            os.system("cls")
            add_task()
        elif todo == CMD_DEL:
            os.system("cls")
            delete_task()
        elif todo == CMD_HELP:
            os.system("cls")
            command()
        elif todo == CMD_SCHEDULE:
            os.system("cls")
            schedule()
        elif todo == CMD_EXIT:
            sys.exit("\nTODO List program terminated.")
        else:
            os.system("cls")
            print(border)
            print(f"'{todo}' is not a recognised command.")
            print(border)
            continue


if __name__ == "__main__":
    main()
