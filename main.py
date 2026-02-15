from sys import argv,exit
from typing import Dict, List
from enum import Enum,auto
from pprint import pprint

class Modes(Enum):
    NONE     = 0,
    OUT      = 1,
    WORDLIST = 2,
    DICTS    = 3,

Map:Dict[str,Modes] = {"-o":Modes.OUT,"-wl":Modes.WORDLIST,"-d":Modes.DICTS}

#static
class Params:
    Outs:List[str]
    WordLists:Dict[str,List[str]]
    Dicts:List[str]
    def __init__(self):
        self.Outs      = []
        self.WordLists = {}
        self.Dicts     = []
params = Params()

def ParseArgs():
    mode:Modes = Modes.NONE;
    currentWordList:str = ""
    for i, arg in enumerate(argv):
        if i == 0: 
            continue
        if arg[0] == '-' and arg in Map:
            mode = Map[arg]
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
                    params.WordLists[currentWordList] = []
                    continue
                if(arg in params.WordLists[currentWordList]):
                    print(f"word:{arg} already defined in wordlist:{currentWordList}",end="\n")
                    exit(1)
                params.WordLists[currentWordList].append(arg);
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

def main():
    ParseArgs()
    print("outs:",end="\n")
    for out in params.Outs:
        print(out,end="\n")
    print("Dicts:",end="\n")
    for d in params.Dicts:
        print(d,end="\n")
    print("wordLists:",end="\n")
    pprint(params.WordLists,width = 80)

if __name__ == "__main__":
    main()
