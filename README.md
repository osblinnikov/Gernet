Gernet
=====

Gernet is:

0. Generator of Java and C code from json file
1. Integrated into golang-like workspace structure (http://golang.org/doc/code.html), but can be easily configured
2. Able to build source files from gernet.json file (see example/gernet.json)

If you want to change default path to the Projects workspace directory just change 'PROJECTS_ROOT_PATH' variable in 'builder.py' file. 

Installation
---

Assume that you already have Python installed

Go to your favorite projects directory. Create path to the gernet, on linux you can do so with the following commands:


    cd $PROJECTS_DIRECTORY
    mkdir -p src/github.com/airutech
    cd src/github.com/airutech
    git clone https://github.com/airutech/Gernet.git gernet

Update your PATH with the gernet:

    PATH=$PATH:$PROJECTS_DIRECTORY/src/github.com/airutech/gernet
    
or

    cd gernet
    PATH=$PATH:`pwd`
        
Possibly you don't have yet Cog generator and Mako template engine installed

    pip install Mako

Cog installation steps:

  1. Download Cog from the [Python Package Index](http://pypi.python.org/pypi/cogapp)
  2. Unpack the distribution archive somewhere
  3. Run the setup.py script that was unpacked

        python setup.py install

Enjoy your crossplatform usage of the gernet!


Usage
---

gernet [GernetFilePath] [options]

GernetFilePath can be absolute or relative to current path or 
relative to workspace sources root directory e.g.:

    gernet github.com/airutech/gernet/test/example -lang java

Available Gernet options:

    -lang {generator folder name e.g java or c}
    -c        # execute cleaning only for chosen Topology

Other options can be Cog specific.

Examples:

    gernet .. -lang java -c
    gernet test/example -lang java
    
TODO
---

Add support for C cnets library

Add support for Golang cnets library

