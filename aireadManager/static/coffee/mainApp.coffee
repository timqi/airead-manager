define [
  'angular'
  'static/js/controllers/main'
  'angular-route'
  'angular-ui'
  'angular-bootstrap'
  'angular-bootstrap-tpls'
  'static/lib/ng-table'
  'angular-pnotify'
  'smart-table'
  'dialogs'
], (angular, moduleNames) ->
  console.log('mainApp init')
  console.log('find modules: ', moduleNames)
  app = angular.module 'app', [
    'ngRoute',
    'ui.bootstrap'
    'smartTable.table'
    'ngTable'
    'dialogs'
    'ui.notify'

    # customs
    'controllers'
  ]

  app.moduleList = moduleNames
  app
