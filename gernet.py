#! /usr/bin/env python
import sys
import os

from src.gernetHelpers import PROJECTS_ROOT_PATH
from src.builder import runGernet


def printHelp():
    print "**********************"
    print "Gernet is a generator based on COG"
    print "Generate full implementations of cnets topologies"
    print "Usage: gernet [TopologyFilePath] [options]"
    print "Examples:"
    print "  gernet .. "
    print "  gernet icanchangethisdomain/SomeProjectName  #generate with every available generator"
    print "TopologyFilePath can be absolute, relative to current path, or "
    print "relative to projects root path e.g.:"
    print "  gernet github.com\\osblinnikov\\gernet\\example "
    print "**********************"
    print "Available options:"
    print "  -c        # execute cleaning only for chosen Topology"
    print "**********************"
    print "Other options can be Cog specific."
    print "  If you want to change default path to the Projects directory please see the"
    print "  gernetHelpers.py file and PROJECTS_ROOT_PATH variable"
    print "**********************"


def Gernet(argv):
    jsonFile = "gernet.json"
    yamlFile = "gernet.yaml"
    TopologyDirs = []
    firstRealArgI = 1
    #try to find the TopologyDirs right here
    if len(argv) > firstRealArgI:
        pPr = None
        #try to find the TopologyDirs in the specified absolute path
        if os.path.exists(os.path.join(argv[firstRealArgI],jsonFile)) or os.path.exists(os.path.join(argv[firstRealArgI],yamlFile)) :
            TopologyDirs.append(os.path.join(argv[firstRealArgI]))
        #try to find the TopologyDirs in the specified relative to current path
        elif os.path.exists(os.path.join(os.getcwd(),argv[firstRealArgI],jsonFile)) or os.path.exists(os.path.join(os.getcwd(),argv[firstRealArgI],yamlFile)):
            TopologyDirs.append(os.path.join(os.getcwd(),argv[firstRealArgI]))
        #try to find the TopologyDirs in the specified path from projects src root
        elif os.path.exists(os.path.join(PROJECTS_ROOT_PATH,argv[firstRealArgI],jsonFile)) or os.path.exists(os.path.join(PROJECTS_ROOT_PATH,argv[firstRealArgI],yamlFile)):
            TopologyDirs.append(os.path.join(PROJECTS_ROOT_PATH,argv[firstRealArgI]))
        elif argv[firstRealArgI] == "." or os.path.exists(os.path.join(os.getcwd(),argv[firstRealArgI])):
            pPr = os.path.join(os.getcwd(),argv[firstRealArgI])
        elif os.path.exists(os.path.join(PROJECTS_ROOT_PATH,argv[firstRealArgI])):
            pPr = os.path.join(PROJECTS_ROOT_PATH,argv[firstRealArgI])
        elif os.path.exists(argv[firstRealArgI]):
            pPr = argv[firstRealArgI]
        if pPr != None:
            for root, dirs, files in os.walk(pPr):
                if os.path.exists(os.path.join(pPr,root,jsonFile)) or os.path.exists(os.path.join(pPr,root,yamlFile)):
                    TopologyDirs.append(os.path.join(pPr,root))

    if len(TopologyDirs) == 0 and os.path.exists(os.path.join(os.getcwd(),jsonFile)):
        firstRealArgI = 0
        TopologyDirs.append(os.getcwd())
    elif len(TopologyDirs) == 0:
        print "No "+os.path.join(os.getcwd(),jsonFile)
        if len(argv) > firstRealArgI:
            print "No "+os.path.join(argv[firstRealArgI],jsonFile)
            print "No "+os.path.join(os.getcwd(),argv[firstRealArgI],jsonFile)
        if len(argv) > firstRealArgI:
            print "No "+os.path.join(PROJECTS_ROOT_PATH,'src',argv[firstRealArgI],jsonFile)
        print "NO gernet.json files found"
        printHelp()
        exit()

    for d in TopologyDirs:
        try:
            runGernet(firstRealArgI, argv, d)
        except:
            print "-------------"
            print "Exception in: "+d
            print "Unexpected error:", sys.exc_info()[0]
            raise

if __name__ == "__main__":
    Gernet(sys.argv)
