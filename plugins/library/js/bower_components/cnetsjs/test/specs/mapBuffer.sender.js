(function() {
  var bId, onRun, onSend, readersWriters, receivedData, _bufferToReadTest, _bufferToWriteTest, _this;

  importScripts('/dist/Kernel.js', '/dist/readerWriter.js', '/dist/cnetsjsTypes.js', '/dist/MessageChannel.js', '/dist/mapBuffer.js');

  _this = new Kernel(this);

  _this.onStart = function() {
    return console.log("onStart");
  };

  receivedData = null;

  onRun = function(mapBufferId, mapBufferObj) {
    var r;
    switch (mapBufferId) {
      case 0:
        r = readersWriters[mapBufferId].readNext();
        if (r !== null) {
          receivedData = r.obj;
          readersWriters[mapBufferId].readFinished();
          return onSend();
        }
        break;
      case 1:
        return console.log("onRun _bufferToWriteTest");
      default:
        return console.log("onRun, unknown buffer");
    }
  };

  onSend = function() {
    var r;
    if (receivedData === null) {
      return;
    }
    r = readersWriters[1].writeNext();
    if (r !== null) {
      r.obj = receivedData;
      readersWriters[1].writeFinished();
      return receivedData = null;
    } else {
      return setTimeout(onSend, 100);
    }
  };

  _this.onStop = function() {
    return console.log("onStop");
  };

  bId = 0;

  readersWriters = {};

  _bufferToReadTest = new mapBuffer(bId, _this);

  readersWriters[bId++] = _bufferToReadTest.getReader(onRun);

  _bufferToWriteTest = new mapBuffer(bId, _this);

  readersWriters[bId++] = _bufferToWriteTest.getWriter();

}).call(this);
