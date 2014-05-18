define ['./base'], (indexCtlModule) ->
  console.log('home init')
  indexCtlModule.controller 'homeCtl',
    [
      '$scope',
      ($scope) ->
        $scope.pageTitle = 'home'
    ]
