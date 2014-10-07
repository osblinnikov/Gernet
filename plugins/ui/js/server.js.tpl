var http = require('http');
var React = require('react');

var fs = require("fs");
var App = fs.readFileSync("ui/assets/main.js","utf-8");

var jsdom = require("jsdom")

document = null
window = null

http.createServer(function(req, res) {

  if (req.url == '/assets/main.js') {
    res.setHeader('Content-Type', 'text/javascript')
    res.end(App);
  }else{
    jsdom.env({
      features : { QuerySelector : true }, 
      html: '<html><head></head><body><div id="app"><p>If you can see this, something is broken (or JS is not enabled)..</p></div><script type="text/javascript" src="assets/main.js"></script></body>',
      src: [App],
      /*created: function(err, win){
        console.log("created");
        console.log(err);
      },
      loaded: function(err, win){
        console.log("loaded");
        console.log(err);
      },*/
      done: function (err, win) {
        window = win
        document = window.document
        // console.log(window.innerWidth+"x"+window.innerHeight);
        res.setHeader('Content-Type', 'text/html')
        // jQuery is now loaded on the jsdom window created from 'agent.body'
        res.end(document.body.innerHTML);
      }
    });
  }

// The http server listens on port 3000
}).listen(3000)


// A utility function to safely escape JSON for embedding in a <script> tag
function safeStringify(obj) {
  return JSON.stringify(obj).replace(/<\/script/g, '<\\/script').replace(/<!--/g, '<\\!--')
}