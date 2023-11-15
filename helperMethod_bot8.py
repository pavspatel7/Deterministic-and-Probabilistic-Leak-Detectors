from helperMethod import *

# Method to get probability of a cell given the dictionary of probabilities of cell pairs
def get_cell_probability(cell_pair_probability_dict, cell):
    pairs_w_cell = [pair for pair in cell_pair_probability_dict.keys() if pair[0] == cell or pair[1] == cell]
    prob = 0
    for pair in pairs_w_cell:
        prob += cell_pair_probability_dict[pair]
    return prob

# Method to delete pairs from dictionary where probability of leak is determined to be 0
def clean_up(cell_pair_probability_dict):
    combination_to_remove = []
    for pair in cell_pair_probability_dict.keys():
        if cell_pair_probability_dict[pair] == 0:
            combination_to_remove.append(pair)
    
    for items in combination_to_remove:
        del cell_pair_probability_dict[items]

# Method to update probabilities of leak in each possible pair (i, j) given leak in cell k
def leak_in_i_j_given_leak_in_k(cell_pair_probability_dict, k):
    denominator = get_cell_probability(cell_pair_probability_dict, k)
    pairs_without_k = []
    for pair in list(cell_pair_probability_dict.keys()):
        if not (pair[0] == k or pair[1] == k):
            pairs_without_k.append(pair)
        else:
            cell_pair_probability_dict[pair] = cell_pair_probability_dict[pair]/denominator
    for pair in pairs_without_k:
        cell_pair_probability_dict[pair] = 0
    return cell_pair_probability_dict

# Method to update probabilities of leak in each possible pair (i, j) given no leak in cell k
def leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, k):
    denominator = 1 - get_cell_probability(cell_pair_probability_dict, k)
    for pair in list(cell_pair_probability_dict.keys()):
        if pair[0] == k or pair[1] == k:
            cell_pair_probability_dict[pair] = 0
        else:
            cell_pair_probability_dict[pair] = cell_pair_probability_dict[pair]/denominator
    return cell_pair_probability_dict

# Method to calculate beep probability in k given leak in (i, j)
def beep_in_k_given_leak_in_i_and_j(a, grid, start, i, j, distances):
    return beep_in_i_given_leak_in_j(a, grid, start, i, distances) + beep_in_i_given_leak_in_j(a, grid, start, j, distances) - (beep_in_i_given_leak_in_j(a, grid, start, i, distances) * beep_in_i_given_leak_in_j(a, grid, start, j, distances))

# Method to calculate no beep probability in k given leak in (i, j)
def no_beep_in_k_given_leak_in_i_and_j(a, grid, start, i, j, distances):
    return 1 - beep_in_k_given_leak_in_i_and_j(a, grid, start, i, j, distances)

# Method to update probabilities of leak in each possible pair (i, j) given beep in cell k
def prob_leak_given_beep(a, grid, cell_pair_probability_dict, botpos, distances):
    denominator = 0
    for pair in list(cell_pair_probability_dict.keys()):
        temp = cell_pair_probability_dict[pair] * beep_in_k_given_leak_in_i_and_j(a, grid, botpos, pair[0], pair[1], distances)
        denominator += temp

    for pair, probability in cell_pair_probability_dict.items():
        if probability != 0:
            cell_pair_probability_dict[pair] = ((probability * beep_in_k_given_leak_in_i_and_j(a, grid, botpos, pair[0], pair[1], distances))
                                          / denominator)

    return cell_pair_probability_dict

# Method to update probabilities of leak in each possible pair (i, j) given no beep in cell k
def prob_leak_given_no_beep(a, grid, cell_pair_probability_dict, botpos, distances):
    denominator = 0
    for pair in list(cell_pair_probability_dict.keys()):
        temp = cell_pair_probability_dict[pair] * no_beep_in_k_given_leak_in_i_and_j(a, grid, botpos, pair[0], pair[1], distances)
        denominator += temp

    for pair, probability in cell_pair_probability_dict.items():
        if probability != 0:
            cell_pair_probability_dict[pair] = ((probability * no_beep_in_k_given_leak_in_i_and_j(a, grid, botpos, pair[0], pair[1], distances))
                                          / denominator)

    return cell_pair_probability_dict