define ['./mainApp'], (app) ->
  console.log('routes init')
  app.config ($routeProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'templates/home.html', controller: 'homeCtl'

    for m in app.moduleList
      templateUrl = "templates/#{m.url}.html"
      ctlName = "#{m.url}Ctl"
      $routeProvider
        .when "/#{m.url}",
          templateUrl: templateUrl, controller: ctlName