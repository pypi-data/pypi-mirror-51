import unittest

from .ConverterSpy import ConverterSpy
from .. import main_subcommand_convert
from .. import main

class SubcommandConvertTests(unittest.TestCase):

    def test_start(self):

        # setup spy for import
        importSpy = ConverterSpy()
        importSpy.changeIdentifierTo("import")
        importSpy.changeFileExtensionTo(".json")

        # setup spy for export
        exportSpy = ConverterSpy()
        exportSpy.changeIdentifierTo("export")

        # setup arguments
        testArgs = [
            "convert", 
            "Logen/tests/testdata/ExampleJSON_comments.json",
            "just/some/path",
            "import",
            "export",
            "--dryRun"
        ]
        parsedTestArgs = main.parse(testArgs)

        # execute 
        main_subcommand_convert.start(parsedTestArgs, [importSpy, exportSpy])

        # validate
        self.assertTrue(importSpy.didImport())
        self.assertFalse(importSpy.didExport())
        self.assertTrue(exportSpy.didExport())
        self.assertFalse(exportSpy.didImport())
    
    def test_importToIntermediateLocalization(self):
        """Assures that given a converter with correct identifier, the converter is used correctly."""
        
        # prepare sut
        main_subcommand_convert.importConverterIdentifier = "spy"

        # setup spy
        spy = ConverterSpy()
        spy.changeIdentifierTo("spy")

        # define test parameter
        testSourcePath = ""
        converter = [spy]

        # execute and validate
        main_subcommand_convert._importToIntermediateLocalization(testSourcePath, converter)        
        self.assertTrue(spy.didImport)

if __name__ == '__main__':
    unittest.main()