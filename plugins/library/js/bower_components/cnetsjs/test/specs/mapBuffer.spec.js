(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.mapBuffer = require(__dirname + "/../../dist/mapBuffer.js");
    s.Worker = require(__dirname + "/../../dist/Worker.js");
  } else {
    s = self;
  }

  describe("mapBuffer-API", function() {
    return it("should define the used API", function() {
      var m;
      expect(s.mapBuffer).toEqual(jasmine.any(Function));
      m = new s.mapBuffer();
      expect(m.dispatchMessage).toEqual(jasmine.any(Function));
      expect(m.getReader).toEqual(jasmine.any(Function));
      expect(m.getWriter).toEqual(jasmine.any(Function));
      expect(m.readNext).toEqual(jasmine.any(Function));
      expect(m.readNextWithMeta).toEqual(jasmine.any(Function));
      expect(m.readFinished).toEqual(jasmine.any(Function));
      expect(m.writeNext).toEqual(jasmine.any(Function));
      expect(m.writeFinished).toEqual(jasmine.any(Function));
      expect(m.size).toEqual(jasmine.any(Function));
      expect(m.gridSize).toEqual(jasmine.any(Function));
      expect(m.uniqueId).toEqual(jasmine.any(Function));
      expect(m.init).toEqual(jasmine.any(Function));
      expect(m.addConnection).toEqual(jasmine.any(Function));
      expect(m.syncConnections).toEqual(jasmine.any(Function));
    });
  });

  describe("mapBuffer-send-receive", function() {
    return it("should send the given message", function() {
      var buffersLength, done, dstWrGridId, dstWrkPinId, mBufferExchange, mBufferFromReceiver, mBufferToSender, readers_grid_size, result, srcWrkGridId, srcWrkPinId, uniqueId, wrk0, wrk1;
      expect(s.mapBuffer).toEqual(jasmine.any(Function));
      expect(s.Worker).toEqual(jasmine.any(Function));
      wrk0 = new s.Worker('/test/specs/mapBuffer.sender.js');
      wrk1 = new s.Worker('/test/specs/mapBuffer.receiver.js');
      mBufferToSender = new s.mapBuffer();
      mBufferToSender.init(buffersLength = 2, uniqueId = 1000, readers_grid_size = 1);
      mBufferToSender.addConnection(void 0, void 0, void 0, wrk0, dstWrkPinId = 0, dstWrGridId = 0);
      mBufferToSender.syncConnections();
      mBufferExchange = new s.mapBuffer();
      mBufferExchange.init(buffersLength = 2, uniqueId = 1001, readers_grid_size = 1);
      mBufferExchange.addConnection(wrk0, srcWrkPinId = 1, srcWrkGridId = 0, wrk1, dstWrkPinId = 0, dstWrGridId = 0);
      mBufferExchange.syncConnections();
      mBufferFromReceiver = new s.mapBuffer();
      mBufferFromReceiver.init(buffersLength = 2, uniqueId = 1002, readers_grid_size = 1);
      mBufferFromReceiver.addConnection(wrk1, srcWrkPinId = 1, srcWrkGridId = 0, void 0, void 0, void 0);
      mBufferFromReceiver.syncConnections();
      done = false;
      result = void 0;
      runs(function() {
        var obj, rootR1, rootW0;
        rootR1 = mBufferFromReceiver.getReader(function(bufId, target) {
          var obj;
          done = true;
          obj = rootR1.readNext();
          if (obj !== null) {
            result = obj.obj;
            console.log("successfuly read message:" + result);
            return rootR1.readFinished();
          }
        });
        rootW0 = mBufferToSender.getWriter();
        obj = rootW0.writeNext();
        if (obj !== null) {
          console.log("write Next OK");
          obj.obj = "Test Should Be Passed";
          return rootW0.writeFinished();
        }
      });
      waitsFor((function() {
        return done;
      }), "should finish", 2000);
      return runs(function() {
        expect(result).toEqual("Test Should Be Passed");
      });
    });
  });

}).call(this);
