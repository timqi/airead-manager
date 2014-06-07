define [
  './base'
  'static/lib/async'
], (indexCtlModule, async) ->
  moduleName = 'groupManager'
  console.log "#{moduleName} init"
  indexCtlModule.controller "#{moduleName}Ctl",
    [
      '$scope'
      '$http'
      '$dialogs'
      'ngTableParams'
      'notificationService'
      ($scope, $http, $dialogs, ngTableParams, notificationService) ->
        $scope.pageTitle = '用户组管理'

        $scope.objs = []

        $scope.tableParams = new ngTableParams {
          page: 1
          count: 20
        }, {
          counts: [10, 20, 50],
          total: $scope.objs.length,
          getData: ($defer, params) ->
            tabData = $scope.objs;
            tabElems = tabData.slice((params.page() - 1) * params.count(), params.page() * params.count());
            params.total tabElems.length
            $defer.resolve tabElems
        }

        main = () ->
          $scope.query()

        $scope.query = () ->
          $scope.loading = true
          $scope.objs = []

          url = '/groups/infos/'
          console.log 'get %s', url
          $http.get url
          .success (data) ->
              console.log 'receive data: ', data

              $scope.objs = data
              $scope.tableParams.reload()
          .error (data) ->
              console.log 'get %s failed %s', url, data
          .finally () ->
              $scope.loading = false

        getPermId = (name, perms) ->
          for perm in perms
            if perm.name == name
              return perm.id
          return null

        $scope.add = () ->
          group =
            'name': '组名称'
            'permission_names': []

          $scope.addDisabled = true
          dia = $dialogs.create 'templates/groupManagerEdit.html',
            ManagerEditCtl, group, {}

          dia.result.then (obj) ->
            group = obj.group
            perms = obj.perms
            needAddPermIds = (perm.id for perm in perms)
            console.log 'need add perms ', perms, needAddPermIds
            console.log 'add obj', obj
            $http.post '/groups/', $.param(group)
            .success (data) ->
                console.log('add success ', data)
                gid = data.id
                async.forEachSeries needAddPermIds, (pid, cb) ->
                  url = '/group_permissions/'
                  data =
                    group_id: gid
                    permission_id: pid
                  console.log "post #{url}, data: ", data
                  $http.post url, $.param(data)
                  .success (data) ->
                      console.log "add group #{pid} success"
                  .error (data) ->
                      errmsg = "add group #{pid} failed"
                      console.log errmsg, data
                      notificationService.notice errmsg
                  .finally ()->
                      cb()
                  , () ->
                    notificationService.success '修改组成功'
                    $scope.tableParams.reload()
                    $scope.addDisabled = false
                    $scope.query()
            .error (data) ->
                console.log('add failed', data)
            .finally () ->
                $scope.query()
          .finally () ->
              $scope.addDisabled = false

        $scope.edit = (group) ->
          originPerms = (perm for perm in group.permission_names)
          console.log 'origin perms: ', originPerms

          $scope.addDisabled = true
          dia = $dialogs.create 'templates/groupManagerEdit.html',
            ManagerEditCtl, group, {}

          dia.result.then (obj) ->
            group = obj.group
            perms = obj.perms
            console.log 'edit obj', obj
            url = "/groups/#{group.id}?at=put"
            $http.post url, $.param(group)
            .success (data) ->
                console.log 'modify user return ', data
                needAddPermNames = _.difference group.permission_names, originPerms
                needAddPermIds = (getPermId(name, perms) for name in needAddPermNames)
                console.log 'need add perms ', needAddPermNames, needAddPermIds

                needRemovePermNames = _.difference originPerms, group.permission_names
                needRemovePermIds = (getPermId(name, perms) for name in needRemovePermNames)
                console.log 'need remove perms ', needRemovePermNames, needRemovePermIds

                async.forEachSeries needAddPermIds, (pid, cb) ->
                  url = '/group_permissions/'
                  data =
                    group_id: group.id
                    permission_id: pid
                  console.log "post #{url}, data: ", data
                  $http.post url, $.param(data)
                  .success (data) ->
                      console.log "add group #{pid} success"
                  .error (data) ->
                      errmsg = "add group #{pid} failed"
                      console.log errmsg, data
                      notificationService.notice errmsg
                  .finally ()->
                      cb()
                , () ->
                  async.forEachSeries needRemovePermIds, (pid, cb) ->
                    url = "/group_permissions/#{group.id}/#{pid}?at=delete"
                    $http.post url
                    .success (data) ->
                        console.log "delete perm #{pid} success"
                    .error (data) ->
                        errmsg = "delete perm #{pid} failed"
                        console.log errmsg, data
                        notificationService.notice errmsg
                    .finally () ->
                        cb()
                  , () ->
                    notificationService.success '修改组成功'
                    $scope.tableParams.reload()
                    $scope.addDisabled = false
                    $scope.query()
            .error (data) ->
                console.log 'modify user reutrn ', data
                notificationService.notice '修改用户失败'

        main()
    ]

  ManagerEditCtl = [
    '$scope'
    '$modalInstance'
    '$http'
    'notificationService'
    'data'
    ($scope, $modalInstance, $http, notificationService, data) ->
      $scope.obj = data
      $scope.perms = []

      queryPerms = () ->
        url = '/permissions/'
        console.log url
        $http.get url
        .success (data) ->
            console.log 'receive perms: ', data
            $scope.perms = data
        .error (data) ->
            console.log 'get groups failed: ', data
            notificationService.notice '获取权限出错'

      queryPerms()

      $scope.cancel = () ->
        $modalInstance.dismiss 'cancel'

      $scope.save = () ->
        ret =
          group: $scope.obj
          perms: $scope.perms
        $modalInstance.close ret
  ]

  ret =
    group: '权限管理'
    item: '用户组管理'
    url: moduleName

  return ret