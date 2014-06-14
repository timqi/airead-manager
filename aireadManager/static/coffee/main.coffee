require.config
#  urlArgs: "v=" +  (new Date()).getTime()
  baseUrl: '../../'
  paths:
    'jQuery': './static/lib/jquery'
    'jquery.pnotify': './static/lib/jquery.pnotify'
    'select2': './static/lib/select2'
    'angular': './static/lib/angular'
    'angular-route': './static/lib/angular-route'
    'angular-ui': './static/lib/angular-ui'
    'angular-bootstrap': './static/lib/ui-bootstrap'
    'angular-bootstrap-tpls': './static/lib/ui-bootstrap-tpls'
    'angular-sanitize': './static/lib/angular-sanitize.min'
    'angular-translate': './static/lib/angular-translate.min'
    'smart-table': './static/lib/Smart-Table.debug'
    'angular-pnotify': './static/lib/pnotify'
    'angular-select2': './static/lib/ui-select2'
    'dialogs': './static/lib/dialogs'
  shim:
    'jQuery': {'exports': 'jQuery'}
    'jquery.pnotify': {'exports': 'jQuery'}
    'select2': {deps: ['jQuery']}
    'angular': {'exports': 'angular'}
    'angular-route': {deps: ['angular']}
    'angular-ui': {deps: ['angular']}
    'angular-bootstrap': {deps: ['angular']}
    'angular-bootstrap-tpls': {deps: ['angular']}
    'angular-sanitize': {deps: ['angular']}
    'angular-translate': {deps: ['angular']}
    'smart-table': {deps: ['angular']}
    'angular-pnotify': {deps: ['angular', 'jquery.pnotify']}
    'angular-select2': {deps: ['angular', 'select2']}
    'dialogs': {deps: ['angular', 'angular-ui', 'angular-sanitize', 'angular-translate']}

require ['jQuery', 'angular', 'static/js/routes'], ($, angular) ->
  $ ->
    angular.bootstrap document, ['app']