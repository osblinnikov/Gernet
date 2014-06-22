(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.Worker = require(__dirname + "/../../dist/Worker.js");
  } else {
    s = self;
  }

  describe("eval.js", function() {
    it("should eval the given code", function() {
      var done, result, wrk;
      wrk = new s.Worker("/test/specs/eval.js");
      result = null;
      done = false;
      runs(function() {
        wrk.onmessage = function(msg) {
          result = msg.data;
          done = true;
          wrk.terminate();
        };
        wrk.postMessage("postMessage(\"abc\")");
      });
      waitsFor((function() {
        return done;
      }), "should finish", 500);
      runs(function() {
        expect(result).toEqual("abc");
      });
    });
  });

}).call(this);
