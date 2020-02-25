from data_structures.dawg import Dawg

dawg = Dawg()
dawgLoaded = False

def load_dawg(datapath):
    global dawgLoaded
    words = open(datapath).read().splitlines()
    dawg.load_data(words)
    dawgLoaded = True

class vWord:

    def __init__(self, word):
        self.word = word

    def get_similarities(self, maxCost):
        if not dawgLoaded:
            print("Please call load dawg first!")
            return []
        return dawg.search(self.word, maxCost)
        