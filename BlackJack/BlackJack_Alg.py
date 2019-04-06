
import random as rnd

from bib_support import get_card_val


def blackjack_alg_50X50() -> bool:

	if rnd.randint(0, 1) == 0:
		ret = False
	else:
		ret = True


	return ret



def blackjack_alg_WIKIPEDIA_BLACKJACK(caller: object) -> bool:

	# https://en.wikipedia.org/wiki/Blackjack#Basic_strategy

	num_of_aces = len( [ x[0] for x in caller.cards if x[0] == "A" ] )

	card_sum = caller.get_card_sum() 

	known_table_card_value = get_card_val(caller.known_table_cards[0])

	ret = None

	found_pair_match = False
	found_total_match = False

	# check if we have a pair in the first hand, in the begining of the game
	if len(caller.cards) == 2:

		pairs = []
		pairs.append( ["A", len( [ x[0] for x in caller.cards if x[0] == "A" ] )] )
		pairs.append( ["J", len( [ x[0] for x in caller.cards if x[0] == "J" ] )] )
		pairs.append( ["Q", len( [ x[0] for x in caller.cards if x[0] == "Q" ] )] )
		pairs.append( ["K", len( [ x[0] for x in caller.cards if x[0] == "K" ] )] )

		for k in range(2, 11):
			pairs.append( [str(k), len( [ x[0] for x in caller.cards if x[0] == str(k)] )] )



		for pair in pairs:

			if pair[1] >= 2:



				if pair[0] == "2" or pair[0] == "3":
					if known_table_card_value in {1, 8, 9, 10}:
						ret = True
						found_pair_match = True

				if pair[0] == "4":
					if known_table_card_value in {1, 2, 3, 4, 7, 8, 9, 10}:
						ret = True
						found_pair_match = True

				if pair[0] == "5":
					ret = True
					found_pair_match = True

				if pair[0] == "6":
					if known_table_card_value in {1, 7, 8, 9, 10}:
						ret = True
						found_pair_match = True

				if pair[0] == "7":
					if known_table_card_value in {1, 8, 9, 10}:
						ret = True
						found_pair_match = True

				if pair[0] == "9":
					if known_table_card_value in {1, 7, 10}:
						ret = False
						found_pair_match = True

				if pair[0] == "10":
					ret = False
					found_pair_match = True


	# didnt find pairs. So try for a hard or soft hand
	if found_pair_match == False:

		if num_of_aces == 0:

			# HARD HAND (excluding pairs):
			if card_sum <= 11:
				ret = True
				found_total_match = True

			elif card_sum == 12:
				if known_table_card_value >= 4 and known_table_card_value <= 6:
					ret = False
				else:
					ret = True

				found_total_match = True

			elif card_sum >= 13 and card_sum <= 16:
				if known_table_card_value >= 2 and known_table_card_value <= 6:
					ret = False
				else:
					ret = True

				found_total_match = True

			elif card_sum >= 17 and card_sum <= 21:
				ret = False
				found_total_match = True



		else:
			# SOFT HAND (excluding pairs):


			if card_sum >= 13 and card_sum <= 17:
				ret = True
				found_total_match = True

			elif card_sum == 18:
				if known_table_card_value in {1, 9, 10}:
					ret = True
				else:
					ret = False

				found_total_match = True

			elif card_sum >= 19:
				ret = False
				found_total_match = True


			#  bellow seams to improve player win i dont know why
			# ret = False
			# found_total_match = True


	# fall here only if didnt match any other rule above
	if found_pair_match == False and found_total_match == False:
		if card_sum <= 15:
			ret = True
		else:
			ret = False

	return ret





def blackjack_alg_MURCH(caller: object) -> bool:

	# from my guts


	card_sum = caller.get_card_sum()

	known_table_card_value = get_card_val(caller.known_table_cards[0])

	ret = None

	if card_sum <= 13:
		ret = True
	elif card_sum > 13 and card_sum <= 17:
		if known_table_card_value == 1:
			ret = True
		else:
			if card_sum <= 16:
				ret = True
			else:
				ret = False
	else:

		ret = False

	return ret


def blackjack_alg_SIMPLE() -> bool:

	# from my guts2


	card_sum = caller.get_card_sum()


	ret = None

	if card_sum <= 17:
		ret = True

	else:

		ret = False

	return ret




