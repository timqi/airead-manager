treeDef =
  '系统管理':
    '节假日': '1'
    '数据管理': '2'
    '数据库设置': '3'
    '系统设置': '4'

  '权限管理':
    '管理组设置': 1
    '用户': 2

define ['./base'], (indexCtlModule) ->
  console.log('home init')
  indexCtlModule.controller 'HomeCtl',
    [
      '$scope',
      ($scope) ->
        $scope.True = true
        $scope.name = 'Airead Fan'
        $scope.treeDef = treeDef
        $scope.navHeaderList = ['系统管理', '权限管理']


    ]
