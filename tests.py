from bushings import *

def weight_to_duro_test():
	assert weight_to_duro(75) == "90a"
	assert weight_to_duro(75, boardside=False) == "87a"
	assert weight_to_duro(20) == "78a"
	assert weight_to_duro(300) == "97a"

def bushing_pair_test():
	a = BushingPair(87, "TestPair")
	assert a.boardside == "93a"
	assert a.roadside == "90a"
	assert a.label == "TestPair"

def bushing_pair_comp_test():
	a = BushingPair(87, "PairA")
	b = BushingPair(88, "PairB")
	c = BushingPair(70, "PairC")

	assert a.compare_pairs(b) == True
	assert a.compare_pairs(c) == False
