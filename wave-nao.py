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

current_posture = posture_proxy.getPosture()

if current_posture != "Stand":
    # Make NAO stand up
    posture_proxy.goToPosture("StandInit", 1.0)

try:
    with open("C:\\venvProjects\\projectIshani\\flask-server\\responseText.txt", "r") as f:
        text = f.read().replace('\n', ' ')
    tts.say(text)
except Exception as e:
    print("An error ocurred: ", e)

