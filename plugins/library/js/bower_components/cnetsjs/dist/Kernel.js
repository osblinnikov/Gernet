(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
  } else {
    s = self;
  }

  s.Kernel = function(binds) {
    var i, onMessageCallback, slf, _i, _ref;
    if (typeof binds !== 'array') {
      binds = [binds];
    }
    slf = this;
    slf.bindObjects = binds;
    slf.mapBuffers = [];
    slf.isStarted = false;
    slf.directPortId = void 0;
    slf.addBuffer = function(buf) {
      return slf.mapBuffers.push(buf);
    };
    slf.onStart = void 0;
    slf.onStop = void 0;
    slf.postMessage = function(msg) {
      if (slf.bindObjects[0].internalWorker) {
        return slf.bindObjects[0].internalWorker.postMessage(msg);
      } else {
        return slf.bindObjects[0].postMessage(msg);
      }
    };
    slf.onmessage = function(e) {
      var i, _i, _ref, _results;
      _results = [];
      for (i = _i = 0, _ref = slf.bindObjects.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
        if (slf.bindObjects[i].internalWorker) {
          _results.push(slf.bindObjects[i].internalWorker.onmessage(e));
        } else {
          _results.push(slf.bindObjects[i].onmessage(e));
        }
      }
      return _results;
    };
    onMessageCallback = function(e) {
      if (e.data.type === 'stop') {
        if (slf.isStarted) {
          slf.isStarted = false;
          if (slf.onStop) {
            slf.onStop();
          }
          if (self.close) {
            self.close();
          } else {
            console.error("Kernel: onStop: I can't stop myself, no close() method found!");
          }
        }
      }
      if (typeof e.data.bufId !== 'undefined') {
        if (!slf.isStarted && e.data.type !== 'create') {
          if (slf.onStart) {
            slf.onStart();
          }
          slf.isStarted = true;
        }
        if (typeof slf.directPortId !== 'undefined') {
          e.data.portId = slf.directPortId;
        }
        return slf.mapBuffers[e.data.bufId].dispatchMessage(e);
      }
    };
    for (i = _i = 0, _ref = slf.bindObjects.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
      if (slf.bindObjects[i].internalWorker) {
        slf.bindObjects[i].internalWorker.onmessage = onMessageCallback;
      } else {
        slf.bindObjects[i].onmessage = onMessageCallback;
      }
    }
    return true;
  };

  if (isNode) {
    module.exports = s.Kernel;
  }

}).call(this);
