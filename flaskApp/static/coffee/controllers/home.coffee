define ['./base'], (indexCtlModule) ->
  console.log('home init')
  indexCtlModule.controller 'HomeCtl',
    [
      '$scope',
      ($scope) ->
        $scope.pageTitle = 'home'
    ]
