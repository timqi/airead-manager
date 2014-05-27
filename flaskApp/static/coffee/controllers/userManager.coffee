define ['./base'], (indexCtlModule) ->
  console.log 'userManager init'
  indexCtlModule.controller 'userManagerCtl',
    [
      '$scope'
      '$http'
      ($scope, $http) ->
        $scope.pageTitle = '用户管理'

        $scope.columnCollection = [
            {label: 'username', map: 'username'},
            {label: 'Email', map: 'email', type: 'email', isEditable: true}
        ];

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

        $scope.query()
    ]
