define ['./mainApp', './factory'], (app) ->
  console.log('routes init')
  app.config ($routeProvider) ->
    $routeProvider
      .when '/', {
        templateUrl: 'templates/home.html'
        controller: 'homeCtl'
      }


    for m in app.moduleList
      templateUrl = "templates/#{m.url}.html"
      ctlName = "#{m.url}Ctl"
      resolve = {}
      resolve = m.resolve if m.resolve
      $routeProvider
        .when "/#{m.url}", {
          templateUrl: templateUrl
          controller: ctlName
          resolve: resolve
        }