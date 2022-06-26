import tkinter as tk
import time
import sqlite3 as sql
from tkinter import messagebox, Toplevel, END
import tkinter as tk
import time
import sqlite3 as sql
from tkinter import messagebox, Toplevel, END

connection=sql.connect('database1.db')  # open connection to database
c=connection.cursor()

def timestamp():
    t=time.localtime()
    return time.strftime('%H:%M:%S', t)  # returns current time

with open("config.txt", 'r') as file:
    data=file.readlines()
data[1]='8\n'
with open("config.txt", 'w') as file:  # always makes sure the game starts with a maze size of 8
    file.writelines(data)

root=tk.Tk()  # setting up main tkinter window
root.title("Maze Game Launcher")
root.configure(bg="black")
root.minsize(500,400)
title=tk.PhotoImage(file="title.gif")
root.attributes("-fullscreen", False)
t1=tk.Label(root, image=title, borderwidth=0, highlightthickness=0)
t1.place(relx=0.5, rely=0.2, anchor="center")
print("- User started program... | "+timestamp())
loggedIn=False

def forget(widgets):  # disables all widgets passed through in a list
    for item in widgets:
        item.place_forget()

def leveller():  # replaced mazeSize line in config file with the next size up
    with open("config.txt", 'r') as file:
        list_of_lines=file.readlines()

    new=8
    if int(list_of_lines[1]) == 8:
        new = 10
    if int(list_of_lines[1]) == 10:
        new = 15
    if int(list_of_lines[1]) == 15:
        new = 20
    if int(list_of_lines[1]) == 20:
        new = 25
    if int(list_of_lines[1]) == 25:
        new = 35
    if int(list_of_lines[1]) == 35:
        new = 8

    with open("config.txt", 'w') as file:
        list_of_lines[1] = str(new) + "\n"
        file.writelines(list_of_lines)

def quit():
    root.quit()
    print("- User quit the game... | "+timestamp())

def start():
    widgets = [b1, b2, b10, b9]
    forget(widgets)

    b4.place(relx=0.5, rely=0.5, anchor="center")  # username, password and quit
    b5.place(relx=0.5, rely=0.55, anchor="center")
    b11.place(relx=0.5, rely=0.6, anchor="center")

def speedBump():  # a place to bring all functions to before the game starts
    widgets = [l1, l2, l3, e1, e2, e3, b6, l6, l7, l8, o1, b12, b11, b5, b14, l9, b4]
    forget(widgets)

    b8.place(relx=0.5, rely=0.5, anchor="center")
    b3.place(relx=0.5, rely=0.9, anchor="center")
    b15.place(relx=0.5, rely=0.6, anchor="center")

def speedBump2():
    widgets = [b4, b5, b11, b14, l1, l2, l3, e1, e2, e3, b6, o1, l8, b13, b3]
    forget(widgets)
    l9.place(relx=0.5, rely=0.5, anchor="center")
    b4.place(relx=0.5, rely=0.6, anchor="center")

def create_confirm():
    one=False
    two=False

    c.execute("SELECT username FROM Credentials")
    results = c.fetchall()
    for r in range(0, len(results)):
        if results[r][0]==e1.get():  # if username already exists in database
            one=True
            break
    if e2.get()==e3.get():  # if both passwords match
        two=True
    else:
        print("Passwords do not match...")
        b13.config(fg="red")  # highlights 'criteria' widget

    if one==False and two==True:  # if criteria is met
        print("- Valid... ")
        colour_choice=variable.get()

        with open("config.txt", 'r') as file:
            list_of_lines = file.readlines()
            list_of_lines[0] = colour_choice + "\n"  # replaces config file line 0 with choice of colour

        with open("config.txt", 'w') as file:
            file.writelines(list_of_lines)

        c.execute("""
                        INSERT INTO Credentials(username, password, colour)
                        VALUES (?,?,?)
                        """, (e1.get(), e2.get(), variable.get()))

        c.execute("""
                                INSERT INTO Leaderboard(username, score)
                                VALUES (?,?)
                                """, (e1.get(), 10000))

        print("- Account Created! ")
        connection.commit()
        l10 = tk.Label(root, text="LOGGED IN AS:    " + e1.get().upper(), bg="black", borderwidth=0, fg="grey")
        l10.place(relx=0.5, rely=0.8, anchor="center")  # reminder that the user is now logged in
        speedBump2()
    else:
        print("- Account already exists with that username... ")


