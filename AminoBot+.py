#Discord Bot by robytoby154 using discord.py

#Uses a .txt file for database
#Change the database class however you'd like to
#(i.e. if you want to rewrite it to use sqlite3 or mangodb e.t.c.)
#The calls are the only unchangeable part of the database class

#IMPORTS

import discord
from tkinter import *
from tkinter import font
import os
import threading
import time
try:
    import urllib.request
except:
    None

#VARIABLES

bottoggle = False

VERSION = "0.0.0.6"

#SHUTDOWN PROGRAM FUNCTION

def shutdown_program():
    try:
        mainwindow.destroy()
    except:
        None
    exit()

#Ending loop

def ending_loop():
    try:
        while True:
            mainwindow.update()
            time.sleep(0.25)
            continue
    except:
        shutdown_program()

#Direct path for compiled executable directory FUNCTION

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Config Reader CLASS

class configfile():
    def __init__(self, configfile, configtemplate):
        #Config Content: [CMD] [TOKEN, PREFIX] [NONE]
        self.configcontent = [[],[],[]]
        self.tempstr = ""
        self.configfile = configfile
        try:
            with open(configfile, "r") as config:
                filelines = config.readlines()
                for x in range(len(filelines)):
                    try:
                        self.tempstr = filelines[x][filelines[x].find("'") + 1:]
                        if self.tempstr[:self.tempstr.find("'")] == "CMD":
                            self.configcontent[0].append(self.tempstr[self.tempstr.find("'")+1:])
                        elif self.tempstr[:self.tempstr.find("'")] == "TOKEN" or self.tempstr[:self.tempstr.find("'")] == "PREFIX":
                            self.configcontent[1].append(filelines[x])
                        elif self.tempstr[:self.tempstr.find("'")] == "NONE":
                            self.configcontent[2].append(self.tempstr[self.tempstr.find("'")+1:])
                    except:
                        None
        except:
            open(configfile, "a").close()
            open(configfile, "w").close()
            with open(configfile, "w") as cfile:
                with open(resource_path(configtemplate), "r") as configtempfile:
                    cfile.write(configtempfile.read())
            self.__init__(configfile, configtemplate)

    def get_commands(self): #Returns a list of custom commands
        raw_cmds = self.configcontent[0]
        temptriglist = []
        tempstr = ""
        self.yoffset = 0
        self.cmdlist = []
        for x in range(len(raw_cmds)):
            temptriglist.append([])
            aposcount = raw_cmds[x].count("'")
            if aposcount % 2 == 0:
                separloc = raw_cmds[x].find("'/'")
                tempstr = raw_cmds[x][:separloc + 1]
                for z in range(int(aposcount / 2)):
                    temptriglist[x].append(tempstr[tempstr.find("'")+1:tempstr[tempstr.find("'")+1:].find("'") + tempstr.find("'")+1])
                    tempstr = tempstr[tempstr.find("'")+1:]
                    tempstr = tempstr[tempstr.find("'")+1:]
                for y in range(len(temptriglist[x])):
                    if temptriglist[x][y-self.yoffset] == "":
                        temptriglist[x].pop(y-self.yoffset)
                        self.yoffset += 1
                tempstr = raw_cmds[x][separloc+1:]
                tempstr = tempstr[tempstr.find("'")+1:]
                tempstr = tempstr[:tempstr.find("'")]
                temptriglist[x].append(tempstr)
        self.cmdlist = temptriglist
        return self.cmdlist

    def get_middle(self): #Gets token and prefix
        raws = self.configcontent[1]
        self.prefixtemp = []
        self.tokentemp = []
        self.tokprelist = []
        tempstr = ""
        for x in range(len(raws)): #Iterates through possible tokens and prefixes
            if "'PREFIX'" in raws[x]:
                self.prefixtemp.append(raws[x])
            elif "'TOKEN'" in raws[x]:
                self.tokentemp.append(raws[x])
        if len(self.prefixtemp) == 1 and len(self.tokentemp) == 1:
            self.tokprelist.append(self.tokentemp[0])
            self.tokprelist.append(self.prefixtemp[0])
        else:
            return False
        #If only 1 token and 1 prefix is detected --
        for x in range(2): #Get token and prefix
            self.tokprelist[x]
            tempstr = self.tokprelist[x][self.tokprelist[x].find("'") + 1:]
            tempstr = tempstr[tempstr.find("'")+1:][tempstr[tempstr.find("'")+1:].find("'")+1:]
            tempstr = tempstr[:tempstr.find("'")]
            self.tokprelist[x] = tempstr
        return self.tokprelist
        
    def get_none(self):
        return self.configcontent[2]

    def fixfile(self):
        self.tempstr = ""
        with open(self.configfile, "r") as cfile:
            filelines = cfile.readlines()
            self.tk = 0
            self.pr = 0
            self.tempflag = False
            for x in range(len(filelines)):
                try:
                    self.tempstr = filelines[x][filelines[x].find("'") + 1:]
                    if self.tempstr[:self.tempstr.find("'")] == "TOKEN":
                        self.tk += 1
                        if self.tk > 1:
                            self.tempflag = True #If more than 1 token line exists
                    elif self.tempstr[:self.tempstr.find("'")] == "PREFIX":
                        self.pr += 1
                        if self.pr > 1:
                            self.tempflag = True #If more than 1 prefix line exists
                except:
                    None
        return self.tempflag

    def write(self, datafield, to_write):
        if datafield == "token":
            self.entry = "token"
        elif datafield == "prefix":
            self.entry = "prefix"
        else:
            return False
        self.fixfile()
        linenum = -1
        tempstr = ""
        with open(self.configfile, "r") as cfile:
            filelines = cfile.readlines()
        for x in range(len(filelines)):
            num1 = filelines[x].find("'")
            num2 = num1 + len(self.entry) + 2
            if filelines[x][num1:num2].lower() == "'" + self.entry.lower() + "'":
                linenum = x
                num1 = filelines[x][num2:].find("'") + 1
                tempstr = filelines[x][filelines[x][num2 + num1:].find("'") + 1 + num1 + num2:]
        filelines[linenum] = "'" + self.entry.upper() + "':'" + to_write + "'" + tempstr
        if linenum != -1:
            open(self.configfile, "w").close()
            tempfile = open(self.configfile, "w")
            tempfile.write("".join(filelines))
            return True
        else:
            return False

    #Calls --

    def get_token(self): #To load token from config file
        tkpr = self.get_middle()
        if tkpr != False:
            return tkpr[0]
        else:
            return False

    def get_prefix(self): #To load prefix from config file
        tkpr = self.get_middle()
        if tkpr != False:
            return tkpr[1]
        else:
            return False

    def save_token(self, token): #To save token to config file
        return self.write("token", token)

    def save_prefix(self, prefix): #To save prefix to config file
        return self.write("prefix", prefix)

