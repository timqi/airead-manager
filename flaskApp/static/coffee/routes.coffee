define ['./mainApp'], (app) ->
  console.log('routes init')
  app.config ($routeProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'templates/home.html', controller: 'homeCtl'

    for name in app.moduleList
      templateUrl = "templates/#{name}.html"
      ctlName = "#{name}Ctl"
      $routeProvider
        .when "/#{name}",
          templateUrl: templateUrl, controller: ctlName
