import numpy as np
from typing import List, Tuple
import random


def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    # Number of people to be matched
    N = len(scores)

    # Checking for incompatible gender identity/preferences combinations
    for i in range(N):
        for j in range(N):
            if gender_pref[i] != "Bisexual":
                # Unless they are bisexual, make sure i is not matching with someone of the same gender or someone non-binary
                if (gender_id[i] == gender_id[j]) or (gender_id[j] == "Nonbinary"):
                    scores[i][j] = 0  # Set scores to 0 for incompatible match

    half_N = N // 2  # Finds half of N (distinction between proposers and receivers)

    # Decide 1st half to be proposers, 2nd half to be receivers
    proposer_indices = list(range(half_N))
    receiver_indices = list(range(half_N, N))

    # Assign preferences for proposers and receivers
    proposer_prefs = [
        sorted(receiver_indices, key=lambda x: scores[i][x], reverse=True)
        for i in proposer_indices
    ]
    receiver_prefs = [
        sorted(proposer_indices, key=lambda x: scores[i][x], reverse=True)
        for i in receiver_indices
    ]

    matches = {}  # Stores matched pairs
    receiver_dict = {
        receiver_number: i for i, receiver_number in enumerate(receiver_indices)
    }  # Used later for assigning 5 as index of 0, 6 as index of 1, and so on

    # Empty sets and lists to keep track of proposers and receivers
    matched_proposers = set()
    matched_receivers = set()
    free_proposers = list(range(half_N))

    while len(free_proposers) > 0:
        for p in free_proposers:
            for r in proposer_prefs[p]:
                receiver_index = receiver_dict[r]
                # If receiver is not currently matched, match p and r.
                if r not in matched_receivers:
                    matches[p] = r
                    matched_proposers.add(p)
                    matched_receivers.add(r)
                    break
                # p attempts to propose to r
                else:
                    new_p = p
                    current_p = None

                    # Finds the p that r is currently in a relationship with
                    for key, val in matches.items():
                        if val == r:
                            current_p = key
                            break

                    # If r does not prefer new_p to their current partner
                    if receiver_prefs[receiver_index].index(new_p) < receiver_prefs[
                        receiver_index
                    ].index(current_p):
                        # Reject proposal
                        continue
                    # If r prefers new_p to their current partner, match new_p and r
                    else:
                        matches[new_p] = r
                        del matches[current_p]
                        matched_proposers.remove(current_p)
                        matched_receivers.remove(r)
                        matched_proposers.add(new_p)
                        matched_receivers.add(r)
                        break

        free_proposers = [
            p for p in free_proposers if p not in matched_proposers
        ]  # Finds out how many proposers are left

    matches = [(key, val) for key, val in matches.items()]
    return matches


if __name__ == "__main__":
    raw_scores = np.loadtxt("raw_scores.txt").tolist()
    genders = []
    with open("genders.txt", "r") as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open("gender_preferences.txt", "r") as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