#Database CLASS

class DatabaseHandler:
    def __init__(self, databasefilename):
        if databasefilename[-4:] != ".txt":
            self.databasefile = databasefilename + ".txt"
        else:
            self.databasefile = databasefilename
        try:
            open(self.databasefile, "r").close()
        except:
            open(self.databasefile, "a").close()
            newdbwrite = open(self.databasefile, "w")
            newdbwrite.write("UserID,Money,Rank\n")
            newdbwrite.close()

    def changedb(self, newdbcontent):
        content = str(newdbcontent)
        open(self.databasefile, "w").close()
        dbfile = open(self.databasefile, "w")
        dbfile.write(content)
        dbfile.close()

    def datagrab(self, Key):
        self.updaterows()
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            dblines = dbfile.readlines()[1:]
            for x in range(len(dblines)):
                dbline = dblines[x].replace("\n", "")
                linedata = dbline.split(",")
                if linedata[0] == key:
                    return [linedata, x]
        return None

    def valueget(self, valueID, Key):
        valID = str(valueID)
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            valueids = dbfile.readlines()[0].replace("\n", "")
            valueids = valueids.split(",")
            for x in range(len(valueids)):
                if valueids[x] == valID:
                    return [self.datagrab(key)[0][x], x]
        print("No value id : " + valID)

    def valueupdate(self, valueID, Key, newvalue):
        valID = str(valueID)
        key = str(Key)
        update = str(newvalue)
        self.updaterows()
        try:
            with open(self.databasefile, "r") as dbfile:
                dblines = dbfile.readlines()
            data = self.datagrab(key)
            data[0][self.valueget(valID, key)[1]] = update
            dblines[data[1]+1] = ",".join(data[0]) + "\n"
            self.changedb("".join(dblines))
        except:
            print("Could not update " + valID + " for " + key + " to new value " + update)

    def first_line(self):
        with open(self.databasefile, "r") as dbfile:
            firstline = dbfile.readlines()[0].replace("\n", "")
            firstline = firstline.split(",")
        return firstline

    def get_lines(self):
        with open(self.databasefile, "r") as dbfile:
            lines = dbfile.readlines()
        for x in range(len(lines)):
            lines[x] = lines[x].replace("\n", "")
        return lines

    def newkey(self, newkey):
        nkey = str(newkey)
        tempflag = False
        if self.datagrab(nkey) == None:
            with open(self.databasefile, "r") as dbfile:
                try:
                    dbcoms = dbfile.readlines()[0].count(",")
                except:
                    tempflag = True
            if tempflag == True:
                newdb = open(self.databasefile, "w")
                newdb.write("UserID,Money,Rank\n")
                newdb.close()
                dbcoms = dbfile.readlines()[0].count(",")
            for x in range(dbcoms):
                nkey += ",0"
            with open(self.databasefile, "r") as dbfile:
                dbcontent = dbfile.read() + nkey + "\n"
            self.changedb(dbcontent)
            nkey = str(newkey)
            #New user defaults:

            #self.valueupdate("Money", nkey, 25)
            #self.valueupdate("Commands_Used", nkey, 0)
            
            return True
        else:
            return False

    def delcol(self, valueID):
        valID = str(valueID)
        self.z = 0
        self.tempstr = ""
        self.templine = []
        self.reflag = False
        with open(self.databasefile, "r") as dbfile:
            dbline = str(dbfile.readlines()[0].replace("\n", "")).split(",")
            for x in range(len(dbline)):
                if dbline[x] == valID:
                    self.z = x
                    self.reflag = True
        if self.reflag == True:
            with open(self.databasefile, "r") as dbfile:
                dblines = dbfile.readlines()
            for x in range(len(dblines)):
                self.templine = (dblines[x].replace("\n", "")).split(",")
                self.templine.pop(self.z)
                self.tempstr += ",".join(self.templine) + "\n"
            self.changedb(self.tempstr)
        else:
            return False

    def updaterows(self):
        self.tempstr = ""
        with open(self.databasefile, "r") as dbfile:
            filelines = dbfile.readlines()
            comcount = filelines[0].count(",")
            filelines[0] = filelines[0].replace("\n", "")
        with open(self.databasefile, "r") as dbfile:
            readfile = dbfile.read()
        for x in range(len(filelines)-1):
            filelines[x+1] = filelines[x+1].replace("\n", "")
            if filelines[x+1] != "":
                linecom = filelines[x+1].count(",")
                while linecom < comcount:
                    filelines[x+1] += ",0"
                    linecom = filelines[x+1].count(",")
        newfile = "\n".join(filelines) + "\n"
        self.changedb(newfile)

    def addvalueid(self, ValueID):
        valID = str(ValueID)
        fields = self.get_fields()
        tempflag = False
        for x in range(len(fields)):
            if fields[x] == valID:
                tempflag = True
        if tempflag == True:
            return False
        lines = self.get_alldata()
        lines[0] = lines[0] + "," + valID
        self.changedb("\n".join(lines))
        self.updaterows()

    #Calls--

    #Used to interact with database in a user-friendly method

    def get(self, DataField, Key): #Get a cell value
        return self.valueget(DataField, Key)[0]
    def update(self, DataField, Key, NewValue): #Update a cell value
        self.valueupdate(DataField, Key, NewValue)
    def delid(self, DataField): #Delete a data id column
        self.delcol(DataField)
    def addkey(self, Key): #Creates a new row with given key
        return self.newkey(Key)
    def get_fields(self): #Gets fields
        return self.first_line()
    def get_alldata(self): #Gets all lines from database file
        return self.get_lines()
    def addfield(self, DataField): #Adds new data field
        self.addvalueid(DataField)

