(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.mapBuffer = require(__dirname + "/../../dist/mapBuffer.js");
    s.Worker = require(__dirname + "/../../dist/Worker.js");
    s.Kernel = require(__dirname + "/../../dist/Kernel.js");
  } else {
    s = self;
  }

  describe("mapBuffer-send-receive-perf", function() {
    return it("should send many messages during 3 seconds", function() {
      var buffersLength, done, dstWrGridId, dstWrkPinId, grid_id, mBufferFromSender, mBufferToSender, readers_grid_size, srcWrkGridId, srcWrkPinId, uniqueId, wrk0;
      expect(s.mapBuffer).toEqual(jasmine.any(Function));
      expect(s.Worker).toEqual(jasmine.any(Function));
      wrk0 = new s.Worker('/test/specs/mapBufferPerf.sender.js');
      mBufferToSender = new s.mapBuffer();
      mBufferToSender.init(buffersLength = 200, uniqueId = 1004, readers_grid_size = 1, grid_id = 0);
      mBufferToSender.addConnection(void 0, void 0, void 0, wrk0, dstWrkPinId = 0, dstWrGridId = 0);
      mBufferToSender.syncConnections();
      mBufferFromSender = new s.mapBuffer();
      mBufferFromSender.init(buffersLength = 200, uniqueId = 1005, readers_grid_size = 1, grid_id = 0);
      mBufferFromSender.addConnection(wrk0, srcWrkPinId = 1, srcWrkGridId = 0, void 0, void 0, void 0);
      mBufferFromSender.syncConnections();
      done = false;
      runs(function() {
        var errorsCntr, fps, i, nextTickTime, requestAnimFrame, rootR1, rootW0, senderFunc, startTime, _i, _ref, _results;
        startTime = new Date().getTime();
        nextTickTime = startTime + 1000;
        fps = 0;
        errorsCntr = 0;
        rootR1 = mBufferFromSender.getReader(function(bufId, target) {
          var curTime, obj;
          obj = rootR1.readNext();
          if (obj !== null) {
            fps++;
            curTime = new Date().getTime();
            if (curTime > nextTickTime) {
              console.log("fps: " + fps + ", failed writes:" + errorsCntr);
              nextTickTime += 1000;
              errorsCntr = 0;
              fps = 0;
            }
            return rootR1.readFinished();
          }
        });
        requestAnimFrame = (function() {
          var requestAnimationFrame;
          requestAnimationFrame = void 0;
          if (typeof window !== 'undefined') {
            requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame;
          }
          return requestAnimationFrame || function(callback) {
            setTimeout(callback, 0);
          };
        })();
        senderFunc = function() {
          var curTime, obj;
          curTime = new Date().getTime();
          if (curTime > startTime + 3000) {
            done = true;
            return;
          }
          obj = rootW0.writeNext();
          if (obj !== null) {
            return rootW0.writeFinished();
          } else {
            return errorsCntr++;
          }
        };
        rootW0 = mBufferToSender.getWriter(senderFunc);
        _results = [];
        for (i = _i = 0, _ref = buffersLength * 2; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
          _results.push(senderFunc());
        }
        return _results;
      });
      return waitsFor((function() {
        return done;
      }), "should finish", 5000);
    });
  });

}).call(this);
