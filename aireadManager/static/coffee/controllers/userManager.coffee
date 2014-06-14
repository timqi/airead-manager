define [
  './base'
  'jQuery'
  'static/lib/async'
  'static/lib/lodash.min'
  'static/js/utils'
  'dialogs'
], (indexCtlModule, $, async, _, utils) ->
  moduleName = 'userManager'
  console.log "#{moduleName} init"
  indexCtlModule.controller "#{moduleName}Ctl",
    [
      '$scope'
      '$http'
      '$dialogs'
      'ngTableParams'
      'notificationService'
      ($scope, $http, $dialogs, ngTableParams, notificationService) ->
        $scope.pageTitle = '用户管理'

        $scope.objs = []

        $scope.userParams = new ngTableParams {
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

          url = '/users/infos/'
          console.log 'get %s', url
          $http.get url
          .success (data) ->
              console.log 'receive data: ', data

              $scope.objs = data
              $scope.userParams.reload()
          .error (err, status) ->
              console.log 'get %s failed ', url, err
              if status == 403
                notificationService.notice '没有权限'
              else
                notificationService.notice '未知错误'

          .finally () ->
              $scope.loading = false

        getGroupId = (name, groups) ->
          for group in groups
            if group.name == name
              return group.id
          return null

        $scope.add = () ->
          user =
            'username': '用户名'
            'first_name': '名字'
            'last_name': '姓',
            'email': 'e@some.com'
            'password': 'password'
            'is_staff': true,
            'is_active': true,
            'is_superuser': false,
            'group_names': [],

          $scope.addDisabled = true
          dia = $dialogs.create 'templates/userManagerEdit.html',
            userManagerEditCtl, user, {}

          dia.result.then (obj) ->
            console.log 'add obj', obj
            user = obj.user
            groups = obj.groups
            needAddGroupIds = (getGroupId(name, groups) for name in user.group_names)

            $http.post '/users/', $.param(user)
            .success (data) ->
                console.log('add success ', data)
                uid = data.id
                async.forEachSeries needAddGroupIds, (gid, cb) ->
                  url = '/user_groups/'
                  data =
                    user_id: uid
                    group_id: gid
                  console.log "post #{url}, data: ", data
                  $http.post url, $.param(data)
                  .success (data) ->
                      console.log "add group #{gid} success"
                  .error (data) ->
                      errmsg = "add group #{gid} failed"
                      console.log errmsg, data
                      notificationService.notice errmsg
                  .finally ()->
                      cb()
                , () ->
                  notificationService.success '修改用户成功'
                  $scope.userParams.reload()
                  $scope.addDisabled = false
                  $scope.query()
            .error (data) ->
                console.log('add failed', data)
                notificationService.notice
          .finally () ->
              $scope.addDisabled = false

        $scope.edit = (user) ->
          originGroups = (group for group in user.group_names)
          console.log 'origin groups: ', originGroups

          $scope.addDisabled = true
          dia = $dialogs.create 'templates/userManagerEdit.html',
            userManagerEditCtl, user, {}

          dia.result.then (obj) ->
            user = obj.user
            groups = obj.groups
            console.log 'edit obj', obj
            url = "/users/#{user.id}?at=put"
            $http.post url, $.param(user)
            .success (data) ->
                console.log 'modify user return ', data
                needAddGroupNames = _.difference user.group_names, originGroups
                needAddGroupIds = (getGroupId(name, groups) for name in needAddGroupNames)
                console.log 'need add groups ', needAddGroupNames, needAddGroupIds

                needRemoveGroupNames = _.difference originGroups, user.group_names
                needRemoveGroupIds = (getGroupId(name, groups) for name in needRemoveGroupNames)
                console.log 'need remove groups ', needRemoveGroupNames, needRemoveGroupIds

                async.forEachSeries needAddGroupIds, (gid, cb) ->
                  url = '/user_groups/'
                  data =
                    user_id: user.id
                    group_id: gid
                  console.log "post #{url}, data: ", data
                  $http.post url, $.param(data)
                  .success (data) ->
                      console.log "add group #{gid} success"
                  .error (data) ->
                      errmsg = "add group #{gid} failed"
                      console.log errmsg, data
                      notificationService.notice errmsg
                  .finally ()->
                      cb()
                , () ->
                  async.forEachSeries needRemoveGroupIds, (gid, cb) ->
                    url = "/user_groups/#{user.id}/#{gid}?at=delete"
                    $http.post url
                    .success (data) ->
                        console.log "delete group #{gid} success"
                    .error (data) ->
                        errmsg = "delete group #{gid} failed"
                        console.log errmsg, data
                        notificationService.notice errmsg
                    .finally () ->
                        cb()
                  , () ->
                    notificationService.success '修改用户成功'
                    $scope.userParams.reload()
                    $scope.addDisabled = false
                    $scope.query()
            .error (data) ->
                console.log 'modify user reutrn ', data
                notificationService.notice '修改用户失败'

        main()
    ]

  userManagerEditCtl = [
    '$scope'
    '$modalInstance'
    '$http'
    'notificationService'
    'data'
    ($scope, $modalInstance, $http, notificationService, data) ->
      $scope.obj = data
      $scope.groups = []

      queryGroups = () ->
        url = '/groups/'
        console.log url
        $http.get url
        .success (data) ->
            console.log 'receive groups: ', data
            $scope.groups = data
        .error (data) ->
            console.log 'get groups failed: ', data
            notificationService.notice '获取用户组出错'

      queryGroups()

      $scope.cancel = () ->
        $modalInstance.dismiss 'cancel'

      $scope.save = () ->
        ret =
          user: $scope.obj
          groups: $scope.groups
        $modalInstance.close ret
  ]

  ret =
    group: '权限管理'
    item: '用户管理'
    role: utils.Roles.admin
    url: moduleName

  return ret
