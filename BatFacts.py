import smtplib
import time
import random
import os
def message(facts,carriers,msg_from):
	
	intro= 'Thank you for subscribing to Bat Facts!\n'
	pNum=''
	while len(pNum)!=10 and not pNum.isdecimal():
		pNum=input('phone number: ')
	validCarrier=False
	carrier=''
	while True:
		carrier=input('t for T Mobile || v for Verizon || s for Sprint || a for AT&T').lower()
		if carrier in carriers.keys():
			break
	msg_to =pNum+carriers[carrier]
	while True:
		intervalType=input('r for random interval, f for fixed interval').lower()
		if intervalType=='r':
			low=input('low end interval length in minutes: ')*60
			high=input('high end interval length in minutes: ')*60
			break 
		if intervalType=='f':
			fixed=input('interval length in minutes: ')*60
			break
	time.sleep(input("Wait time before starting in minutes: ")*60)
	session.sendmail(msg_from, msg_to, facts[0])	
	for fact in facts[1:]: 
		msg=intro+fact
		print(fact)
		if len(msg)>130:  
			for i in range(129,0,-1):
                		if msg[i]==' ':
                    			sep=i
                   			break
			session.sendmail(msg_from, msg_to, msg[:sep])
			session.sendmail(msg_from, msg_to, msg[sep+1:])
		else:
			session.sendmail(msg_from, msg_to, msg)
		if intervalType=='r':
			interval=random.random()*(high-low)+low
		else:
			interval=fixed
		time.sleep(interval)
	os._exit(0)  

def startMessages(facts):
	msg_from = 'BatFacts'         # who the message is 'from'
	carriers={'t':'@tmomail.net','a':'@txt.att.net','s':'@messaging.sprintpcs.com','v':'@vtext.com'}
	while True:
		newpid = os.fork()
		if newpid == 0:
			message(facts,carriers,msg_from)
		reply = input("q for quit / c for new phone number")
		if reply == 'c': 
			continue
		else:
			break

def main():
    # Send an e-mail or SMS text via GMail SMTP
	file=open('batfacts.txt','r')
	facts=[line.strip() for line in file]
	file.close()
	gmail_username = input("Enter the gmail account to use: ")      # sender's gmail username
	gmail_password = input("Enter the gmail password: ")               # sender's gmail password
	smtp_server = 'smtp.gmail.com'
	smtp_port = 587
	session = smtplib.SMTP(smtp_server, smtp_port)
	session.ehlo()
	session.starttls()
	session.ehlo()
	session.login(gmail_username, gmail_password)
	startMessages(facts)
	session.quit()

main()
