define ['./base'], (indexCtlModule) ->
  console.log('home init')
  indexCtlModule.controller 'HomeCtl',
    [
      '$scope',
      ($scope) ->
        $scope.name = 'Airead Fan'
    ]
