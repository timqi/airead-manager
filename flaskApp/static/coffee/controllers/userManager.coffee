define ['./base'], (indexCtlModule) ->
  console.log 'userManager init'
  indexCtlModule.controller 'userManagerCtl',
    [
      '$scope'
      '$http'
      ($scope, $http) ->
        $scope.pageTitle = '用户管理'

        $scope.userCollection = [
          {firstName: 'Laurent', lastName: 'Renard', birthDate: new Date('1987-05-21'), balance: 102, email: 'whatever@gmail.com'},
          {firstName: 'Blandine', lastName: 'Faivre', birthDate: new Date('1987-04-25'), balance: -2323.22, email: 'oufblandou@gmail.com'},
          {firstName: 'Francoise', lastName: 'Frere', birthDate: new Date('1955-08-27'), balance: 42343, email: 'raymondef@gmail.com'}
        ];

        $scope.query = () ->
          $scope.loading = true
          $scope.userCollection = []

          url = '/users/'
          console.log 'get %s', url
          $http.get url
            .success (data) ->
              console.log 'receive data: ', data
              $scope.userCollection = data
            .error (data) ->
              console.log 'get %s failed %s', url, data
            .finally () ->
              $scope.loading = false

        $scope.query()
    ]
