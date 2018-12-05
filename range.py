from treys import Card, Evaluator
import itertools
import numpy as np

class Hand:
	def __init__(self, hand1, hand2, flop):
		self.hand1 = hand1
		self.hand2 = hand2
		self.flop = flop
		self.allcards = Hand.allCards(self)
		self.cardsLeft = [elem for elem in self.allcards if elem not in self.hand1 and elem not in self.hand2 and elem not in self.flop]
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
		self.hand1_comb = list(itertools.combinations(self.hand1, 2))
		self.hand2_comb = list(itertools.combinations(self.hand2, 2))
		
	def turnAndRiver(self):
		self.turnAndRiverCombos = list(itertools.combinations(self.cardsLeft, 2))

	def calc(self):
		hand1_win = []
		hand2_win = []
		tie = []
		evaluator = Evaluator()
		for x in self.turnAndRiverCombos:
			board = [Card.new(self.flop[0]), Card.new(self.flop[1]), Card.new(self.flop[2]), Card.new(x[0]), Card.new(x[1])]
			hand1_best = None
			for key in self.hand1_comb:
				hand1 = [Card.new(key[0]), Card.new(key[1])]
				score = evaluator.evaluate(board, hand1)
				if hand1_best is None or score < hand1_best:
					hand1_best = score
			hand2_best = None
			for key in self.hand2_comb:
				hand2 = [Card.new(key[0]), Card.new(key[1])]
				score = evaluator.evaluate(board, hand2)
				if hand2_best is None or score < hand2_best:
					hand2_best = score
			if hand1_best == hand2_best:
				tie.append(1)
			elif hand1_best > hand2_best:
				hand2_win.append(1)
			elif hand1_best < hand2_best:
				hand1_win.append(1)
		total = sum(hand1_win)+sum(hand2_win)+sum(tie)
		print("TIE", sum(tie)/total)
		print("HAND1WIN", sum(hand1_win)/total)
		print("HAND2WIN", sum(hand2_win)/total)


h1 = ["Ad", "Ac", "Td", "9c"]
h2 = ["Ks", "Kh", "Th", "Qs"]
flop = ["2c", "2s", "5d"]
test = Hand(h1, h2, flop)

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