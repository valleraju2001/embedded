# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:05:21 2021

@author: Uday
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 14:31:06 2021

@author: Uday
"""

from sys import exit
import smtplib
import speech_recognition as sr
import pyttsx3
import easyimap as e
from email.message import EmailMessage
import imaplib as im
import email as e
import os

unm="gadenagaramya9@gmail.com"
pwd="nagaramya"

r=sr.Recognizer()

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',150)

def speak(strg):
    print(strg)
    engine.say(strg)
    engine.runAndWait()
    
def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        strg="Speak Now:"
        speak(strg)
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            return text
        except:
            strg="sorry could not recognize what you said"
            speak(strg)
            
  
def email_list():
    lists = {
        'hello': 'n160802@rguktn.ac.in',
        'manikanta': 'n160292@rguktn.ac.in',
        'ishwar': 'n160338@rguktn.ac.in',
        'pindi': 'n160108@rguktn.ac.in',
        'jivan': 'n160102@rguktn.ac.in',
        'satya': 'n160829@rguktn.ac.in',
        'ramya':'n161249@rguktn.ac.in',
        'prasanna':'n161282@rguktn.ac.in',
        'raju':'n161288@rguktn.ac.in'
    }
    return lists

def email_info():
    speak('To whom u want to send email')
    person = listen()
    t = email_list()#checking mail in the list or not
    try:
        person=person.lower()
        speak(person)
        print("your sender mail is:",t[person])
        speak(t[person])
        speak('subject of the mail')
        sub = listen()
        print('subject of the mail is :', sub)
        speak('Body of the mail')
        body = listen()
        print('body of the mail is :', body)
        send_mail(t[person], sub, body)
    except:
        print('no email found please try again')
        speak('no email found please try again')
        email_info()

def send_mail(receiver, sub, msg):
    email = EmailMessage()
    email['From'] = 'gadenagaramya9@gmail.com'
    email['To'] = receiver
    email['Subject'] = sub
    email.set_content(msg)
    speak("say 0 for no attachemt to add (or) 1 for add attachment : ")#file attaching
    attachment_response = listen()
    if (attachment_response == '1' or attachment_response=='one'):
        file_number = 0
        files = []
        print('your files in this path are:\n')
        speak('your files in this path are:')
        for entry in os.scandir('.'):
            if entry.is_file():
                print(str(file_number) + ". " + entry.name)
                speak(str(file_number) + "is " + entry.name)
                files.append(entry.name)
                file_number += 1
        speak(("say file number to add : "))
        file_number =int(listen())
        with open(files[file_number], 'rb') as f:
            file_data = f.read()
            file_name = f.name

        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
    try:
        print('if you want to change mail composing please say zero or stop the mail choose one or continue choose two')
        speak('if you want to change mail composing please say zero or stop the mail choose one or continue choose two')
        t=listen()
        t=t.lower()
        speak(t)
        if(t=='2' or t=='tu' or t=='two' or t==2 or t=='to'):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('gadenagaramya9@gmail.com', 'nagaramya')
            server.send_message(email)
            print('Mail sent.....')
            speak('mail sent')
        elif(t=='0' or t=='zero'):
            email_info()
        elif(t=='1' or t=='one'):
            return 0
    except:
        print('Something went wrong')
        speak('something went wrong please try again')
        email_info()

"""def sendmail(receiver,subject,message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    
    server.login('gadenagaramya9@gmail.com','nagaramya')
    email=EmailMessage()
    email['From']='Sender_Email'
    email['To']=receiver
    email['Subject']=subject
    email.set_content(message)
    server.send_message(email)
    strg="successfully sent a mail"
    speak(strg)
    """
        
    
def readmail():
    server=e.connect("imap.gmail.com",unm,pwd)
    server.listids()
    
    strg="Please say the Serial Number of the email you wanna read starting from latest"
    speak(strg)
    
    a=listen()
    if(a=="Tu"):
        a="2"
    b=int(a)-1
    
    email=server.mail(server.listids()[b])
    
    strg="The email is from: "
    speak(strg)
    speak(email.from_addr)
    strg="The subject of the email is: "
    speak(strg)
    speak(email.title)
    strg="The body of email is : "
    speak(strg)
    speak(email.body)
    
def inbox_check():
    mail = im.IMAP4_SSL("imap.gmail.com")
    mail.login('gadenagaramya9@gmail.com', 'nagaramya')
    stat, total_msgs = mail.select("inbox")
    result, data = mail.uid('search', None, "ALL")
    inbox_list = data[0].split()
    recent = inbox_list[-1]
    result2, data2 = mail.uid('fetch', recent, '(RFC822)')
    raw_mail = data2[0][1].decode("utf-8")
    e_msg = e.message_from_string(raw_mail)
    string = str(total_msgs[0])
    tot_count = string[2:-1]
    mail.select()
    uscount = len(mail.search(None, 'UnSeen')[1][0].split())  # unseen mails count
    unseen = str(uscount)
    print('total mails are :', tot_count)
    speak("total mails received")
    speak(tot_count)
    print("Number of Unseenmails:" + unseen)
    speak("Number of unseen mails")
    speak(unseen)
    print("Receiver : ", e_msg['To'])
    print("You received recent mail from : \n", e_msg['From'])
    speak("You received recent mail from")
    speak(e_msg['From'])
    print("Subject of the mail is : \n", e_msg['Subject'])
    speak("Subject of the mail is")
    speak(e_msg['Subject'])
    for part in e_msg.walk():
        if part.get_content_type() == 'text/plain':
            a = part.get_payload()
            speak("Body of the mail is ")
            print("Body of the mail is : \n", a)
            speak(a)
    
strg="Welcome to voice controlled email service"
speak(strg)

while(1):
    
    strg="What do you want to do?"
    speak(strg)
    
    strg="speak CHECK to check your inbox  speak SEND to Send email  speak READ to Read Inbox  speak EXIT to Exit"
    speak(strg)
    
    ch=listen()
    
    if (ch=="send"):
        email_info()
        """strg="You have chosen to send an email"
        speak(strg)
        
        strg="to whome you want to send"
        speak(strg)
        person=listen()
        person=person.lower()
        t = email_list()
        
        try:
            print("your sender mail is:",t[person])
            speak(t[person])    
            strg="speak subject of mail: "        
            speak(strg)
            subject=listen()
            strg="you said the subject of mail as :"
            speak(strg)
            speak(subject)
            strg="speak body of mail: "
            speak(strg)
       
            message=listen()
            strg="you said the message as :"
            speak(strg)
            speak(message)
            receiver=t[person]
        
            sendmail(receiver,subject,message)
        except:
            print('no email found please try again')
            speak('no email found please try again')
        """
        
    elif (ch=="read"):
        strg="You have chosen to read email"
        speak(strg)
        readmail()
        
    elif (ch=="check"):
        speak("You choose an option to check inbox")
        inbox_check()
        
        
    elif (ch=="exit"):
        strg="You have chosen to exit, bye bye"
        speak(strg)
        exit()
        
    else:
        strg="Invalid choice, you said: "
        speak(strg)
        speak(ch)
    
    