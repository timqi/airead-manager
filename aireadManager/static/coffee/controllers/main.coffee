define [
  './base'
  './test'
  './home'
  './userManager'
  './groupManager'
  './test_perm'
], (indexCtlModule) ->
  moduleName = 'main'

  indexCtlModule.controller 'mainCtl',
    [
      '$scope'
      '$rootScope'
      '$http'
      'notificationService'
      ($scope, $rootScope, $http, notificationService) ->
        $scope.name = 'Airead Fan'
        $scope.True = true
        $scope.treeDef = {}
        $scope.navHeaderList = ['系统管理', '权限管理', 'hide']

        genTreeDef = (moduleList, user) ->
          treeDef = {}
          for m in moduleList
            if m.role
              if m.role not in user.permission_tags
                continue

            if not treeDef[m.group]
              treeDef[m.group] = {}

            treeDef[m.group][m.item] =
              name: m.item
              url: m.url
              needPerm: m.needPerm

          return treeDef

        getUser = () ->
          url = '/users/infos/now'
          console.log "get #{url}"
          $http.get url
          .success (data) ->
              console.log 'get cur user: ', data
              $scope.curUser = data
              $scope.treeDef = genTreeDef(modules, $scope.curUser)
          .error (err) ->
              console.log 'get current user failed', err
              notificationService.notice '获取当前用户失败'

        getUser()
    ]

  ret =
    group: 'hide'
    item: 'main'
    url: moduleName

  args = Array.prototype.slice.apply arguments
  modules = args.slice(1)
  modules.push(ret)

  return modules
