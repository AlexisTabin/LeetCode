class Trie:

    def __init__(self):
        self.value : str = None
        self.children = {} # list Trie
        self.isEnd = False        

    def insert(self, word: str) -> None:
        if not word:
            self.isEnd = True
            return
        if word[0] not in self.children:
            nextLetter = Trie()
            nextLetter.value = word[0]
            self.children[word[0]] = nextLetter
            nextLetter.insert(word[1:])
        else:
            nextLetter = self.children[word[0]]
            nextLetter.insert(word[1:])  

    def search(self, word: str) -> bool:
        if not word:
            return self.isEnd
        if word[0] not in self.children:
            return False
        else:
            nextLetter = self.children[word[0]]
            return nextLetter.search(word[1:])
        

    def startsWith(self, prefix: str) -> bool:
        if not prefix:
            return True
        if prefix[0] not in self.children:
            return False
        else:
            nextLetter = self.children[prefix[0]]
            return nextLetter.startsWith(prefix[1:])        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)