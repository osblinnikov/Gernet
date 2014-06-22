(function() {
  var bufferKernelParams, bufferReadData, isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
  } else {
    s = self;
  }

  bufferReadData = function() {
    var self;
    self = this;
    self.nested_buffer_id = 0;
    self.writer_grid_id = 0;
    self.data = null;
    return true;
  };

  bufferKernelParams = function(target, grid_id, additionalData) {
    var self;
    self = this;
    self.target = target;
    self.additionalData = additionalData;
    self.grid_id = grid_id;
    self.internalId = 0;
    self.copy = function() {
      return new bufferKernelParams(self.target, self.grid_id, self.additionalData);
    };
    self.getObj = function() {
      return {
        additionalData: self.additionalData,
        grid_id: self.grid_id,
        internalId: self.internalId
      };
    };
    return true;
  };

  s.cnetsjsTypes = {
    bufferReadData: bufferReadData,
    bufferKernelParams: bufferKernelParams
  };

  if (isNode) {
    module.exports = {
      bufferReadData: bufferReadData,
      bufferKernelParams: bufferKernelParams
    };
  }

}).call(this);
