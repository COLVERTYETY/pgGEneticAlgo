import keyboard
import os

selected = 0
meanulist = []

def show_menu():
    global selected , meanulist
    print("\n" * 30)
    print("select a map:")
    for i in range(len(meanulist)):
        header = " "
        ender = " "
        if selected == i:
            header = ">"
            ender = "<"
        print(header + meanulist[i] +ender )

def up():
    global selected
    if selected == 0:
        return
    selected -= 1
    show_menu()

def down():
    global selected, meanulist
    if selected == (len(meanulist)-1):
        return
    selected += 1
    show_menu()

def getfile():
    global meanulist,selected
    meanulist = os.listdir('../maps')
    show_menu()
    keyboard.add_hotkey('up', up)
    keyboard.add_hotkey('down', down)
    keyboard.wait('enter')
    return "../maps/"+str(meanulist[selected])