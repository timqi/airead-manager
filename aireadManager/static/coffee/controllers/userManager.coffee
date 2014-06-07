define [
  './base'
  'jQuery'
  'angular'
  'dialogs'
], (indexCtlModule, $, angular) ->
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
          .error (data) ->
              console.log 'get %s failed %s', url, data
          .finally () ->
              $scope.loading = false

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
            $http.post '/users/', $.param(obj)
            .success (data) ->
                console.log('add success ', data)
            .error (data) ->
                console.log('add failed', data)
            .finally () ->
                $scope.query()
          .finally () ->
              $scope.addDisabled = false

        $scope.edit = (user) ->
          $scope.addDisabled = true
          dia = $dialogs.create 'templates/userManagerEdit.html',
            userManagerEditCtl, user, {}

          dia.result.then (obj) ->
            console.log 'edit obj', obj
            url = "/users/#{user.id}?at=put"
            $http.post url, $.param(obj)
            .success (data) ->
                console.log 'modify user return ', data
                notificationService.success '修改用户成功'
            .error (data) ->
                console.log 'modify user reutrn ', data
                notificationService.notice '修改用户失败'
            .finally () ->
                $scope.addDisabled = false
                $scope.query()

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
        $modalInstance.close $scope.obj

  ]

  ret =
    group: '权限管理'
    item: '用户管理'
    url: moduleName

  return ret
