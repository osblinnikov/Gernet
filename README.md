Gernet
=====

Gernet is:

0. Generator of Java, JavaScript, C or any other code from single gernet.json file
1. Uses plugin-architecture - simply write your own generator-plugin and point gernet in "type" field of gernet.json
1. Integrated into golang-like workspace structure (http://golang.org/doc/code.html), but can be easily configured
2. Able to build source files from gernet.json file (see example/gernet.json)

If you want to change default path to the Projects workspace directory just change 'PROJECTS_ROOT_PATH' variable in 'builder.py' file. 

Installation
---

Assume that you already have Python installed

Go to your favorite projects directory. Create path to the gernet, on linux you can do so with the following commands:


    cd $PROJECTS_DIRECTORY
    mkdir -p src/github.com/osblinnikov
    cd src/github.com/osblinnikov
    git clone https://github.com/osblinnikov/Gernet.git gernet

Update your PATH with the gernet:

    PATH=$PATH:$PROJECTS_DIRECTORY/src/github.com/osblinnikov/gernet
    
or

    cd gernet
    PATH=$PATH:`pwd`
        
Enjoy your crossplatform usage of the gernet!

    gernet test


Usage
---

gernet [GernetFilePath] [options]

GernetFilePath can be absolute or relative to current path or 
relative to workspace sources root directory e.g.:

    gernet github.com/osblinnikov/gernet/test/example

Available Gernet options:

    -c        # execute cleaning only for chosen Topology

Other options can be Cog specific.

Examples:

    gernet .. -c
    gernet test/example
    
TODO
---

Add full support for C cnets library

Add support for JavaScript cnets library

Add support for Golang cnets library