#List Box CLASS

class listbox:
    def __init__(self, parent, hi = 13, wi = 32):
        self.parent = parent
        frame = Frame(self.parent, width=250, height=30, bd=1)
        self.frame = frame
        self.frame.pack()
        self.listbx = Listbox(frame, height=hi, width = wi)
        self.listbx.pack(side=LEFT,fill=Y)
        self.scrollbr = Scrollbar(frame)
        self.scrollbr.pack(side=RIGHT, fill=Y)
        self.listbx.config(yscrollcommand = self.scrollbr.set)
        self.scrollbr.config(command = self.listbx.yview)
        self.frame.update()
        self.hi = hi
        self.wi = wi
        
    def AddNew(self, text):
        self.listbx.insert(END, text)
        self.listbx.select_set(END)
        self.listbx.yview(END)
        self.listbx.update()
        
    def selfreset(self):
        self.frame.destroy()
        frame = Frame(self.parent, width=250, height=30, bd=1)
        self.frame = frame
        self.frame.pack()
        self.listbx = Listbox(frame, height=self.hi, width = self.wi)
        self.listbx.pack(side=LEFT,fill=Y)
        self.scrollbr = Scrollbar(frame) 
        self.scrollbr.pack(side=RIGHT, fill=Y)
        self.listbx.config(yscrollcommand = self.scrollbr.set)
        self.scrollbr.config(command = self.listbx.yview)
        self.frame.update()

