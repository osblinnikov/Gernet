(function() {
  var isNode, s;

  isNode = typeof module !== "undefined" && module.exports;

  if (isNode) {
    s = {};
    s.cnetsjsTypes = require('./cnetsjsTypes.js');
    s.readerWriter = require('./readerWriter.js');
    s.MessageChannel = require('./MessageChannel.js');
  } else {
    s = self;
  }

  s.mapBuffer = function(curBufId, kernelObjToAddBuffer) {
    var addWorker, self, sendCreateMesg, writeLocally;
    self = this;
    self.curBufId = curBufId;
    self.kernelObjToAddBuffer = kernelObjToAddBuffer;
    if (self.kernelObjToAddBuffer) {
      self.kernelObjToAddBuffer.addBuffer(self);
    }
    self.ports = [];
    self.buffers = [];
    self.buffers_to_read = [];
    self.buffers_addData = [];
    self.buffers_grid_ids = [];
    self.unique_Id = 0;
    self.readers_grid_size = 0;
    self.free_buffers = [];
    self.gridQ = [];
    self.faultyWriteQueue = [];
    self.callbacksOnWrite = [];
    self.callbacksOnRead = [];
    self.channels = [];
    self.srcWorkers = {};
    self.dstWorkers = {};
    self.srcPorts = [];
    self.srcPortsPins = [];
    self.dstPorts = [];
    self.dstPortsPins = [];
    self.amIsource = false;
    self.amIdestination = false;
    self.initialized = false;
    self.gridId = -1;
    self.init = function(buffersLength, unique_Id, readers_grid_size, gridId) {
      var i, _i;
      if (self.initialized) {
        return;
      }
      self.initialized = true;
      for (i = _i = 0; 0 <= buffersLength ? _i < buffersLength : _i > buffersLength; i = 0 <= buffersLength ? ++_i : --_i) {
        self.buffers.push({});
        self.buffers_to_read.push(0);
        self.buffers_addData.push({});
        self.free_buffers.push(i);
        self.buffers_grid_ids.push(-1);
      }
      self.unique_Id = unique_Id;
      self.readers_grid_size = readers_grid_size;
      return self.gridId = gridId;
    };
    self.dispatchMessage = function(ev) {
      var i, lastIndex, msg, p, params, _i, _ref, _s;
      if (typeof self.curBufId !== 'undefined' && ev.data.bufId !== self.curBufId) {
        console.error("wrong buffer id ev.bufId(" + ev.data.bufId + ")!=self.curBufId(" + self.curBufId + ")");
        return;
      }
      msg = ev.data;
      if (msg.type !== 'create' && !self.ports.length) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " dispatchEvent: (!ev.ports)");
        return;
      }
      switch (msg.type) {
        case 'create':
          if (ev.ports) {
            _s = self;
            for (i = _i = 0, _ref = ev.ports.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
              lastIndex = self.ports.length;
              ev.ports[i].onmessage = (function(lastIndex) {
                return function(e) {
                  e.data.portId = lastIndex;
                  if (_s.kernelObjToAddBuffer) {
                    return _s.kernelObjToAddBuffer.onmessage(e);
                  } else {
                    return _s.dispatchMessage(e);
                  }
                };
              })(lastIndex);
              self.ports.push({
                wrk: ev.ports[i],
                bufId: msg.data.portsBufIds[i]
              });
            }
          }
          if (msg.data.connectLocal && self.kernelObjToAddBuffer && typeof curBufId !== 'undefined') {
            self.ports.push({
              wrk: self.kernelObjToAddBuffer,
              bufId: -10
            });
            self.kernelObjToAddBuffer.directPortId = self.ports.length - 1;
          }
          if (self.buffers.length > 0 || self.initialized) {
            console.error("ERROR: mapBuffer " + self.unique_Id + " dispatchEvent create: multiple initialization msg: type=" + msg.type);
            return null;
          }
          p = msg.data;
          return self.init(p.buffersLength, p.unique_Id, p.readers_grid_size, p.gridId);
        case 'write':
          if (!msg.data.additionalData) {
            msg.data.additionalData = {};
          }
          if (self.amIsource) {
            console.error(self.amIsource + " " + self.unique_Id + " write msg.portId " + msg.portId);
            return null;
          }
          msg.data.additionalData.bufId = msg.data.ownBufId;
          msg.data.additionalData.portId = msg.portId;
          msg.data.additionalData.internalId = msg.data.internalId;
          self.faultyWriteQueue.push(msg.data);
          return writeLocally();
        case 'read':
          if (!msg.data.additionalData) {
            msg.data.additionalData = {};
          }
          if (self.amIdestination) {
            console.error(self.amIdestination + " " + self.unique_Id + " read msg.portId " + msg.portId);
            return null;
          }
          msg.data.additionalData.portId = msg.portId;
          params = new s.cnetsjsTypes.bufferKernelParams(self, -1, msg.data.additionalData);
          params.internalId = msg.data.internalId;
          self.readFinished(params);
          return writeLocally();
        default:
          console.error("ERROR: mapBuffer " + self.unique_Id + " dispatchEvent: unknown msg: type=" + msg.type);
      }
    };
    writeLocally = function() {
      var params, r, _results;
      _results = [];
      while (self.faultyWriteQueue.length > 0) {
        params = new s.cnetsjsTypes.bufferKernelParams(self, self.faultyWriteQueue[0].gridId, self.faultyWriteQueue[0].additionalData);
        r = self.writeNext(params);
        if (r !== null) {
          r.obj = (self.faultyWriteQueue.shift()).obj;
          _results.push(self.writeFinished(params));
        } else {
          break;
        }
      }
      return _results;
    };
    self.getReader = function(callback) {
      var container;
      if (self.amIsource) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " getReader: you are setting me destination, but i'm already source, i can't be destination and source at the same time");
        return null;
      }
      self.amIdestination = true;
      container = {};
      if (typeof callback === 'function') {
        self.callbacksOnWrite.push(callback);
      }
      return new s.readerWriter.reader(new s.cnetsjsTypes.bufferKernelParams(self, self.gridId, container));
    };
    self.getWriter = function(callback) {
      var container;
      if (self.amIdestination) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " getWriter: you are setting me source, but i'm already destination, i can't be destination and source at the same time");
        return null;
      }
      self.amIsource = true;
      container = {};
      if (typeof callback === 'function') {
        self.callbacksOnRead.push(callback);
      }
      return new s.readerWriter.writer(new s.cnetsjsTypes.bufferKernelParams(self, -1, container));
    };
    self.readNext = function(params) {
      return self.readNextWithMeta(params).data;
    };
    self.readNextWithMeta = function(params) {
      var m, res;
      res = new s.cnetsjsTypes.bufferReadData();
      if (self !== params.target) {
        return res;
      }
      m = params.target;
      if (m === null || self.readers_grid_size === 0) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " readNextWithMeta: Some Input parameters are wrong");
        return res;
      }
      if (self.gridQ.length > 0) {
        params.internalId = self.gridQ.shift();
        if (params.internalId >= 0 && params.internalId < self.buffers.length) {
          res.data = self.buffers[params.internalId];
          res.writer_grid_id = self.buffers_grid_ids[params.internalId];
        }
      }
      return res;
    };
    self.readFinished = function(params) {
      var i, m, msgToSend, objPort, _i, _ref;
      if (self !== params.target) {
        return -1;
      }
      m = params.target;
      if (m === null || self.readers_grid_size === 0) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " readFinished: Some Input parameters are wrong");
        return -1;
      }
      if (--self.buffers_to_read[params.internalId] > 0) {
        return 0;
      }
      self.free_buffers.push(params.internalId);
      if (typeof self.buffers_addData[params.internalId].portId !== 'undefined' && self.buffers_addData[params.internalId].portId >= 0) {
        objPort = self.ports[self.buffers_addData[params.internalId].portId];
        msgToSend = {
          unique_Id: self.unique_Id,
          bufId: self.buffers_addData[params.internalId].bufId,
          type: 'read',
          data: {
            internalId: self.buffers_addData[params.internalId].internalId
          }
        };
        objPort.wrk.postMessage(msgToSend);
        self.buffers_addData[params.internalId].portId = void 0;
      }
      for (i = _i = 0, _ref = self.callbacksOnRead.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
        self.callbacksOnRead[i](self.curBufId, self);
      }
      return 0;
    };
    self.writeNext = function(params) {
      var m, res;
      res = null;
      if (self !== params.target) {
        return res;
      }
      m = params.target;
      if (m === null || self.readers_grid_size === 0) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " writeNext: Some Input parameters are wrong");
        return res;
      }
      if (self.free_buffers.length > 0) {
        params.internalId = self.free_buffers.shift();
        if (self.buffers_to_read[params.internalId] > 0) {
          console.error("ERROR: mapBuffer " + self.unique_Id + " writeNext: ERROR not all readers read buffer " + params.internalId + ", there are " + self.buffers_to_read[params.internalId] + " remain!\n");
          return res;
        }
        res = self.buffers[params.internalId];
        self.buffers_addData[params.internalId] = params.additionalData;
      }
      return res;
    };
    self.writeFinished = function(params) {
      var i, m, msgToSend, res, _i, _j, _ref, _ref1;
      res = -1;
      if (self !== params.target) {
        return res;
      }
      m = params.target;
      if (m === null || self.readers_grid_size === 0) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " writeFinished: Some Input parameters are wrong");
        return res;
      }
      if (self.buffers_to_read[params.internalId] > 0) {
        console.error("ERROR: mapBuffer " + self.unique_Id + " writeFinished: ERROR not all readers read buffer " + params.internalId + ", there are " + self.buffers_to_read[params.internalId] + " remain!\n");
        return res;
      }
      if (self.amIsource) {
        self.buffers_to_read[params.internalId] = self.readers_grid_size;
      } else {
        self.buffers_to_read[params.internalId] = 1;
      }
      if (self.amIsource && typeof self.buffers_addData[params.internalId].portId === 'undefined') {
        for (i = _i = 0, _ref = self.ports.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
          msgToSend = {
            unique_Id: self.unique_Id,
            bufId: self.ports[i].bufId,
            type: 'write',
            data: {
              gridId: self.gridId,
              obj: self.buffers[params.internalId].obj,
              internalId: params.internalId,
              ownBufId: self.curBufId
            }
          };
          self.ports[i].wrk.postMessage(msgToSend);
        }
      }
      if (self.amIdestination) {
        self.gridQ.push(params.internalId);
        self.buffers_grid_ids[params.internalId] = params.grid_id;
      }
      for (i = _j = 0, _ref1 = self.callbacksOnWrite.length; 0 <= _ref1 ? _j < _ref1 : _j > _ref1; i = 0 <= _ref1 ? ++_j : --_j) {
        self.callbacksOnWrite[i](self.curBufId, self);
      }
      return res;
    };
    self.size = function(params) {
      return self.buffers.length;
    };
    self.gridSize = function(params) {
      return self.readers_grid_size;
    };
    self.uniqueId = function(params) {
      return self.unique_Id;
    };
    self.syncConnections = function() {
      var gridId, worker, _ref, _ref1;
      _ref = self.srcWorkers;
      for (gridId in _ref) {
        worker = _ref[gridId];
        if (worker !== self) {
          sendCreateMesg(worker, self.dstPorts, self.dstPortsPins, gridId);
        }
      }
      _ref1 = self.dstWorkers;
      for (gridId in _ref1) {
        worker = _ref1[gridId];
        if (worker !== self) {
          sendCreateMesg(worker, self.srcPorts, self.srcPortsPins, gridId);
        }
      }
      return true;
    };
    sendCreateMesg = function(worker, ports, portsPins, gridId) {
      var msgToSend;
      msgToSend = {
        unique_Id: self.unique_Id,
        bufId: worker.pinId,
        type: 'create',
        data: {
          gridId: gridId,
          connectLocal: worker.connectLocal,
          portsBufIds: portsPins,
          buffersLength: self.size(),
          unique_Id: self.unique_Id,
          readers_grid_size: self.gridSize()
        }
      };
      return worker.wrk.postMessage(msgToSend, ports);
    };
    addWorker = function(isSrc, gridId, wrk, thisBufferPinIdInWorker, port) {
      var portCont, portContIds, wrks;
      if (isSrc) {
        wrks = self.srcWorkers;
        portCont = self.srcPorts;
        portContIds = self.srcPortsPins;
      } else {
        wrks = self.dstWorkers;
        portCont = self.dstPorts;
        portContIds = self.dstPortsPins;
      }
      if (wrks[gridId]) {
        console.log("debug: several connections on the same worker");
        return;
      }
      if (!wrk) {
        wrks[gridId] = {
          wrk: self
        };
        return;
      }
      if (port) {
        portCont.push(port);
        portContIds.push(thisBufferPinIdInWorker);
      }
      wrks[gridId] = {
        connectLocal: !port,
        pinId: thisBufferPinIdInWorker,
        wrk: wrk
      };
      return true;
    };
    self.addConnection = function(srcWrk, srcWrkPin, srcWrkIdInRWGrid, dstWrk, dstWrkPin, dstWrkIdInRWGrid) {
      var ch, lastIndex, _s;
      if (srcWrk && dstWrk) {
        ch = new s.MessageChannel();
        self.channels.push(ch);
        addWorker(true, srcWrkIdInRWGrid, srcWrk, srcWrkPin, ch.port1);
        addWorker(false, dstWrkIdInRWGrid, dstWrk, dstWrkPin, ch.port2);
      } else if (srcWrk) {
        if (self.amIsource) {
          console.error("ERROR: mapBuffer " + self.unique_Id + " addConnection: you are setting me destination, but i'm already source, i can't be destination and source at the same time");
          return -1;
        }
        self.amIdestination = true;
        _s = self;
        self.ports.push({
          wrk: srcWrk,
          bufId: dstWrkPin
        });
        lastIndex = self.ports.length - 1;
        srcWrk.addEventListener("message", function(e) {
          if (e.data.unique_Id !== self.unique_Id) {
            return;
          }
          e.data.portId = lastIndex;
          if (_s.kernelObjToAddBuffer) {
            return _s.kernelObjToAddBuffer.onmessage(e);
          } else {
            return _s.dispatchMessage(e);
          }
        }, false);
        addWorker(true, srcWrkIdInRWGrid, srcWrk, srcWrkPin, false);
      } else if (dstWrk) {
        if (self.amIdestination) {
          console.error("ERROR: mapBuffer " + self.unique_Id + " addConnection: you are setting me source, but i'm already destination, i can't be destination and source at the same time");
          return -1;
        }
        self.amIsource = true;
        _s = self;
        self.ports.push({
          wrk: dstWrk,
          bufId: dstWrkPin
        });
        lastIndex = self.ports.length - 1;
        dstWrk.addEventListener("message", function(e) {
          if (e.data.unique_Id !== self.unique_Id) {
            return;
          }
          e.data.portId = lastIndex;
          if (_s.kernelObjToAddBuffer) {
            return _s.kernelObjToAddBuffer.onmessage(e);
          } else {
            return _s.dispatchMessage(e);
          }
        }, false);
        addWorker(false, dstWrkIdInRWGrid, dstWrk, dstWrkPin, false);
      } else {
        console.error("ERROR: mapBuffer " + self.unique_Id + " addConnection: neither source nor destination was specified");
        return -1;
      }
      return 0;
    };
    return true;
  };

  if (isNode) {
    module.exports = s.mapBuffer;
  }

}).call(this);
