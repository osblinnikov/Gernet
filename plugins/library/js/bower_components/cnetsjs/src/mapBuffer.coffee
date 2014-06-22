isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.cnetsjsTypes = require('./cnetsjsTypes.js')
  s.readerWriter = require('./readerWriter.js')
  s.MessageChannel = require('./MessageChannel.js')
else
  s = self

s.mapBuffer = (curBufId, kernelObjToAddBuffer)->
  self = this
  self.curBufId = curBufId
  self.kernelObjToAddBuffer = kernelObjToAddBuffer
  if self.kernelObjToAddBuffer
    self.kernelObjToAddBuffer.addBuffer(self)
  self.ports = []

  self.buffers = []
  self.buffers_to_read = []
  self.buffers_addData = []
  self.buffers_grid_ids = []

  self.unique_Id = 0
  self.readers_grid_size = 0

  self.free_buffers = []
  self.gridQ = []

  self.faultyWriteQueue = []
  
  self.callbacksOnWrite = []
  self.callbacksOnRead = []

  self.channels = [] #channels for data transfer
  self.srcWorkers = {}
  self.dstWorkers = {}
  self.srcPorts = []
  self.srcPortsPins = []
  self.dstPorts = []
  self.dstPortsPins = []
  self.amIsource = false
  self.amIdestination = false
  self.initialized = false
  self.gridId = -1

  self.init = (buffersLength,unique_Id,readers_grid_size,gridId)->
    if self.initialized
      return
    self.initialized = true

    for i in [0...buffersLength]
      self.buffers.push({})
      self.buffers_to_read.push(0)
      self.buffers_addData.push({})
      self.free_buffers.push(i)
      self.buffers_grid_ids.push(-1)
    self.unique_Id = unique_Id
    self.readers_grid_size = readers_grid_size
    self.gridId = gridId
    # console.log "mapBuffer "+self.unique_Id+"  INIT: self.gridId "+self.gridId

  self.dispatchMessage = (ev)->
    if  typeof self.curBufId != 'undefined' and ev.data.bufId!=self.curBufId
      console.error "wrong buffer id ev.bufId("+ev.data.bufId+")!=self.curBufId("+self.curBufId+")"
      return
    # if typeof portId == 'undefined'
    #   portId = -1 #indicates that event received via local onmessage, or direct call
    msg = ev.data

    if msg.type!='create' and !self.ports.length
      console.error "ERROR: mapBuffer "+self.unique_Id+" dispatchEvent: (!ev.ports)"
      return

    switch msg.type
      when 'create'
        if ev.ports
          _s = self
          for i in [0...ev.ports.length]
            lastIndex = self.ports.length
            ev.ports[i].onmessage = ((lastIndex) ->
                return (e)->
                  # e.data.bufId = _s.curBufId
                  e.data.portId = lastIndex
                  if _s.kernelObjToAddBuffer
                    _s.kernelObjToAddBuffer.onmessage(e)
                  else
                    _s.dispatchMessage(e)
              )(lastIndex)
            self.ports.push {wrk:ev.ports[i], bufId: msg.data.portsBufIds[i]}


        if msg.data.connectLocal and self.kernelObjToAddBuffer and typeof curBufId != 'undefined'
          self.ports.push {wrk:self.kernelObjToAddBuffer, bufId:-10}
          self.kernelObjToAddBuffer.directPortId = self.ports.length - 1

        if self.buffers.length > 0 || self.initialized
          console.error "ERROR: mapBuffer "+self.unique_Id+" dispatchEvent create: multiple initialization msg: type="+msg.type
          return null

        p = msg.data
        self.init(p.buffersLength,p.unique_Id,p.readers_grid_size,p.gridId)

      when 'write'
        if !msg.data.additionalData
          msg.data.additionalData = {}
        if self.amIsource
          console.error self.amIsource+" "+self.unique_Id+" write msg.portId "+msg.portId
          return null
        msg.data.additionalData.bufId = msg.data.ownBufId
        msg.data.additionalData.portId = msg.portId
        msg.data.additionalData.internalId = msg.data.internalId #need to store, for sending it back
        self.faultyWriteQueue.push(msg.data)
        #write messages from faulty queue
        writeLocally()

      when 'read'
        if !msg.data.additionalData
          msg.data.additionalData = {}
        if self.amIdestination
          console.error self.amIdestination+" "+self.unique_Id+" read msg.portId "+msg.portId
          return null
        msg.data.additionalData.portId = msg.portId
        params = new s.cnetsjsTypes.bufferKernelParams(self, -1, msg.data.additionalData)
        params.internalId = msg.data.internalId
        # console.log "mapBuffer "+self.unique_Id+" read!"
        self.readFinished(params)
        #write messages from faulty queue
        writeLocally()
        
      else
        console.error "ERROR: mapBuffer "+self.unique_Id+" dispatchEvent: unknown msg: type="+msg.type
        return
      
  writeLocally = ->
    while self.faultyWriteQueue.length > 0
      # console.log "self.faultyWriteQueue[0].gridId "+self.faultyWriteQueue[0].gridId
      params = new s.cnetsjsTypes.bufferKernelParams(self, self.faultyWriteQueue[0].gridId, self.faultyWriteQueue[0].additionalData)
      # console.log "mapBuffer "+self.unique_Id+" writeNext: params.additionalData.portId "+params.additionalData.portId
      r = self.writeNext(params)
      if r != null
        # console.log "writeLocally"
        r.obj = (self.faultyWriteQueue.shift()).obj
        self.writeFinished(params)
      else
        break
  
  self.getReader = (callback)->
    if self.amIsource
      console.error "ERROR: mapBuffer "+self.unique_Id+" getReader: you are setting me destination, but i'm already source, i can't be destination and source at the same time"
      return null
    self.amIdestination = true
    container = {}
    if typeof callback == 'function'
      self.callbacksOnWrite.push(callback)
    # console.log "mapBuffer "+self.unique_Id+" self.gridId "+self.gridId
    return new s.readerWriter.reader(new s.cnetsjsTypes.bufferKernelParams(self,self.gridId,container))

  self.getWriter = (callback)->
    if self.amIdestination
      console.error "ERROR: mapBuffer "+self.unique_Id+" getWriter: you are setting me source, but i'm already destination, i can't be destination and source at the same time"
      return null
    self.amIsource = true
    container = {}
    if typeof callback == 'function'
      self.callbacksOnRead.push(callback)
    return new s.readerWriter.writer(new s.cnetsjsTypes.bufferKernelParams(self,-1,container))

  self.readNext = (params)->
    return self.readNextWithMeta(params).data
  
  self.readNextWithMeta = (params)->
    res = new s.cnetsjsTypes.bufferReadData()
    if self != params.target
      return res
    m = params.target
    if m==null or self.readers_grid_size == 0
      console.error "ERROR: mapBuffer "+self.unique_Id+" readNextWithMeta: Some Input parameters are wrong"
      return res

    if self.gridQ.length > 0
      params.internalId = self.gridQ.shift()
      if params.internalId >= 0 && params.internalId < self.buffers.length
        res.data = self.buffers[params.internalId]
        res.writer_grid_id = self.buffers_grid_ids[params.internalId]

    return res

  self.readFinished = (params)->
    # console.log "mapBuffer "+self.unique_Id+" readFinished:"
    if self != params.target
      return -1
    m = params.target
    if m==null or self.readers_grid_size == 0
      console.error "ERROR: mapBuffer "+self.unique_Id+" readFinished: Some Input parameters are wrong"
      return -1
    
    if --self.buffers_to_read[params.internalId] > 0
      return 0
    # console.log "mapBuffer "+self.unique_Id+" readFinished: buffers_to_read["+params.internalId+"]  = "+self.buffers_to_read[params.internalId]
    self.free_buffers.push(params.internalId)

    #check if it was written by another worker
    if typeof self.buffers_addData[params.internalId].portId != 'undefined' and self.buffers_addData[params.internalId].portId >= 0
      # console.log "send read"
      objPort = self.ports[self.buffers_addData[params.internalId].portId]
      # console.log objPort.wrk
      msgToSend = 
        unique_Id: self.unique_Id
        bufId: self.buffers_addData[params.internalId].bufId
        type: 'read'
        data:
          internalId: self.buffers_addData[params.internalId].internalId
      objPort.wrk.postMessage(msgToSend)
      # console.log self.buffers_addData[params.internalId].portId
      self.buffers_addData[params.internalId].portId = undefined #clean up the info
    # else
    #   console.log ("mapBuffer "+self.unique_Id+" readFinished: locally written - locally read")
    for i in [0...self.callbacksOnRead.length]
      self.callbacksOnRead[i](self.curBufId,self)#to notify local readers
    
    return 0
  
  self.writeNext = (params)->
    res = null
    if self != params.target
      return res
    m = params.target
    if m==null or self.readers_grid_size == 0
      console.error "ERROR: mapBuffer "+self.unique_Id+" writeNext: Some Input parameters are wrong"
      return res
    if self.free_buffers.length > 0
      params.internalId = self.free_buffers.shift()
      if self.buffers_to_read[params.internalId] > 0
        console.error "ERROR: mapBuffer "+self.unique_Id+" writeNext: ERROR not all readers read buffer "+params.internalId+", there are "+self.buffers_to_read[params.internalId]+" remain!\n"
        return res
      res = self.buffers[params.internalId]
      # if typeof params.additionalData.portId != 
      self.buffers_addData[params.internalId] = params.additionalData
      # else
      #   self.buffers_addData[params.internalId].portId = undefined#to make sure portId is undefined

    return res

  self.writeFinished = (params)->
    res = -1
    if self != params.target
      return res
    m = params.target
    if m==null or self.readers_grid_size == 0
      console.error "ERROR: mapBuffer "+self.unique_Id+" writeFinished: Some Input parameters are wrong"
      return res
    if self.buffers_to_read[params.internalId] > 0
      console.error "ERROR: mapBuffer "+self.unique_Id+" writeFinished: ERROR not all readers read buffer "+params.internalId+", there are "+self.buffers_to_read[params.internalId]+" remain!\n"
      return res

    if self.amIsource
      self.buffers_to_read[params.internalId] = self.readers_grid_size
    else
      self.buffers_to_read[params.internalId] = 1

    if self.amIsource and typeof self.buffers_addData[params.internalId].portId == 'undefined'
      
      for i in [0...self.ports.length]
        # console.log "self.ports[i].bufId "+self.ports[i].bufId
        # console.log "wrote "+self.gridId
        msgToSend = 
          unique_Id: self.unique_Id
          bufId: self.ports[i].bufId
          type: 'write'
          data:
            gridId: self.gridId
            obj: self.buffers[params.internalId].obj
            internalId: params.internalId
            ownBufId: self.curBufId
        self.ports[i].wrk.postMessage(msgToSend)
    # if self.ports.length + 1 < self.readers_grid_size
      # console.warn "WARN: mapBuffer "+self.unique_Id+" writeFinished: self.ports.length + 1 < self.readers_grid_size self.amIdestination="+self.amIdestination

    if self.amIdestination
      self.gridQ.push(params.internalId)
      # console.log "params.grid_id "+params.grid_id
      self.buffers_grid_ids[params.internalId] = params.grid_id

    # if self.callbacksOnWrite.length == 0
    #   console.warn "WARN: mapBuffer "+self.unique_Id+" writeFinished: self.callbacksOnWrite.length == 0 "+self.amIsource+" "+self.buffers_addData[params.internalId].portId
    # else
    for i in [0...self.callbacksOnWrite.length]
      self.callbacksOnWrite[i](self.curBufId,self)#to notify local readers

    return res

  self.size = (params)->
    return self.buffers.length

  self.gridSize = (params)->
    return self.readers_grid_size

  self.uniqueId = (params)->
    return self.unique_Id

  self.syncConnections = ->
    # console.log "sync src"
    for gridId, worker of self.srcWorkers
      if worker!=self
        sendCreateMesg(worker,self.dstPorts, self.dstPortsPins,gridId)

    # console.log "sync dst"
    for gridId, worker of self.dstWorkers
      if worker!=self
        sendCreateMesg(worker,self.srcPorts, self.srcPortsPins,gridId)
    true

  sendCreateMesg = (worker,ports, portsPins,gridId)->
    # console.log "create "+self.unique_Id
    # console.log portsPins
    msgToSend =
      unique_Id: self.unique_Id
      bufId: worker.pinId
      type: 'create'
      data:
        gridId: gridId
        connectLocal: worker.connectLocal
        portsBufIds: portsPins
        buffersLength: self.size()
        unique_Id: self.unique_Id
        readers_grid_size: self.gridSize()
    worker.wrk.postMessage(msgToSend, ports)

  addWorker = (isSrc, gridId, wrk, thisBufferPinIdInWorker, port)->
    if isSrc
      wrks = self.srcWorkers
      portCont = self.srcPorts
      portContIds = self.srcPortsPins
    else
      wrks = self.dstWorkers
      portCont = self.dstPorts
      portContIds = self.dstPortsPins
    if wrks[gridId]
      console.log "debug: several connections on the same worker"
      return
    
    if !wrk
      wrks[gridId] =
        wrk: self #OURSELVES AS WORKER
      #   port: port
      return

    if port
      portCont.push port
      portContIds.push thisBufferPinIdInWorker

    wrks[gridId] =
      connectLocal: !port
      pinId: thisBufferPinIdInWorker
      wrk: wrk

    true

  self.addConnection = (srcWrk,srcWrkPin,srcWrkIdInRWGrid,dstWrk,dstWrkPin,dstWrkIdInRWGrid)->
    if srcWrk and dstWrk
      #we have source and destination workers
      ch = new s.MessageChannel()
      self.channels.push ch
      # console.log "addConnection interconnection"
      addWorker(true,srcWrkIdInRWGrid,srcWrk,srcWrkPin,ch.port1)
      addWorker(false,dstWrkIdInRWGrid,dstWrk,dstWrkPin,ch.port2)

    else if srcWrk
      #we have only source specified, so we are actual destination
      if self.amIsource
        console.error "ERROR: mapBuffer "+self.unique_Id+" addConnection: you are setting me destination, but i'm already source, i can't be destination and source at the same time"
        return -1
      # console.log "addConnection root is destination"
      self.amIdestination = true
      _s = self
      self.ports.push {wrk: srcWrk,bufId:dstWrkPin}
      lastIndex = self.ports.length - 1
      srcWrk.addEventListener("message",(e)->
        # console.log "!!!!!!!!!!!!!!!!!!!!!!!!!!! message to root as destination "+_s.curBufId
        if e.data.unique_Id != self.unique_Id
          # console.error "unique_Id is not match"
          return
        # e.data.bufId = _s.curBufId
        e.data.portId = lastIndex
        if _s.kernelObjToAddBuffer
          _s.kernelObjToAddBuffer.onmessage(e)
        else
          _s.dispatchMessage(e)
      ,false)

      addWorker(true,srcWrkIdInRWGrid,srcWrk,srcWrkPin,false)

    else if dstWrk
      #we have onle destination specified, so we are actual source
      if self.amIdestination
        console.error "ERROR: mapBuffer "+self.unique_Id+" addConnection: you are setting me source, but i'm already destination, i can't be destination and source at the same time"
        return -1
      # console.log "addConnection root is source"
      self.amIsource = true
      _s = self
      self.ports.push {wrk: dstWrk,bufId:dstWrkPin}
      lastIndex = self.ports.length - 1
      dstWrk.addEventListener("message",(e)->
        # console.log "!!!!!!!!!!!!!!!!!!!!!!!!!!! message to root as source "+_s.curBufId
        if e.data.unique_Id != self.unique_Id
          # console.error "unique_Id is not match"
          return
        # e.data.bufId = _s.curBufId
        e.data.portId = lastIndex
        if _s.kernelObjToAddBuffer
          _s.kernelObjToAddBuffer.onmessage(e)
        else
          _s.dispatchMessage(e)
      ,false)

      addWorker(false,dstWrkIdInRWGrid,dstWrk,dstWrkPin,false)

    else
      console.error "ERROR: mapBuffer "+self.unique_Id+" addConnection: neither source nor destination was specified"
      return -1
    return 0

  true

if isNode
  module.exports = s.mapBuffer