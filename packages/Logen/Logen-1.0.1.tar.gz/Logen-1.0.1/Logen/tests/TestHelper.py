import difflib
from typing import List

from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

def createExampleIntermediateLocalization(
    addComment: bool,
    localizationId: str = "FileName"
) -> IntermediateLocalization:

    if addComment:
        entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
    else: 
        entry = IntermediateEntry("Key1", "Value1")
    language = IntermediateLanguage("ExampleLanguage", [entry])
    return IntermediateLocalization(localizationId, [language])

def errorMessageForLocalizationFile( 
    expectation: LocalizationFile,
    actual: LocalizationFile
) -> str:

    errorMessage = ""
    if expectation.filepath != actual.filepath:
        errorMessage += "Different filepath\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.filepath)
        errorMessage += "\t- actual:      {}\n".format(actual.filepath)
    if expectation.filecontent != actual.filecontent:
        errorMessage += "Different filecontent\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.filecontent)
        errorMessage += "\t- actual:      {}\n".format(actual.filecontent)
    return errorMessage

def errorMessageForIntermediateLocalization( 
    expectation: IntermediateLocalization, 
    actual: IntermediateLocalization
) -> str:

    errorMessage = ""
    if expectation.localizationIdentifier != actual.localizationIdentifier:
        errorMessage += "Different localizationIdentifier\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.localizationIdentifier)
        errorMessage += "\t- actual:      {}\n".format(actual.localizationIdentifier)
    if expectation.intermediateLanguages != actual.intermediateLanguages:
        if len(expectation.intermediateLanguages) != len(actual.intermediateLanguages):
            errorMessage += "Different length of intermediate languages:\n"
            errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateLanguages))
            errorMessage += "\t- actual:      {}\n".format(len(actual.intermediateLanguages))
        for index in range(0, min(len(expectation.intermediateLanguages), len(actual.intermediateLanguages))):
            errorMessage += errorMessageForIntermediateLanguage(expectation.intermediateLanguages[index], actual.intermediateLanguages[index])
    return errorMessage

def errorMessageForIntermediateLanguage( 
    expectation: IntermediateLanguage, 
    actual: IntermediateLanguage
) -> str:

    errorMessage = ""
    if expectation.languageIdentifier != actual.languageIdentifier:
        errorMessage += "Different languageIdentifier\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.languageIdentifier)
        errorMessage += "\t- actual:      {}\n".format(actual.languageIdentifier)
    if expectation.intermediateEntries != actual.intermediateEntries:
        if len(expectation.intermediateEntries) != len(actual.intermediateEntries):
            errorMessage += "Different length of intermediateEntries:\n"
            errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateEntries))
            errorMessage += "\t- actual:      {}\n".format(len(actual.intermediateEntries))
        for index in range(0, min(len(expectation.intermediateEntries), len(actual.intermediateEntries))):
            errorMessage += errorMessageForIntermediateEntry(expectation.intermediateEntries[index], actual.intermediateEntries[index])
    return errorMessage

def errorMessageForIntermediateEntry( 
    expectation: IntermediateEntry, 
    actual: IntermediateEntry
) -> str:
    errorMessage = ""
    if expectation.key != actual.key:
        errorMessage += "Different key\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.key)
        errorMessage += "\t- actual:      {}\n".format(actual.key)
    if expectation.value != actual.value:
        errorMessage += "Different value for entry with key: {}\n".format(expectation.key)
        errorMessage += "\t- expectation: {}\n".format(expectation.value)
        errorMessage += "\t- actual:      {}\n".format(actual.value)
        errorMessage += "Diff: {} at {}\n".format(diff_content(expectation.value, actual.value), diff_positions(expectation.value, actual.value))
    if expectation.comment != actual.comment:
        errorMessage += "Different comment for entry with key: {}\n".format(expectation.key)
        errorMessage += "\t- expectation: {}\n".format(expectation.comment)
        errorMessage += "\t- actual:      {}\n".format(actual.comment)
        errorMessage += "Diff: {} at {}\n".format(diff_content(expectation.comment, actual.comment), diff_positions(expectation.comment, actual.comment))
    return errorMessage

def diff_content(a: str, b: str) -> List[str]:
    return [li for li in difflib.ndiff(a, b) if li[0] != ' ']

def diff_positions(a: str, b: str) -> List[int]:
    minimumLength = min(len(a), len(b))
    return [i for i in range(0, minimumLength) if a[i] != b[i]]