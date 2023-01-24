'''
Blackjack Project by Muhammad Musa
For class CIS 115
'''

import random as ra
import time

#This is a bool to determine if anyone has won the game yet
hasWinner = False

#Now we create the hands as lists
botHand = []
userHand = []

#Creates the sum variables for later
botSum = 0
userSum = 0

#Lest we forget to ask the user their name
user = input("Please input your name: ")

#Now we should create the win/loss/tie counters within this wonderful class with functions to add them
class Counter():
	def __init__(self):
		self.userWins = 0
		self.botWins = 0
		self.gameTies = 0
		self.totalGames = 0
		self.winRate = 0

	def addUWin(self):
		self.userWins += 1

	def addBWin(self):
		self.botWins += 1

	def tieGame(self):
		self.gameTies += 1

	def setTotalGames(self):
		self.totalGames = self.userWins + self.botWins + self.gameTies

	def setWinRate(self):
		if self.totalGames > 0:
			self.winRate = (self.userWins * 100)//self.totalGames

#Now to create a class for our drawing ability
#Dictionary is setup as CARD: [VALUE, COUNTER]
class Draw:
	def __init__(self):
		self.card = None

		self.deck = {
			'Empty':[0,0],
			'Ace':[1,4],
			'One':[1,4],
			'Two':[2,4],
			'Three':[3,4],
			'Four':[4,4],
			'Five':[5,4],
			'Six':[6,4],
			'Seven':[7,4],
			'Eight':[8,4],
			'Nine':[9,4],
			'Ten':[10,4],
			'Jack':[10,4],
			'Queen':[10,4],
			'King':[10,4],
		}

	#Now within this class we need to create some functions for actually drawing and assigning cards
	#This draws a card from the list, checks the counter and then if its out of cards it draws again, otherwise it lowers the counter by one
	def getCard(self):
		self.card = ra.choice(list(self.deck))
		if self.deck[self.card][1] <= 0:
			self.getCard()
		else:
			cardValue = self.deck[self.card][0]
			cardCounter = self.deck[self.card][1]
			self.deck[self.card] = [cardValue, cardCounter - 1]

	#Assigns the card to the user
	def assignUser(self):
		userHand.append(self.card)
		if self.card == 'Ace':
			print(f"Dealer draws an {self.card} for {user}.")
		elif self.card == "Eight":
			print(f"Dealer draws an {self.card} for {user}.")
		else:
			print(f"Dealer draws a {self.card} for {user}.")

	#Assigns the card to the bot
	def assignBot(self):
		botHand.append(self.card)
		print(f"Dealer draws a card for their own hand.")

	#Initial draw of two cards each
	def fullDraw(self):
		self.getCard()
		self.assignUser()
		time.sleep(0.5)
		self.getCard()
		self.assignBot()
		time.sleep(0.5)
		self.getCard()
		self.assignUser()
		time.sleep(0.5)
		self.getCard()
		self.assignBot()

	#Single draw for user
	def userDraw(self):
		self.getCard()
		self.assignUser()
	
	#Single draw for bot
	def botDraw(self):
		self.getCard()
		self.assignBot()

	def clearHands(self):
		global botHand, userHand, botSum, userSum
		botSum = 0
		userSum = 0
		botHand = []
		userHand = []

#Assigning 'd' to access the Draw class and 'c' to access the Counter class
d = Draw()
c = Counter()

#This creates the sums of the hands
def newSum():
	global botSum, userSum, botHand, userHand
	botSum = 0
	userSum = 0
	for botCard in botHand:
		botValue = d.deck[botCard][0]
		botSum += botValue

	for userCard in userHand:
		userValue = d.deck[userCard][0]
		userSum += userValue
	return botSum, userSum

#Checks if the bot has 21 to win, over 21 to bust, or under 15 to hit
def botCheck():
	global hasWinner
	if botSum == 21:
		print(f"Dealer has 21, dealer wins!\nFull hand: {botHand}")
		c.addBWin()
		hasWinner = True
		playAgain()
	elif botSum > 21:
		print(f"Dealer has {botSum}, dealer busts!\nFull hand: {botHand}")
		c.addUWin()
		hasWinner = True
		playAgain()
	elif botSum < 15:
		print(f"Full dealer hand: {botHand}")
		print(f"Dealer hits")
		d.botDraw()
		newSum()

#does the same as botCheck but for the user, allows the user to hit or stand
def userCheck():
	print(f"Dealer's hand: [X, {botHand[1]}]")
	print(f"{user}'s hand: {userHand} with a sum of {userSum}")
	global hasWinner
	if userSum == 21:
		print(f"{user} has 21, {user} wins!")
		c.addUWin()
		hasWinner = True
		playAgain()
	elif userSum > 21:
		print(f"{user} has {userSum}, {user} busts!")
		c.addBWin()
		hasWinner = True
		playAgain()
	choice = input("Would you like to [h]it, or [s]tand? ")
	if choice == 'h':
		d.userDraw()
		newSum()
		userCheck()
	elif choice == 's':
		compareHands()
	else:
		print(f"{choice} is not a valid choice, please try again.")
		userCheck()

#This compares the two hands after revealing the dealer's full hand
def compareHands():
	global hasWinner
	print(f"Dealer's hand is {botHand} with a sum of {botSum}.")
	if botSum > userSum:
		print(f"Dealer wins with a {botSum}.")
		c.addBWin()
		hasWinner = True
	elif userSum > botSum:
		print(f"{user} wins with a {userSum}.")
		c.addUWin()
		hasWinner = True
	elif userSum == botSum:
		print(f"Tied Game!")
		hasWinner = True
		c.tieGame()

#Main function of course
def main():
	#Starts by clearing everything
	d.clearHands()
	#Then it fills it back in
	d.fullDraw()
	#Starts the actual process
	newSum()
	userCheck()
	#If there isn't a winner after the userCheck it runs the botCheck
	if hasWinner == False:
		print(f"Dealer's hand was {botHand} for a total of {botSum}.")
		botCheck()
		playAgain()
	else:
		playAgain()

#Gives the user the choice of playing again or not, shows off all the stats for winrates from the Counters when exiting
def playAgain():
	c.setTotalGames()
	c.setWinRate()
	choice = input("Would you like to play again? (y for yes, n for no) ")
	if choice == "y":
		main()
	elif choice == "n":
		print(f"Thank you for playing, {user}.")
		print(f"You won {c.winRate}% of games!")
		print(f"You won {c.userWins} time(s), lost {c.botWins} time(s) and, tied {c.gameTies} time(s) of the {c.totalGames} played.")
		exit()
	else:
		print(f"I'm sorry, {user}, but '{choice}' is not valid. Please try again.")
		playAgain()

#Boilerplate :)
if __name__ == "__main__":
	main()