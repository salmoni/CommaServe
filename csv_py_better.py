


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
    def __init__(self, fileName, delims, quotes, lineend, headerrow = false, row = 0):
        self.fileName = fileName
        self.delims = delims
        self.quotes = quotes
        self.lineend = lineend
        self.headerrow = headerrow # Is there a header row? 
        self.row = 0 # starting row, defaults to 0
        self.NumberCols = 0
        self.NumberRows = 0

    def __iter__(self):
        return self

    def next(self):
        line = self.fin.next()
        return self.ParseLine(line)

	def Import(self):
		# Get all data into a single bundle
		fin = codecs.open(self.FileName.fileName, encoding='utf-8')
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
		# split file into rows
        # get delimiters
        if self.headerrow:
			# User has indicated there is a header row
			self.headers = self.ParseLine(data[beginRow-1], delims, quotes)
		
    def ParseLine(self, line):
        """
        Parses a line of CSV text into components. This attempts to
        be a proper parser that can cope with multiple delimiters.
        
        Lots of comments because I find it hard to follow. If you don't, then congrats.
        """
        inQuote = False # flag for being 'within' quotes
        token = '' # current token
        tokens = [] # list of tokens
        for char in line:
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
            else: # And if char is anything else...
                token += char # add to token
        if len(token) > 0: # Check if last item is worth recording (len > 0)
            tokens.append(token) # add to list of tokens
        return tokens # return list of tokens
        
