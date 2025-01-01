"""
A CSV import module that does better than the default one. MIT license.

Works where "csv" and "readline" don't.

Advantages:
* Multiple delimiters
* Multiple string definers
* Can start at an arbitrary row
* Allows multiple lines in a cell (e.g., new_line in the middle of a cell is
  not split into two cells)

Disadvantages:
* It's slow. Would you rather accurate and slow or fast and wrong?
* Not memory efficient (reads data into a munge). Moore's Law - don't
  fail me now!

This code could be adapted to read a file gradually and write each
new line as it's calculated to a file to be more efficient. This one
though is made for small data.
"""

from __future__ import unicode_literals
import os
import os.path
import codecs


def makeNumber(valueString):
    try:
        returnVal = int(valueString)
    except ValueError:
        try:
            returnVal = float(valueString)
        except ValueError:
            returnVal = valueString
    return returnVal


def ReadWholeCSV(fileName, delims=",", quotes='"', lineEnd=None,
                 headerRow=False, startRow=0, encoding="utf-8"):
    """
    Reads the whole of a file and attempts to return it as a list of lists
    that can be converted to a CSV file.
    """
    # Gets all data into a single bundle (list of lists - converted easily)
    fin = codecs.open(fileName, encoding=encoding)
    data = fin.read()
    fin.close()
    # Convert the data into a list of lines.
    # Accounts for newlines in quotes being one cell. It's a 1 pass process.
    outData = []  # Stores all the data
    inQuote = False  # flag for being 'within' quotes. We're not yet...
    maybeLineEnding = False
    startNewLine = False
    token = '' # current token
    tokens = [] # list of tokens in this line
    rowNumber = 0 # record this to ensure we start from the right row
    for char in data: # iterate, iterate...
        if maybeLineEnding is True and char == lineEnd[1]:
            # 2nd character match!
            startNewLine = True # Set this to ensure a new line is done below
            maybeLineEnding = False # Reset this
        if inQuote: # We're in the middle of a quote...
            if char == inQuoteChar: # ...and have a matching quote character...
                tokens.append(token)
                # add the token to list (ignore quote character)
                token = '' # and begin new token
                inQuote = False # flag that we're not in a quote any more
            else: # But if char is a non-matching quote...
                token += char # ... add char to token
        elif char in delims: # or if char is a delimiter...
            token = makeNumber(token)
            tokens.append(token) # add token to list
            token = '' # and begin new token
        elif char in quotes: # But if char is a quote...
            token = "" # Reset to remove starting spaces
            inQuoteChar = char
            # record it to check for matching quote later
            # (remember multiple quote chars?)
            inQuote = True # and flag that we're now in a quotation
        elif len(lineEnd) == 1 and char == lineEnd:
            # Non-Windows new line character?
            startNewLine = True # Set this to start a new line below
        elif len(lineEnd) > 1 and char == lineEnd[0]: # got first of windows line end chars
            maybeLineEnding = True # So we've got the first character of a Windows new line.
        elif startNewLine is False: # And if char is anything else...
            token += char # add to token
        # We now have a complete single line here
        if startNewLine is True:
            startNewLine = False
            rowNumber = rowNumber + 1
            if len(token) > 0: # Check if last item is worth recording (len > 0)
                tokens.append(token) # add to list of tokens
            if rowNumber >= startRow + 1: # Do we record this row or not?
                outData.append(tokens) # Yes, we do.
            inQuote = False # Reset for new row
            token = '' # Reset for new row
            tokens = [] # Reset for new row
    if headerRow is True: # All data read in. Is there a header?
        header = outData.pop(0) # If so, let's grab it from data
    return header, outData


def ReturnColumn(data, columnNumber):
    """
    Returns a column of data. If cell (or indeed column) does not exist,
    a None value is substituted.
    A nice, useful function to read in CSV files and access column data at will.
    """
    columnData = []
    if len(data) > 0: # Check if there's data
        for idxRow in data: # Iterate through the rows
            try:
                columnData.append(idxRow[columnNumber]) # Append...
            except IndexError: # But if not
                columnData.append(None) # Add none
    return columnData


