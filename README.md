# CommaServe
CommaServe is a better (for me!) CSV library than that built-in. 

* Multiple delimiters in one file
* Multiple string delimiters
* Specified line endings (Unix, Windows, MacOS (old)
* Multi-line statements (if a line ending appears within quote delimiters, it's considered part of the cell and NOT a new line
* Headers can be specified, if so, they are stored in a separate attribute from the data
* Can start at an arbitrary row (if your source files begin with empty rows, you can skip them with this rather than hunting them down after import)
* Allows access to columnar data. If a cell is empty, a None value is returned, shouldn't crash. 
* Designed to work with very awkward CSV files.
* Converts integer strings to integers, float strings to floats
* Works in a functional way (does whole file in one go) or OO way (as iterator - more memory friendly)

## HOW TO USE
### General set up 
First, set up the variables you want: The filename, the delimiters, quote characters, line endings (uses platform default if none specified), whether there's a header row and start row number.
~~~
import CommaServe
filename = "test.csv"
delims = ",;"
quotes = '"'
lineEnd ="\r\n"
headerRow =True
startRow = 0
~~~
### Functional
Call the function. 
~~~
header, data = CommaServe.ReadWholeCSV(filename, delims, quotes, lineEnd, headerRow, startRow)
print(data)
~~~
Use "ReturnColumn(colnumber)" to get columnar data
~~~
print("Column = ", CommaServe.ReturnColumn(data[4])) # Print a column's data
~~~
### Object oriented
Instantiate the CSVObject object with filename, delimiters, quote delimites, lineend (platform standard as default), headerrow and startrow.
Iterate through the object like this:
~~~
data = CommaServe.CSVObject(filename, delims, quotes, lineEnd, headerRow, startRow)
for row in data:
    print(row)
~~~
Nice!
