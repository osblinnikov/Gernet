(function() {
  var MessagePort, isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
  } else {
    s = self;
  }

  MessagePort = function(anotherPort) {
    var findListener, listeners, listenersSize, listenersWithCapture, slf;
    slf = this;
    slf.anotherPort = anotherPort;
    if (slf.anotherPort) {
      slf.anotherPort.anotherPort = slf;
    }
    slf.isClosed = false;
    listenersSize = 0;
    listeners = {};
    listenersWithCapture = {};
    findListener = function(type, listener, useCapture) {
      var i, l, t, tv, v;
      l = listeners["" + useCapture];
      if (!l) {
        return false;
      }
      for (i in l) {
        v = l[i];
        if (v === type) {
          for (t in v) {
            tv = v[t];
            if (tv === listener) {
              return [i, t];
            }
          }
        }
      }
      return false;
    };
    slf.addEventListener = function(type, listener, useCapture) {
      var l;
      if (slf.isClosed) {
        return;
      }
      if (!findListener(type, listener, useCapture)) {
        l = listeners["" + useCapture];
        if (!l) {
          l = listeners["" + useCapture] = {};
        }
        if (!l[type]) {
          l[type] = [];
        }
        l[type].push(listener);
        return listenersSize++;
      }
    };
    slf.removeEventListener = function(type, listener, useCapture) {
      var r;
      if (slf.isClosed) {
        return;
      }
      r = findListener(type, listener, useCapture);
      if (!r) {
        return;
      }
      listeners["" + useCapture][r[0]].splice(r[1], 1);
      listenersSize--;
      if (listeners["" + useCapture][r[0]].length === 0) {
        return delete listeners["" + useCapture][r[0]];
      }
    };
    slf.dispatchEvent = function(evt, pfResult) {
      var i, l, t, tv, type, useCapture, v, _results;
      if (slf.isClosed) {
        return;
      }
      type = evt.type;
      if (type === 'message' && "function" === typeof slf.onmessage) {
        slf.onmessage(evt);
      }
      if (listenersSize <= 0) {
        return;
      }
      _results = [];
      for (useCapture in listeners) {
        l = listeners[useCapture];
        if (useCapture === "false" && !pfResult) {
          continue;
        }
        _results.push((function() {
          var _results1;
          _results1 = [];
          for (i in l) {
            v = l[i];
            if (i === type) {
              _results1.push((function() {
                var _results2;
                _results2 = [];
                for (t in v) {
                  tv = v[t];
                  console.log(tv);
                  _results2.push(tv(this, evt));
                }
                return _results2;
              }).call(this));
            } else {
              _results1.push(void 0);
            }
          }
          return _results1;
        }).call(this));
      }
      return _results;
    };
    slf.start = function() {
      return slf.isClosed = false;
    };
    slf.close = function() {
      return slf.isClosed = true;
    };
    slf.postMessage = function(msg, ports) {
      return slf.anotherPort.dispatchEvent({
        data: msg,
        ports: ports,
        type: 'message'
      }, true);
    };
    return true;
  };

  if (!s.MessageChannel) {
    s.MessageChannelArtificial = true;
    s.MessageChannel = function() {
      var slf;
      slf = this;
      slf.port1 = new MessagePort(void 0);
      slf.port2 = new MessagePort(slf.port1);
      return true;
    };
    if (isNode) {
      module.exports = s.MessageChannel;
    }
  }

}).call(this);
