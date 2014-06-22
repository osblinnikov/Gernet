(function() {
  var isNode, reader, s, writer;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
  } else {
    s = self;
  }

  reader = function(bufKernParam) {
    var self;
    self = this;
    self.buffer = bufKernParam;
    self.readNextWithMeta = function() {
      if (!self.buffer) {
        return {};
      }
      return self.buffer.target.readNextWithMeta(self.buffer);
    };
    self.readNext = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.readNext(self.buffer);
    };
    self.readFinished = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.readFinished(self.buffer);
    };
    self.size = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.size(self.buffer);
    };
    self.getGridId = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.gridId;
    };
    self.timeout = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.timeout(self.buffer);
    };
    self.gridSize = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.gridSize(self.buffer);
    };
    self.uniqueId = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.uniqueId(self.buffer);
    };
    self.addSelector = function(linkCont) {
      if (!self.buffer) {
        return -1;
      }
      return self.buffer.target.addSelector(self.buffer, linkCont);
    };
    return true;
  };

  writer = function(bufKernParam) {
    var self;
    self = this;
    self.buffer = bufKernParam;
    self.writeNext = function(make_timeout) {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.writeNext(self.buffer, make_timeout);
    };
    self.writeFinished = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.writeFinished(self.buffer);
    };
    self.size = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.size(self.buffer);
    };
    self.getGridId = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.gridId;
    };
    self.timeout = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.timeout(self.buffer);
    };
    self.gridSize = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.gridSize(self.buffer);
    };
    self.uniqueId = function() {
      if (!self.buffer) {
        return 0;
      }
      return self.buffer.target.uniqueId(self.buffer);
    };
    self.copy = function() {
      return new writer(self.buffer.copy());
    };
    return true;
  };

  s.readerWriter = {
    reader: reader,
    writer: writer
  };

  if (isNode) {
    module.exports = {
      reader: reader,
      writer: writer
    };
  }

}).call(this);
