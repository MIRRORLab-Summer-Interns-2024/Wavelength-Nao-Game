
import time
import multiprocessing
import speech_recognition as sr
from openai import OpenAI
import json
import random
import os
import subprocess

# Command to run the Python 2 script
command = ["python2", "wave-nao.py"]

openAIKey = os.environ.get("OPENAI_API_KEY")

'''
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')
'''

'''
microphones = sr.Microphone.list_microphone_names()
for index, name in enumerate(microphones):
  print(f"Microphone with index {index} and name \"{name}\" found")
'''

# Initialize the recognizer
r = sr.Recognizer()


# Initialize the OpenAI client
client = OpenAI(api_key=openAIKey)
MODEL = "gpt-4o"


chat_history = [{"role": "system", "content": "You are a NAO robot that plays a game. You are both the gamemaster and a clue giver of the game wavelength. Wavelength is a game in which the gamemaster provides a category of things to all players. The clue givers are given a random number between 1 and 10 inclusive. Each clue giver must provide the guesser a simple thing within the category that, in their opinion, matches the ranking of the number out of ten that they were provided. Each clue giver gets a different category. As each clue is given, the guesser makes a prediction on what the number is. Once all clues have been given, the guesser must provide their final guess of the number from 1-10."}]

responseH = ""

with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "w") as f:
	json.dump(chat_history,f)

		
def speak(mic,person):
	print(person, mic)
	with sr.Microphone(device_index=mic) as source:
		r.adjust_for_ambient_noise(source)
		print("Listening for " + person)
		audio = r.listen(source)
		print("Stop Listening")
		try:
			text = r.recognize_google(audio)
			print("mic " + str(mic) + " " + person + " said: " + text)
			return text


		except Exception as e:
			print("I didn't catch that. Please say that again.")
			speak(mic,person)

def chatGPT(prompt):
# read current chat history	
	global responseH
	with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "r") as f:
		chat_history = json.load(f)
		chat_history.append({'role': 'user', 'content': prompt})

		completion = client.chat.completions.create(
			model= MODEL,
			messages= chat_history
		)

		response = completion.choices[0].message.content
		#print(response)

		# Add the assistant's response to the chat history
		chat_history.append({"role": "assistant", "content": response})

		# Save the updated chat history back to the file
		with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "w") as f:
			json.dump(chat_history, f)

		responseH += "\n" + response 

def say():
	global responseH
	with open("C:\\venvProjects\\projectIshani\\flask-server\\responseText.txt", "w") as f:
		f.write(responseH)
	responseH = ""

	# Run the command and capture the output
	result = subprocess.run(command, capture_output=True, text=True)


def record(prompt):
	# read current chat history
	if prompt != None:
		with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "r") as f:
			chat_history = json.load(f)
			chat_history.append({'role': 'user', 'content': prompt})

			# Save the updated chat history back to the file
			with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "w") as f:
				json.dump(chat_history, f)

savePlayers = "n"

with open("C:\\venvProjects\\projectIshani\\flask-server\\responseText.txt", "w") as f:
	f.write(" ")

while True:
	start = "y"

	if start == "y":

		print("Let's play Wavelength!")

		readIntructions = input("Do you want to hear the game instructions? (y/n): ")

		if readIntructions == "y":
			responseH = "Wavelength is a game in which the gamemaster provides a category of things to all players. The NAO robot acts as both the gamemaster and a player. The clue givers are given a random number between 1 and 10 inclusive. Each clue giver must provide the guesser a simple thing within the category that, in their opinion, matches the ranking of the number out of ten that they were provided. Each clue giver gets a different category. As each clue is given, the guesser makes a prediction on what the number is. Once all clues have been given, the guesser must provide their final guess of the number from 1-10."
			say()

		if savePlayers == "n":
			numPlayers = int(input("How many players? "))

			names = [0 for i in range(numPlayers)]
			
			for i in range(0,numPlayers):
				names[i] = input("Enter Player " + str(i+1) + "'s name: ")

		guesser = random.randint(0, numPlayers-1)

		record("The guesser is " + names[guesser]  + ". Guesser, look away.")
		#print("The guesser is " + names[guesser]  + ". Guesser, look away.")
		responseH +=  "\n" + "The guesser is " + names[guesser]  + ". Guesser, look away." 
		say()

		# random number
		randomNum = random.randint(1, 10)

		time.sleep(1)
		print("The number is: " + str(randomNum))

		chatGPT("There are " + str(numPlayers - 1) + " clue givers. In the next few questions we will ask you to provide a category for the clue giver to give a word on. We will provide their name, clue, and the predicted number that the guesser came up with. After that happens for multiple people, you will act as a clue giver and give a word on a new category that you come up with. The correct number that the guesser is trying to guess is " + str(randomNum) + "Provide 'Ok, let's get started!' if you understand this message. ")
		say()

		for i in range(0, numPlayers):

			if i!=guesser:
				# generate category for player i
				record("Player " + names[i] + " this is your category: ")
				#print("Player " + names[i] + " this is your category: ")
				responseH += "\n" + "Player " + names[i] + " this is your category: "
				say()

				chatGPT("Give me a random category of items that is simple in one word. Make it interesting, and choose random things, like items in a house, or minecraft mobs, or computer brands. Don't choose those, but do cool and different stuff. Stuff like fruits is boring. Also animals and colors are also so boring. Get really creative with it and only respond with the one word. Keep changing the theme so that the same theme does not appear too many times in a row.")
				say()

				# press enter to speak, let player i say the word & record down
				record("Press enter if the clue giver is ready to say the word")
				responseH += "\n" + "Press enter if the clue giver is ready to say the word"
				say()
				input("Press enter if the clue giver is ready to say the word")
				record(speak(1, names[i])) 
				
				# press enter to speak, let guesser guess & record
				record("Press enter if the guesser is ready to take a guess")
				responseH += "\n" + "Press enter if the guesser is ready to take a guess"
				say()
				input("Press enter if the guesser is ready to take a guess")
				record(speak(1, names[guesser]))

		chatGPT("All clue givers have now gone besides you. Now come up with another category to give yourself. Then come up with a clue for that category. Try and help the guesser get closer to the correct number. So if the guesser's most recent prediction is a number that is far below the correct number, give it an item that is higher than the true number so hopefully their prediction get closer to the real number. And the opposite is true. Now, provide your response without giving an explanation of why you chose that word. Provide your response by saying: 'My category is' the category 'and my clue is' the clue")	
		say()

		record("Press enter if the Guesser is ready to give the final guess!")
		responseH += "\n" +"Press enter if the Guesser is ready to give the final guess!"
		say()
		input("Press enter if the Guesser is ready to give the final guess!")
		record(speak(1, names[guesser])) 

		chatGPT("Look at the guesser's most recent answer which is their final guess, and tell them if they are correct by looking at the correct number. Make sure you tell them what the correct number was if they got it wrong.")
		say()

		with open("C:\\venvProjects\\projectIshani\\flask-server\\X.txt", "w") as f:
			f.write(" ")

		start = input("Start a new game? (y/n): ")
		savePlayers = input("Are the players the same? (y/n): ")
	else: 
		break