#Refresh Userdata Boxes FUNCTION

def refresh_boxes():
    global userdatabox, fieldsbox
    userdatabox.selfreset()
    fieldsbox.selfreset()
    thelines = (DatabaseHandler("Userdata.txt").get_lines())
    for x in range(len(thelines)):
        userdatabox.AddNew(thelines[x].replace(",", " / "))

    thefields = DatabaseHandler("Userdata.txt").get_fields()
    for x in range(len(thefields)):
        fieldsbox.AddNew(thefields[x])

#Addfield FUNCTION

def addfield():
    global fieldnameent
    fieldn = fieldnameent.get()
    inst1 = DatabaseHandler("Userdata.txt").first_line()
    DatabaseHandler("Userdata.txt").addfield(fieldn)
    inst2 = DatabaseHandler("Userdata.txt").first_line()
    if inst1 != inst2:
        fieldnameent.delete(0, END)
        fieldnameent.insert(0, "Added " + fieldn)
    else:
        fieldnameent.delete(0, END)
        fieldnameent.insert(0, "Couldn't add " + fieldn)
    fieldnameent.update()
    time.sleep(0.3)
    fieldnameent.delete(0, END)
    refresh_boxes()

#Delfield FUNCTION

def delfield():
    global fieldnameent
    fieldn = fieldnameent.get()
    inst1 = DatabaseHandler("Userdata.txt").first_line()
    DatabaseHandler("Userdata.txt").delid(fieldn)
    inst2 = DatabaseHandler("Userdata.txt").first_line()
    if inst1 != inst2:
        fieldnameent.delete(0, END)
        fieldnameent.insert(0, "Deleted " + fieldn)
    else:
        fieldnameent.delete(0, END)
        fieldnameent.insert(0, "Couldn't delete " + fieldn)
    fieldnameent.update()
    time.sleep(0.3)
    fieldnameent.delete(0, END)
    refresh_boxes()