def logged_in():
    global loggedIn
    loggedIn=True
    print("- User successfully logged in... | "+timestamp())
    widgets = [l1, l2, e4, e5, b7, b13, l9, b4]
    forget(widgets)

    l6.place(relx=0.5, rely=0.5, anchor="center")
    b12.place(relx=0.5, rely=0.6, anchor="center")
    l10 = tk.Label(root, text="LOGGED IN AS:    "+e4.get().upper(), bg="black", borderwidth=0, fg="grey")
    l10.place(relx=0.5, rely=0.8, anchor="center")

def level2():  # these functions progress to the next level and import the next script to launch it
    leveller()
    import second.Level2 as two
    two.run()
    level2button.place_forget()
    level3button.place(relx=0.5, rely=0.5, anchor="center")

def level3():
    leveller()
    import third.Level3 as three
    three.run()
    level3button.place_forget()
    level4button.place(relx=0.5, rely=0.5, anchor="center")

def level4():
    leveller()
    import fourth.Level4 as four
    four.run()
    level4button.place_forget()
    level5button.place(relx=0.5, rely=0.5, anchor="center")

def level5():
    leveller()
    import fifth.Level5 as five
    five.run()
    level5button.place_forget()
    level6button.place(relx=0.5, rely=0.5, anchor="center")

def level6():
    global loggedIn
    leveller()
    import sixth.Level6 as six
    six.run()
    widgets = [level6button, b1, b8]
    forget(widgets)
    endButton.place(relx=0.5, rely=0.5, anchor="center")

def endScreen():
    endButton.place_forget()
    b15.place_forget()

    with open("score.txt", 'r') as file:
        lines=file.readlines()
        entries=[]
        for x in range(0, len(lines)):
            entries.append(lines[x].strip())

    final_score = 0
    for x in range(0, len(entries)):
        final_score += float(entries[x][3:])  # gathers final score from text file

    print("Your final score is: "+str(final_score))

    c.execute("SELECT * FROM Leaderboard")
    results=c.fetchall()
    found=False

    for x in range(0, len(results)):
        if results[x][0]==str(e4.get()):  # if username already in database
            found=True
            index=x

    if loggedIn == True:
        if final_score < results[index][1]:  # if new score is lower than old score  # and if user is logged in
            c.execute("DELETE FROM Leaderboard WHERE username=?", (e4.get(),))  # delete old record
            c.execute("""
                                                INSERT INTO Leaderboard(username, score)
                                                VALUES (?,?)
                                                """, (e4.get(), final_score))  # write new record

            connection.commit()
    else:
        pass

def startGame():
    widgets = [b4, b5, b11]
    forget(widgets)

    import first.Level1 as one
    one.run()
    level2button.place(relx=0.5, rely=0.5, anchor="center")

def login_confirm():
    c.execute("SELECT * FROM Credentials WHERE username=?", (e4.get(),))  # checks if username exists
    exist = c.fetchone()
    if exist is None:
        print("- User entered username that doesn't exist (or used incorrect syntax)... | "+timestamp())
        b13.config(fg="red")

    elif len(e4.get())<=2:  # makes sure username is at least three characters long
        print("- User entered username with 3 or less characters")
        b13.config(fg="red")
    else:
        if exist[1]==str(e5.get()):  # checks if password matches database
            colour_choice = exist[2]
            colour_choice=colour_choice.lower()

            with open("config.txt", 'r') as file:
                list_of_lines=file.readlines()
                list_of_lines[0]=colour_choice+"\n"

            with open("config.txt", 'w') as file:
                file.writelines(list_of_lines)

            logged_in()
        else:
            print("- User entered incorrect password for a valid account... | "+timestamp())
            b13.config(fg="red")
    loggedIn=True

    return loggedIn

