import os
from typing import List, Optional

from ..converter.ConverterInterface import ConverterInterface as Base
from ..lib import FileHelper
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

class iOSEnumConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self) -> str: return ".swift"

    def identifier(self) -> str: return "ios_enum"

    def importDescription(self) -> str: return "No import possible."

    def exportDescription(self) -> str: return "Exports the content of an intermediate localization to a swift enum providing easy and convenience access to the keys."

    def toIntermediate(self, filepath: str) -> Optional[IntermediateLocalization]: raise NotImplementedError
        
    def fromIntermediate(self, intermediateLocalization: IntermediateLocalization) -> List[LocalizationFile]:
        listOfLocalizationFiles = []

        content = self._makeiOSGeneratedWarning()
        content += FileHelper.readFile("Logen/templates/template_ios_enum_documentation.txt")

        filename = self._makeFilename(intermediateLocalization.localizationIdentifier)

        # Keys are equal for every language, thus just use the first one.
        language = intermediateLocalization.intermediateLanguages[0]

        content += "extension LocalizableKeys {\n"
        content += "    enum {0}: String {{\n".format(intermediateLocalization.localizationIdentifier)
        for entry in language.intermediateEntries:
            content += self._makeIOSEnumEntry(entry.key)
        content += "    }\n"
        content += "}"

        localizationFile = LocalizationFile(filename, content)
        listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles
        
    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------

    def _makeiOSGeneratedWarning(self) -> str:
        warning = FileHelper.readFile("Logen/templates/template_common_generated_warning.txt")
        return "/*\n{}\n */\n".format(warning)

    def _makeFilename(self, sectionKey: str) -> str:
        # This line capitalizes the first letter in the sectionKey.
        # This is used as part of the filename, so it will be capitalizesd as it should be.
        # We can't use .capitalize() or .title() because that would lowercase all other chars.
        sectionName = ' '.join(word[0].upper() + word[1:] for word in sectionKey.split())
        return "{}LocalizableKeys.swift".format(sectionName)

    def _makeIOSEnumEntry(self, key: str) -> str:
        newKey = key.replace(".", "_")
        return "        case {} = \"{}\"\n".format(newKey, key)