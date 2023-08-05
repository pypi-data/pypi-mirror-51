import unittest

from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile
from ..model.MergeResult import MergeResult

from ..converter.AndroidConverter import AndroidConverter

class TestJSONConverter(unittest.TestCase):

    # common subject under test for all test cases
    # Using an abritary converter class to test common merge functionality.
    sut = AndroidConverter()

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    def test_merge_differentLocalizationIdentifier(self):
        example = IntermediateLocalization("Example", [])
        otherExample = IntermediateLocalization("OtherExample", [])
        result = self.sut.merge(example, otherExample)
        self.assertEqual(result, None)

    def test_merge_equalEntries(self):
        (example, otherExample) = self._createExampleIntermediateLocalizations()
        merged = self.sut.merge(example, otherExample)

        listOfLanguageIdentifier = []
        for intermediateLanguage in merged.result.intermediateLanguages:
            listOfLanguageIdentifier.append(intermediateLanguage.languageIdentifier)

        self.assertEqual(sorted(listOfLanguageIdentifier), sorted(["de", "en"]))
        self.assertEqual(merged.missingEntries, [])

    def test_merge_unequalEntries(self):
        example, otherExample = self._createExampleIntermediateLocalizations()
        example.intermediateLanguages[0].intermediateEntries.append(IntermediateEntry("FirstNewKey", "FirstNewValue"))
        otherExample.intermediateLanguages[0].intermediateEntries.append(IntermediateEntry("SecondNewKey", "SecondNewValue"))
        newResult = self.sut.merge(example, otherExample)
        self.assertEqual(newResult.missingEntries, [IntermediateEntry("FirstNewKey", "FirstNewValue"), IntermediateEntry("SecondNewKey", "SecondNewValue")])
    
    #--------------------------------------------------
    # Testcases for helper methods
    #--------------------------------------------------

    def test_compareEntries(self):
        firstList = [1, 2, 3]
        secondList = [1, 2, 4]
        result = self.sut._findUniqueEntries(firstList, secondList)
        expectation = [3, 4]
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLocalizations(self):
        entry = IntermediateEntry("Key1", "Value1")
        
        germanLanguage = IntermediateLanguage("de", [entry])
        example = IntermediateLocalization("FileName", [germanLanguage])

        englishLanguage = IntermediateLanguage("en", [entry])
        otherExample = IntermediateLocalization("FileName", [englishLanguage])
        
        return (example, otherExample)

if __name__ == '__main__':
    unittest.main()