def viewCriteria():
    messagebox.showinfo("Credential Criteria", "Username must be at least 3 characters long, unique and passwords "
                                               "must match")

def viewCriteria2():
    messagebox.showinfo("Colour selection", "Multiple colour choices for your sprite are offered to avoid any "
                                            "confusion for people who suffer with colourblindness. "
                                            "                                                                 "
                                            "                                                                 "
                                            "Note: Your sprite"
                                            " will be against a black and white surface.")

def viewCriteria3():
    messagebox.showinfo("How to play", "The goal is to reach the red square in the lower right corner"
                                       " in the quickest amount of time possible."
                                       "                                                                     "
                                       "                                                                "
                                       "      You can control your sprite by using WASD or the arrow keys.")

def createAccount():
    print("- User started the account creation process... | "+timestamp())

    widgets = [b4, b5, b11, b3]
    forget(widgets)

    b14.place(relx=0.6, rely=0.8, anchor="center")
    l1.place(relx=0.5, rely=0.4, anchor="center")
    l2.place(relx=0.5, rely=0.5, anchor="center")
    l3.place(relx=0.5, rely=0.6, anchor="center")
    e1.place(relx=0.5, rely=0.45, anchor="center")
    e2.place(relx=0.5, rely=0.55, anchor="center")
    e3.place(relx=0.5, rely=0.65, anchor="center")
    b6.place(relx=0.5, rely=0.9, anchor="center")
    o1.place(relx=0.5, rely=0.8, anchor="center")
    l8.place(relx=0.5, rely=0.7, anchor="center")
    b13.place(relx=0.7, rely=0.9, anchor="center")
    b3.place(relx=0.3, rely=0.9, anchor="center")

def login():
    print("- User started the login process... | "+timestamp())

    widgets=[b4,b5,b11,b14, l1, l2, l3, e1, e2, e3, b6, o1, l8, b13, b3, l9]

    forget(widgets)

    l1.place(relx=0.5, rely=0.5, anchor="center")
    l2.place(relx=0.5, rely=0.6, anchor="center")
    e4.place(relx=0.5, rely=0.55, anchor="center")
    e5.place(relx=0.5, rely=0.65, anchor="center")
    b7.place(relx=0.5, rely=0.7, anchor="center")
    b13.place(relx=0.7, rely=0.7, anchor="center")

def leaderboard():  # launches mini leaderboard window to show current scores
    leaderboardWindow=Toplevel()
    leaderboardWindow.title("Leaderboard")
    leaderboardWindow.geometry("400x400")
    leaderboardWindow.config(bg="grey7")
    close=tk.Button(leaderboardWindow, text="CLOSE", bg="grey7", borderwidth=1, fg="white", command=leaderboardWindow.destroy)
    close.place(relx=0.5, rely=0.9, anchor="center")

    c.execute("SELECT * FROM Leaderboard")
    exist = c.fetchall()

    scores={}
    for x in range(0, len(exist)):
        scores.update({exist[x][0]: exist[x][1]})  # adds scores to dictionary

    for_display=[]
    for key, value in scores.items():  # adds keys and their respective values to list
        if value < 10000:
            for_display.append([key, value])


    for x in range(0, len(for_display)):
        for y in range(0, len(for_display[x])):
            w=tk.Text(leaderboardWindow, width=10, height=1, bg="grey7", fg="white", borderwidth=0)
            w.grid(row=x, column=y)
            w.insert(END, for_display[x][y])

def fullscreenOn():
    root.attributes("-fullscreen", True)

def fullscreenOff():
    root.attributes("-fullscreen", False)

