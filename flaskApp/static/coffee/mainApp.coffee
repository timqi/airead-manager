define [
  'angular',
  'angular-route',
  'angular-ui',
  'angular-bootstrap',
  'angular-bootstrap-tpls',

  #custom
  'controllers/index'
], (angular) ->
  console.log('mainApp init')
  angular.module 'app', [
    'ngRoute',
    'ui.bootstrap'

    # customs
    'controllers'
  ]
