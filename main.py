
import webbrowser
from AppOpener import open
from AppOpener import close
from googlesearch import search
from send_message import *
import subprocess



def show_history():
    query = "select * from history"
    data = cursor.execute(query).fetchall()
    datee = []
    start_time = []
    end_time= []
    print(data)
    for item in data:
        datee.append(item[0])
        start_time.append(item[1])
        end_time.append(item[2])
    data = pandas.DataFrame({"date":datee,"start time":start_time,"end time":end_time})
    
       
    
    data.to_excel("history.xlsx",index=False)
    os.system("history.xlsx")




def send_email():
    try:
        speaker.speak("Email Module Activated..........")
        speaker.speak("say the message to be sent.")
        message = get_message()
        
        speaker.speak("say the subject of the email")
        subject = get_email_subject()
        
        speaker.speak("select the name of the recepient by their name")
        users= get_user_email()
        
        message = formate_message(message)
        
        users = check_emails_in_database(users)
        
        for i in users:
            speaker.speak(f"sending email to {i}")
            msg = f"""hello, {i}
            
    {message}
                
regards Gagan
            """
            sed_an_email(msg,users[i],subject)
        speaker.speak("emails sent sccessfully ")
        
        
        
    except Exception as e:
        speaker.speak("internal error occured")
        speaker.speak("ending email module")
        
        
def show_saved_emails():
    names = conn.execute("select name from emails ").fetchall()
    emails = conn.execute("select email from emails").fetchall()
    emergency = conn.execute("select emergency from emails").fetchall()
    name = []
    email = []
    emer = []
    for i in range(len(names)):
        name.append(names[i][0])
        email.append(emails[i][0])
        if emergency[i][0] == None:
            emer.append('')
        else:
            emer.append(emergency[i][0])
    print(emer)
    
    data = pandas.DataFrame({"recepeiant":name,"emails":email,"emergency_email(set any characters values to set as emergency)":emer})
    print(data)
    data.to_excel("emails.xlsx",index=False)
    
    speaker.speak("you can edit these data, the change will be applied in database. ")
    os.system("emails.xlsx")
    
    data = pandas.read_excel("emails.xlsx")
    names = data['recepeiant']
    emails = data['emails']
    emergency = data.get('emergency_email(set any characters values to set as emergency)','null')
    
    conn.execute("delete from emails;")
    conn.commit()
    speaker.speak("saving the data")
    print(names)
    print(emails)
    for i in range(len(names)):
        if  not isinstance(emergency[i],str) :
            emer = 'null'
            query = f"insert into emails values('{names[i]}','{emails[i]}',{emer});"
        else:
            query = f"insert into emails values('{names[i]}','{emails[i]}','{emergency[i]}');"
        conn.execute(query)
        conn.commit()
            
    speaker.speak("data saved succesfully")
def show_saved_contact():
    names = conn.execute("select name from contact ").fetchall()
    emails = conn.execute("select mob_number from contact").fetchall()
    emergency = conn.execute("select emergency from contact").fetchall()
    name = []
    email = []
    emer = []
    for i in range(len(names)):
        name.append(names[i][0])
        email.append(emails[i][0])
        if emergency[i][0] == None:
            emer.append('')
        else:
            emer.append(emergency[i][0])
    
    data = pandas.DataFrame({"names":name,"contact":email,"emergency_contact(set any characters values to set as emergency)":emer})
    
    data.to_excel("contacts.xlsx",index=False)
    
    speaker.speak("you can edit these data, the change will be applied in database.")
    os.system("contacts.xlsx")
    

    
    data = pandas.read_excel("contacts.xlsx")
    names = data['names']
    emails = data['contact']
    emergency = data['emergency_contact(set any characters values to set as emergency)']
    conn.execute("delete from contact;")
    conn.commit()
    speaker.speak("saving the data")
    for i in range(len(names)):
        if  not isinstance(emergency[i],str) :
            emer = 'null'
            query = f"insert into contact values('{names[i]}','{emails[i]}',{emer});"
        else:
            query = f"insert into contact values('{names[i]}','{emails[i]}','{emergency[i]}');"
        conn.execute(query)
        conn.commit()
    speaker.speak("contacts saved successfully")
        


def send_whats_message():
    try:
        speaker.speak("whatsapp module activated")
        speaker.speak("say the message to be sent.")
        msg = get_message()
        
        speaker.speak("say the names of the users")
        
        users = get_user_email()
        
        users = check_contacts_in_database(users)
        
        speaker.speak("do u like to send sms bomber")
        yes = str(takecmd()).lower()
        bomber =  0
        if any(map(lambda x : x in yes,["yes","send"])) and not "no" in yes:
            speaker.speak("say the number of the times the message has to be sent")
            bomber = get_bomber()
        msg = formate_message(msg)
        msg = msg.replace('"',"")
        for i in users:
            send_what_s_message(msg,users[i],int(bomber))
            time.sleep(3)
            
        speaker.speak("whats app message sent successfully")
        speaker.speak("ending whats app module")
        time.sleep(3)
        close("google chrome",match_closest=True)
    except Exception as e:
        speaker.speak("internal error occured ending message module")
        print(e)
        
