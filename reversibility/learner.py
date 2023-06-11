import sys, os
import random
import numpy as np
from itertools import count, chain
import copy 

"""
This is currently "pseudocode" for the idea.

To experiment:
1. Clone pycolab in the same directory of this file.
2. `cd pycolab`
3. `pip install -e .`
4. Open IPython in a folder that contains this file and the pycolab repo
5. `%run learner.py%
6. Interact with the history in `game_histories`
"""

from pycolab.examples import warehouse_manager


def gen_history():
    game_histories = []

    n_episodes = 1
    max_game_steps = 100

    # Randomly generate history:
    for _ in range(n_episodes):
        episode = []
        game = warehouse_manager.make_game(0)
        obs, r, discount = game.its_showtime()

        for _ in range(max_game_steps):
            a = random.randint(0, 3)
            pos = game.things['P'].position
            episode.append([obs.board, pos, a])
            obs, r, discount = game.play(a)
            if game.game_over:
                pos = game.things['P'].position
                episode.append([obs.board, pos, None])
                break

        game_histories.append(episode)

    return game_histories


# Now we have some history, time to learn from it!

def gen_conditions():
    # We need to distribute complexity (= distance)
    # Each condition is a position and an object
    max_distance = 2
    max_time = 0
    objs = 11

    n_rel_positions = max_distance*2 + 1

    zipped = zip(range(max_distance + 1), range(0, -max_distance - 1, -1))
    cols = [0] + [x for xx in zipped for x in xx]
    rows = cols

    # loop through conditions in order of complexity:
    for time in range(max_time+1):
        for n in range(n_rel_positions*2):
            gen = distribute(n, 2, n_rel_positions)
            for i, j in gen:
                for obj in range(objs):
                    yield [-time, cols[i], rows[i], obj]


def init_rule(preconditions, action, postcondition):
    def rule(s0, s, pos, a):
        if a != action:
            return None
        states = [s0, s]
        for t, row, col, obj in preconditions:
            if states[t][row, col] != obj:
                return None
        return postcondition
    return rule

def distribute(n, bins, n_max):
    """
    Distributes the integer `n` into `bins` number of terms that sum to n.

    # Args:
        n: integer, the number to distribute
        bins: integer, the number of terms distriubte into
        n_max: the maximum value of any bin
    """
    if bins == 0:
        return []

    if bins == 1:
        return [[min(n, n_max)]]

    def gen():
        i0 = max(0, n - n_max*(bins-1))
        i1 = min(n+1, n_max+1)
        for i in range(i0, max(i0, i1)):
            for x in distribute(n - i, bins - 1, n_max):
                yield x + [i]
    return gen()


def init_rule_gen():
    """
    A rule is a (set of) conditions on the current state, and an action, and the condition on the state that this action would result in. 
    
    We define complexity of a rule as the number of conditions times the spatial distance between in the conditions.
    
    This function returns an iterator of the next 'least complex' set of possible rules.
    """
    preconditions = list(gen_conditions())
    postconditions = list(gen_conditions())

    
    for n_preconditions in count(1):
        # General forumula for maximal complexity (we just have n_preconditions = 1 for now)
        max_complexity = n_preconditions*len(preconditions) + len(postconditions)

        for i in range(max_complexity):
            for j in range(min(i, len(postconditions))):
                # We just need one postcondition per rule
                postcondition = postconditions[j]
                remaining = max_complexity - j
                for precondition_config in distribute(remaining, n_preconditions, len(preconditions)):
                    precondition = [preconditions[i] for i in precondition_config]
                    for action in range(4):
                        yield init_rule(precondition, action, postcondition)

def find_simplest_explanations(game_histories):
    rules_gen = init_rule_gen()
    failed = True
    while failed:
        failed = False
        rules = next(rules_gen)
        episode = game_histories[0]
        s0 = episode[0][0]
        for i in range(len(episode) - 1):
            s, pos, a = episode[i]
            sp = episode[i + 1][0]

            predicted_changes = set()
            for rule in rules:
                postcondition = rule(s0, s, pos, a)
                row, col, obj = postcondition
                if sp[row, col] != postcondition:
                    failed = True
                    break
                else:
                    predicted_changes.add((row, col))

            diff = s != sp
            changes = np.where(diff)
            changes = set(zip(*changes)) 
            # Check if we predicted all changes:
            if len(changes - predicted_changes) > 0:
                failed = True
                break
                
        return rules

def main():
    history = gen_history()

    # The whole algorithm, loops indefinitely
    if input('Try to find rules that explain? (y/n)') == 'y':
        found_rules = find_simplest_explanations(history)
    
if __name__ == '__main__':
    main()
