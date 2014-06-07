define [
  './base'
  './home'
  './userManager'
  './test'
], (indexCtlModule) ->
  moduleName = 'main'

  ret =
    group: 'hide'
    item: 'main'
    url: moduleName

  args = Array.prototype.slice.apply arguments
  modules = args.slice(1)
  modules.push(ret)

  indexCtlModule.controller 'mainCtl',
    [
      '$scope',
      ($scope) ->
        genTreeDef = (moduleList) ->
          treeDef = {}
          for m in moduleList
            if not treeDef[m.group]
              treeDef[m.group] = {}

            treeDef[m.group][m.item] =
              name: m.item
              url: m.url
              needPerm: m.needPerm

          return treeDef


        $scope.name = 'Airead Fan'
        $scope.True = true
        $scope.treeDef = genTreeDef(modules)
        $scope.navHeaderList = ['系统管理', '权限管理']
    ]


  return modules
