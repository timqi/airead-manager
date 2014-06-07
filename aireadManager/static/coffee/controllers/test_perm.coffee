'use strict'
define [
  './base'
  'static/lib/async'
], (indexCtlModule, async) ->
  moduleName = 'test_perm'
  console.log "#{moduleName} init"

  indexCtlModule.controller "#{moduleName}Ctl",
    [
      '$scope'
      '$http'
      'ngTableParams'
      'notificationService'
      ($scope, $http, ngTableParams, notificationService) ->
        $scope.pageTitle = '权限测试'
        $scope.permissions = []

        $scope.tableParams = new ngTableParams {
          page: 1,
          count: 10
        }, {
          counts: [10, 20, 50],
          total: $scope.permissions.length,
          getData: ($defer, params) ->
            tabData = $scope.permissions;
            tabElems = tabData.slice((params.page() - 1) * params.count(), params.page() * params.count());
            params.total(tabElems.length)
            $defer.resolve(tabElems)
        }

        getUserPermissions = () ->
          url = '/users/infos/now'
          $http.get(url)
            .success (data) ->
              console.log 'recevice data: ', data
              $scope.userInfo = data
            .error (data) ->
              console.log "get #{url} error: ", data

        getUserPermissions()

        getPermissions = () ->
          url = '/permissions/'
          $http.get(url)
            .success (data) ->
              console.log 'recevice permissions: ', data
              $scope.permissions = data
              $scope.tableParams.reload()
            .error (data) ->
              console.log "get #{url} error: ", data

        getPermissions()

        $scope.hasPerm = (perm) ->
          return perm in $scope.userInfo['permission_tags']

        testPerm = (perm, cb) ->
          ret = true

          url = "/test_perm/#{perm}"
          console.log "test url: #{url}"
          $http.get url
            .success (data) ->
              console.log 'test success: ', data
              ret = true
            .error (data) ->
              console.log 'test error: ', data
              ret = false
            .finally () ->
              cb(ret)

        $scope.testPerms = () ->
          async.forEachSeries $scope.permissions, (perm, cb) ->
            testPerm perm['tag'], (result) ->
              perm.tested = true
              perm.testRet = result
              cb()
          , () ->
            notificationService.success '测试完成'

    ]

  ret =
    group: 'hide'
    item: '权限测试'
    url: moduleName

  return ret