b1=tk.Button(root, text="START", bg="black", borderwidth=0, fg="white", command=start)
b2=tk.Button(root, text="LEADERBOARD", bg="black", borderwidth=0, fg="white", command=leaderboard)
b3=tk.Button(root, text="QUIT", bg="black", borderwidth=0, fg="white", command=quit)
b4=tk.Button(root, text="LOGIN", bg="black", borderwidth=0, fg="white", command=login)
b5=tk.Button(root, text="CREATE ACCOUNT", bg="black", borderwidth=0, fg="white", command=createAccount)
b6=tk.Button(root, text="CONFIRM", bg="black", borderwidth=0, fg="white", command=create_confirm)
b7=tk.Button(root, text="CONFIRM", bg="black", borderwidth=0, fg="white", command=login_confirm)
b8=tk.Button(root, text="START GAME", bg="black", borderwidth=0, fg="white", command=startGame)
b9=tk.Button(root, text="FULLSCREEN ON", bg="black", borderwidth=0, fg="white", command=fullscreenOn)
b10=tk.Button(root, text="FULLSCREEN OFF", bg="black", borderwidth=0, fg="white", command=fullscreenOff)
b11=tk.Button(root, text="CONTINUE AS GUEST", bg="black", borderwidth=0, fg="white", command=speedBump)
b12=tk.Button(root, text="OK", bg="black", borderwidth=0, fg="white", command=speedBump)
b13=tk.Button(root, text="VIEW CRITERIA", bg="black", borderwidth=0, fg="white", command=viewCriteria)
b14=tk.Button(root, text="?", bg="black", borderwidth=1, fg="white", command=viewCriteria2)
b15=tk.Button(root, text="HOW TO PLAY", bg="black", borderwidth=0, fg="white", command=viewCriteria3)
level2button=tk.Button(root, text="CLICK TO ADVANCE TO LEVEL 2/6", bg="black", borderwidth=0, fg="white", command=level2)
level3button=tk.Button(root, text="CLICK TO ADVANCE TO LEVEL 3/6", bg="black", borderwidth=0, fg="white", command=level3)
level4button=tk.Button(root, text="CLICK TO ADVANCE TO LEVEL 4/6", bg="black", borderwidth=0, fg="white", command=level4)
level5button=tk.Button(root, text="CLICK TO ADVANCE TO LEVEL 5/6", bg="black", borderwidth=0, fg="white", command=level5)
level6button=tk.Button(root, text="CLICK TO ADVANCE TO LEVEL 6/6", bg="black", borderwidth=0, fg="white", command=level6)
endButton=tk.Button(root, text="FINISH", bg="black", borderwidth=0, fg="white", command=endScreen)
l1=tk.Label(root, text="USERNAME:", bg="black", borderwidth=0, fg="white")
l2=tk.Label(root, text="PASSWORD:", bg="black", borderwidth=0, fg="white")
l3=tk.Label(root, text="CONFIRM PASSWORD:", bg="black", borderwidth=0, fg="white")
l4=tk.Label(root, text="USERNAME TAKEN", bg="black", borderwidth=0, fg="red")
l5=tk.Label(root, text="USERNAME IS VALID", bg="black", borderwidth=0, fg="green")
l6=tk.Label(root, text="SUCCESSFULLY LOGGED IN", bg="black", borderwidth=0, fg="white")
l7=tk.Label(root, text="LOGGED IN", bg="black", borderwidth=0, fg="grey")
l8=tk.Label(root, text="SELECT SPRITE COLOUR", bg="black", borderwidth=0, fg="white")
l9=tk.Label(root, text="ACCOUNT CREATED", bg="black", borderwidth=0, fg="white")
e1=tk.Entry(root)  # username (create account)
e2=tk.Entry(root, show="*")  # password
e3=tk.Entry(root, show="*")  # confirm password
e4=tk.Entry(root)  # username (login)
e5=tk.Entry(root, show="*")  # password
variable = tk.StringVar()
choices = ['green','blue','purple','yellow','orange']
variable.set(choices[0]) # default value
o1=tk.OptionMenu(root, variable, *choices)  # colour choice

#############starting menu##############
b1.place(relx=0.5, rely=0.5, anchor="center")  # makes widgets stay in center
b2.place(relx=0.5, rely=0.55, anchor="center")
b3.place(relx=0.5, rely=0.9, anchor="center")
b9.place(relx=0.5, rely=0.65, anchor="center")
b10.place(relx=0.5, rely=0.7, anchor="center")
#########################################

root.mainloop()
connection.close()