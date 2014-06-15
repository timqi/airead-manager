define [
  'angular'
  'static/js/controllers/main'
  'angular-route'
  'angular-ui'
  'angular-bootstrap'
  'angular-bootstrap-tpls'
  'angular-ng-table'
  'angular-pnotify'
  'smart-table'
  'angular-select2'
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
    'ui.select2'

    # customs
    'controllers'
  ]

  app.moduleList = moduleNames

  app.config [
    '$httpProvider'
    ($httpProvider) ->
      $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
  ]
  app
