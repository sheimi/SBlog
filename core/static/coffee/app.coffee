sblogApp = angular.module 'sblogApp', ['ngRoute', 'ngAnimate', 'ngProgress']

getResolveFunc = (url, params) ->
  if not params
    params= {}
  resolveFunc = ($q, $http, $location, ngProgress) ->
    ngProgress.color '#FFB85C'
    ngProgress.start()
    defer = $q.defer()
    $http
      url: url
      method: 'GET'
      params: params
     .success (data) ->
       defer.resolve data
       ngProgress.complete()
     .error  (data, status) ->
       ngProgress.complete()
       # TODO show error
       $location.url '/'
    return defer.promise
  return resolveFunc


routes =
  '/':
    templateUrl: '/static/templates/post-list.html'
    controller: 'PostListCtrl'
    resolve:
      posts: getResolveFunc '/api/v1/posts'
  '/tags':
    templateUrl: '/static/templates/tags.html'
    controller: 'TagsCtrl'
    resolve:
      data: getResolveFunc '/api/v1/posts/tags'
  '/tags/:tag':
    templateUrl: '/static/templates/tags.html'
    controller: 'TagsCtrl'
    resolve:
      data: getResolveFunc '/api/v1/posts/tags'
  '/archives':
    templateUrl: '/static/templates/post-archives.html'
    controller: 'ArchivesCtrl'
    resolve:
      posts: getResolveFunc '/api/v1/posts/archives'
  '/:category/:year/:month/:day/:file':
    templateUrl: '/static/templates/post-detail.html'
    controller: 'PostDetailsCtrl'
    resolve:
      post: ($route, $q, $http, $location, ngProgress) ->
        params =
          category: $route.current.params.category
          year: $route.current.params.year
          month: $route.current.params.month
          day: $route.current.params.day
          file: $route.current.params.file
        url = "/api/v1/posts/details"
        return getResolveFunc(url, params)($q, $http, $location, ngProgress)

defaultRoute =
  redirectTo: '/'


routingFunc = ($routeProvider, $locationProvider) ->
  for url, config of routes
    $routeProvider.when url, config
  $routeProvider.otherwise defaultRoute
  $locationProvider.html5Mode
    enabled: true
    requireBase: false

sblogApp.config ['$routeProvider', '$locationProvider', routingFunc]
