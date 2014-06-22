(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
  } else {
    s = self;
  }

  if (!s.Worker || !s.MessageChannel || s.MessageChannelArtificial === true) {
    s.Worker = function(scriptFile) {
      var clearImmediate, evalStringContents, findListener, fs, getHTTPObject, http, importScripts, listeners, listenersSize, listenersWithCapture, postMessage, requestAnimFrame, setImmediate, slf, started, stop, strResponse, __fileContent, __iterate, __onIterate, __ports, __text, __timer;
      slf = this;
      __timer = null;
      __text = [];
      __ports = [];
      __fileContent = null;
      started = false;
      slf.internalWorker = {};
      slf.onerror = null;
      slf.onmessage = null;
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
                    _results2.push(tv(evt));
                  }
                  return _results2;
                })());
              } else {
                _results1.push(void 0);
              }
            }
            return _results1;
          })());
        }
        return _results;
      };
      importScripts = function() {
        var arrName, i, j, params, script;
        isNode = typeof module !== "undefined" && module.exports && __dirname;
        params = Array.prototype.slice.call(arguments);
        i = 0;
        j = params.length;
        while (i < j) {
          if (isNode) {
            arrName = params[i].split('/').pop().split('.');
            arrName.pop();
            this[arrName.join('.')] = require(process.cwd() + "/" + params[i]);
          } else {
            script = document.createElement("SCRIPT");
            script.src = params[i];
            script.setAttribute("type", "text/javascript");
            document.getElementsByTagName("HEAD")[0].appendChild(script);
          }
          i++;
        }
      };
      postMessage = function(text) {
        slf.dispatchEvent({
          data: text,
          type: 'message'
        }, true);
        return false;
      };
      slf.internalWorker = {
        postMessage: postMessage
      };
      stop = function() {
        return slf.terminate();
      };
      setImmediate = setImmediate || function(cb) {
        __timer = setTimeout(cb, 0);
      };
      clearImmediate = clearImmediate || function(timer) {
        return clearTimeout(timer);
      };
      requestAnimFrame = (function() {
        var requestAnimationFrame;
        requestAnimationFrame = void 0;
        if (typeof window !== 'undefined') {
          requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame;
        }
        return requestAnimationFrame || function(callback) {
          setTimeout(callback, 1);
        };
      })();
      slf.postMessage = function(text, ports) {
        __ports.push(ports);
        __text.push(text);
        __iterate();
        return true;
      };
      __iterate = function() {
        requestAnimFrame(__onIterate);
        return true;
      };
      __onIterate = function() {
        var ex;
        if (__text.length || __ports.length) {
          try {
            if ("function" === typeof slf.internalWorker.onmessage) {
              slf.internalWorker.onmessage({
                data: __text.shift(),
                ports: __ports.shift()
              });
            }
            return true;
          } catch (_error) {
            ex = _error;
            if ("function" === typeof slf.onerror) {
              return slf.onerror(ex);
            }
          }
        }
        return false;
      };
      slf.terminate = function() {
        if (__timer !== null) {
          clearImmediate(__timer);
          __timer = null;
        }
        return true;
      };
      getHTTPObject = function() {
        var e, xmlhttp;
        xmlhttp = void 0;
        try {
          xmlhttp = new XMLHttpRequest();
        } catch (_error) {
          e = _error;
          try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
          } catch (_error) {
            e = _error;
            xmlhttp = false;
          }
        }
        return xmlhttp;
      };
      evalStringContents = function(__fileContent) {
        eval(__fileContent);
        if (typeof this.onmessage === 'function') {
          return slf.internalWorker.onmessage = this.onmessage;
        }
      };
      http = getHTTPObject();
      if (http) {
        http.open("GET", scriptFile, false);
        http.send(null);
        if (http.readyState === 4) {
          strResponse = http.responseText;
          switch (http.status) {
            case 404:
              alert("Error: Not Found. The requested function could not be found.");
              break;
            case 500:
              alert(strResponse);
              break;
            default:
              __fileContent = strResponse;
          }
        }
      } else {
        fs = require('fs');
        __fileContent = fs.readFileSync(process.cwd() + scriptFile, "utf8");
      }
      evalStringContents.bind(slf)(__fileContent);
      return true;
    };
    if (isNode) {
      module.exports = s.Worker;
    }
  }

}).call(this);
