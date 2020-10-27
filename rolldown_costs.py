import random as r
import matplotlib.pyplot as plt
import numpy as np

def rolldown(start_value = 50, end_value = 0, initial_win_prob=3.0/7, end_win_prob=3.0/7, streak = -1, debug=False, is_streaking=True):
    #Determines the opportunity cost of a rolldown.

    #state variables
    base = 5
    current_money = end_value
    old_money     = start_value
    spent_money   = start_value-end_value

    current_streak = streak
    old_streak     = streak

    current_match_result = 0
    old_match_result     = 0

    
    #helper objects
    def update_streaks(current_match, old_match, current_streak, old_streak):
        #update new_streak 
        if current_match > 0 and current_streak > 0:
            current_streak += 1
        elif current_match == 0 and current_streak < 0:
            current_streak -= 1
        else:
            current_streak = int((current_match-0.5)/0.5)

        #update old_streak
        if old_match > 0 and old_streak > 0:
            old_streak += 1
        elif current_match == 0 and old_streak < 0:
            old_streak -= 1
        else:
            old_streak = (old_match-0.5)/0.5

        #return tuple
        return (current_streak, old_streak)

    def streak_income(streak):
        streak = abs(streak)

        if streak <= 1:
            return 0
        elif streak <= 3:
            return 1
        elif streak <= 4:
            return 2
        else:
            return 3

    #main code
    while(current_money < 50):

        #results of match
        opponent_str = r.random()
        current_match_result = opponent_str < end_win_prob
        old_match_result = opponent_str < initial_win_prob

        #calculating streak values.
        current_streak, old_streak = update_streaks(current_match_result, old_match_result, current_streak, old_streak)

        #updating bank
        current_money += base + min(current_money//10,5) + current_match_result + streak_income(current_streak)
        old_money     += base + min(old_money//10,5)     + old_match_result     + streak_income(old_streak)
        
        if debug:
            print("Next round: " + str(current_money))

    return (old_money-spent_money)-current_money


def sample_rolldown(start_value=50, end_value=0, initial_win_prob = 3.0/7, end_win_prob = 4.0/7, streak = -1, size=1000):
    #rolls down size number of times, returns a list of results.
    
    return [rolldown(start_value, end_value, initial_win_prob, end_win_prob, streak, False) for x in range(0,size)]


def dev(lst):
    avg = sum(lst)/len(lst)
    return ((1.0/(len(lst)-1)) * sum([(x-avg)**2 for x in lst]))**(0.5)


def rolldown_from_50(iwin, ewin, streak=-1):
    #Rolls down from 50 to every x between 0 and 49 (inclusive)
    #returns a list of the values, starting from the top (49)
    #each element of the list is of the form:
    #   (average, min, max, deviation)

    lst = []
    for x in range(49,-1, -1):
        result = sample_rolldown(50,x,iwin,ewin, streak)
        avg = sum(result) / 1000
        minimum = min(result)
        maximum = max(result)
        deviation = dev(result)
        lst.append((avg,minimum,maximum,deviation))
    return lst



