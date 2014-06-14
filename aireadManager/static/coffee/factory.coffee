define ['./mainApp'], (app) ->
  # just for factory example, no use
  app.factory 'curUser', [
    '$http'
    '$rootScope'
    'notificationService'
    ($http, $rootScope, notificationService) ->
      curUserUrl = '/users/infos/now'
      curUserPromise = $http.get curUserUrl
      .success (data) ->
          console.log 'cur user receive', data
          $rootScope['curUser'] = data
      .error (err) ->
          console.log "get cur user #{curUserUrl} failed", err
          notificationService.notice '获取当前用户失败'

      return {
        curUserPromise: curUserPromise
      }
  ]