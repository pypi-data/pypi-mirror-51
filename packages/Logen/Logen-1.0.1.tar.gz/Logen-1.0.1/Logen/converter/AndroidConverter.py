import os
from typing import List, Optional, Tuple

from ..converter.ConverterInterface import ConverterInterface as Base
from ..lib import FileHelper
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

class AndroidConverter(Base):

    #--------------------------------------------------
    # private properties
    #--------------------------------------------------

    _nameTagOpenStart = "<string name=\""
    _nameTagOpenEnd = "\">"
    _nameTagClose = "</string>"
    _folderNamePrefix = "values-"

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self) -> str:
        return ".xml"

    def identifier(self) -> str: 
        return "android" 

    def importDescription(self) -> str: 
        return "Parses the given '.xml' file and creates an intermediate localization. All lines which don't contain a localized string, are ignored."

    def exportDescription(self) -> str: 
        return "Writes the content of an intermediate localization to a '.xml' file for an Android app. It prefixes all keys with the identifier of the file for easier autocompletion on Android side."

    def toIntermediate(
        self,
        filepath: str
    ) -> IntermediateLocalization:
        filename = FileHelper.filename(filepath)
        localizationIdentifier = filename.replace(self.fileExtension(), "")

        foldername = FileHelper.directoryName(filepath)
        languageIdentifier = foldername.replace(self._folderNamePrefix, "")

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []

        # A line may or may not contain a comment. Start with an empty string as default.
        comment = ""

        for line in lines: 
            if "<!--" in line and "-->" in line:
                # The next line may containe a entry with a comment.
                comment = self._extractComment(line)
                continue

            entry = self._processLine(line, localizationIdentifier, comment)
            if entry is not None:
                intermediateEntries.append(entry)

            # Reset value of comment for next line.
            comment = ""
        
        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

    def fromIntermediate(
        self,
        intermediateLocalization: IntermediateLocalization
    ) -> List[LocalizationFile]:
        identifier = intermediateLocalization.localizationIdentifier
        languages = intermediateLocalization.intermediateLanguages
        listOfLocalizationFiles = []
        for language in languages:
            filename = "values-{}/{}.xml".format(language.languageIdentifier, identifier)
            content = "\n    <!-- {} --> \n\n".format(identifier)
            for entry in language.intermediateEntries:
                androidKey = "{}.{}".format(identifier, entry.key)
                content += self._makeAndroidEntry(androidKey, entry.value, entry.comment)

            filecontent = self._makeAndroidGeneratedWarning() + FileHelper.readFile("Logen/templates/template_android_resource_file.txt").format(content)
            localizationFile = LocalizationFile(filename, filecontent)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------

    def _processLine(
        self, 
        line: str, 
        localizationIdentifier: str, 
        comment: str = ""
    ) -> Optional[IntermediateEntry]:

        if not self._validLine(line):
            return None

        # remove leading whitespace
        while line.startswith(" "):
            line = line[1:]

        (key, line) = self._extractKey(line, localizationIdentifier)
        (value, _) = self._extractValue(line)
        
        return IntermediateEntry(key, value, comment)

    def _validLine(self, line: str) -> bool:
        return self._nameTagOpenStart in line and self._nameTagClose in line

    def _extractComment(self, line: str) -> str:
        comment = line

        # remove leading whitespaces before comment tag
        while comment.startswith(" "):
            comment = comment[1:]

        # remove trailing whitespaces after comment tag
        while comment.endswith(" "):
            comment = comment[:len(comment) - 1]

        # remove start of comment tag
        if comment.startswith("<!--"):
            comment = comment.replace("<!--", "")

        # remove end of comment tag
        if comment.endswith("-->"):
            comment = comment.replace("-->", "")
        
        # remove leading whitespaces before comment
        while comment.startswith(" "):
            comment = comment[1:]
        
        # remove trailing whitespaces after comment
        while comment.endswith(" "):
            comment = comment[:len(comment) - 1]
        return comment

    def _extractKey(self, line: str, localizationIdentifier: str) -> Tuple[str, str]:
        # Remove start of name tag.
        if line.startswith(self._nameTagOpenStart):
            prefixLength = len(self._nameTagOpenStart)
            line = line[prefixLength:]

        # Remove name attribute and save it as key.
        key = ""
        while not line.startswith(self._nameTagOpenEnd):
            key += line[:1]
            line = line[1:]
        key = self._correctEntry(key)

        # This converter prefixes any generated android localization key with "localizationIdentifier.".
        # Remove them here to get a valid IntermediateEntry which is comparable and thus mergable.
        keyPrefix = "{}.".format(localizationIdentifier)
        key = key.replace(keyPrefix, "")

        # Remove end of name tag
        if line.startswith(self._nameTagOpenEnd):
            line = line[2:]

        return (key, line)

    def _extractValue(self, line: str) -> Tuple[str, str]:
        # Remove and save value until end of line.
        value = ""
        while not line.startswith(self._nameTagClose):
            value += line[:1]
            line = line[1:]
        value = self._correctEntry(value)
        value.replace("\"", "\\\"")
        return (value, line)

    def _correctEntry(self, input: str) -> str:
        entry = input
        while entry.startswith(" "):  # Remove leading whitespaces from key
            entry = entry[1:]
        if entry.startswith("\""):    # Remove leading quote sign
            entry = entry[1:]
        while entry.endswith(" "):    # Remove trainling whitespaces from key
            entry = entry[:-1]
        if entry.endswith("\""):      # Remove trailing quote sign
            entry = entry[:-1]
        return entry

    def _makeAndroidGeneratedWarning(self) -> str:
        warning = FileHelper.readFile("Logen/templates/template_common_generated_warning.txt")
        return "<!-- \n{} \n-->\n\n".format(warning)

    def _makeAndroidEntry(
        self, 
        key: str, 
        value: str, 
        comment: str
    ) -> str:
        value = value.replace("\"", "\\\"")
        value = value.replace("'", "\\'")
        return "    <!-- {} -->\n    <string name=\"{}\">{}</string>\n".format(comment, key, value)
