isNode = typeof module isnt "undefined" and module.exports

#JUST FOR SIMULATION OF OPENING NESTED CHANNEL AND WORKER
importScripts( '/dist/Worker.js', '/dist/MessageChannel.js')

chan = new MessageChannel()
wrk1 = new Worker("/test/specs/msgch.receiver.js")


channelPort = undefined
@onmessage = (e) ->
  msg = e.data
  ports = e.ports
  if ports && ports.length
    channelPort = ports[0]
    # console.log "sender received: port "
    # channelPort.onmessage = getChannelMessage
  else
    # console.log "sender received: "+msg
    if channelPort
      channelPort.postMessage(msg)
  return