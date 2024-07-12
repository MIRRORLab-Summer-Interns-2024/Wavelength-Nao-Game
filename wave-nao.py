import time
import naoqi
from naoqi import ALProxy

tts = ALProxy

# text to speech proxy
tts = ALProxy("ALTextToSpeech", "10.60.198.90", 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", "10.60.198.90", 9559)


# posture proxy
posture_proxy = ALProxy("ALRobotPosture",  "10.60.198.90", 9559)

# Make NAO stand up
posture_proxy.goToPosture("StandInit", 1.0)

while True:
    try:
        with open("C:\\venvProjects\\projectIshani\\flask-server\\responseText.txt", "r") as f:
            text = f.readline()
            lines = f.readlines()
        tts.say(text)
        with open("C:\\venvProjects\\projectIshani\\flask-server\\responseText.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != text:
                    f.write(line)
                
        time.sleep(1)
    except Exception as e:
        
        print("An error occurred: ", e)
        time.sleep(1)
