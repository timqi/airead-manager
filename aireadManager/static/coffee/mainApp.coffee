define [
  'angular'
  'controllers/index'
  'angular-route'
  'angular-ui'
  'angular-bootstrap'
  'angular-bootstrap-tpls'
  'smart-table'
  'dialogs'
], (angular, moduleNames) ->
  console.log('mainApp init')
  console.log('find modules: ', moduleNames)
  app = angular.module 'app', [
    'ngRoute',
    'ui.bootstrap'
    'smartTable.table'
    'dialogs'

    # customs
    'controllers'
  ]

  app.moduleList = moduleNames
  app
