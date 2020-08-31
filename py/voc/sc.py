from spellchecker import SpellChecker
'''
spell = SpellChecker()

# find those words that may be misspelled
misspelled = spell.unknown(['let', 'us', 'wlak','on','the','groun'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))
'''

class SC:

    def __init__(self):
        self.spell = SpellChecker()

    def check(self, word):
        res = {}
        misspelled = self.spell.unknown([word])
        for word in misspelled:
            print("Oops...You may spell the wrong word. Here're possible candidates:")
            print("\t"+", ".join(self.spell.candidates(word)))
            # print(type(self.spell.candidates(word)))
            res["error"] = "Oops...You may spell the wrong word."
            res["candi"] = list(self.spell.candidates(word))
            return False, res
        return True, res

if __name__ == "__main__":
    sc = SC()
    print(sc.check("wod"))
