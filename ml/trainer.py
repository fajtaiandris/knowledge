# encoding: utf-8
#!/usr/bin/python

import sys, getopt, logging, corenlp
from constants import *

#-------------------------- CONSTANTS ------------------------------------------
RAW_PATH = "./raw-texts/"
ANNOTATION_PATH = "./annotation-data/"
TRAINING_DATA_PATH = "./training-data/"
CORENLP_PATH = "./stanford-ner-2020-11-17/stanford-ner.jar"
PROP = "./sign-ext.prop"
CLASSIFIER = "./sign-ext-model.ser.gz"

def make_data ():
    logging.info("DATA MADE")
    nlp.convert_raw_with_ann_to_tsv(RAW_PATH, ANNOTATION_PATH, TRAINING_DATA_PATH)

def train ():
    logging.info("TRAIN")
    nlp.train(TRAINING_DATA_PATH, PROP)

def test ():
    logging.info("TEST")
    nlp.test_for_file(CLASSIFIER, "./testing-data/2.signature.txt.txt.tsv")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    opts, args = getopt.getopt(sys.argv[1:], '', ['train', 'test', 'make-data'])
    train_arg, test_arg, make_arg = False, False, False

    for opt, arg in opts:
        if opt in ['--train']:
            train_arg = True
        elif opt in ['--test']:
            test_arg = True
        elif opt in ['--make-data']:
            make_arg = True

    if (train_arg == test_arg == make_arg == False ):
        print("""
USAGE
-----

--make-data
    Make the training data from the input files

--train
    Train the model based on the training data

--test
    Test the model based on the testing data
""")
        exit(2)

    nlp = corenlp.CoreNLP(CORENLP_PATH)
    if make_arg: make_data()
    if train_arg: train()
    if test_arg: test()