#Toggle Userdata GUI FUNCTION

def toggle_userdataGUI():
    global userdatabox, fieldsbox, userdatawindow, USERDATAIMG, userdatacanvas, userdataphoto, fieldnameent
    try:
        userdatawindow.title("Userdata")
        userdatawindow.destroy()
        return
    except:
        None
    userdatawindow = Toplevel()
    userdatawindow.iconbitmap(WINDOWICONICO)
    
    userdatawindow.title("Userdata")
    userdatawindow.geometry("500x250")
    userdatawindow.resizable(height = False, width = False)
    
    userdataphoto = PhotoImage(file = USERDATAIMG)
    
    userdatacanvas = Canvas(userdatawindow)
    userdatacanvas.pack(fill = "both", expand = True)
    userdatacanvas.config(bg = "yellow")
    userdatacanvas.create_image(0, 0, image=userdataphoto, anchor="nw")
    
    userdataboxcnv = Canvas(userdatawindow, height = 235, width = 200)
    userdataboxcnv.place(x = 5, y = 30)
    userdatabox = listbox(parent = userdataboxcnv)

    userdatalbl = Label(userdatawindow, text = "Userdata:", bg = "#20AA49")
    userdatalbl.place(x = 84, y = 8)

    fieldscnv = Canvas(userdatawindow, height = 5, width = 5)
    fieldscnv.place(x = 243, y = 30)
    fieldsbox = listbox(parent = fieldscnv, hi = 13, wi = 13)

    fieldslbl = Label(userdatawindow, text = "Fields:", bg = "#20AA49")
    fieldslbl.place(x = 273, y = 8)

    thelines = (DatabaseHandler("Userdata.txt").get_lines())
    
    for x in range(len(thelines)):
        userdatabox.AddNew(thelines[x].replace(",", " / "))
        
    thefields = DatabaseHandler("Userdata.txt").get_fields()
    for x in range(len(thefields)):
        fieldsbox.AddNew(thefields[x])
        
    fieldnamelbl = Label(userdatawindow, text = "Field Name:", bg = "#20AA49")
    fieldnamelbl.place(x = 393, y = 61)
    fieldnameent = Entry(userdatawindow, width = 20)
    fieldnameent.place(x = 365, y = 115)
    delfieldbtn = Button(userdatawindow, text = "Delete Field", bg = "#880015", activebackground = "#880015", bd = 0, command = delfield)
    delfieldbtn.place(x = 391, y = 209)
    addfieldbtn = Button(userdatawindow, text = "Add Field", bg = "#20AA49", activebackground = "#20AA49", bd = 0, command = addfield)
    addfieldbtn.place(x = 398, y = 172)
    userdatawindow.mainloop()

#Commands CLASS

