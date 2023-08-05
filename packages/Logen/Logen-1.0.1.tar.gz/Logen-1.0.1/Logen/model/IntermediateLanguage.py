from typing import List

from ..model.IntermediateEntry import IntermediateEntry

class IntermediateLanguage: 

    def __init__(self, languageIdentifier: str, intermediateEntries: List[IntermediateEntry]):
        self.languageIdentifier = languageIdentifier
        self.intermediateEntries = intermediateEntries
        
    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior"""
        if not isinstance(other, IntermediateLanguage): return NotImplemented
        
        sameIdentifier = self.languageIdentifier == other.languageIdentifier

        sortedOwnEntries = sorted(self.intermediateEntries, key = lambda x: x.key)
        sortedOtherEntries = sorted(other.intermediateEntries, key = lambda x: x.key)
        sameEntries = sortedOwnEntries == sortedOtherEntries

        return sameIdentifier and sameEntries
        
    def __str__(self) -> str:
        description = "IntermediateLanguage:\n   LanguageIdentifier: {}\n".format(self.languageIdentifier)
        for entry in self.intermediateEntries:
            description += str(entry) + "\n"
        return description