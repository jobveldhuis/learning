#!/usr/bin/python3

# Program that indicates how many matches there can be found in DNA
# Note that CSV files should contain a header, so we know what sequences to check for
# Usage: $ python dna.py database sequence

import sys
import csv


def main():
    d, s = check_args()
    dna = get_dna(s)
    dna_length = len(dna)
    sequences = {}
    dnaSequences = get_sequences(d)

    # Copy array to dictionary with gene as key
    for seq in dnaSequences:
        sequences[seq] = 0

    # Start a loop through all sequences
    for k in sequences:
        l = len(k)
        tmp = 0
        max = 0

        for c in range(dna_length):
            # Makes sure that we don't count a sequence twice
            if tmp != 0:
                tmp = 0

            # See if the DNA at cursor point c is equal to the DNA we are looking for.
            # If so, see if the strand of DNA before the cursor point is equal to the DNA we are looking for.
            # If so, start counting.
            if dna[c: c + l] == k:
                tmp += 1
                while dna[c - l: c] == dna[c: c + l]:
                    tmp += 1
                    c += l

            # Now, compare the temp to the max variable
            if tmp > max:
                max = tmp

        sequences[k] += max

    # Open the csv file and iterate through it as a dictionary
    with open(d) as f:
        subjects = csv.DictReader(f)
        for subject in subjects:
            i = 0
            for k in sequences:
                if sequences[k] == int(subject[k]):
                    i += 1

            if i == len(sequences):
                print(subject['name'])
                sys.exit()

    print("No match")


# Gets the DNA from the text file and stores it in memory
def get_dna(txt):
    try:
        with open(txt) as f:
            reader = csv.reader(f)
            for row in reader:
                dna = str(row)
    except csv.Error as e:
        sys.exit('Error when reading text: {}'.format(e))
    except FileNotFoundError:
        sys.exit('Error when reading text file. Could not find specified sequence-file.')

    return dna


# Gets the sequences to check from the database csv file
def get_sequences(database):
    try:

        # Opens the database and reads only the first line
        # Omits the first string, since this is always 'Names'

        with open(database) as f:
            reader = csv.reader(f, delimiter=',')
            s = next(reader)
            sequences = s[1:]

    except csv.Error as e:
        sys.exit('Error when reading csv in line {}: {}'.format(reader.line_num, e))
    except FileNotFoundError as e:
        sys.exit('Error when reading csv. Could not find specified database.')

    return sequences


# Checks whether or not the right amount of args is specified
def check_args():
    a = sys.argv[1:]
    c = len(a)

    if c != 2:
        sys.exit("Usage: $ python dna.py database sequence")

    return (sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()