from treys import Card, Evaluator
import itertools

class Hand:
	def __init__(self, hand, flop):
		self.hand = hand
		self.flop = flop
		self.allcards = Hand.allCards(self)
		self.cardsLeft = [elem for elem in self.allcards if elem not in self.hand and elem not in self.flop]
		#print(self.cardsLeft)
		Hand.twoCardHandsFunc(self)
		Hand.turnAndRiver(self)
		Hand.calc(self)

	def allCards(self):
		faces = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
		suits = ["s", "c", "d", "h"]
		allcards = []
		for key in faces:
			for x in suits:
				hand = key+x
				allcards.append(hand)
		return allcards

	def twoCardHandsFunc(self):
		self.twoCardHands = list(itertools.combinations(self.hand, 2))
		
	def turnAndRiver(self):
		self.turnAndRiverCombos = list(itertools.combinations(self.cardsLeft, 2))
		print(len(self.turnAndRiverCombos))

	def calc(self):
		evaluator = Evaluator()
		# board = [Card.new(self.flop[0]), Card.new(self.flop[1]), Card.new(self.flop[2])]
		for x in self.turnAndRiverCombos:
			board = [Card.new(self.flop[0]), Card.new(self.flop[1]), Card.new(self.flop[2]), Card.new(x[0]), Card.new(x[1])]
			for key in self.twoCardHands:
				hand = [Card.new(key[0]), Card.new(key[1])]
				print(evaluator.evaluate(board, hand))


test = Hand(["9d", "8d", "7c", "6c"], ["As", "Kc", "Jh"])

"""
board = [
    Card.new('Ah'),
    Card.new('Kd'),
    Card.new('Jc')
]
hand = [
    Card.new('Ts'),
    Card.new('Th')
]

Card.print_pretty_cards(board + hand)

evaluator = Evaluator()
score = evaluator.evaluate(board, hand)
classi = evaluator.get_rank_class(score)

print(score, evaluator.class_to_string(classi))


"""