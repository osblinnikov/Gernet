isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

bufferReadData = ->
  self = this
  self.nested_buffer_id = 0
  self.writer_grid_id = 0
  self.data = null
  true

bufferKernelParams = (target, grid_id, additionalData)->
  self = this
  self.target = target
  self.additionalData = additionalData
  self.grid_id = grid_id
  self.internalId = 0
  self.copy = ->
    return new bufferKernelParams(self.target, self.grid_id, self.additionalData)
  self.getObj = ->
    return {additionalData: self.additionalData, grid_id: self.grid_id, internalId: self.internalId}
  true


s.cnetsjsTypes =
  bufferReadData: bufferReadData
  bufferKernelParams: bufferKernelParams

if isNode
  module.exports = 
    bufferReadData: bufferReadData
    bufferKernelParams: bufferKernelParams