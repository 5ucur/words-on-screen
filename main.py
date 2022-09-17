import itertools
import random
import os

# TO DO
# Timer
# Maybe make perms not a dict
# Limit amount of permutations for each length

# Prepare for making dicts
dicts = {
    'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}, 'f': {}, 'g': {}, 'h': {},
    'i': {}, 'j': {}, 'k': {}, 'l': {}, 'm': {}, 'n': {}, 'o': {}, 'p': {},
    'q': {}, 'r': {}, 's': {}, 't': {}, 'u': {}, 'v': {}, 'w': {}, 'x': {},
    'y': {}, 'z': {}
}

# Look in the dicts directory
for file in os.listdir('phrases'):
    # Take the letter and number from the filename
    # The letter represents the first letter of the words in the file
    # The number represents the lenght of the words in the file
    let = file.split('_')[1].split('.')[0]
    num = file.split('_')[0]
    # Open that file
    with open(os.path.join('phrases', file)) as current:
        # Take from it the words and put them in the corresponding dict
        dicts[let][num] = list(map(str.strip, current))

# Open the file with basewords
with open('bases') as bfile:
    # Make a list of those words
    bases = list(map(str.strip, bfile))

# Get all permutations of a string, if they are an accepted word
def get_perms(string):
    # Start with a set containing that string
    # A set because there could be duplicates
    # e.g. 'larger' will give two instances of 'gear'
    new = {string}
    # Go through all acceptable lengths, i.e. four to length of the string
    for length in range(4, len(string)+1):
        # Get every permutation of a length
        for item in itertools.permutations(string, length):
            # Make a string of that permutation
            word = ''.join(item)
            # If there are less permutations than a certain maximal number 
            if len(new) < 52:
                # And if the word is an acceptable one
                # i.e. if it exists in the dict for its first letter and length
                if word in dicts[word[0]][str(len(word))]:
                    # Add it to the set
                    new.add(word)
            # If there are enough permutations
            else:
                # Stop the inner loop 
                break
        # If the inner loop did not break
        else:
            # Continue working
            continue
        # Stop the outer loop if the inner loop breaks
        break
    # Return a dictionary of permutations, where
    #  Key is the permutation
    #  Value is a list of the following three elements
    #   A string of underscores of the length of the permutation
    #   The permutation's guessed value
    #   The permutation itself
    return {word:["_"*len(word), 0, word] for word in new}

# Key for sorting the permutations by length of the word
def wordlen(perm):
    # Return the length of the first element (underscore string, see above)
    return len(perm[0])

# Key for sorting the permutations alphabetically
def wordlet(perm):
    # Return the first letter of the third element (permutation itself, see above)
    return perm[2][0]

# Turn a list into chunks of length n
def chunks(lst, n):
    # Go through the list's length in steps of n
    for i in range(0, len(lst), n):
        # Yield a chunk of the list of size n
        yield lst[i:i + n]

# Transpose a list of lists
def transpose(lst):
    # Return the transposed list
    return list(map(list, itertools.zip_longest(*lst, fillvalue='')))

# Determine if a word should be showed or not
def show_or_not(words):
    # Start with an empty list
    new = []
    # Go through all of the words
    for val in words:
        # If the second element (guessed value, see above) is zero
        if not val[1]:
            # Append the first element (underscore string, see above)
            new.append(val[0])
        # If the guessed value is one
        else:
            # Append the third element (permutation itself, see above)
            new.append(val[2])
    # Return the list of words
    return new

# Print the game, with the solution word and all its permutations
def print_game(word, perms):
    # Make a list from the word, to make it shufflable
    solution = list(word)
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    # Shuffle the word
    random.shuffle(solution)
    # Print the shuffled word
    print(''.join(solution))
    # Print a separator
    print('*'*len(solution))
    # Sort the permutations alphabetically
    words = sorted(perms.values(), key=wordlet)
    # Sort the permutations by length
    words = sorted(words, key=wordlen)
    # Split the permutations into chunk and transpose them
    words = transpose(list(chunks(show_or_not(words), 4)))
    # For each chunk
    for chunk in words:
        # Print it, separated by a space
        print(' '.join(chunk))

# Generate a solution and its permutations
def generate():
    # Start with an empty dict of permutations
    perms = {}
    # As long as there are fewer than a minimal number of permutations
    while len(perms) < 4:
        # Choose a random word
        solution = random.choice(bases)
        # Generate its permutations
        perms = get_perms(solution)
    # Return the generated elements
    return solution, perms

# Main function
if __name__ == "__main__":
    # Generate the solution and permutations
    solution, perms = generate()
    # While not all of the words have been guessed
    # i.e. while there are still words with a guess value of zero
    while not all([val[1] for val in perms.values()]):
        # Print the game
        print_game(solution, perms)
        # Take the guess
        guess = input(']')
        # If the guess is in the permutations
        if perms.get(guess):
            # Change the guess value of that word to one
            perms[guess][1] = 1
    # Upon finishing the game (guessing the last word),
    #  print the game once again to show all the words
    print_game(solution, perms)
