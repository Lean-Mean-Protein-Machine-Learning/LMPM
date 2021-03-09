import pandas as pd
import sklearn
import sys
sys.path.append('../UniRep/')

from unirep_utils import get_UniReps

# Importing dG parameters to params_dict
params = pd.read_csv('../notebooks/Params.csv', header=None)
lst = params[0].values
params.set_index(lst, inplace=True)
del params[0]
params_dict = defaultdict(list)
for i, row in params.iterrows():
    for position in range(1, len(row) + 1):
        params_dict[i].append(float(row.loc[position]))


def check_sequence_input(sequence):
    """
    Checks the input sequence to ensure that amino acids are in
    single-letter format

    Args:
        sequence (str): amino acid sequence in single-letter format

    Returns:
        None
    """



def ambiguous_amino_acids(sequence):
    """
    Raises an error for ambiguous amino acids: X, B, and U

    Args: sequence (str): amino acid sequence in single-letter format

    Returns:
        None
    """



def model_organism_selection(organism):
    """
    Imports trained model of secretion scores based on organism data set

    Args:
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)

    Returns:
        model: trained model of secretion probabilities for organism
    """



def secretion_score_unirep(sequence, organism):
    """
    Finds the secretion probability of given sequence based on model
    and UniRep representation only

    Args:
        sequence (str): amino acid sequence in single-letter format
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)

    Returns:
        predicted_class (str): predicted class of sequence
                        (cytoplasm, membrane, secreted)
        secretion_score (float): probability of sequence being 
                                    in secreted class
    """
    # Select the model based on the organism
    model = model_organism_selection(organism)

    # Obtain unirep representation of sequence
    unirep_values = get_uniReps(sequence)[0]
    unirep_values = unirep_values.reshape(1, -1)

    # Returns class of given sequence
    predicted_class = model.predict(unirep_values)

    # Grab the probabilities from the model
    classes = list(model.classes_)
    prediction_probabilities = list(model.predict_proba(unirep_values)[0])

    # Returns probability of being secreted class
    secretion_score = prediction_probabilities[classes.index('secreted')]
    
    return predicted_class, secretion_score


def calculate_transmembrane_dg(sequence):
    """
    Calculates the free energy of transmembrane insertion of the sequence

    Args:
        sequence (str): amino acid sequence in single-letter format

    Returns:
        transmembrane_dG (float): free energy calculation
    """
    # First, make sure the sequence is longer than 19 residues
    if sequence < 19:
        raise ValueError('dG cannot be computed on sequences \
                            less than 19 residues')

    # Next, check if there are any ambiguous amino acids
    ambiguous_amino_acids(sequence)

    # Starts dG calculations
    dg_values = []

    # Scans the sequence for every 19-residue frame
    for j in range(len(sequence)-18):
        running_total = 0
        segment = sequence(j:j+19)
        for k, amino_acid in enumerate(segment):
            running_total += params_dict[amino_acid][k]
        dg_values.append(running_total)

    # Finds the minimum dG value
    transmembrane_dG = min(dg_values)

    return transmembrane_dG


def secretion_optimization_unirep(sequence, position, organism):
    """
    Introduces amino acid point mutation at given position to improve
    probability of given sequence to be part of the secreted class

    Args:
        sequence (str): amino acid sequence in single-letter format
        position (int): given position where point mutations can occur
                        (where first residue is position 0)
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)

    Returns:
        sequence (str): mutated amino acid sequence
        point_mutation_dict (dict): dictionary of point mutation amino acid
                                    and secretion score
    """
    # First, find the initial class and initial secretion score
    initial_class, initial_score = secretion_score_unirep(sequence, organism)
    print('The initial sequence is:', sequence)
    print('The initial localization clas is:', initial_class)
    print('The initial probability of being in the secreted class is:', 
        initial_score)

    # Define list of amino acids
    amino_acids = ['G', 'A', 'L', 'M', 'F', 
                    'W', 'K', 'Q', 'E', 'S', 
                    'P', 'V', 'I', 'C', 'Y', 
                    'H', 'R', 'N', 'D', 'T']

    # Set up point mutations
    mutated_scores_list = []
    for residue in amino_acids:
        sequence_list = list(sequence)
        sequence_list[position] = residue
        mutated_sequence = "".join(sequence_list)
        mutated_class, mutated_score = secretion_score_unirep(
            sequence, organism)
        mutated_scores_list.append(mutated_score)
        # Replace initial sequence if mutated secretion score is better
        if mutated_score > initial_score:
            sequence = mutated_sequence
            initial_score = mutated_score
            initial_class = mutated_class

    print('The mutated sequence is:', sequence)
    print('The mutated class is:', initial_class)
    print('The mutated probability of being in the secreted class is:',
        mutated_score)

    # Plot point mutations and scores
    plt.plot(amino_acids, mutated_scores_list)
    plt.xlabel('Amino Acid Point Mutation at Position %d' % position)
    plt.ylabel('Probability of Secretion Class')

    # Create dictionary of point mutations and scores
    point_mutation_dict = {amino_acids[i]: mutated_scores_list[i]
        for i in range(len(amino_acids))}

    return sequence, point_mutation_dict


def secretion_optimization_all_positions(sequence, organism):
    """
    """