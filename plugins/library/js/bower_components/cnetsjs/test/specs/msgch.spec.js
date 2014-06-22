(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.MessageChannel = require(__dirname + "/../../dist/MessageChannel.js");
    s.Worker = require(__dirname + "/../../dist/Worker.js");
  } else {
    s = self;
  }

  describe("MessageChannel-API", function() {
    return it("should define the used API", function() {
      var ch;
      expect(s.MessageChannel).toEqual(jasmine.any(Function));
      ch = new s.MessageChannel();
      expect(ch.port1).toEqual(jasmine.any(Object));
      expect(ch.port2).toEqual(jasmine.any(Object));
    });
  });

  describe("MessageChannel-send", function() {
    return it("should send the given message", function() {
      var ch, done, result, wrk1, wrk2;
      expect(s.MessageChannel).toEqual(jasmine.any(Function));
      expect(s.Worker).toEqual(jasmine.any(Function));
      ch = new s.MessageChannel();
      wrk1 = new s.Worker("/test/specs/msgch.sender.js");
      wrk1.postMessage("", [ch.port1]);
      wrk2 = new s.Worker("/test/specs/msgch.receiver.js");
      wrk2.postMessage("", [ch.port2]);
      result = null;
      done = false;
      runs(function() {
        wrk2.onmessage = function(msg) {
          result = msg.data;
          done = true;
          wrk2.terminate();
        };
        wrk1.postMessage("abc");
      });
      waitsFor((function() {
        return done;
      }), "should finish", 2000);
      return runs(function() {
        expect(result).toEqual("abc");
      });
    });
  });

}).call(this);
