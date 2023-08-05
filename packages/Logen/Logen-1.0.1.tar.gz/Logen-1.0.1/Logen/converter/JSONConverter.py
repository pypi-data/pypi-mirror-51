from typing import List, Optional

from ..converter.ConverterInterface import ConverterInterface as Base
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile
from ..lib import JsonHelper

class JSONConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self) -> str: return ".json"

    def identifier(self) -> str: return "json"

    def importDescription(self) -> str: return "Takes a json file with the format '{}' and converts it into an intermediate localization.".format(self._commonFormatDescription())

    def exportDescription(self) -> str: return "Converts an intermediate localization into the format '{}' and exports it as a json file.".format(self._commonFormatDescription())

    def toIntermediate(self, filepath: str) -> Optional[IntermediateLocalization]:
        dict = JsonHelper.readJSON(filepath)

        # JsonHelper could not read json file at given path.
        if dict is None:
            return None

        for sectionKey, sectionValue in dict.items():

            listOfLanguages = []

            # Check for correct format of json.
            if not type(sectionValue) is type({}):
                return None

            for languageKey, localization in sectionValue.items():
                listOfEntries = []
                for key, value in localization.items():
                    # Even when "-signs are escaped in json, they are no longer escaped when converted to a dict.
                    # Thus escape them here again.
                    correctedValue = value.replace("\"", "\\\"")
                    entry = IntermediateEntry(key, correctedValue)
                    listOfEntries.append(entry)
                language = IntermediateLanguage(languageKey, listOfEntries)
                listOfLanguages.append(language)
            return IntermediateLocalization(sectionKey, listOfLanguages)
        
        # Default return, if json could not be converted.
        return None

    def fromIntermediate(self, intermediateLocalization: IntermediateLocalization) -> List[LocalizationFile]:
        localizationFiles = []

        localizationDict = {}
        languageDict = {}
        for language in intermediateLocalization.intermediateLanguages:

            entryDict = {}
            for entry in language.intermediateEntries:
                entryDict[entry.key] = entry.value
            
            languageDict[language.languageIdentifier] = entryDict
            localizationDict[intermediateLocalization.localizationIdentifier] = languageDict
            localizationContent = JsonHelper.dictToJSONString(localizationDict)

            filename = "{}{}".format(intermediateLocalization.localizationIdentifier, self.fileExtension())
            localizationFile = LocalizationFile(filename, localizationContent)
            localizationFiles.append(localizationFile)
        
        return localizationFiles

    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------

    def _commonFormatDescription(self) -> str: return "{ filename: { language: { key: value } } }"
