#!/usr/bin/python
#
#   Copyright 2012-2015 Michele Filannino
#
#   gnTEAM, School of Computer Science, University of Manchester.
#   All rights reserved. This program and the accompanying materials
#   are made available under the terms of the GNU General Public License.
#
#   authors: Michele Filannino
#   email:  filannim@cs.man.ac.uk
#
#   For details, see www.cs.man.ac.uk/~filannim/

import re
import sys


def is_valid_sentence(sentence, line_number):
    '''It returns whether a CONLL-represented sentence is valid.

    It check the following things:
     - 8 or 10 columns must be defined
     - IDs must be numbers
     - IDs must not be duplicated
     - All the IDs must be used from 1 to N, no gaps are allowed
     - CPOSTAG and POSTAG must be formed by characters only
     - HEAD and PHEAD must be numeric and referring to an existing ID.

     The implementation is corto-circuited for performance reasons. It means
     that only the first violation is printed out and it immediately returns
     True.

    '''
    length = 0
    start_line = line_number

    conll = sentence.strip().split('\n')
    length = len(conll)
    line_counter = 1
    for conll_line in conll:
        line = conll_line.strip().split('\t')
        if not(len(line) == 8 or len(line) == 10):
            if len(line) > 1:
                print str(start_line + line_counter - 1), \
                    '** wrong line dimension **', line
            return True

        # ID
        if not(re.match('[0-9]+', line[0].strip())) or \
                line[0] != str(line_counter).strip():
            print str(start_line + line_counter - 1), \
                '** wrong ID format **', line
            return True

        # FORM
        if not re.match('.+', line[1]):
            print str(start_line + line_counter - 1), \
                '** wrong FORM content **', line
            return True

        # LEMMA
        if not re.match('.+', line[2]):
            print str(start_line + line_counter - 1), \
                '** wrong LEMMA content **', line
            return True

        # CPOSTAG
        if not re.match('[A-Za-z-+]|_', line[3]):
            print str(start_line + line_counter - 1), \
                '** wrong CPOSTAG content **', line
            return True

        # POSTAG
        if not re.match('[A-Za-z-+]|_', line[4]):
            print str(start_line + line_counter - 1), \
                '** wrong POSTAG content **', line
            return True

        # FEATS
        if not re.match('[.\|]*|_', line[5]):
            print str(start_line + line_counter - 1), \
                '** wrong FEATS content **', line
            return True

        # HEAD
        if not(re.match('[0-9]+', line[6])) or int(line[6]) > length:
            print str(start_line + line_counter - 1), \
                '** wrong HEAD content **', line
            return True

        # DEPREL
        if not re.match('.+|_', line[7]):
            print str(start_line + line_counter - 1), \
                '** wrong DEPREL content **', line
            return True

        if len(line) == 10:
            # PHEAD
            if not re.match('[0-9]+|_', line[8]):
                print str(start_line + line_counter - 1), \
                    '** wrong PHEAD content **', line
                return True

            else:
                if re.match('[0-9]+', line[8]):
                    if int(line[8]) > length:
                        print str(start_line + line_counter - 1), \
                            '** wrong PHEAD number **', line
                        return True

            # PDEPREL
            if not re.match('.+|_', line[9]):
                print str(start_line + line_counter - 1), \
                    '** wrong PDEPREL content **', line
                return True

        line_counter += 1
    return False


def main():
    line_number = 1
    start_line = 1
    n_of_max_sentences = int(sys.argv[2])
    n_of_valid_sentences = 0
    conll = ''
    output = open(sys.argv[1] + '.filtered', 'w')
    for line in open(sys.argv[1], 'rU'):
        if n_of_valid_sentences >= n_of_max_sentences:
            break
        if len(line.strip()) > 0:
            conll += line
        else:
            if not is_valid_sentence(conll.strip(), start_line):
                # save in a file
                output.write(conll)
                output.write('\n')
                n_of_valid_sentences += 1
            start_line = line_number + 1
            conll = ''
        line_number += 1

if __name__ == '__main__':
    main()
