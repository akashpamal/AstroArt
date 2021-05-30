from runner import Simulator
import sys
import random
import time
import pickle
import multiprocessing
import os
import io
from PIL import Image
import ssl
import random
import math
import sys

from kmeansIdentifier import kMeans_quantization


# NUM_PLANETS = 27
# WINDOW_SIZE = (1440, 800)
# # FILENAME = str(sys.argv[1])
# FILENAME = "./input_images/DABABY CAR LESSS GOOOOOO.jpeg"
# REFERENCE_IMAGE, COLORS = kMeans_quantization(Image.open(FILENAME),  NUM_PLANETS / 3)
# REFERENCE_PIXELS = REFERENCE_IMAGE.load()
# REFERENCE_IMAGE.show()



NUM_PLANETS = 3
WINDOW_SIZE = (1440, 800)
# FILENAME = str(sys.argv[1])
FILENAME = "./input_images/DABABY CAR LESSS GOOOOOO.jpeg"
GOAL_IMAGE = Image.open(FILENAME)
COLORS = (255, 0, 0), (0, 255, 0), (0, 0, 255)
REFERENCE_PIXELS = GOAL_IMAGE.load()
GOAL_IMAGE.show()

# Pick a number of planets - 27
# Image with dimesnions (1440, 800)
#--------
# KMeans on the picture to find the colors
# Start with random starting locations
# Population size of 100
# NUM_CLONES = 10
# breeding strategy - average of the two positions for that particle
# strategy - list of (x, y) positions, the order of the colors stays consistent in the strategy
# error function - difference in pixel value for every rgb in every pixel

def error(orbit_image, goal_image):
    orbit_image = Image.open(orbit_image)
    pixels = orbit_image.load()
    total_error = 0
    for x in range(WINDOW_SIZE[0]):
        for y in range(WINDOW_SIZE[1]):
            total_error += sum((goal_image[x, y][color]-pixels[x, y][color]) ** 2 for color in range(3))
    return total_error


def initialize_board(matrix):
    return board

def place_piece(board, piece, location, orientation_to_metadata, parity, num_holes):
    pass

def find_num_holes(board):
    pass
#     return largest_column_height_difference, standard_deviation_column_height_difference # TODO return average_col_height and use it in the heuristic

def get_parity(matrix): # TODO use matrix_heights here so you don't have to iterate through the entire board
    pass

def heuristic(board, strategy, num_lines_cleared, parity, num_holes): # add component to measure game_over
    pass

def play_game(strategy, orientation_to_metadata, orientation_to_pieces, all_orientations, display_output=False):
    pass

def generate_starting_population():
    global WINDOW_SIZE, POPULATION_SIZE
    # return [[random.random() - .5] for generation in range(POPULATION_SIZE)]

    starting_population = []
    for i in range(POPULATION_SIZE):
        current_generation = []
        for color in COLORS:
            current_generation.extend([(random.random() - .5, random.random() - .5, random.random() * WINDOW_SIZE[0], random.random() * WINDOW_SIZE[1], random.random() * 5, color) for elem in range(NUM_PLANETS)])
        starting_population.append(current_generation)
    return starting_population

def create_tournaments(generation):
    global POPULATION_SIZE
    global TOURNAMENT_SIZE
    both_tournaments = random.sample(generation, TOURNAMENT_SIZE * 2)
    tournament_1, tournament_2 = both_tournaments[ : TOURNAMENT_SIZE], both_tournaments[TOURNAMENT_SIZE : TOURNAMENT_SIZE * 2]
    tournament_1.sort(reverse=True)
    tournament_2.sort(reverse=True)
    for elem in tournament_1: # TODO delete this exception and all other exceptions
        if elem in tournament_2 or elem not in generation:
            raise Exception("Logic error in create_tournaments")
    return tournament_1, tournament_2

def breed_strategies(strategy_1, strategy_2): # length of each strategy is 27. Each element is an (x, y) tuple. Each strategy should have the same color planets in the same order
    global MUTATION_RATE
    global NUM_DIGITS_TO_ROUND
    global NUM_STRATEGY_ASPECTS
    global EXPONENT_MIN, EXPONENT_MAX
    strategy_1 = list(strategy_1) # TODO use one type of data structure everywhere or only convert between structures in one place
    strategy_2 = list(strategy_2)
    num_crossover_points = int(random.random() * (len(strategy_1) - 1))
    crossover_indices = random.sample([elem for elem in range(NUM_STRATEGY_ASPECTS)], num_crossover_points) # TODO prebuild some random crosssover_indices_lists and just choose them in this method. This will save the time of having to recreate these lists of indices for each call of this method
    child = strategy_2.copy()
    for index in crossover_indices:
        child[index] = strategy_1[index]
    if random.random() < MUTATION_RATE:
        mutate_index = int(random.random() * len(strategy_1))
        if mutate_index < NUM_STRATEGY_ASPECTS / 2:
            child[mutate_index] += round(random.random(), NUM_DIGITS_TO_ROUND)
        else:
            child[mutate_index] = round(random.uniform(EXPONENT_MIN, EXPONENT_MAX), NUM_DIGITS_TO_ROUND)
    child = tuple(child)
    return child

