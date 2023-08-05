import unittest

from ..lib import FileHelper
from ..lib import JsonHelper

from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

from ..converter.iOSConverter import iOSConverter

from ..tests import TestHelper

class TestiOSConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = iOSConverter()

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    def test_toIntermediate(self):
        expectation = TestHelper.createExampleIntermediateLocalization(addComment = True)
        result = self.sut.toIntermediate("Logen/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        self.assertEqual(expectation, result, msg = TestHelper.errorMessageForIntermediateLocalization(expectation, result))

    def test_toIntermediate_noComments(self):
        # Create an expectation without comments.
        # The default localizationIdentifier needs to be changed, because it is constructed from the input filepath. 
        # Thus it will be "FileName_noComments" and not "FileName".
        expectation = TestHelper.createExampleIntermediateLocalization(
            addComment = False,
            localizationId = "FileName_noComments"
        )
        
        result = self.sut.toIntermediate("Logen/tests/testdata/ExampleLanguage.lproj/FileName_noComments.strings")
        self.assertEqual(expectation, result, msg = TestHelper.errorMessageForIntermediateLocalization(expectation, result))

    def test_fromIntermediate(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("Logen/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = TestHelper.createExampleIntermediateLocalization(addComment = True)
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result)

    def test_fromIntermediate_noComments(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("Logen/tests/testdata/ExampleLanguage.lproj/FileName_noComments.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = TestHelper.createExampleIntermediateLocalization(addComment = False)
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result, msg = TestHelper.errorMessageForLocalizationFile(expectation, result))

    #--------------------------------------------------
    # Testcases for helper methods
    #--------------------------------------------------

    def test_localizationIdentifierFromFilepath(self):
        filepath = "/some/filepath/de.lproj/TestIdentifier.strings"
        result = self.sut._localizationIdentifierFromFilepath(filepath)
        expectation = "TestIdentifier"
        self.assertEqual(expectation, result)

    def test_languageIdentifierFromFilepath(self):
        filepath = "/some/filepath/de.lproj/TestIdentifier.strings"
        result = self.sut._languageIdentifierFromFilepath(filepath)
        expectation = "de"
        self.assertEqual(expectation, result)

    def test_extractKeyFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        key = self.sut._extractKeyFromLine(line)
        self.assertEqual("someKey", key)

    def test_correctKey(self):
        self.assertEqual("key", self.sut._correctEntry("key"))
        self.assertEqual("key", self.sut._correctEntry("   key"))
        self.assertEqual("key", self.sut._correctEntry("key   "))
        self.assertEqual("key", self.sut._correctEntry("\"key\""))
        self.assertEqual("key", self.sut._correctEntry("   \"key\""))
        self.assertEqual("key", self.sut._correctEntry("\"key\"   "))
        self.assertEqual("key", self.sut._correctEntry("   \"key\"   "))

    def test_extractValueFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        value = self.sut._extractValueFromLine(line)
        self.assertEqual("someValue", value)

    def test__lineFromIntermediateEntry_WithComment(self):
        entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
        expectation = "/* This is just a nonsence example. */\n\"Key1\" = \"Value1\";\n"
        result = self.sut._lineFromIntermediateEntry(entry)
        self.assertEqual(expectation, result)

    def test__lineFromIntermediateEntry_WithoutComment(self):
        entry = IntermediateEntry("Key1", "Value1")
        expectation = "\"Key1\" = \"Value1\";\n"
        result = self.sut._lineFromIntermediateEntry(entry)
        self.assertEqual(expectation, result)

if __name__ == '__main__':
    unittest.main()