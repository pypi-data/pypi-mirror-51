import abc
from typing import List, Optional

from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile
from ..model.MergeResult import MergeResult

class ConverterInterface:
    """
    Used as a base for all converter. 
    Defines some methods that need to be implemented by conforming converter and some common methods for all converter.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def fileExtension(self) -> str: 
        """A string which defines the extensions of files that can be processed by the specific subclass of converter.

        Returns
        -------
            A string containing the extension of a file that can be processed by the specific subclass of converter.

        Raises
        ------
        NotImplementedError
            If this method is not overriden by a subclass.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def identifier(self) -> str: 
        """A string which identifies a specific subclass of converter to select it in the subcommand 'convert'.

        Returns
        -------
            A string containing the identifier of the specific subclass of converter to identify it and make it selectable by the command line.

        Raises
        ------
        NotImplementedError
            If this method is not overriden by a subclass.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def importDescription(self) -> str: 
        """Contains a description of the import function of a specific converter which will be shown by the 'list' subcommand.

        Returns
        -------
            A string describing the import function of a specific subclass of converter. This description will be shown by the 'list' subcommand.

        Raises
        ------
        NotImplementedError
            If this method is not overriden by a subclass.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def exportDescription(self) -> str: 
        """Contains a description of the export function of a specific converter which will be shown by the 'list' subcommand.

        Returns
        -------
            A string describing the export function of a specific subclass of converter. This description will be shown by the 'list' subcommand.

        Raises
        ------
        NotImplementedError
            If this method is not overriden by a subclass.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def toIntermediate(
        self,
        filepath: str
    ) -> Optional[IntermediateLocalization]:
        """Reads content of file at given filepath and converts it to an IntermediateLocalization.
        
        Parameters
        ----------
        filepath: str
            Path to file from which the content will be converted to an intermediate localization.

        Returns
        -------
        IntermediateLocalization:
            Instance of class IntermediateLocalization containing the converted content of the file.

        Raises
        ------
        NotImplementedError
            If no converting method is available for the content.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def fromIntermediate(
        self, 
        intermediateLocalization: IntermediateLocalization
    ) -> List[LocalizationFile]: 
        """Converts intermediate localization to specific format.
        
        Parameters
        ----------
        intermediateLocalization: IntermediateLocalization
            The intermediate localization to be converted.

        Returns
        -------
        [LocalizationFile]:
            A list of LocalizationFiles encapsulating filepath and content.

        Raises
        ------
        NotImplementedError
            If no converting method is available for this intermediate localization.
        """
        raise NotImplementedError


    def merge(
        self, 
        first: IntermediateLocalization, 
        second: IntermediateLocalization
    ) -> Optional[MergeResult]:
        """Merges the two given intermediate localizations together into one.

        There may be cases, where it is useful to merge two intermediate localizations together.
        E.g. when using the ios converter and there is one file 'de.lproj/File.strings' and one 'en.lproj/File.strings',
        than the end result should be one single intermediate localization with both languages combined.
        Another aproach would be to handle this case when importing a folder of multiple '*.lproj' directorys,
        but this would need a special handling on importing. And how should other setups be handled?
        Thus it is easier to add this method for merging two intermediate localizations together.
        
        Parameters
        ----------
        first: IntermediateLocalization
            The first intermediate localization to be merged with the other one.
        
        second: IntermediateLocalization
            The second intermediate localization to be merged with the other one

        Returns
        -------
        MergeResult:
            An instance of MergeResult encapsulating the new merged intermediate localization as well as a list of intermediate entries that were only contained by one of the two original intermediate localizations.
            May also return None, when the two given intermediate localizations don't have the same localizationIdentifier.
        """

        # Make sure, both are objects of type IntermeditateLocalization.
        if not type(first) is IntermediateLocalization or not type(second) is IntermediateLocalization:
            return None

        # Make sure, both have the same identifier, else cancel.
        if not first.localizationIdentifier == second.localizationIdentifier:
            return None

        languages = first.intermediateLanguages + second.intermediateLanguages

        listOfMissingEntries: List[IntermediateEntry] = []
        for firstLanguage in first.intermediateLanguages:
            for secondLanguage in second.intermediateLanguages:
                listOfMissingEntries += self._findUniqueEntries(firstLanguage.intermediateEntries, secondLanguage.intermediateEntries)

        return MergeResult(IntermediateLocalization(first.localizationIdentifier, languages), listOfMissingEntries)

    def _findUniqueEntries(
        self, 
        firstList: list,
        secondList: list
    ) -> list:
        for item in firstList[:]:
            if item in secondList:
                # Remove items, that are in both lists.
                firstList = list(filter(lambda x: x != item, firstList))
                secondList = list(filter(lambda x: x != item, secondList))

        # Return remainig items, which are only in one of both lists.
        return firstList + secondList
