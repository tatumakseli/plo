from treys import Card, Evaluator
import itertools
import numpy as np

class Hand:

	def __init__(self, range1, range2, flop):
		self.flop = flop
		self.range1 = range1
		self.range2 = range2
		self.range_comb = [(x,y) for x in self.range1 for y in self.range2]
		self.range1pc = []
		self.range2pc = []
		self.tie = []
		for key in self.range_comb:
			result = Hand.hand_vs_hand(self, key[0], key[1], flop)
			if result is not None:
				self.range1pc.append(result[0])
				self.range2pc.append(result[1])
				self.tie.append(result[2])
			else:
				print(key[0], key[1])
		self.range1_win = np.mean(self.range1pc)
		self.range2_win = np.mean(self.range2pc)
		self.tie_win = np.mean(self.tie)
		print(self.range1_win, self.range2_win, self.tie_win)

	def hand_vs_hand(self, hand1, hand2, flop):
		self.hand1 = hand1
		self.hand2 = hand2
		if not [x for x in self.hand1 if x in self.hand2] and not [x for x in self.flop if x in self.hand1 or x in self.hand2]:
				self.allcards = Hand.allCards(self)
				self.cardsLeft = [elem for elem in self.allcards if elem not in self.hand1 and elem not in self.hand2 and elem not in self.flop]
				#print(self.cardsLeft)
				Hand.twoCardHandsFunc(self)
				Hand.turnAndRiver(self)
				return Hand.calc(self)
		else:
			return None

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
		tie_pc = sum(tie)/total
		hand1_pc = sum(hand1_win)/total
		hand2_pc = sum(hand2_win)/total
		return hand1_pc, hand2_pc, tie_pc



r1 = [["Ad", "Jc", "Td", "9c"], ["Ad", "Kd", "Qc", "Jc"]]
r2 = [["As", "Kh", "Th", "Qs"], ["9d", "8d", "7c", "6c"], ["Ad", "Ah", "Ks", "Kh"]]
flop = ["2c", "2s", "5d"]
test = Hand(r1, r2, flop)

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




###HAND VS HAND


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