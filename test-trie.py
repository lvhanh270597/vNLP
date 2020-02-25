

from data_structures.trie import Trie
from data_structures.dawg import Dawg

words = open("./algorithms/am-ngu.txt").read().splitlines()

trie = Trie()
trie.load_data(words)
dawg = Dawg()
dawg.load_data(words)

text = " ".join(words)
timeSumTrie = 0
timeSumDawg = 0
for word in text.split():
    results = trie.search(word, 1)
    # print(results)
    # print("Search time: %g s" % trie.searchTime)
    timeSumTrie += trie.searchTime
    results = dawg.search(word, 1)
    # print(results)
    # print("Search time: %g s" % dawg.searchTime)
    timeSumDawg += dawg.searchTime
    # print("-" * 60)

print("Trie process with time: ", timeSumTrie)
print("Dawg process with time: ", timeSumDawg)