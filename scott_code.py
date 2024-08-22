from datetime import date, datetime, timedelta
#import pandas as pd

# try:
#     passtrack_data = pd.read_excel("PassTrack Data.xlsx")
# except FileNotFoundError:
#     passtrack_data = pd.DataFrame(columns= "ID#", "First Name", "Last Name", "# of Pass", "# of Mins", "# of Over")

# TO DO:
# - make a check to see if someone is out already and report their name and expected return time.
# - figure out and write code to make barcode list from student ID (idToBarcodeConverter)
# - subtract time from total minutes out when they return early
# - add code to accept input from a barcode scanner
# - figure out how to save data to a spreadsheet
# - add code to send output to a printer

#Program Settings and variables
TEACHER = "Mr. Scoπ"
ROOMNUMBER = 219
PASSLENGTH = 10
HEADER = 30
passCount = 0

# Dictionary ID:[First Name, Last Name, total passes, total minutes out, overtime passes]
studentList = {
    100010:["Joe", "James", 10, 9, 10],
    100008:["Hankley", "Hef", 11, 11, 9],
    100001:["Andy", "Anderson", 12, 13, 8],
    100002:["Bob", "Bakersonman", 13, 15, 7],
    100003:["Carl", "Candylopolis", 14, 17, 6],
    100004:["Devin", "Dupointmanson", 15, 19, 5],
    100005:["Earl", "Edward-Eversilly", 16, 21, 4],
    100006:["Frank", "Fillagragoriuslys", 17, 23, 3],
    100007:["Gary", "Gregarious-Gaspotson", 18, 25, 2],
    100010:["jerry", "Jippopotomasmacksonly", 19, 27, 1],
    100011:["Kristinofsky", "Kappoperniaslims", 20, 29, 0],
    100012:["Longaferson", "Langley-Lopperfonso", 21, 31, 11],
    100009:["Indiana", "Ivandrophs-Ickersonmansly", 22, 33, 12],
    200546:["Serenity", "McCoy", 0, 789798, 0],
    200158:["Vu", "Phan", 0, 987, 0]}

#Finds text width for centering purposes
def textWidth(text, fontSize):
    canvas = document.createElement("canvas")
    ctx = canvas.getContext("2d")
    if fontSize == 10:
        ctx.font = "10pt Arial"
    if fontSize == 15:
        ctx.font = "15pt Arial"
    if fontSize == 20:
        ctx.font = "20pt Arial"
    if fontSize == 25:
        ctx.font = "25pt Arial"
    if fontSize == 30:
        ctx.font = "30pt Arial"
    textMetrics = ctx.measureText(text)
    textWidth = textMetrics.width
    return textWidth

def printBarCode(bcInt, y):
    bcStr = str(bcInt)
    for i in range(len(bcStr)):
        line = Line(105 + 2*i, y, 105 + 2*i, y + 60)
        if bcStr[i] == '1':
            add(line)

def idToBarcodeConverter(idNumber):
    #fix this to ACUTALLY convert idNumber into a list
    bC = 1001011011010101100101011010100110110101011001011010101001101011011010010101101010011011010100101101101
    return bC

#Prints separate lines of text
def LineOfText(text, position, fontSize, height):
    txt = Text(text)
    offset = textWidth(text, fontSize) / 2
    #Decides where to put text horizontally on receipt
    if position == "center":
        txt.set_position(200-offset, height)
    elif position == "left":
        txt.set_position(100-offset, height)
    elif position == "right":
        txt.set_position(300-offset, height)
    #Sets font size
    if fontSize == 5:
        txt.set_font("5pt Arial")
    elif fontSize == 10:
        txt.set_font("10pt Arial")
    elif fontSize == 15:
        txt.set_font("15pt Arial")
    elif fontSize == 20:
        txt.set_font("20pt Arial")
    elif fontSize == 25:
        txt.set_font("25pt Arial")
    elif fontSize == 30:
        txt.set_font("30pt Arial")
    add(txt)