def create_strategy(generation):
    tournament_1, tournament_2 = create_tournaments(generation)
    for strat in tournament_1:
        if random.random() < WIN_PROBABILITY:
            strategy_1 = strat
            break
    for strat in tournament_2:
        if random.random() < WIN_PROBABILITY:
            strategy_2 = strat
            break
    child_strategy = breed_strategies(strategy_1[1], strategy_2[1])
    child_strategy = tuple([round(elem, NUM_DIGITS_TO_ROUND) for elem in child_strategy])
    return child_strategy

def genetic_algorithm_search():
    global orientation_to_metadata, orientation_to_pieces, all_orientations, NUM_CORES_TO_USE
    # if len(sys.argv)
    # do_next = input('(N)ew process, or (L)oad saved process? I can also LoadMax (LM) or LoadTest(LT). Please select your choice: ').upper()
    do_next = 'N'
    # do_next = 'N'
    while do_next != 'N' and do_next != 'L' and do_next != 'LT' and do_next != 'LM':
        do_next = input("Sorry, I didn't understand that. Would you like to: (N)ew process, or (L)oad saved process? ").upper()
    
    if do_next == 'N':
        generation = generate_starting_population()
        generation_count = 0

        start_time = time.perf_counter()
        temp_gen = []

        simulator_object = Simulator(generation, WINDOW_SIZE)
        orbit_image_list = simulator_object.evaluate_generation()
        if len(orbit_image_list) != len(generation):
            raise Exception("orbit image list and generation have different lengths")
        for index, strategy in enumerate(generation):
            orbit_image = orbit_image_list[index]
            # fitness, strategy = fitness_function(strategy, index + 1)
            fitness = 1 / error(orbit_image, GOAL_IMAGE)
            temp_gen.append((fitness, strategy))
        generation = temp_gen
        generation.sort(reverse=True)
        print('Average:', sum([elem[0] for elem in generation]) / len(generation))
        print('Generation:', generation_count)
        print('Best strategy so far:', max(generation))
        total_time_taken = time.perf_counter() - start_time
        print('Time taken for this generation ', generation_count, ': ', total_time_taken, ' seconds', sep='')
    elif do_next == 'L':
        filename = input('What filename? ')
        # filename = 'over_50000_part_4.pkl'
        generation, generation_count, total_time_taken = pickle.load(open(filename, "rb" ))
        print('Average:', sum([elem[0] for elem in generation]) / len(generation))
        print('Generation:', generation_count)
        print('Best strategy so far:', max(generation))
        print('Time taken up to this generation ', generation_count, ': ', total_time_taken, ' seconds', sep='')
    elif do_next == 'LT':
        filename = input('What filename? ')
        generation, generation_count, total_time_taken = pickle.load(open(filename, "rb" ))
        print('Average:', sum([elem[0] for elem in generation]) / len(generation))
        print('Generation:', generation_count)
        print('Best strategy so far:', max(generation))
        print('Time taken up to this generation ', generation_count, ': ', total_time_taken, ' seconds', sep='')
        games = []
        while True:
            games.append(play_game(generation[0][1], orientation_to_metadata, orientation_to_pieces, all_orientations))
            print('Running average:', sum(games) / len(games))
    elif do_next == 'LM':
        filename = input('What filename? ')
        generation, generation_count, total_time_taken = pickle.load(open(filename, "rb" ))
        print('Average:', sum([elem[0] for elem in generation]) / len(generation))
        print('Generation:', generation_count)
        print('Best strategy so far:', max(generation))
        print('Time taken up to this generation ', generation_count, ': ', total_time_taken, ' seconds', sep='')
        max_score = 0
        for i in range(100):
            result = play_game(generation[0][1], orientation_to_metadata, orientation_to_pieces, all_orientations)
            max_score = max((result, max_score))
            print('Game score:', result)
            print('Max score so far:', max_score)
            print()

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    # do_next = 'C'
    while True:
    # for i in range(2):
        # do_next = 'C' if max(generation)[0] < 1_000_000 else 'S'
        do_next = input('(P)lay a game with current best strategy, (S)ave current progress, or (C)ontinue? ').upper()
        while do_next != 'P' and do_next != 'S' and do_next != 'C':
            do_next = "I'm sorry, I didn't understand that. Would you like to: (P)lay a game with current best strategy, (S)ave current progress, or (C)ontinue? ".upper()
        if do_next == 'P':
            play_game(generation[0][1], orientation_to_metadata, orientation_to_pieces, all_orientations, display_output=True)
        elif do_next == 'S':
            filename = input('What filename? ')
            # filename = 'over_50000_part_5.pkl'
            pickle.dump((generation, generation_count, total_time_taken), open(filename, "wb"))
            break
        elif do_next == 'C':
            start_time = time.perf_counter()
            generation_count += 1
            generation = get_next_generation(generation)
            total_time_taken += time.perf_counter() - start_time
            print('Average:', sum([elem[0] for elem in generation]) / len(generation))
            print('Generation:', generation_count)
            print('Best strategy so far:', max(generation))
            print('Time taken up to this generation ', generation_count, ': ', total_time_taken, ' seconds', sep='')
            if len(sys.argv) > 1:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = os.path.join(directory, str(generation_count)+'_'+'generation_'+str(int(generation[0][0]))+'.pkl')
                with open(filename, "wb") as save_file:
                    pickle.dump((generation, generation_count, total_time_taken), save_file)

        # sys.exit()

