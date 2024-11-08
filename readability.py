import argparse
import re
from math import ceil

from nltk import sent_tokenize, regexp_tokenize


def get_file_names():
    parser = argparse.ArgumentParser(description='Readability Score')
    parser.add_argument('input_file_name', type=str, help='Text to analyze')
    parser.add_argument('words_file_name', type=str, help='Words most frequently used')
    args = parser.parse_args()
    return args.input_file_name, args.words_file_name


def main() -> None:
    automated_readability_scores_ages = {
        1: (5, 6), 2: (6, 7), 3: (7, 8), 4: (8, 9), 5: (9, 10), 6: (10, 11), 7: (11, 12), 8: (12, 13), 9: (13, 14),
        10: (14, 15), 11: (15, 16), 12: (16, 17), 13: (17, 18), 14: (18, 22)
    }

    # parse file paths from command line arguments
    input_file_name, words_file_name = get_file_names()

    # read file contents
    with open(input_file_name, 'r') as file:
        text = file.read()

    with open(words_file_name, 'r') as file:
        lines = file.readlines()
    easy_words = [word.rstrip() for word in lines]

    # count characters, words, difficult words and sentences in text
    count_char = len(regexp_tokenize(text, r'\S'))
    count_words = len(words := regexp_tokenize(text, r'[0-9A-z\']+'))
    count_difficult_words = len([word for word in words if word not in easy_words])
    count_sent = len(sent_tokenize(text))

    # count syllables in text
    vowels = re.findall(r'[aeiouy]+', text, re.IGNORECASE)
    triple_vowels = re.findall('[aeiouy]{3}', text, re.IGNORECASE)
    silent_vowels = re.findall(r'[aeiouy][^aeiouy\W]+e\W', text, re.IGNORECASE)
    count_syllables = len(vowels) + len(triple_vowels) - len(silent_vowels)

    # calculate automated readability index, flesch-kincaid readability test and dale-chall readability index
    ari_score = ceil(4.71 * count_char / count_words + 0.5 * count_words / count_sent - 21.43)
    fk_score = ceil(0.39 * count_words / count_sent + 11.8 * count_syllables / count_words - 15.59)
    dc_score = ceil(0.1579 * (perc_diff_words := count_difficult_words / count_words * 100) + 0.0496 *
                    (count_words / count_sent) + (3.6365 if perc_diff_words >= 0.05 else 0))

    # calculate average age from automated readability scores
    ari_age1, ari_age2 = automated_readability_scores_ages[ari_score]
    fk_age1, fk_age2 = automated_readability_scores_ages[fk_score]
    dc_age1, dc_age2 = automated_readability_scores_ages[dc_score]
    age_avg = (min(ari_age1, fk_age1, dc_age1) + max(ari_age2, fk_age2, dc_age2)) / 2

    # display results
    print('Text:', text)
    print(f'\nCharacters: {count_char}\nSentences: {count_sent}\nWords: {count_words}\n'
          f'Difficult words: {count_difficult_words}\nSyllables: {count_syllables}\n')
    print(
        f'Automated Readability Index: {ari_score}. '
        f'The text can be understood by {ari_age1}-{ari_age2} year olds.\n'
        f'Flesch–Kincaid Readability Test: {fk_score}. '
        f'The text can be understood by {fk_age1}-{fk_age2} year olds.\n'
        f'Dale-Chall Readability Index: {dc_score}. '
        f'The text can be understood by {dc_age1}-{dc_age2} year olds.\n'
        f'This text should be understood in average by {age_avg} year olds.'
    )


if __name__ == '__main__':
    main()
