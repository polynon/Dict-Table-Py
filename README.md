
# Dict-Table-Py

Dict-Table-Py is a searching tool used to grab vaules tied to words
and output them the vaules in a new table

### Limits

Currently suported datatable types

- csv read and write

### Usage

`-o`   Flag is used to mark the output files  
`-wl`  Flag is used to mark the Search spaces first arg of this flag is the name of the search space 
Output Flag and wordList flag have to have the same number of names  
`-d`   Flag is used to mark what files to look through  
`-c`   Flag is used to mark the following wordlists as not case sensitive  
`-C`   Flag is used to mark the following wordlists as case sensitive  

### Basic Example

##### build\.sh

`python main.py -o want.csv love.csv \
-wl want want desire wish need -wl love love like enjoy\
-d dictionarys/spanish.csv dictionarys/french.csv `

We map the wordList want to the output file want\.csv and love to the output file love\.csv
Then we tell the program to search through the files dictionarys/spanish\.csv and dictionary/french\.csv
