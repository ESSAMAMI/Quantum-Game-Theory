import random
import signal
import sys
from termcolor import colored

firstRound = True # set this to true, will change it back to false after run

global p1Score, p2Score, roundnumber
p1Score, p2Score, roundnumber = 0,0,1

global grudgerIsContent
grudgerIsContent = True

global lastplayerWakeUp
lastplayerWakeUp = None

global lastp2wakeUp
lastp2wakeUp = None

global playerActionList
playerActionList = []

#each function outputs Wake Up as True and not Wake Up as False
def allWakeUp():
	return True

def allNotWakeUp():
	return False

def rand():
	#returns a random boolean (t/f)
	return bool(random.getrandbits(1))

def player():
	#interperets player input
	while True:
		playerChoice = str(input(colored("\n\tWake Up? (Y/N or (Q to quit)): ","blue")))
		if playerChoice.lower() == "q":
			print('See u later ;)')
			sys.exit()
		if playerChoice.lower() == "pvp":
			playermap["p2"] = player
			continue
		if playerChoice.lower() == "y" or playerChoice.lower() == "yes":
			return True
		if playerChoice.lower() == "n" or playerChoice.lower() == "no":
			return False
		else:
			print(colored("\tNot a valid answer. Try agin!\n","red"))
			continue

def grudger():
	#uses variable grudgerIsContent
	if grudgerIsContent:
		return True
	else:
		return False

def tft():
	#uses variable lastplayerWakeUp
	if firstRound:
		return True
	else:
		return playerActionList[-1]


def oppositetft():
	if firstRound:
		return False
	else:
		return not playerActionList[-1]


def signal_handler(sig, frame):
    print(colored('\n\tYou pressed Ctrl+C ! Au revoir.😁',"yellow"))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Full list of strategies (input them like this)
# "p1": tft,
# "p2": player
# replace tft and player with the strategies you want to use

# grudger - always Wake Up until the other player does not Wake Up, after that it will never Wake Up again
# rand - random, like a coin toss.
# player - allows the user to input moves as Y or N
# tft - Wake Up on the first round, then follows the other player's last move.
# allWakeUp - always Wake Up.
# allNotWakeUp - never Wake Up.
# oppositetft - Does not Wake Up on the first round, then does the opposite of the other player's last move.

strats = [grudger, rand, player, tft, allWakeUp, allNotWakeUp, oppositetft]

#change the functions used to change behavior of player1 and player2

playermap = {
	"p1": player,
	"p2": random.choice(strats)
}

while playermap["p2"] == player:
	playermap["p2"] = random.choice(strats)

while roundnumber <= 4:
	p1wakeUp = playermap["p1"]() #find the function name of p1 in playermap, call it
	p2wakeUp = playermap["p2"]() #find the function name of p1 in playermap, call it

	#CALCULATE SCORES
	if p1wakeUp and p2wakeUp:
		p1Score += 2
		p2Score += 2
	elif p1wakeUp and not p2wakeUp:
		p1Score += 0 #just for show
		p2Score += 4
		if playermap["p1"] == grudger:
			grudgerIsContent = False
	elif not p1wakeUp and p2wakeUp:
		p1Score += 4
		p2Score += 0 #just for show
		if playermap["p2"] == grudger:
			grudgerIsContent = False
	elif not p1wakeUp and not p2wakeUp:
		p1Score += 3
		p2Score += 3

	#Print Wake Up/not Wake Up for each player
	print("")
	print(colored("\t(p1) WakeUp: " + str(p1wakeUp),"grey"))
	print(colored("\t(p2) WakeUp: " + str(p2wakeUp) + "\n","grey"))

	print(colored("\t(p1) Reward(s): " + str(p1Score), "green"))
	print(colored("\t(p2) Reward(s): " + str(p2Score) + "\n","green"))

	roundnumber += 1 #next round
	firstRound = False #first round over, used for strategies like tft, oppositetft, and grudger

	playerActionList.append(p1wakeUp) #add the player's moves to the list

#Determine the winner
if p1Score > p2Score:
	print("\t(p1) won by " + str(p1Score - p2Score) + " points.")
elif p1Score == p2Score:
	print("\t(p1) tied with " + playermap["p2"].__name__ + " (p2)")
else:
	print("\t(p2) won by " + str(p2Score - p1Score) + " points.")

#Tell them who they played against, wont really matter if computer player was chosen
print("\tYou played against " + str(playermap["p2"].__name__) + ".")
