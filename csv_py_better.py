"""
A CSV import module that does better than the default one.

Works where "csv" and "readline" don't.

Advantages:
* Multiple delimiters
* Multiple string definers
* Can start at an arbitrary row
* Allows multiple lines in a cell (e.g., new_line in the middle of a cell is not split into two cells)

Disadvantages:
* It's slow. Would you rather accurate and slow or fast and wrong?
* Not memory efficient (reads data into a munge). Moore's Law - don't fail me now!

This code could be adapted to read a file gradually and write each new line as it's
calculated to a file to be more efficient. This one though is made for small data.
"""

from __future__ import unicode_literals
import os, os.path, sys, codecs


class CSVObject(object):
	"""
	This class instantiates a file object as an interable. It means that
	CSV files can be read more efficiently than reading the entire data
	into memory.
	"""
	def __init__(self, fileName, delims = ",", quotes = '"', lineEnd = None, headerRow = False, startRow = 0, encoding="utf-8"):
		self.fileName = fileName
		self.delims = delims
		self.quotes = quotes
		if lineEnd != None:
			self.lineEnd = lineEnd
		else:
			# use platform default
			self.lineEnd = os.linesep
		self.headerRow = headerRow # Is there a header row?
		self.startRow = startRow # starting row, defaults to 0
		self.encoding = encoding # encoding: Defaults to UTF-8. Good idea? :-/
		self.header = [] # actual header row
		self.outData = [] # stores the output data

	def Import(self):
		# Gets all data into a single bundle (list of lists - can be converted easily)
		fin = codecs.open(self.fileName, encoding=self.encoding)
		data = fin.read()
		fin.close()

		# Convert the data into a list of lines.
		# This must account for newlines within quotes being treated as a cell. It's a one process thing.
		inQuote = False # flag for being 'within' quotes. We're not yet...
		maybeLineEnding = False
		startNewLine = False
		token = '' # current token
		tokens = [] # list of tokens in this line
		rowNumber = 0 # record this to ensure we start from the right row
		for char in data: # iterate, iterate...
			if maybeLineEnding == True and char == self.lineEnd[1]: # Oh! Windows line ending second character match!
				startNewLine = True # Set this to ensure a new line is done below
				maybeLineEnding = False # Reset this
			if inQuote: # so if we're in the middle of a quote...
				if char == inQuoteChar: # ...and have a matching quote character...
					tokens.append(token) # add the token to list (ignore quote character)
					token = '' # and begin new token
					inQuote = False # flag that we're not in a quote any more
				else: # But if char is a non-matching quote...
					token += char # ...just add to token
			elif char in self.delims: # or if char is a delimiter...
				if len(token) > 0: # ...and token is worth recording...
					tokens.append(token) # add token to list
					token = '' # and begin new token
				else: # if token has 0 length and no content...
					pass # ...adjacent delimiters so do nothing
			elif char in self.quotes: # But if char is a quote...
				token = "" # Reset to remove starting spaces
				inQuoteChar = char # record it to check for matching quote later
				inQuote = True # and flag that we're in a quotation
			elif len(self.lineEnd) == 1 and char == self.lineEnd: # Non-Windows new line character?
				startNewLine = True # Set this to start a new line below
			elif len(self.lineEnd) > 1 and char == self.lineEnd[0]: # got first of windows line end chars
				maybeLineEnding = True # So we've got the first character of a Windows new line.
			elif startNewLine == False: # And if char is anything else...
				token += char # add to token

			if startNewLine == True:
				startNewLine = False
				rowNumber = rowNumber + 1
				if len(token) > 0: # Check if last item is worth recording (len > 0)
					tokens.append(token) # add to list of tokens
				if rowNumber >= self.startRow + 1: # Do we record this row or not?
					self.outData.append(tokens) # Yes, we do.
				inQuote = False # Reset for new row
				token = '' # Reset for new row
				tokens = [] # Reset for new row
		if headerRow == True: # All data read in. Is there a header?
			self.header = self.outData.pop(0) # If so, let's grab it from data

	def ReturnColumn(self, columnNumber):
		"""
		Returns a column of data. If cell (or indeed column), None value is substituted.
		A nice, useful function to read in CSV files and access column data at will.
		"""
		columnData = []
		if len(self.outData) > 0: # Check if there's data
			for idxRow in self.outData: # Iterate through the rows
				try:
					columnData.append(idxRow[columnNumber]) # Append...
				except IndexError: # But if not
					columnData.append(None) # Add none
		return columnData


if __name__ == "__main__":
	filename = "test.csv"
	delims = ",;"
	quotes = '"'
	lineEnd ="\r\n"
	headerRow =True
	startRow = 0
	testcase = CSVObject(filename, delims, quotes, lineEnd, headerRow)
	testcase.startRow = startRow
	testcase.Import()
	print("Header = ", testcase.header, len(testcase.header))
	print("Data   = ", testcase.outData)
	print("Column = ", testcase.ReturnColumn(0))
