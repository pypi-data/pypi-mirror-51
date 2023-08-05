import unittest

from .. import main

class MainTests(unittest.TestCase):
    
    def test_parse_convert(self):   
        
        expectedFunction = main.subcommandConvert
        expectedSourcePath = "just/some/random/path"
        expectedDestinationPath = "just/another/random/path"
        expectedImporterIdentifier = "importConverter"
        expectedExporterIdentifier = "exportConverter"

        testArgs = [
            "convert", 
            expectedSourcePath,
            expectedDestinationPath,
            expectedImporterIdentifier,
            expectedExporterIdentifier,
            "--dryRun",
            "--verbose"
        ]
        
        parsedTestArgs = main.parse(testArgs)

        self.assertEqual(expectedFunction, parsedTestArgs.func)
        self.assertEqual(expectedSourcePath, parsedTestArgs.source)
        self.assertEqual(expectedDestinationPath, parsedTestArgs.destination)
        self.assertEqual(expectedImporterIdentifier, parsedTestArgs.importConverter)
        self.assertEqual(expectedExporterIdentifier, parsedTestArgs.exportConverter)
        self.assertTrue(parsedTestArgs.dryRun)
        self.assertTrue(parsedTestArgs.verbose)

    def test_parse_list(self):

        expectedFunction = main.subcommandList

        testArgs = [ "list" ]
        
        parsedTestArgs = main.parse(testArgs)
        self.assertEqual(expectedFunction, parsedTestArgs.func)

if __name__ == '__main__':
    unittest.main()