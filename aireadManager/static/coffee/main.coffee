require.config
#  urlArgs: "v=" +  (new Date()).getTime()
  baseUrl: '../../'
  paths:
    'jQuery': './static/bower_components/jquery/dist/jquery'
    'angular': './static/lib/angular'
    'angular-route': './static/bower_components/angular-route/angular-route'
    'angular-ui': './static/bower_components/angular-ui/build/angular-ui'
    'angular-bootstrap': './static/bower_components/angular-bootstrap/ui-bootstrap'
    'angular-bootstrap-tpls': './static/bower_components/angular-bootstrap/ui-bootstrap-tpls'
    'angular-sanitize': './static/lib/angular-sanitize.min'
    'angular-translate': './static/lib/angular-translate.min'
    'smart-table': './static/lib/Smart-Table.debug'
    'dialogs': './static/lib/dialogs'
  shim:
    'jQuery': {'exports': 'jQuery'}
    'angular': {'exports': 'angular'}
    'angular-route': {deps: ['angular']}
    'angular-ui': {deps: ['angular']}
    'angular-bootstrap': {deps: ['angular']}
    'angular-bootstrap-tpls': {deps: ['angular']}
    'angular-sanitize': {deps: ['angular']}
    'angular-translate': {deps: ['angular']}
    'smart-table': {deps: ['angular']}
    'dialogs': {deps: ['angular', 'angular-ui', 'angular-sanitize', 'angular-translate']}

require ['jQuery', 'angular', 'static/js/routes'], ($, angular) ->
  $ ->
    angular.bootstrap document, ['app']