#PRINTS RECEIPT
def printReceipt(pc):
    spacing = HEADER

    #1) Pass Title
    LineOfText("PassTrack", "center", 10, spacing)
    spacing = spacing + 30 + 10
    
    #2) Teacher name
    LineOfText(TEACHER, "center", 30, spacing)
    spacing = spacing + 10 + 10
    
    #3) Room number
    room = "Room #" + str(ROOMNUMBER)
    LineOfText(room, "center", 10, spacing)
    spacing = spacing + 10 + 10
    
    # Line
    line = Line(20, spacing, 380, spacing)
    add(line)
    spacing = spacing + 30 + 10
    
    #4) Student name. (Changes font height for long names)
    if textWidth(student, 30) < 380:
        LineOfText(student, "center", 30, spacing)
    elif textWidth(student, 25) < 380:
        LineOfText(student, "center", 25, spacing)
    elif textWidth(student, 20) < 380:
        LineOfText(student, "center", 20, spacing)
    elif textWidth(student, 15) < 380:
        LineOfText(student, "center", 15, spacing)
    elif textWidth(student, 10) < 380:
        LineOfText(student, "center", 10, spacing)
    else:
        LineOfText(student, "center", 5, spacing)
    spacing = spacing + 15 + 10
    
    #5) Student ID#
    id = "ID# " + str(studentID)
    LineOfText(id , "center", 10, spacing)
    spacing = spacing + 10 + 10
    
    #6) Total Passes
    passes = "Total Passes: " + str(totalPasses)
    LineOfText(passes, "center", 10, spacing)
    spacing = spacing + 10 + 10
    
    #7) Total Overtime Passes
    overtimePasses = "Overtime Passes: " + str(totalOvertimePasses)
    LineOfText(overtimePasses, "center", 10, spacing)
    spacing = spacing + 10 + 10
    
    #8) Total Time Out
    timeOut = "Total Minutes Out: " + str(totalTimeOut)
    LineOfText(timeOut, "center", 10, spacing)
    spacing = spacing + 10 + 10
    
    # Line
    line = Line(20, spacing, 380, spacing)
    add(line)
    spacing = spacing + 30 + 10
    
    #9) Date
    today = str(date.today().strftime("%B %d, %Y"))
    LineOfText(today, "center", 30, spacing)
    spacing = spacing + 25 + 10
    
    #10) Time Left Class
    time = datetime.now()
    lTime = time.strftime("%I:%M %p")
    LineOfText("Left Class at:", "left", 10, spacing)
    LineOfText(lTime, "left", 25, spacing + 35)
    
    #11) Return Time
    rTime = time + timedelta(minutes=PASSLENGTH)
    rTime = rTime.strftime("%I:%M %p")
    LineOfText("Return To Class By:", "right", 10, spacing)
    LineOfText(rTime, "right", 25, spacing + 35)
    spacing = spacing + 65
    
    #12) Bar Code
    bcList = idToBarcodeConverter(studentID)
    printBarCode(bcList, spacing)
    spacing = spacing + 70
    
    #13) Pass #
    passCount = pc + 1
    num = Text(passCount)
    num.set_position(400 - 30, spacing)
    num.set_font("5pt Arial")
    add(num)

#COLLECTS STUDENT ID (Put code for barcode scanner input here)
studentID = int(input("Enter ID #: "))

#Adds to Total Passes and Total Minutes Out
studentList[studentID][2] = studentList[studentID][2] + 1
studentList[studentID][3] = studentList[studentID][3] + PASSLENGTH

#Looks up ID information
student = (studentList[studentID][0] + ' ' + studentList[studentID][1])
totalPasses = studentList[studentID][2]
totalTimeOut = studentList[studentID][3]
totalOvertimePasses = studentList[studentID][4]

printReceipt(passCount)