def get_next_generation(generation):
    global POPULATION_SIZE
    global NUM_CLONES
    global TOURNAMENT_SIZE
    global WIN_PROBABILITY
    global MUTATION_RATE
    global NUM_DIGITS_TO_ROUND
    global NUM_CORES_TO_USE
    next_gen = []
    used_strategies = set()
    strategies_to_process = []
    for i in range(NUM_CLONES):
        tuplified_strategy = tuple(generation[i][1])
        next_gen.append((generation[i][0], tuplified_strategy))
        used_strategies.add(tuplified_strategy) # TODO make strategy a tuple everywhere
    while len(used_strategies) < POPULATION_SIZE:
        child_strategy = create_strategy(generation)
        if child_strategy in used_strategies:
            continue
        used_strategies.add(child_strategy) # add the key to used_strategies
        strategies_to_process.append(child_strategy)
    inputs = [(strategy, orientation_to_metadata, orientation_to_pieces, all_orientations, index) for index, strategy in enumerate(strategies_to_process)]
    if NUM_CORES_TO_USE is None:
        with multiprocessing.Pool() as pool:
            next_gen += pool.starmap(fitness_function, inputs)
    else:
        with multiprocessing.Pool(NUM_CORES_TO_USE) as pool:
            next_gen += pool.starmap(fitness_function, inputs)
    # for child in used_strategies:
    #     child = fitness_function(child, orientation_to_metadata, orientation_to_pieces, all_orientations, len(next_gen))
    #     next_gen.append(child)
    next_gen.sort(reverse=True) # TODO only sort by the heuristic, disregard the strategy itself when sorting
    return next_gen

POPULATION_SIZE = 2
# NUM_CLONES = int(.15 * POPULATION_SIZE)
NUM_CLONES = 0
TOURNAMENT_SIZE = 2
WIN_PROBABILITY = .75
MUTATION_RATE = .8

NUM_STRATEGY_ASPECTS = 16
NUM_DIGITS_TO_ROUND = 4
EXPONENT_MIN = .5
EXPONENT_MAX = 2

NUM_TRIALS = 10
NUM_TRIALS_TO_DROP = 7
NUM_PIECES_LIMITED = 700

NUM_CORES_TO_USE = None # if this is None, use all available cores. Otherwise, use the number of cores specified by this constant

# orientation_to_metadata, orientation_to_pieces, all_orientations = None, None, None

# CONFIGURE PLAY GAME
def play_game(strategy, orientation_to_metadata, orientation_to_pieces, all_orientations, display_output=False):
    # return play_game_unlimited(strategy, orientation_to_metadata, orientation_to_pieces, all_orientations, display_output)
    return play_game_restricted(strategy, orientation_to_metadata, orientation_to_pieces, all_orientations, display_output)

# CONFIGURE FITNESS FUNCTION
def fitness_function(strategy, strategy_number=None):
    orbit_image = Runner(generation)
    return 1 / error()


def main():
    # model_tetris_runner()
    genetic_algorithm_search()
    # pickle.dump(all_explored_boards, open("all_explored_boards_1.pkl", "wb"))

if __name__ == '__main__':
    main()
