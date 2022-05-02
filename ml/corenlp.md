# 📙 Using Stanford CoreNLP

Extract of the [Stanford NER CRF FAQ](https://nlp.stanford.edu/software/crf-faq.html#a).

## 1. Creating the training data

1. Break the raw data text into tokens (words).  
A blank line separates two "documents".
```bash
$ java -cp stanford-ner.jar edu.stanford.nlp.process.PTBTokenizer \
       data.txt > data.tok
```

2. Annotate every token as other.
```bash
$ perl -ne 'chomp; print "$_\tO\n"' data.tok > data.tsv
```

3. Annotate the tokens manually.

## 2. Train the model

1. Create a properties file (.prop). Premade features are listed [here](https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/ie/NERFeatureFactory.html).
```bash
#                                                  location of the training file
trainFile = data.tsv
#                         location where you would like to save (serialize) your
#                classifier; adding .gz at the end automatically gzips the file,
#                                          making it smaller, and faster to load
serializeTo = ner-model.ser.gz
#                structure of your training file; this tells the classifier that
#                  the word is in column 0 and the correct answer is in column 1
map = word=0,answer=1
#               This specifies the order of the CRF: order 1 means that features
#              apply at most to a class pair of previous class and current class
#                                               or current class and next class.
maxLeft=1
#                                 these are the features we'd like to train with
#                                      some are discussed below, the rest can be
#                                     understood by looking at NERFeatureFactory
useClassFeature=true
useWord=true
#              word character ngrams will be included up to length 6 as prefixes
#                                                              and suffixes only
useNGrams=true
noMidNGrams=true
maxNGramLeng=6
usePrev=true
useNext=true
useDisjunctive=true
useSequences=true
usePrevSequences=true
#                            the last 4 properties deal with word shape features
useTypeSeqs=true
useTypeSeqs2=true
useTypeySequences=true
wordShape=chris2useLC
```

2. Train the model.
```bash
$ java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier \
       -prop model.prop
```

## 3. Testing the model

1. Create test source in a similar format as `data.tsv`.
```bash
$ java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier \
       -loadClassifier ner-model.ser.gz \
       -testFile test.tsv
```
