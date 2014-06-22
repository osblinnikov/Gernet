isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

if !s.Worker or !s.MessageChannel or s.MessageChannelArtificial is true
  s.Worker = (scriptFile) ->
    slf = this
    __timer = null
    __text = []
    __ports = []
    __fileContent = null
    started = false
    slf.internalWorker = {}
    slf.onerror = null
    slf.onmessage = null

    listenersSize = 0
    listeners = {}
    listenersWithCapture = {}
    findListener = (type,listener, useCapture)->
      l = listeners[""+useCapture]
      if not l
        return false

      for i,v of l
        if v == type
          for t,tv of v
            if tv == listener
              return [i,t]
      return false

    slf.addEventListener = (type, listener, useCapture)->
      if !findListener(type, listener, useCapture)
        l = listeners[""+useCapture]
        if not l
          l = listeners[""+useCapture] = {}
        if !l[type]
          l[type] = []
        l[type].push(listener)
        listenersSize++

    slf.removeEventListener = (type, listener, useCapture)->
      r = findListener(type, listener, useCapture)
      if !r
        return
      listeners[""+useCapture][r[0]].splice(r[1], 1)
      listenersSize--
      if listeners[""+useCapture][r[0]].length == 0
        delete listeners[""+useCapture][r[0]]


    slf.dispatchEvent = (evt, pfResult)->
      type = evt.type
      # console.log "dispatchEvent to host"
      if type == 'message' and "function" is typeof slf.onmessage
        slf.onmessage(evt)
      if listenersSize <= 0
        return
      for useCapture,l of listeners
        if useCapture=="false" and not pfResult
          continue
        # console.log "dispatchEvent"
        # l = listeners[useCapture]#for capturing
        for i,v of l
          if i == type
            for t,tv of v
              tv(evt)


    importScripts = ->
      isNode = typeof module isnt "undefined" and module.exports and __dirname

      #turn arguments from pseudo-array in to array in order to iterate it
      params = Array::slice.call(arguments)
      i = 0
      j = params.length

      while i < j
        if isNode
          arrName = params[i].split('/').pop().split('.')
          arrName.pop()
          this[arrName.join('.')] = require(process.cwd()+"/"+params[i])
        else
          script = document.createElement("SCRIPT")
          script.src = params[i]
          script.setAttribute "type", "text/javascript"
          document.getElementsByTagName("HEAD")[0].appendChild script
        i++
      return

    
    
    # child has run its and called for it's parent to be notified
    postMessage = (text) ->
      # console.log "outPost"
      # console.log text
      slf.dispatchEvent({data:text, type:'message'},true)
      # return slf.onmessage(data: text)  if "function" is typeof slf.onmessage
      false
    
    slf.internalWorker =
      postMessage: postMessage


    stop = ->
      slf.terminate()

    
    setImmediate = setImmediate or (cb) ->
      __timer = setTimeout cb, 0
      return

    clearImmediate = clearImmediate or (timer)->
      clearTimeout timer

    requestAnimFrame = (->
      requestAnimationFrame = undefined
      if typeof window!= 'undefined'
        requestAnimationFrame = window.requestAnimationFrame or window.webkitRequestAnimationFrame or window.mozRequestAnimationFrame
      return requestAnimationFrame or (callback) ->
        setTimeout callback, 1
        return
    )()

    # Method that starts the threading
    slf.postMessage = (text,ports) ->
      # console.log "inPost"
      __ports.push(ports)
      __text.push(text)
      __iterate()
      true

    __iterate = ->
      # Execute on a timer so we dont block (well as good as we can get in a single thread)
      # if __timer == null
      #   __timer = setImmediate(__onIterate)

      #request next available moment instead of looping
      requestAnimFrame(__onIterate)
      true

    __onIterate = ->
      if __text.length or __ports.length
        try
          # console.log "postMessage to worker"
          # console.log __text[0]
          slf.internalWorker.onmessage data: __text.shift(), ports:__ports.shift()   if "function" is typeof slf.internalWorker.onmessage
          return true
        catch ex
          return slf.onerror(ex)  if "function" is typeof slf.onerror
      false

    slf.terminate = ->
      if __timer != null
        clearImmediate(__timer)
        __timer = null
      true

    
    # HTTP Request
    getHTTPObject = ->
      xmlhttp = undefined
      try
        xmlhttp = new XMLHttpRequest()
      catch e
        try
          xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        catch e
          xmlhttp = false
      xmlhttp
    
    evalStringContents = (__fileContent)->
      # slf.internalWorker = {}
      eval __fileContent
      if typeof this.onmessage is 'function'
        slf.internalWorker.onmessage = this.onmessage
      # slf.internalWorker.postMessage = postMessage

    http = getHTTPObject()
    if http
      http.open "GET", scriptFile, false
      http.send null
      if http.readyState is 4
        strResponse = http.responseText
        
        #var strResponse = http.responseXML;
        switch http.status
          when 404 # Page-not-found error
            alert "Error: Not Found. The requested function could not be found."
          when 500 # Display results in a full s for server-side errors
            alert strResponse
          else
            __fileContent = strResponse
            # IE functions will become delagates of the instance of Worker
    else
      fs = require('fs')
      __fileContent = fs.readFileSync( process.cwd()+scriptFile, "utf8")
    
    evalStringContents.bind(slf)(__fileContent)
    
    #
    #         at this point we now have:
    #         a delagate "onmessage(event)"
    #         
    # slf.importScripts = (src) ->
      
    #   # hack time, this will import the script but not wait for it to load...
    #   script = document.createElement("SCRIPT")
    #   script.src = src
    #   script.setAttribute "type", "text/javascript"
    #   document.getElementsByTagName("HEAD")[0].appendChild script
    #   true

    true


  if isNode
    module.exports = s.Worker