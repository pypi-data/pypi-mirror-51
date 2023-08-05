from typing import List

from ..model.IntermediateLanguage import IntermediateLanguage

class IntermediateLocalization:

    def __init__(self, localizationIdentifier: str, intermediateLanguages: List[IntermediateLanguage]):
        self.localizationIdentifier = localizationIdentifier
        self.intermediateLanguages = intermediateLanguages

    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior"""
        if not isinstance(other, IntermediateLocalization): return NotImplemented

        sameIdentifier = self.localizationIdentifier == other.localizationIdentifier
        sortedOwnLanguages = sorted(self.intermediateLanguages, key = lambda x: x.languageIdentifier)
        sortedOtherLanguages = sorted(other.intermediateLanguages, key = lambda x: x.languageIdentifier)
        sameLanguages = sortedOwnLanguages == sortedOtherLanguages

        return sameIdentifier and sameLanguages

    def __str__(self) -> str:
        description = "IntermediateLocalization:\nLocalizationIdentifier: {}\n".format(self.localizationIdentifier)
        for language in self.intermediateLanguages:
            description += str(language)
        return description