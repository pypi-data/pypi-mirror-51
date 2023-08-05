class LocalizationFile:

    def __init__(self, filepath: str, filecontent: str):
        self.filepath = filepath
        self.filecontent = filecontent

    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior"""
        if not isinstance(other, LocalizationFile): return NotImplemented
        return self.filepath == other.filepath and self.filecontent == other.filecontent

    def __str__(self) -> str:
         return "LocalizationFile:\nFilepath: {}\nContent: {}".format(self.filepath, self.filecontent)