class commands():
    def __init__(self, userdatafile):
        self.userdata_attributes = []
        self.udfile = userdatafile

    def cmd(self, cmd, userid): #Process command
        cmdlist = configfile("CONFIG.txt", resource_path(DEFAULTCONFIGTEMPLATE)).get_commands()
        self.cmd = cmd
        self.prefix = configfile("CONFIG.txt", resource_path(DEFAULTCONFIGTEMPLATE)).get_prefix()
        self.slct = ""
        for x in range(len(cmdlist)):
            for y in range(len(cmdlist[x])-1):
                if self.prefix + cmdlist[x][y] == self.cmd[:len(self.prefix)+len(cmdlist[x][y])]:
                    if self.cmd[len(self.prefix)+len(cmdlist[x][y]):].find(" ") <= 0:
                        if self.cmd[len(self.prefix)+len(cmdlist[x][y]):].find(" ") == -1:
                            if len(self.cmd) == len(self.prefix) + len(cmdlist[x][y]):
                                self.slct = cmdlist[x][len(cmdlist[x])-1]
                        else:
                            self.slct = cmdlist[x][len(cmdlist[x])-1]
        if self.slct == "":
            return False
        self.db = DatabaseHandler(self.udfile)
        self.db.addkey(userid)
        uservars = self.load_variables(userid)
        num1 = 0
        num2 = 0
        usertemp = []
        usertempoffset = 0
        for x in range(self.slct.count("@")):
            num1 = self.slct.find("@") + 1
            if num1 != 0:
                num2 = self.slct[num1:].find("@") + num1
                if num1 -1 != num2:
                    try:
                        if self.slct[num1:num2] != "user":
                            self.slct = self.slct[:num1-1] + uservars[self.slct[num1:num2]] + self.slct[num2:]
                        else:
                            usertemp.append(self.slct.find("@"))
                            self.slct = self.slct[:num1-1] + self.slct[num1:num2-4] + self.slct[num2:]
                    except:
                        self.slct = self.slct[:num1-1] + self.slct[num1:num2] + self.slct[num2:]
                else:
                    self.slct = self.slct.replace("@", "")
        for x in range(len(usertemp)):
            self.slct = self.slct[:usertemp[x - usertempoffset]] + uservars["user"] + self.slct[usertemp[x - usertempoffset]:]
            usertemp.pop(x - usertempoffset)
            usertempoffset += 1
            for z in range(len(usertemp)):
                usertemp[z] += len(uservars["user"])
            
        return self.slct

    def load_variables(self, userid): #Load variables for commands
        self.userdict = {}
        with open(self.udfile, "r") as dbfile:
            firstline = (dbfile.readlines()[0].replace("\n", "")).split(",")
        varlist = firstline
        for x in range(len(varlist)):
            self.userdict["userdata_" + varlist[x]] = self.db.get(varlist[x], userid)
        self.userdict["user"] = "<@!" + str(userid) + ">"
        return self.userdict

#Bot CLASS

class DiscordBot(discord.Client):
    async def on_ready(self):
        versionlbl.config(text = "Bot Running...")
        mainwindow.update()
        #When bot is connected --

    async def on_message(self, message):
        if message.author == self.user:
            return
        cmds = commands("Userdata.txt")
        temp = cmds.cmd(message.content, message.author.id)
        if temp != False:
            await message.channel.send(temp)

#Toggle Bot FUNCTION--

def togglebot():
    global bottoggle, mainwindowbgimg, discbot, tobot
    #When bot is started
    if bottoggle == False:
        try:
            discbot = DiscordBot()
            tobot = threading.Thread(target = discbot.run, args = (tokenent.get(),), daemon = True)
            tobot.start()
            try:
                mainwindowbgimg = PhotoImage(file = BOTACTIVEIMG)
            except:
                None
            startbtn.config(text = "Stop Bot", bg = "#770000", activebackground = "#760000")
            bottoggle = True
        except:
            None

    #When bot is stopped
    else:
        try:
            try:
                mainwindowbgimg = PhotoImage(file = MAINPAGEIMG)
            except:
                None
            startbtn.config(text = "Start Bot", bg = "#005500", activebackground = "#005500")
            bottoggle = False
        except:
            None
    maincanvas.create_image(0, 0, image = mainwindowbgimg, anchor = "nw")
    mainwindow.update()

#Button Images --

MAINPAGEIMG = resource_path("background1canvas.png")
BOTACTIVEIMG = resource_path("background2canvas.png")
HELPBTNIMG = resource_path("helpbutton.png")
WINDOWICONICO = resource_path("discordbot.ico")
COMMANDSBTNIMG = resource_path("commandsbtn.png")
USERDATABTNIMG = resource_path("userdatabtn.png")
USERDATAIMG = resource_path("userdatabackgroundimg.png")
DEFAULTCONFIGTEMPLATE = "DEFAULTCONFIGTEMPLATE.txt"
HELPFILE = "HELPTEMPLATE.txt"

