import time, os
import RPi.GPIO as GPIO


def cameraInit():
	import picamera, time
	camera = picamera.PiCamera()
	time.sleep(2)
	return camera
	
def takePicture(camera, filename):	
	c = camera
	os.system("mplayer ~/Desktop/PiCameraTest/cclick-01.mp3 >/dev/null 2>&1")
	c.capture(filename)

def imaggaUpload(filename):
	import requests
	img = filename
	api_key = '' #Your API Key
	api_secret = '' #Your API Secret

	responseContentID = requests.post('https://api.imagga.com/v1/content',
					auth=(api_key, api_secret),
					files = {"file": open(img,"r")})

	contentID=responseContentID.json()["uploaded"][0]["id"]
	uploadStatus = responseContentID.json()["status"]
	return contentID
	print("Upload status: "+uploadStatus)
	print("ContentID: "+contentID)

def imaggaTag(contentID):	
	import requests
	cID = contentID
	api_key = '' #Your API Key
	api_secret = '' #Your API Secret
	
	responseTag = requests.get('https://api.imagga.com/v1/tagging?content=%s' % cID,
					auth=(api_key, api_secret))
	tags = responseTag.json()["results"][0]["tags"]
	print"Item tags : "
	for i in range(0,5):
		print tags[i]["tag"].encode("ascii")+":"+str(round(tags[i]["confidence"],2));

	result = tags[0]["tag"].encode("ascii")
	cofidence = str(round(tags[0]["confidence"],2)) +"%";

		
	#t1 = "espeak -ven+f8 -k5 -s150 "+"'The Item is '" +result+"'Confidence is '"+cofidence +" >/dev/null 2>&1"
	t2 = "Item is " +result+", which confidence is "+cofidence+"."
	os.system("sudo speech.sh "+t2+" >/dev/null 2>&1")


camera = cameraInit()
GPIO.setmode(GPIO.BOARD)
buttomPin=3
GPIO.setup(buttomPin,GPIO.IN)

prev_input=1
i=0
filename="test"
pNum=1
print "Press the button to take a picture"
while True:	
	input=GPIO.input(buttomPin)
	if ((not prev_input) and input):
		i += 1
		print "Taking picture..."
		image = filename+str(pNum)+".jpg"
		takePicture(camera,image)		
		print image
		print "Uploading picture..."
		imageID = imaggaUpload(image)
		imaggaTag(imageID)
		print "Done!\n"
		print "Press the button to take a picture"
		pNum=pNum+1
	prev_input=input
	time.sleep(0.1)
