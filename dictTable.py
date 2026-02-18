from sys import argv,exit
from typing import Dict, List
from enum import Enum,auto
from pprint import pprint

class Modes(Enum):
    NONE       = 0,
    OUT        = 1,
    WORDLIST   = 2,
    DICTS      = 3,
    CASESEN    = 4,
    NOTCASESEN = 5,

Map:Dict[str,Modes] = {"-o":Modes.OUT,"-wl":Modes.WORDLIST,"-d":Modes.DICTS,"-c":Modes.NOTCASESEN,"-C":Modes.CASESEN}

class WordList:
    List:List[str]
    CaseSensitive:bool
    def __init__(self):
        self.List = []
        self.CaseSensitive = True

#static
class Params:
    Outs:List[str]
    WordListsKeys:List[str]
    WordLists:Dict[str,WordList]
    Dicts:List[str]
    def __init__(self):
        self.Outs          = []
        self.WordListsKeys = []
        self.WordLists     = {}
        self.Dicts         = []
params = Params()

def ParseArgs():
    mode:Modes = Modes.NONE;
    currentWordList:str = ""
    CaseSensitive:bool = True;
    for i, arg in enumerate(argv):
        if i == 0: 
            continue
        if arg[0] == '-' and arg in Map:
            mode = Map[arg]
            if mode == Modes.CASESEN:
                CaseSensitive = True
            if mode == Modes.NOTCASESEN:
                CaseSensitive = False
            currentWordList = ""
            continue
        match mode:
            case Modes.OUT:
                if(arg in params.Outs):
                    print(f"output file:{arg} has already been provided",end="\n")
                    exit(1)
                params.Outs.append(arg)
            case Modes.WORDLIST:
                if currentWordList == "":
                    currentWordList = arg
                    if currentWordList in params.WordLists:
                        print(f"wordList:{currentWordList} is already defined",end="\n")
                        exit(1)
                    params.WordListsKeys.append(currentWordList)
                    wl = WordList()
                    wl.CaseSensitive = CaseSensitive
                    params.WordLists[currentWordList] = wl 
                    continue
                if(arg in params.WordLists[currentWordList].List):
                    print(f"word:{arg} already defined in wordlist:{currentWordList}",end="\n")
                    exit(1)
                params.WordLists[currentWordList].List.append(arg);
            case Modes.DICTS:
                if(arg in params.Dicts):
                    print(f"dictinary file:{arg} has already been provided",end="\n")
                    exit(1)
                params.Dicts.append(arg)
            case Modes.NONE:
                print(f"expacted flag before argument:{arg}",end="\n")
                exit(1)
            case _:
                print("unexpected flag mode[code bug]",end="\n")
                exit(1)

DictionaryWithMeanings:Dict[str,Dict[str,List[str]]] = {}

def ParseCsvFile(file:str):
    try:
       with open(file,"r") as csv:
           definetions:List[str] = []
           DictionaryWithMeanings[file] = {}
           while True:
                definetions = []
                line = csv.readline()
                if not line:
                    break
                definetions = line.split(",")
                for key in params.WordListsKeys:
                    for word in params.WordLists[key].List:
                        defi = definetions[0]
                        if not params.WordLists[key].CaseSensitive:
                            word = word.lower()    
                            defi = defi.lower()
                        if defi != word:
                            continue 
                        if defi not in DictionaryWithMeanings[file]:
                            DictionaryWithMeanings[file][defi] = definetions[1:-1:]
                            continue
                        for item in definetions[1:-1:]:
                            DictionaryWithMeanings[file][defi].append(item)
    except FileNotFoundError:
        print(f"file:{file} does not exist",end="\n")
        exit(1)

def WriteCsvFile(file:str,key:str):
    #don't think writing to file can fail
    words:List[str] = params.WordLists[key].List 
    with open(file,"w") as csv:
        for word in words:
            csv.write(f"{word},")
        csv.write("\n")
        for key in list(DictionaryWithMeanings.keys()):
            csv.write(f"{key},")
            for w in words:
                if w in DictionaryWithMeanings[key]:
                    csv.write("[")
                    for item in DictionaryWithMeanings[key][w]:
                        csv.write(f"{item},")
                    csv.write("],")
                else:
                    csv.write("[NULL],")
            csv.write("\n")

def main():
    ParseArgs()
    if(len(params.WordLists) != len(params.Outs)):
        print("number of wordlists and outout files must be the same",end="\n")
        exit(1)
    #parsing of dictionarys
    for d in params.Dicts:
        ParseCsvFile(d)
    for i,file in enumerate(params.Outs):
        WriteCsvFile(file,params.WordListsKeys[i])
    return

if __name__ == "__main__":
    main()
