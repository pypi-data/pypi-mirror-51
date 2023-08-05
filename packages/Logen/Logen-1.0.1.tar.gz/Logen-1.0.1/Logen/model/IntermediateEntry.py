class IntermediateEntry:

    def __init__(self, key: str, value: str, comment: str = ""):
        self.key = key
        self.value = value
        self.comment = comment

    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior"""
        if not isinstance(other, IntermediateEntry): return NotImplemented
        return self.key == other.key and self.value == other.value and self.comment == other.comment

    def __hash__(self) -> int:
        return (self.key + self.value + self.comment).__hash__()

    def __str__(self) -> str:
        return "   IntermediateEntry: " + self.key + ": " + self.value