#!usr/bin/env python3
import json
import sys
import os
import math

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # Initialize scores to some constant (Subtracting = more similar, Adding = less similar)
    user1_score = 70
    user2_score = 70

    # If user1 likes user2's gender, we'll say they're more similar by subtracting
    if user2.gender in user1.preferences:
        user1_score -= 5
    else:
        user1_score += 60

    if user1.gender in user2.preferences:
        user2_score -= 5
    else:
        user2_score += 60

    # Calculate the difference between their grad years
    grad_year_difference = abs(user1.grad_year - user2.grad_year)

    # The closer they are in grad year, the more compatible they will be
    if grad_year_difference >= 3:
        user1_score += 10
        user2_score += 10
    elif grad_year_difference == 2:
        user1_score -= 3
        user2_score -= 3
    elif grad_year_difference == 3:
        user1_score -= 10
        user2_score -= 10
    else:
        user1_score -= 14
        user2_score -= 14

    for i in range(len(user1.responses)):
        user1_response = user1.responses[i]
        user2_response = user2.responses[i]

        if user1_response == user2_response:
            # Calculate the percentage of users who chose the same response for this question
            same_response_percentage = sum(
                1 for user in users if user.responses[i] == user1_response
                ) / len(users)

            # For every answer that matched, subtract a weight that is based on the percentage of people who answered the same way
            weight = 1 / same_response_percentage
            user1_score -= weight
            user2_score -= weight

    # If the scores become negative, set them to 0.
    if user1_score < 0:
        user1_score = 0

    if user2_score < 0:
        user2_score = 0

    # Assume user1_score and user2_score are perpendicular vectors, and find vector sum
    weighted_sum = math.sqrt(user1_score**2 + user2_score**2)

    # Max score (polar opposites) will be 70 + 60 + 10 = 140.
    # If both players get 135, their vector sum will be 140 * math.sqrt(2).
    # Our final score should be a value between 1 and 0, 1 meaning most similar.
    # weighted_sum should always be < or = the max score

    final_score = 1 - (weighted_sum) / (140 * math.sqrt(2))

    return final_score

if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))