#!/usr/bin/python3
# Usage: $ python readability.py string
# When string is unspecified, prompts the user for string

import sys


def main():
    s = get_string()
    sentences, words, letters = get_properties(s)
    # Letters per hundred words
    ratio_letters = calc_ratio(letters, words)
    # Sentences per hundred words
    ratio_sentences = calc_ratio(sentences, words)
    score = calc_score(ratio_letters, ratio_sentences)
    print("{}".format(score))
    sys.exit()


# Calculates a ratio as a/b and returns a rounded int
def calc_ratio(a, b):
    return (a / b) * 100


def calc_score(l, s):
    score = int(round(0.0588 * l - 0.296 * s - 15.8))
    if score < 1:
        return "Before Grade 1"
    elif score > 16:
        return "Grade 16+"

    return "Grade " + str(score)


# Gets the properties of a string
def get_properties(string):
    c = 0
    string_length = len(string)
    sentences = 0
    words = 1  # The last word in a sentence is otherwise not counted in method specified below
    letters = 0
    for c in range(string_length):
        if string[c] == " ":
            words += 1
        if string[c] == ".":
            sentences += 1
        if string[c] == "!":
            sentences += 1
        if string[c] == "?":
            sentences += 1
        if string[c].isalpha():
            letters += 1

    return sentences, words, letters


def get_string():
    if len(sys.argv) != 1:

        return sys.argv[1:]

    return input("Text: ")


if __name__ == "__main__":
    main()