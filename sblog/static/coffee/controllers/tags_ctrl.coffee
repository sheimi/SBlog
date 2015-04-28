sblogApp = angular.module 'sblogApp'

TagsCtrl = ($scope, $rootScope, $http, $routeParams, data) ->
  $rootScope.title = "Tags"
  for post in data.posts
    post.tagNames = {}
    for tag in post.tags
      post.tagNames[tag.name] = true
  $scope.posts = data.posts
  $scope.tags = data.tags
  $scope.tagSelected = if $routeParams.tag then $routeParams.tag else 'All'

  $scope.selectTag = (tag) ->
    $scope.tagSelected = tag

  $scope.tagPostFilter = (value, index) ->
    if $scope.tagSelected == 'All'
      return true
    return $scope.tagSelected of value.tagNames

sblogApp.controller 'TagsCtrl', ['$scope', '$rootScope', '$http', '$routeParams', 'data', TagsCtrl]
