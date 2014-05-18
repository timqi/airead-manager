treeDef =
  '系统管理':
    '节假日': '1'
    '数据管理': '2'
    '数据库设置': '3'
    '系统设置': '4'

  '权限管理':
    '管理组设置': ''
    '用户': 'userManager'


define ['./base'], (indexCtlModule) ->
  indexCtlModule.controller 'MainCtl',
    [
      '$scope',
      ($scope) ->
        $scope.name = 'Airead Fan'
        $scope.True = true
        $scope.treeDef = treeDef
        $scope.navHeaderList = ['系统管理', '权限管理']
    ]