def sendemergency():
    
    email_tule = conn.execute("select email from emails where emergency not null").fetchall()
    
    if not email_tule:
        speaker.speak("no emergency emails found, so sending emails to first 3 emails")
        email_tule = conn.execute("select email from emails limit 3").fetchall()
    emails = [email[0] for email in email_tule]
        
        

    pwd = str(subprocess.run(["cd"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout).replace("b'","").replace("'","").replace(r"\\","\\")
    pwd = pwd[:len(pwd)-3]
    print(pwd+"\\locationscript.ps1")
    cmd = f'powershell -ExecutionPolicy ByPass -File "{pwd}locationscript.ps1" '
    print(r"{}".format(cmd))
    
    location = str(subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout)
    
    latitude = (location[:location.index(r"\r")]).replace("b'","")
    logitude = (location[location.index(r"\n")+2:]).replace("b'","")
    logitude = logitude[:logitude.index(r"\r")]
    
    link = f"https://maps.google.com/maps?q={latitude},{logitude}"
    for i in emails:
        sed_an_email(message=f"emergency alert \n the location is {link}",subject="sos message",to_email= i)
    pass

    contacts = conn.execute("select mob_number from contact where emergency not null;").fetchall()
    
    if not contacts:
        speaker.speak("no emergency emails found, so sending emails to first 3 emails")
        contacts = conn.execute("select email from emails limit 3").fetchall()
    number = [cont[0] for cont in contacts]
    
    for i in number:
        send_what_s_message("this is emergency message the location is "+link,mob_number=i,bomber=0)
    time.sleep(2)
    close("google chrome",match_closest=True)
    
        
    
        
     
p_time = None
start_time = None
c_date = None
    
try:
    checktable()
    while 1:
        repeat_error = False
        a = str(takecmd(repeat_error))
        if("activate" in a.lower()):
            p_time = time.localtime(time.time())
            start_time = f"{p_time.tm_hour}:{p_time.tm_min}:{p_time.tm_sec}"
            c_date = f"{p_time.tm_mday}/{p_time.tm_mon}/{p_time.tm_year}"
            print("Assistant activated")
            speaker.speak("Assistant activated")
            while 1:
                
                quitvar = str(takecmd()).lower()
                value = quitvar.split(" ")
                #open anything
                print(quitvar)
                if quitvar or quitvar != " " or quitvar !="none" or quitvar != None or quitvar!=None:
                    if "open" in quitvar:
                        quitvar = quitvar.replace("open","")
                        try:
                            open(quitvar,match_closest=True,throw_error=True,output=True)
                            speaker.speak("Opening the Application.")
                        except Exception as e:
                            speaker.speak("opening the result in google")
                            links = search(quitvar,tld="co.in", num=5, stop=10, pause=2)
                            for j in links:
                                webbrowser.open(j)
                                break
                            
                            
                            
                    #close an application
                    elif "close" in quitvar:
                        a.replace("close","")
                        try:
                            close(quitvar,match_closest=True,output=True,throw_error=True)
                            speaker.speak("Application closed")
                        except:
                            speaker.speak("Application is not runnning")
                        
                        
                            
                    #generate image with ai
                    elif "system shutdown" in quitvar and not "no" in quitvar:
                        cursor = conn.cursor()
                        end_time = time.localtime(time.time())
                        endtime2 = f"{end_time.tm_hour}:{end_time.tm_min}:{end_time.tm_sec}"
                        count = "select count(*) from history;"
                        count =  cursor.execute(count).fetchall() 
                        query = f"insert into history(datee,start_time,end_time,sino) values('{c_date}','{start_time}','{endtime2}','{count[0][0]}');"
                        cursor.execute(query)
                        conn.commit()
                        conn.close()
                        speaker.speak("System Shut Downing")
                        os.system("shutdown /s /t 1")   
                    elif "system lock" in quitvar:
                        os.system("Rundll32.exe user32.dll,LockWorkStation")
                    
                    
                    #send an emails to users
                    #email key is  send an emil to user_name and the is message is
                    elif "send email" in quitvar:
                        send_email()
                    
                    
                    elif "send" in  quitvar and "message" in quitvar:
                        send_whats_message()
                    
                                
                    elif value[0] == "search":
                        quitvar = quitvar.replace("search ","")
                        quitvar = quitvar.replace(" ","+")
                        webbrowser.open(f"https://www.google.com/search?q={quitvar}")
                                        
                            
                    elif quitvar == "deactivate":
                        cursor = conn.cursor()
                        end_time = time.localtime(time.time())
                        endtime2 = f"{end_time.tm_hour}:{end_time.tm_min}:{end_time.tm_sec}"
                        count = "select count(*) from history;"
                        count =  cursor.execute(count).fetchall() 
                        query = f"insert into history(datee,start_time,end_time,sino) values('{c_date}','{start_time}','{endtime2}','{count[0][0]}');"
                        cursor.execute(query)
                        conn.commit()
                        speaker.speak("Okay, Assistant is shutting down.")
                        break
                    
                    elif "show saved emails" in quitvar:
                        show_saved_emails()
                    
                    
                        
                    elif "show saved contacts" in quitvar:
                        show_saved_contact()

                    elif "show access history" in quitvar:
                        show_history()
                        
                            
                    elif "emergency" in quitvar:
                        sendemergency()
                        
                    elif "gemini" in quitvar:
                        speaker.speak(get_message_info(quitvar))
        elif "emergency" in str(a).lower():
                        sendemergency()           
                    
                    
                
                    
except KeyboardInterrupt:
    cursor = conn.cursor()
    end_time = time.localtime(time.time())
    endtime2 = f"{end_time.tm_hour}:{end_time.tm_min}:{end_time.tm_sec}"
    count = "select count(*) from history;"
    count =  cursor.execute(count).fetchall() 
    query = f"insert into history(datee,start_time,end_time,sino) values('{c_date}','{start_time}','{endtime2}','{count[0][0]}');"
    cursor.execute(query)
    conn.commit()
    conn.close()
    speaker.speak("program exits!")
    exit()
            
except Exception as e:
    print(e)
    speaker.speak("internal error occured ")
    conn.commit()
    conn.close()
                

                
                    
                        
            
           
    
