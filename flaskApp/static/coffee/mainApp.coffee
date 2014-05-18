define [
  'angular',
  'controllers/index',
  'angular-route',
  'angular-ui',
  'angular-bootstrap',
  'angular-bootstrap-tpls',

], (angular, moduleNames) ->
  console.log('mainApp init')
  console.log('find modules: ', moduleNames)
  app = angular.module 'app', [
    'ngRoute',
    'ui.bootstrap'

    # customs
    'controllers'
  ]

  app.moduleList = moduleNames
  app
