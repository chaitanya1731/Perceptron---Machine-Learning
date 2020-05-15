import collections
import os
import re
import sys
import copy
from document import Document

trainDataset = {}
testDataset = {}
classes = ["ham", "spam"]

def getDataset(storage_dict, directory, true_class):
    for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        if os.path.isfile(filePath):
            with open(filePath, 'r') as text_file:
                text = text_file.read()
                storage_dict.update({filePath: Document(text, getWordsCollection(text), true_class)})

def getWordsCollection(text):
    wordsCollection = collections.Counter(re.findall(r'\w+', text))
    return dict(wordsCollection)

def getStopwords(filename):
    words = []
    with open(filename, 'r') as txt:
        words = (txt.read().splitlines())
    return words

def getFilteredDataset(stopwords, dataset):
    datasetWithoutStopwords = copy.deepcopy(dataset)
    for word in stopwords:
        for j in datasetWithoutStopwords:
            if word in datasetWithoutStopwords[j].getWordFrequency():
                del datasetWithoutStopwords[j].getWordFrequency()[word]
    return datasetWithoutStopwords

def getVocabulary(dataset):
    vocab = []
    for i in dataset:
        for j in dataset[i].getWordFrequency():
            if j not in vocab:
                vocab.append(j)
    return vocab

def trainWeights(weights, constant, trainDataset, iterations, classes):
    for i in iterations:
        for d in trainDataset:
            sumOfWeights = weights['weight_zero']
            for f in trainDataset[d].getWordFrequency():
                if f not in weights:
                    weights[f] = 0.0
                sumOfWeights += weights[f] * trainDataset[d].getWordFrequency()[f]
            perceptron_output = 0.0
            if sumOfWeights > 0:
                perceptron_output = 1.0
            target_value = 0.0
            if trainDataset[d].getTrueClass() == classes[1]:
                target_value = 1.0
            for w in trainDataset[d].getWordFrequency():
                weights[w] += float(constant) * float((target_value - perceptron_output)) * \
                              float(trainDataset[d].getWordFrequency()[w])

def applyWeights(weights, instance):
    sumOfWeights = weights['weight_zero']
    for i in instance.getWordFrequency():
        if i not in weights:
            weights[i] = 0.0
        sumOfWeights += weights[i] * instance.getWordFrequency()[i]
    if sumOfWeights > 0:
        return 1
    else:
        return 0

def getCorrectGuesses(dataset, isFilteredDataset):
    correctGuesses = 0
    for i in dataset:
        if isFilteredDataset == 0:
            guess = applyWeights(weights, dataset[i])
        else:
            guess = applyWeights(weightsWithoutStopwords, dataset[i])
        if guess == 1:
            dataset[i].setLearnedClass(classes[1])
            if dataset[i].getTrueClass() == dataset[i].getLearnedClass():
                correctGuesses += 1
        if guess == 0:
            dataset[i].setLearnedClass(classes[0])
            if dataset[i].getTrueClass() == dataset[i].getLearnedClass():
                correctGuesses += 1
    return correctGuesses

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Please enter correct arguments')
        sys.exit()
    trainSpamPath, trainHamPath = sys.argv[1] + "/spam/", sys.argv[1] + "/ham/"
    testSpamPath, testHamPath = sys.argv[2] + "/spam/", sys.argv[2] + "/ham/"
    iterations, constant = sys.argv[4], sys.argv[5]

    getDataset(trainDataset, trainSpamPath, classes[1])
    getDataset(trainDataset, trainHamPath, classes[0])
    getDataset(testDataset, testSpamPath, classes[1])
    getDataset(testDataset, testHamPath, classes[0])

    stopwords = getStopwords(sys.argv[3])

    trainDatasetWithoutStopwords = getFilteredDataset(stopwords, trainDataset)
    testDatasetWithoutStopwords = getFilteredDataset(stopwords, testDataset)

    trainVocabulary = getVocabulary(trainDataset)
    trainVocabularyWithoutStopwords = getVocabulary(trainDatasetWithoutStopwords)

    weights = {'weight_zero': 1.0}
    weightsWithoutStopwords = {'weight_zero': 1.0}
    for i in trainVocabulary:
        weights[i] = 0.0
    for i in trainVocabularyWithoutStopwords:
        weightsWithoutStopwords[i] = 0.0

    trainWeights(weights, constant, trainDataset, iterations, classes)
    trainWeights(weightsWithoutStopwords, constant, trainDatasetWithoutStopwords, iterations, classes)

    # For unfiltered dataset, pass 0 as second parameter (flag for filtered dataset)
    CorrectGuessTrain = getCorrectGuesses(trainDataset, 0)
    trainAccuracy = (float(CorrectGuessTrain) / float(len(trainDataset)) * 100.0)

    # For unfiltered dataset, pass 0 as second parameter (flag for filtered dataset)
    CorrectGuessTestData = getCorrectGuesses(testDataset, 0)
    testAccuracyWithStopwords = (float(CorrectGuessTestData) / float(len(testDataset)) * 100.0)

    # For filtered dataset, pass 1 as second parameter (flag for filtered dataset)
    CorrectGuessTestWithoutStopwords = getCorrectGuesses(testDatasetWithoutStopwords, 1)
    testAccuracyWithoutStopwords = (float(CorrectGuessTestWithoutStopwords) / float(len(testDatasetWithoutStopwords)) * 100.0)

    print("Learning constant: {} \t # of iterations: {}".format(float(constant), int(iterations)))
    print('Training \t Test_with_stopwords \t Test_without_stopwords')
    print('%f' % trainAccuracy + '\t %f' % testAccuracyWithStopwords + '\t\t %f' % testAccuracyWithoutStopwords)

    output = open("Accuracy.txt", "w")
    output.write("Learning constant: {} \t # of iterations: {}".format(float(constant), int(iterations)))
    output.write("\n")
    output.write('Training \t Test_with_stopwords \t Test_without_stopwords')
    output.write("\n")
    output.write('%f' % trainAccuracy + '\t %f' % testAccuracyWithStopwords +
                 '\t\t %f' % testAccuracyWithoutStopwords)
    output.write("\n")
    output.close()
