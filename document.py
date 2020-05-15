class Document:
    text = ""
    wordFrequency = {}
    actualClass = ""
    learnedClass = ""

    def __init__(self, text, counter, actualClass):
        self.text = text
        self.wordFrequency = counter
        self.actualClass = actualClass

    def getText(self):
        return self.text

    def getWordFrequency(self):
        return self.wordFrequency

    def getTrueClass(self):
        return self.actualClass

    def getLearnedClass(self):
        return self.learnedClass

    def setLearnedClass(self, guess):
        self.learnedClass = guess
