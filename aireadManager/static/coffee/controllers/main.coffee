define [
  './base'
  './test'
  './home'
  './userManager'
  './groupManager'
  './test_perm'
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
      '$scope'
      '$http'
      'notificationService'
      ($scope, $http, notificationService) ->
        $scope.user = {}
        $scope.name = 'Airead Fan'
        $scope.True = true
        $scope.treeDef = {}
        $scope.navHeaderList = ['系统管理', '权限管理', 'hide']

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

        $scope.treeDef = genTreeDef(modules)

        getUser = () ->
          url = '/users/infos/now'
          console.log "get #{url}"
          $http.get url
          .success (data) ->
              $scope.user = data
          .error (err) ->
              console.log 'get current user failed', err
              notificationService.notice '获取当前用户失败'

        getUser()
    ]


  return modules
