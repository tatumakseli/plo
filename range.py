class Hand:
	def __init__(self, hand, flop):
		self.hand = hand
		self.flop = flop
		self.allcards = Hand.allCards(self)
		self.cardsLeft = [elem for elem in self.allcards if elem not in self.hand]
		print(self.cardsLeft)

	def allCards(self):
		faces = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
		suits = ["s", "c", "d", "h"]
		allcards = []
		for key in faces:
			for x in suits:
				hand = key+x
				allcards.append(hand)
		return allcards


test = Hand(["9d", "8d", "7c", "6c"], ["As", "Kc", "Jh"])

