from common_variables import *
from email.message import EmailMessage
import smtplib
import pyautogui as pg
import pywhatkit


        
def get_message()->str:
    while 1:
        message = str(takecmd())
        
        speaker.speak("the message is "+message)
        
        speaker.speak("is that message correct")
        yes =str(takecmd()).lower()
        if any(map(lambda x: x in yes,["yes","correct"])) and not "no" in yes:
            return message
        speaker.speak("please say the message correctly")
    

    
def get_email_subject()->str:
    while 1:
        message = str(takecmd())
        
        speaker.speak("the sunject is "+message)
        
        speaker.speak("is the subject correct")
        yes = str(takecmd()).lower()
        if any(map(lambda x : x in yes,["yes","correct"]))and not "no" in yes:
            return message
        speaker.speak("please say the subject clearly")
        
def get_user_email()->list:
    while 1:
        users = str(takecmd()).lower()+" select"
        
        count_of_users = users.count("select")-1
        user_name_list = []
        for i in range(count_of_users):
            users = users[users.index("select")+7:]
            user_name = users[:users.index("select")-1]
            user_name_list.append(user_name)
        if not user_name_list:
            speaker.speak("selected names are empty say the names correctly")
            continue
        file = open("virtual.txt","w")
        for i in user_name_list:
            file.write(i+"\n")
        file.close()
        speaker.speak("if anything is wrong make the necessary changes and save and close it")
        os.system("virtual.txt")
        
        file = open("virtual.txt","r")
        user_name_list = []
        for i in file:
            user_name_list.append(i[:len(i)-1])
        file.close()
        
        
            
        return user_name_list
        
        
def check_emails_in_database(user_name_list)->dict:
    speaker.speak("checking the emails of the users in database")
    one_emails = {}
    multi_emails = {}
    no_emails = []
    
    
    for i in user_name_list:
        email = cursor.execute(f"select e.name ,e.email from emails e where e.name like '%{i}%';").fetchall()
        if len(email) ==1:
            one_emails[i] = email[0][1]
        elif len(email) >1:
            multi_emails[i] = email
        else:
            no_emails.append(i)
            
            
    
    if multi_emails:
        speaker.speak("there are some multiple names in database")
        file = open("virtual.txt","w")
        for i in multi_emails:
            file.write(i+"\n")
        file.close()
        speaker.speak("your input data will be displayed, make your changes and , save, and colse the text file")
        os.system("virtual.txt")
        
        file = open("virtual.txt","r")
        for i in file:
            v = i[:len(i)-1]
            if multi_emails[v]:
                one_emails[v] = multi_emails[v]
        file.close()   
        
            
    if no_emails:
        speaker.speak("there are some names that they are not present in my data")
        speaker.speak("do you like to add their emails")
        yes = str(takecmd()).lower()
        if "yes" in yes:
            file = open("virtual.txt","w")
            for i in no_emails:
                while 1 :
                    speaker.speak(f"say the email for {i}")
                    email = str(takecmd()).lower()
                    if " at " in email:
                        email = email.replace(" at ","@")
                        email = email.replace(" ","")
                        file.write(email="\n")
                        break
                    speaker.speak("invalid email format")
            file.close()
            emails = []
            speaker.speak("your input data will be displayed, make your changes and , save and colse the text file")
            os.system("virtual.txt")
            
            file = open("virtual.txt","r")
            for i in file:
                emails.append(i[:len(i)-1])
            i=0
            for j in no_emails :
                if emails[i]:
                    one_emails[j] = emails[i]
                    cursor.execute(f"insert into emails(name,email) values('{j.lower()}','{emails[i]}');")
                    conn.commit()
                i+=1   
    speaker.speak("users found ")
    return one_emails
                    
def sed_an_email(message:str,to_email:str,subject:str="Message by Virtual Assisstent")->bool:
        try:
            your_email_id = "gagan.mdhanush@gmail.com"
            your_app_pass = ""
            msg = EmailMessage()
            msg.set_content(message)
            msg['From'] = your_email_id
            msg['To'] = to_email
            msg["Subject"] = subject
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(your_email_id,your_app_pass)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False                  
        
        
        
def get_bomber()->int:
    while 1:
        try: 
            number = str(takecmd()).lower()+" "
            
            number = number[number.index(' ')+1:]
            number = number[:number.index(" ")]
            number = int(number)
            speaker.speak(f"your input is {number}")
            speaker.speak("is that correct ")
            
            yes = str(takecmd()).lower()
            if any(map(lambda x:x in yes,["yes","correct"])) and not("no" in yes):
                return number
        except ValueError:
            speaker.speak("please say the number correctly")
            

            
        
        
def check_contacts_in_database(user_name_list)->dict:
    speaker.speak("checking the conatct number of the users in database")
    one_emails = {}
    multi_emails = {}
    no_emails = []
    
    
    for i in user_name_list:
        if not i:
            continue
        email = cursor.execute(f"select e.name ,e.mob_number from contact e where e.name like '%{i}%';").fetchall()
        if len(email) ==1:
            one_emails[i] = email[0][1]
        elif len(email) >1:
            multi_emails[i] = email
        else:
            no_emails.append(i)
            
            
    
    if multi_emails:
        speaker.speak("there are some multiple names in database")
        
        file = open("virtual.txt","w")
        for i in multi_emails:
            file.write(i+"\n")
        file.close()
        speaker.speak("your input data will be displayed make your changes and save and colse the text file")
        os.system("virtual.txt")
        
        file = open("virtual.txt","r")
        for i in file:
            v = i[:len(i)-1]
            if multi_emails[v]:
                one_emails[v] = multi_emails[v]
        file.close()   
        
            
    if no_emails:
        speaker.speak("there are some names that they are not present in my data")
        speaker.speak("do you like to add their contact")
        yes = str(takecmd()).lower()
        if "yes" in yes:
            file = open("virtual.txt","w")
            for i in no_emails:
                while 1 :
                    speaker.speak(f"say the number for {i}")
                    number = str(takecmd()).lower()
                    number = number.replace(" ","")
                    try: 
                        number = int(number)
                        file.write(str(number)+"\n")
                        break
                    except :
                        speaker.sepak("invalid number type plase say agian")
                    
            file.close()
            emails = []
            speaker.speak("your input data will be displayed make your changes and save and colse the text file")
            os.system("virtual.txt")
            
            file = open("virtual.txt","r")
            for i in file:
                emails.append(i[:len(i)-1])
            i=0
            for j in no_emails :
                if emails[i]:
                    one_emails[j] = emails[i]
                    cursor.execute(f"insert into contact(name,mob_number) values('{j.lower()}','{emails[i]}');")
                    conn.commit()
                i+=1   
    speaker.speak("users found ")
    return one_emails
    
def send_what_s_message(message,mob_number,bomber):
    pywhatkit.sendwhatmsg_instantly("+91"+mob_number,message)
    if bomber:
        for _ in range(bomber):
            pg.typewrite(message)
            pg.press("enter")
    