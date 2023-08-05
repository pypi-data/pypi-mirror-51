import unittest

from ..converter.JSONConverter import JSONConverter
from ..lib import FileHelper, JsonHelper
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

from ..tests import TestHelper

class TestJSONConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = JSONConverter()

    #--------------------------------------------------
    # Testcases
    #--------------------------------------------------

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        dict = JsonHelper.readJSON("Logen/tests/testdata/ExampleJSON_noComments.json")
        expectation = JsonHelper.dictToJSONString(dict).replace('\n', '').replace(' ', '')

        exampleDict = self._createExampleDict()
        result = JsonHelper.dictToJSONString(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_toIntermediate(self):
        """Assures equality between converted dict and expected intermediate representation"""
        expectation = TestHelper.createExampleIntermediateLocalization(addComment = False)
        result = self.sut.toIntermediate("Logen/tests/testdata/ExampleJSON_noComments.json")
        self.assertEqual(expectation, result)

    def test_fromIntermediate(self):
        """Assures equality between json dict created from intermediate localization and expected content of file."""
        expectedFilepath = "FileName.json"
        expectedDict = JsonHelper.readJSON("Logen/tests/testdata/ExampleJSON_noComments.json")
        expectedContent = JsonHelper.dictToJSONString(expectedDict)
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        localization = TestHelper.createExampleIntermediateLocalization(addComment = False)
        result = self.sut.fromIntermediate(localization)[0]
        self.assertEqual(expectation, result, msg=TestHelper.errorMessageForLocalizationFile(expectation, result))

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleDict(self):
        entriesDict = {}
        entriesDict["Key1"] = "Value1"

        languageDict = {}
        languageDict["ExampleLanguage"] = entriesDict

        fileDict = {}
        fileDict["FileName"] = languageDict
        return fileDict

if __name__ == '__main__':
    unittest.main()
