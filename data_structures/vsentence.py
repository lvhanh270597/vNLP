from data_structures.vtext import vText

class vSentence(vText):

    def __init__(self, text=None, num_revision=1):
        super().__init_(text, num_revision)
        self.sentence = text

    def __str__(self):
        return f'vSentence("{self.sentence}")'
    
