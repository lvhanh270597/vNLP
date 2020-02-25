from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.util import ngrams
from collections import Counter
from pyvi import ViTokenizer, ViPosTagger, ViUtils
import matplotlib.pyplot as plt
import urllib.request
from vicorrect.model import CorrectVietnameseSentence
from bs4 import BeautifulSoup, Comment
from textblob import TextBlob
import pickle
import html
import re


vocab, white_list = None, None
def load_data(white_list_path, vocab_path):
    global vocab, white_list
    vocab = open(vocab_path).read().splitlines()
    vocab = set(vocab)
    words = open(white_list_path).read().splitlines()
    white_list = dict()
    for word in words:
        white_list[word.lower()] = word

class vText:
    
    default_regex = [
        (r"<.*?>", " ")                      # Remove html tags
    ]
    punkts = set(",.:!?")
    adjust_regex = [
        ( r"^\s+", "" ), 
        ( r"\s{2,}", " " ),
        ( r"\s+([\,\.\:\?\!])", r"\1" ),
        ( r"([\,\.\:\?\!])(\s+)?[\,\.\:\?\!]+", r"\1" ),
        ( r"\s$", "" ),
    ]

    def __init__(self, text=None, num_revision=1):
        self.set_init(text, num_revision)

    def set_init(self, text, num_revision):
        self.num_revision = num_revision
        self.text = text
        self.backup = [text] * num_revision
        self.freqWords, self.freqChars = None, None

    def get_from_url(self, url, num_revision=1):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read() # The data u need
        text = data.decode("utf8")
        self.set_init(text, num_revision)

    def rotate_data(self):
        self.backup = self.backup[1: ]
        self.backup.append(self.text)

    def sub(self, regex_list=None):
        self.rotate_data()
        if regex_list is None:
            regex_list = self.default_regex
        for regexFind, regexReplace in regex_list:
            pattern = re.compile(regexFind)
            self.text = re.sub(pattern, regexReplace, self.text)
        return self.text

    def remove_html_tag(self, remove_content_tags=("script", "style", "i")):
        self.rotate_data()
        soup = BeautifulSoup(self.text) # create a new bs4 object from the html data loaded
        for script in soup(remove_content_tags): # remove all javascript and stylesheet code
            script.extract()
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        # get text
        self.text = ' '.join([t for t in soup.find_all(text=True)][1:])
        self.text = re.sub(re.compile(r"<br(\s+)?(/)?>"), "\n", self.text)
        return self.text

    def adjust(self):
        self.sub(self.adjust_regex)
        return self.text

    def tokenize(self, lang="vi"):
        self.rotate_data()
        if lang == "vi":
            self.text = ViTokenizer.tokenize(self.text)
        if lang == "en":
            self.text = " ".join(word_tokenize(self.text))
        return self.text

    def word_freq(self):
        tokens = [w for w in word_tokenize(self.text) if w.isalnum()]
        self.freqWords = Counter(tokens)
        self.sortFreqWords = {
            k: v for k, v in sorted(
                self.freqWords.items(), key=lambda item: item[1]
            )
        }
        return self.freqWords
    
    def word_plot(self, type_plot="desc", top_size=10):
        if self.freqWords is None:
            self.word_freq()
        if type_plot == "asc":
            x = list( range( 1, len(self.freqWords) + 1 ) )[ :top_size]
            y = list( self.sortFreqWords.values() )[ : top_size]
            labels = list( self.sortFreqWords.keys() )[: top_size]
        if type_plot == "desc":
            x = list( range( 1, len(self.freqWords) + 1 ) )[ :top_size]
            y = list( self.sortFreqWords.values() )[-top_size : ][::-1]
            labels = list( self.sortFreqWords.keys() )[-top_size : ][::-1]
        if type_plot in ["asc", "desc"]:
            plt.plot(x, y)
            # You can specify a rotation for the tick labels in degrees or with keywords.
            plt.xticks(x, labels, rotation='vertical')
            # Pad margins so that markers don't get clipped by the axes
            plt.margins(0.2)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.15)
            plt.show()

    def char_freq(self):
        self.freqChars = Counter(self.text)
        self.sortFreqChars = {
            k: v for k, v in sorted(
                self.freqChars.items(), key=lambda item: item[1]
            )
        }
        return self.freqChars

    def char_plot(self, type_plot="desc", top_size=10):
        if self.freqChars is None:
            self.char_freq()
        if type_plot == "asc":
            x = list( range( 1, len(self.freqChars) + 1 ) )[ :top_size]
            y = list( self.sortFreqChars.values() )[ : top_size]
            labels = list( self.sortFreqChars.keys() )[: top_size]
        if type_plot == "desc":
            x = list( range( 1, len(self.freqChars) + 1 ) )[ :top_size]
            y = list( self.sortFreqChars.values() )[-top_size : ][::-1]
            labels = list( self.sortFreqChars.keys() )[-top_size : ][::-1]
        if type_plot in ["asc", "desc"]:
            plt.plot(x, y)
            # You can specify a rotation for the tick labels in degrees or with keywords.
            plt.xticks(x, labels, rotation='vertical')
            # Pad margins so that markers don't get clipped by the axes
            plt.margins(0.2)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.15)
            plt.show()

    def separate( self, list_chars=(' ', '.', ) ):
        tokens = set()
        queue = [self.text]
        while len(queue) > 0:
            first = queue[0]
            queue = queue[1: ]
            success = False
            for c in list_chars:
                current = first.split(c)
                if len(current) > 1:
                    queue.extend(current)
                    success = True
                    break
            if not success:
                tokens.add(first)
        return tokens

    def extract_ngrams(self, num):
        tokens = word_tokenize(self.text)
        return [pair for pair in ngrams(tokens, num)]

    def pos_tag(self):
        self.rotate_data()
        self.tokenize()
        return ViPosTagger.postagging(self.text)

    def remove_accents(self):
        self.rotate_data()
        self.text = ViUtils.remove_accents(self.text).decode("utf-8")
        return self.text

    def add_accents(self):
        self.rotate_data()
        self.text = ViUtils.add_accents(self.text)
        return self.text

    def add_my_accents(self,  fpath, type_of_loader="text"):
        try:
            self.correctLoaded
        except:
            self.load_corrector(fpath, type_of_loader)
        self.rotate_data()
        self.text = self.correctLoaded.predict([self.text])[0][0]
        return self.text

    def load_corrector(self, fpath, type_of_loader):
        if type_of_loader == "text":
            self.correctLoaded = CorrectVietnameseSentence(verbose=True)
            dataset = open(fpath).read().splitlines()
            self.correctLoaded.fit(dataset)
        if type_of_loader == "binary":
            self.correctLoaded = pickle.load(open(fpath, "rb"))

    def get_words_function(self, function):
        tokens = word_tokenize(self.text)
        words = [w for w in tokens if function(w)]
        return words

    def detect_language(self):
        return TextBlob(self.text).detect_language()
    
    def translate(self, toLang="vi"):
        self.text = TextBlob(self.text).translate(to=toLang)
        return self.text

    def preprocessing(self, list_of_regex):
        global white_list, vocab
        if (vocab is None) or (white_list is None):
            print("Warning***: Please load data before using this function!")
            return None
        self.rotate_data()
        self.sub(list_of_regex)
        tokens = self.tokenize(lang="en").split()
        lemmatizer = WordNetLemmatizer()
        words = []
        removeWords = set()
        for token in tokens:
            if token in self.punkts:
                words.append(token)
                continue
            if token.istitle() or token.isupper():
                words.append(token)
                continue
            if token.isalpha() and ((token.lower() in white_list) or (token.lower() in vocab)):
                words.append(token)
                continue
            ntoken = lemmatizer.lemmatize(token)
            if ntoken.isalpha() and ((ntoken.lower() in white_list) or (ntoken.lower() in vocab)):
                words.append(token)
                continue
            removeWords.add(token)
        for i, word in enumerate(words):
            if word.isalpha():
                if word.lower() in white_list:
                    words[i] = white_list[word.lower()]
                    continue
                if not word.islower():
                    words[i] = word.title()
        self.text = " ".join(words)
        self.adjust()
        return self.text, removeWords

    def __str__(self):
        return f'vText("{self.text}")'
    