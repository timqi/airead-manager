define ['./base'], (indexCtlModule) ->
  console.log('userManager init')
  indexCtlModule.controller 'userManagerCtl',
    [
      '$scope',
      ($scope) ->
        $scope.pageTitle = '用户管理'
    ]
