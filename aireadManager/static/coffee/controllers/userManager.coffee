define ['./base', 'dialogs'], (indexCtlModule) ->
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
          $scope.addDisabled = true
          dia = $dialogs.create 'templates/userManagerEdit.html',
            userManagerEditCtl, {}, {}

          dia.result.then (obj) ->
            console.log 'add obj', obj
            $http.post '/users/', obj
              .success (data) ->
                console.log('add success ', data)
              .error (data) ->
                console.log('add failed', data)
              .finally () ->
                $scope.query()
          .finally () ->
            $scope.addDisabled = false

        main()
    ]

  userManagerEditCtl = [
    '$scope'
    '$modalInstance'
    'data'
    ($scope, $modalInstance, data) ->
      $scope.obj = data

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
