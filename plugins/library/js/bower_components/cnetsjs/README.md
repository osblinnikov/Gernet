cnetsjs
=======

cnets actors javascript library, leverage on crossbrowser emulation of webworkers (tested on Node, Chrome, Firefox).

Currently it is ready for hacks, but was not used in production yet

#To run tests

For Firefox:  open test/index.html directly in the browser

For Chrome:  run startChrome.sh script and open test/index.html in opened browser

#For developers 

    npm install
    gulp

go to `http://localhost:4000/test/`

Or to run tests from the console:

    sudo npm install --global jasmine-node
    gulp build && jasmine-node test/specs
