define [
  './base',
  './main',
  './home',
  './userManager',
  './test'
], (controllerModule) ->
  ctlList = []
  for q in controllerModule._invokeQueue
    name = q[2][0]
    throw 'controller name not end with Ctl' if name.slice(-3) != 'Ctl'
    ctlList.push(name.slice(0, -3))

  ctlList
