(function() {
  var chan, channelPort, isNode, wrk1;

  isNode = typeof module !== "undefined" && module.exports;

  importScripts('/dist/Worker.js', '/dist/MessageChannel.js');

  chan = new MessageChannel();

  wrk1 = new Worker("/test/specs/msgch.receiver.js");

  channelPort = void 0;

  this.onmessage = function(e) {
    var msg, ports;
    msg = e.data;
    ports = e.ports;
    if (ports && ports.length) {
      channelPort = ports[0];
    } else {
      if (channelPort) {
        channelPort.postMessage(msg);
      }
    }
  };

}).call(this);
