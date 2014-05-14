define ['./base'], (indexCtlModule) ->
  indexCtlModule.controller 'MainCtl',
    [
      '$scope',
      ($scope) ->
        $scope.name = 'Airead Fan'
    ]
