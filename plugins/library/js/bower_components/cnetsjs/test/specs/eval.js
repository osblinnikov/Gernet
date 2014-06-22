(function() {
  this.onmessage = function(code) {
    eval(code.data);
  };

}).call(this);
