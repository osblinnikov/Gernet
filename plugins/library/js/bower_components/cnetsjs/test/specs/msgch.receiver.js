(function() {
  var channelPort, getChannelMessage;

  channelPort = void 0;

  this.onmessage = function(e) {
    var msg, ports;
    msg = e.data;
    ports = e.ports;
    if (ports && ports.length) {
      channelPort = ports[0];
      channelPort.onmessage = getChannelMessage;
    }
  };

  getChannelMessage = function(e) {
    var msg;
    msg = e.data;
    postMessage(msg);
    return close();
  };

}).call(this);
