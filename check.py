#!/usr/bin/env python3
import requests
import nexmo

try:
	f=open("code","r")
	last_code=f.read()
	f.close() 
except FileNotFoundError:
	last_code = ''

try:
    r = requests.head("https://hackuj.ksiazka.sekurak.pl/api/get-image?id=D7YevAAtU1z84TcHY4FD0bJkpX0v1Kpw9rlK5w2jR44=")
    code = str(r.status_code)
    print(r.status_code)
    #r = requests.head("http://localhost/test12/aaa")
    #print(r.status_code)

    # prints the int of the status code. Find more at httpstatusrappers.com :)
except requests.ConnectionError:
    print("failed to connect")
    code = 'failed'

if code != last_code:
	print("Send sms")
	client = nexmo.Client(key='', secret='')
	client.send_message({
		'from': 'Nexmo',
		'to': '48..',
		'text': 'HTTP code is ' + code + '...',
	})

	#client.send_message({
	#	'from': 'Nexmo',
	#	'to': '48..',
	#	'text': 'HTTP code is ' + code + '...',
	#})

f=open("code","w")
f.write(code)
f.close() 