class CSVObject(object):
    """
    This class instantiates a file object as an interable. It means that
    CSV files can be read more efficiently than reading the entire data
    into memory.

    It might be slow because it opens the file and reads the line then closes
    the file again. This is rather than leave the file open because the
    demand might need time between reads.
    """
    def __init__(self, fileName, delims=",", quotes='"', lineEnd=None,
                 headerRow=False, startRow=0, encoding="utf-8"):
        self.fileName = fileName
        self.delims = delims
        self.quotes = quotes
        if lineEnd is not None:
            self.lineEnd = lineEnd
        else:
            # use platform default
            self.lineEnd = os.linesep
        self.headerRow = headerRow # Is there a header row?
        self.startRow = startRow # starting row, defaults to 0
        self.encoding = encoding # encoding: Defaults to UTF-8. Good idea? :-/
        self.header = [] # actual header row
        self.outData = [] # stores the output data
        self.charIndex = 0 # the index of the character being read
        self.rowNumber = 0 # record this to ensure we start from the right row
        # Attempts to open the file

    def __iter__(self):
        return self

    def __next__(self):
        # find the correct row number to start from
        while 1:
            if self.rowNumber < self.startRow:
                # Read in unneeded lines and continue
                self.fin = codecs.open(self.fileName, encoding=self.encoding)
                line = self.GetSingleLine()
                self.fin.close()
            else:
                # Read in needed lines and return them
                self.fin = codecs.open(self.fileName, encoding=self.encoding)
                line = self.GetSingleLine()
                self.fin.close()
                return line

    def GetSingleLine(self):
        # Reads the next line from the position of charIndex onwards.
        self.fin.seek(self.charIndex)
        # This must account for newlines within quotes being treated as a cell. It's a one process thing.
        inQuote = False # flag for being 'within' quotes. We're not yet...
        maybeLineEnding = False
        startNewLine = False
        token = '' # current token
        tokens = [] # list of tokens in this line
        while 1: # iterate, iterate...
            char = self.fin.read(1)
            if char != '':
                # If not yet end-of-file, let's read in some data
                if maybeLineEnding is True and char == self.lineEnd[1]: # Oh! Windows line ending second character match!
                    startNewLine = True # Set this to ensure a new line is done below
                    maybeLineEnding = False # Reset this
                if inQuote: # We're in the middle of a quote...
                    if char == inQuoteChar: # ...and have a matching quote character...
                        tokens.append(token) # add the token to list (ignore quote character)
                        token = '' # and begin new token
                        inQuote = False # flag that we're not in a quote any more
                    else: # But if char is a non-matching quote...
                        token += char # ... add char to token
                elif char in self.delims: # or if char is a delimiter...
                    token = makeNumber(token)
                    tokens.append(token) # add token to list
                    token = '' # and begin new token
                elif char in self.quotes: # But if char is a quote...
                    token = "" # Reset to remove starting spaces
                    inQuoteChar = char # record it to check for matching quote later (remember multiple quote chars?)
                    inQuote = True # and flag that we're now in a quotation
                elif len(self.lineEnd) == 1 and char == self.lineEnd: # Non-Windows new line character?
                    startNewLine = True # Set this to start a new line below
                elif len(self.lineEnd) > 1 and char == self.lineEnd[0]: # got first of windows line end chars
                    maybeLineEnding = True # So we've got the first character of a Windows new line.
                elif startNewLine is False: # And if char is anything else...
                    token += char # add to token
                if startNewLine is True:
                    # We now have a complete single line here
                    startNewLine = False
                    if len(token) > 0: # Check if last item is worth recording (len > 0)
                        tokens.append(token) # add to list of tokens
                    if self.rowNumber >= self.startRow + 1: # Do we record this row or not?
                        self.outData.append(tokens) # Yes, we do.
                    self.rowNumber = self.rowNumber + 1 # Add another row number to read correct rows in
                    self.charIndex = self.fin.tell() # Get new file position for next read
                    return tokens
            else:
                raise StopIteration


if __name__ == "__main__":
    """
    Just some code to test
    """
    filename = "test.csv"
    delims = ",;"
    quotes = '"'
    lineEnd = "\r\n"
    headerRow = True
    startRow = 0
    header, data = ReadWholeCSV(filename, delims, quotes, lineEnd, headerRow, startRow)
    # testcase = CSVObject(filename, delims, quotes, lineEnd, headerRow)
    # testcase.startRow = startRow
    # testcase.Import()
    print()
    print("TESTING FUNCTION VERSION")
    print(header)
    for row in data:
        print(row)
    print(ReturnColumn(data, 0))
    print()
    print("TESTING ITERATOR VERSION")
    testCase2 = CSVObject(filename, delims, quotes, lineEnd, headerRow, startRow)
    for row in testCase2:
        print(row)
