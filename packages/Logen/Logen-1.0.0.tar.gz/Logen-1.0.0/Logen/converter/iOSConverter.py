import os
from typing import List, Optional

from ..converter.ConverterInterface import ConverterInterface as Base
from ..lib import FileHelper
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

class iOSConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self) -> str: return ".strings"

    def identifier(self) -> str: return "ios"

    def importDescription(self) -> str: return "Imports a '.strings' file containing the localization of an iOS app and converts it to an intermediate localization. Ignores all lines exept lines with a key-value-pair."

    def exportDescription(self) -> str: return "Exports the content of an intermediate localization to a '.strings' file for an iOS app."

    def toIntermediate(self, filepath: str) -> Optional[IntermediateLocalization]:
        localizationIdentifier = self._localizationIdentifierFromFilepath(filepath)
        languageIdentifier = self._languageIdentifierFromFilepath(filepath)

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []

        # A line may or may not contain a comment. Start with an empty string as default.
        comment = ""

        for line in lines:
            if ("//" in line) or ("/*" in line and "*/" in line):
                # The next line may containe a entry with a comment.
                comment = self._extractCommentFromLine(line)
                continue

            if line.startswith("\""):
                key = self._extractKeyFromLine(line)
                value = self._extractValueFromLine(line)
                intermediateEntries.append(IntermediateEntry(key, value, comment))

            # Reset value of comment for next line.
            comment = ""

        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

    def fromIntermediate(self, intermediateLocalization: IntermediateLocalization) -> List[LocalizationFile]:
        listOfLocalizationFiles = []

        sectionHeaderTemplate = FileHelper.readFile("Logen/templates/template_ios_section_header.txt")

        for language in intermediateLocalization.intermediateLanguages:

            content = self._makeiOSGeneratedWarning()
            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.intermediateEntries:
                content += self._lineFromIntermediateEntry(entry)

            filename = "{}.lproj/{}.strings".format(language.languageIdentifier, intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------
    
    def _localizationIdentifierFromFilepath(self, filepath: str) -> str:
        filename = os.path.basename(filepath)
        return filename.replace(".strings", "")

    def _languageIdentifierFromFilepath(self, filepath: str) -> str:
        foldername = os.path.dirname(filepath).split("/")[-1]
        return foldername.replace(".lproj", "")

    # Currently just sopports one line commands.
    def _extractCommentFromLine(self, line: str) -> str:
        comment = self._correctEntry(line)
        if comment.startswith("//"):
            comment = comment[2:]
        if (comment.startswith("/*") and comment.endswith("*/")):
            comment = comment[2:-2]
        while comment.startswith(" "):
            comment = comment[1:]
        while comment.endswith(" "):
            comment = comment[:-1]
        return comment

    def _extractKeyFromLine(self, line: str) -> str:
        # Split line between key and value.
        # This will not work, if there is a "=" in the key!
        key = line.split("=")[0]
        key = self._correctEntry(key)
        return key

    def _extractValueFromLine(self, line: str) -> str:
        value = line.split("=", 1)[1][:-1] # Split string on first occurence of =, take second part and cut out last character (;)
        value = self._correctEntry(value)
        value.replace("\"", "\\\"")
        return value

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

    def _makeiOSGeneratedWarning(self) -> str:
        warning = FileHelper.readFile("Logen/templates/template_common_generated_warning.txt")
        return "/*\n{}\n */\n".format(warning)

    def _lineFromIntermediateEntry(self, entry: IntermediateEntry) -> str:
        # add comment
        line = ""
        if entry.comment != "":
            line += "/* {} */\n".format(entry.comment)
        value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
        line += "\"{}\" = \"{}\";\n".format(entry.key, value)
        return line