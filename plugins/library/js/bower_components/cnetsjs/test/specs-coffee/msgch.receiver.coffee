channelPort = undefined
@onmessage = (e) ->
  msg = e.data
  ports = e.ports
  if ports && ports.length
    channelPort = ports[0]
    channelPort.onmessage = getChannelMessage
    # console.log "recevier received: port "
  # else
    # console.log "receiver received: "+msg
  return

getChannelMessage = (e)->
  msg = e.data
  # console.log "receiver getChannelMessage "+msg
  postMessage(msg)
  close()