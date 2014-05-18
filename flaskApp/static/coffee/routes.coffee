define ['./mainApp'], (app) ->
  console.log('routes init')
  app.config ($routeProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'templates/home.html', controller: 'HomeCtl'
      .when '/home',
        templateUrl: 'templates/home.html', controller: 'HomeCtl'
#      .when '/signup',
#        templateUrl: 'views/sessions/signup.html', controller: 'sessions.SignupCtrl'
#      .when '/signin',
#        templateUrl: 'views/sessions/signin.html', controller: 'sessions.SigninCtrl'
#      .otherwise
#        redirectTo: '/'