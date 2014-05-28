define ['./base', 'dialogs'], (indexCtlModule) ->
  console.log 'userManager init'
  indexCtlModule.controller 'userManagerCtl',
    [
      '$scope'
      '$http'
      '$dialogs'
      ($scope, $http, $dialogs) ->
        $scope.pageTitle = '用户管理'

        $scope.columnCollection = [
            {label: 'username', map: 'username'},
            {label: 'Email', map: 'email', type: 'email', isEditable: true}
        ];

        main = () ->
          $scope.query()

        $scope.query = () ->
          $scope.loading = true
          $scope.userCollection = []

          url = '/users/'
          console.log 'get %s', url
          $http.get url
            .success (data) ->
              console.log 'receive data: ', data

              for record in data
                user =
                  username: record.username
                  email: record.email

                console.log 'user', user
                $scope.userCollection.push user
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