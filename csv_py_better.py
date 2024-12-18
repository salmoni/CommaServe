


"""
A CSV import module that does better than the default one. 

Advantages:
* Multiple delimiters
* Multiple string definers
* Can start at an arbitrary row
* Allows multiple lines (e.g., new_line in the middle of a cell is not split into two cells)

Disadvantages:
* It's slow. Would you rather accurate and slow or fast and wrong?
* Not memory efficient. Moore's Law - don't fail me now!
"""

from __future__ import unicode_literals
import os, os.path, sys, codecs

class CSVObject(object):
	"""
	This class instantiates a file object as an interable. It means that
	CSV files can be read more efficiently than reading the entire data
	into memory.
	"""
	def __init__(self, fileName, delims, quotes, lineend, headerrow = False, startRow = 0):
		self.fileName = fileName
		self.delims = delims
		self.quotes = quotes
		self.lineend = lineend
		self.headerrow = headerrow # Is there a header row? 
		self.startRow = startRow # starting row, defaults to 0
		self.NumberCols = 0
		self.NumberRows = 0
		self.header = [] # actual header row
		self.outdata = [] # stores the output data

	def __iter__(self):
		return self

	def next(self):
		line = self.fin.next()
		return self.ParseLine(line)

	def Import(self):
		# Get all data into a single bundle
		fin = codecs.open(self.fileName, encoding='utf-8')
		data = fin.read()
		fin.close()
		# Figure out if the line ending is not supplied
		if self.lineend == None:
			lineterm = "\n"
			lineEnds = ['\n','\r\n','\r']
			maxes = []
			for lineEnd in lineEnds:
				maxes.append(self.GetMax(data, lineEnd))
			# Select the most common line ending
			lineTerm = lineEnds[lineEnds.index(max(lineEnds))-1]
		# Discover the estimated number of rows (not sure if needed)
		self.NumberRows = len(data)
		# get delimiters
		if self.headerrow:
			# User has indicated there is a header row so let's get it, else ignore
			#self.headers = self.ParseSingleLine(data[beginRow-1], delims, quotes)
			self.NumberRows = self.NumberRows - 1 #should only count data not header row
		# Convert the data into a list of lines. 
		# This must account for newlines within quotes being treated as a cell. It's a one process thing.
		
		inQuote = False # flag for being 'within' quotes. We're not yet...
		maybeLineEnding = False
		startNewLine = False
		token = '' # current token
		tokens = [] # list of tokens in this line
		rowNumber = 0
		for char in data:
			if maybeLineEnding == True and char == self.lineend[1]:
				startNewLine = True
				maybeLineEnding = False
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
				inQuoteChar = char # record it to check for matching quote later
				inQuote = True # and flag that we're in a quotation
			elif len(self.lineend) == 1 and char == self.lineend:
				startNewLine = True
			elif len(self.lineend) > 1 and char == self.lineend[0]: # got first of windows line end chars
				maybeLineEnding = True
			elif startNewLine == False: # And if char is anything else...
				token += char # add to token


			if startNewLine == True:
				startNewLine = False
				rowNumber = rowNumber + 1
				if len(token) > 0: # Check if last item is worth recording (len > 0)
					tokens.append(token) # add to list of tokens
				if rowNumber >= self.startRow + 1:
					self.outdata.append(tokens)
				inQuote = False
				token = ''
				print("Reset tokens")
				tokens = []
		if headerrow == True:
			self.header = self.outdata[0]
			self.outdata.pop(0)

	def ReturnColumn(self, columnNumber):
		"""
		Returns a column of data. If cell (or indeed column), None value is substituted.
		A nice, useful function to read in CSV files and access column data at will. 
		"""
		if len(self.outdata) > 0:
			columnData = []
			for idxRow in self.outdata:
				try:
					columnData.append(idxRow[columnNumber])
				except IndexError:
					columnData.append(None)
		return columnData


if __name__ == "__main__":
	filename = "test.csv"
	delims = ",;"
	quotes = '"'
	lineend ="\r\n"
	headerrow =True
	startRow = 0
	testcase = CSVObject(filename, delims, quotes, lineend, headerrow, startRow)
	testcase.Import()
	print("Header = ", testcase.header)
	print("Data   = ", testcase.outdata)
	print("Column = ", testcase.ReturnColumn(4))
