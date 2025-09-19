class Spreadsheet:
    def __init__(self, rows: int):
        self.values = dict()

    def setCell(self, cell: str, value: int) -> None:
        self.values[cell] = value

    def resetCell(self, cell: str) -> None:
        self.values[cell] = 0

    def getValue(self, formula: str) -> int:
        ans = 0
        for value in formula[1:].split("+"):
            try:
                ans += int(value)
            except ValueError:
                try:
                    ans += self.values[value]
                except KeyError:
                    pass
        return ans


# Your Spreadsheet object will be instantiated and called as such:
# obj = Spreadsheet(rows)
# obj.setCell(cell,value)
# obj.resetCell(cell)
# param_3 = obj.getValue(formula)
# param_3 = obj.getValue(formula)
