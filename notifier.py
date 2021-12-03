# Program     : TODO List Notifier
# Language    : Python
# Version     : 3.9
# Author      : Ken
# Created     : 10/09/2020
# Modified    : 24/11/2021
#
# Enables Windows 10 dialog message box and toast
# notification for created tasks that are due in the main program.

import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
import todo
import os
from pathlib import Path

# _TODO database source
file = Path(r"Path\todo.txt")
# Windows powershell app AUMID
app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

# Notifier
notification_manager = notifications.ToastNotificationManager
notifier = notification_manager.create_toast_notifier(app)

# Setting up notification message
# https://docs.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/adaptive-interactive-toasts?
# tabs=builder-syntax
notification_message = """
  <toast scenario="reminder" launch="action=viewEvent&amp;eventId=1983">
    <visual>
      <binding template='ToastGeneric'>
        <text>Todo List</text>
        <text>There is a task due TODAY!</text>
        <text placement="attribution">Technological University Dublin - Tallaght</text>
      </binding>
    </visual>
    
    <actions>    
        <input id="snoozeTime" type="selection" defaultInput="15">
            <selection id="1" content="1 minute"/>
            <selection id="15" content="15 minutes"/>
            <selection id="60" content="1 hour"/>
            <selection id="240" content="4 hours"/>
        </input>
        
        <action activationType="system" arguments="snooze" hint-inputId="snoozeTime" content="" />
        <action content="Dismiss" arguments="action=dismiss"/>
    </actions>        
  </toast>
"""

# Convert notification message to XML Document
xml_doc = dom.XmlDocument()
xml_doc.load_xml(notification_message)

# Setting up notification condition/trigger
if os.path.exists(file):
    todo.task_list(None)
    with open(file) as todo:
        timedelta = list()
        lines = todo.readlines()

        for num, line in enumerate(lines):
            if num == 0:
                continue

            line_split = line.split("\t")

            if line_split[2].isalpha():
                pass
            else:
                timedelta.append(int(line_split[2]))

        if 0 in timedelta:
            notifier.show(notifications.ToastNotification(xml_doc))
