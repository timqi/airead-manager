define ['./mainApp'], (app) ->
  console.log('routes init')
  app.config ($routeProvider) ->
    $routeProvider
      .when '/',
        template: '<h1>Main {{name}} </h1>', controller: 'MainCtl'
      .when '/home',
        template: '<h1>Home {{name}} </h1>', controller: 'HomeCtl'
#      .when '/signup',
#        templateUrl: 'views/sessions/signup.html', controller: 'sessions.SignupCtrl'
#      .when '/signin',
#        templateUrl: 'views/sessions/signin.html', controller: 'sessions.SigninCtrl'
#      .otherwise
#        redirectTo: '/'