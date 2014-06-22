(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.Worker = require(__dirname + "/../../dist/Worker.js");
  } else {
    s = self;
  }

  describe("WebWorker-API", function() {
    it("should define the used API", function() {
      var wrk;
      expect(s.Worker).toEqual(jasmine.any(Function));
      wrk = new s.Worker("/test/specs/eval.js");
      expect(wrk.postMessage).toEqual(jasmine.any(Function));
      expect(wrk.terminate).toEqual(jasmine.any(Function));
      wrk.terminate();
    });
  });

}).call(this);