#Load/Save Token FUNCTION

def loadtoken():
    config = configfile("CONFIG.txt", DEFAULTCONFIGTEMPLATE)
    tokenent.delete(0, END)
    tokenent.insert(0,config.get_token())

def savetoken():
    config = configfile("CONFIG.txt", DEFAULTCONFIGTEMPLATE)
    if tokenent.get() != "" and tokenent.get() != "No Token Inserted":
        config.save_token(str(tokenent.get()))
    else:
        tokenent.delete(0, END)
        tokenent.insert(0,"No Token Inserted")

def load_custom_commands():
    cmds = configfile("CONFIG.txt", DEFAULTCONFIGTEMPLATE).get_commands()
    print(cmds)

#GUI Setup

mainwindow = Tk()
mainwindow.title("Amino Bot")
mainwindow.geometry("375x175")
mainwindow.resizable(height = False, width = False)
maincanvas = Canvas()
maincanvas.pack(fill = "both", expand = True)
startbtnfont = font.Font(family = "Comic Sans MS", size = 16)
loadsavebtnfont = font.Font(family = "Comic Sans MS", size = 10)
startbtn = Button(mainwindow, text = "Start Bot", bg = "#005500", bd = 0, font = startbtnfont, activebackground = "#005500", command = togglebot)
startbtn.place(x = 242, y = 115)
versionlbl = Label(mainwindow, text = "v" + VERSION, bg = "#626262")
versionlbl.place(x = 176, y = 75)
tokenent = Entry(mainwindow, width = 35)
tokenent.place(x = 5, y = 100)
tokenlbl = Label(mainwindow, text = "Enter token here:", bg = "#626262")
tokenlbl.place(x = 5, y = 75)

loadtokenbtn = Button(mainwindow, text = "Load Token", font = loadsavebtnfont, bg = "#969696", bd = 0, activebackground = "#969696", command = loadtoken)
savetokenbtn = Button(mainwindow, text = "Save Token", font = loadsavebtnfont, bg = "#177d36", bd = 0, activebackground = "#177d36", command = savetoken)
commandsbtn = Button(mainwindow, bd = 0, bg = "#626262", activebackground = "#626262")
userdatabtn = Button(mainwindow, bd = 0, bg = "#626262", activebackground = "#626262", command = toggle_userdataGUI)
helpbtn = Button(mainwindow, bd = 0, bg = "#626262", activebackground = "#626262", command = create_help_file)
helplbl = Label(mainwindow, bg = "#626262", text = "- Help")
helplbl.place(x = 45, y = 15)

loadtokenbtn.place(x = 5, y = 140)
savetokenbtn.place(x = 110, y = 140)
commandsbtn.place(x = 257, y = 32)
userdatabtn.place(x = 257, y = 68)
helpbtn.place(x = 5, y = 5)

#Aesthetics

try:
    #Main window
    mainwindow.iconbitmap(WINDOWICONICO)
    mainwindowbgimg = PhotoImage(file = MAINPAGEIMG)
    maincanvas.create_image(0, 0, image = mainwindowbgimg, anchor = "nw")

    #Commands Btn
    commandsphoto = PhotoImage(file = COMMANDSBTNIMG)
    commandsphoto = commandsphoto.subsample(8, 8)
    commandsbtn.config(image = commandsphoto)

    #Userdata Btn
    userdataphotoimg = PhotoImage(file = USERDATABTNIMG)
    userdataphotoimg = userdataphotoimg.subsample(8, 8)
    userdatabtn.config(image = userdataphotoimg)

    #Help Btn
    help_photo = PhotoImage(file = HELPBTNIMG)
    help_photo = help_photo.subsample(15, 15)
    helpbtn.config(image = help_photo)
except:
    None

mainwindow.mainloop()
