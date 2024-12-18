# csv_py_better
A better (for me!) CSV library than that in the included. 

* Multiple delimiters in one file
* Multiple string delimiters
* Specify line endings (Unix, Windows, MacOS (old)
* Multi-line statements (if a line ending appears within quote delimiters, it's considered part of the cell and NOT a new line
* Headers can be specified, if so, they are stored in a separate attribute from the data
* Can start at an arbitrary row (if your source files begin with empty rows, you can skip them with this rather than hunting them down after import)
* Allows access to columnar data. If a cell is empty, a None value is returned, shouldn't crash. 
* Designed to work with very awkward CSV files. 

## HOW TO USE

Instantiate the CSVObject object with filename, delimiters, quote delimites, lineend (platform standard as default), headerrow and startrow.
Call the "import" method
Use "object.header" for the header
Use "object.outdata" for the data
Use "ReturnColumn(colnumber)" to get columnar data

For example:

~~~
filename = "test.csv"
delims = ",;" # Let's use two delimiters for some reason
quotes = '"' # Double quotes
lineend ="\r\n" # Windows line endings
headerrow =True # There is a header row
startRow = 0 # Start on row 0
testcase = CSVObject(filename, delims, quotes, lineend, headerrow, startRow) # Instantiate the object
testcase.Import() # Do an import
print("Header = ", testcase.header) # Print the header
print("Data   = ", testcase.outdata) # Print the data
print("Column = ", testcase.ReturnColumn(4)) # Print a column's data
~~~
Nice!
