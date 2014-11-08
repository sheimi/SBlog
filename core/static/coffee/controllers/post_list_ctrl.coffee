sblogApp = angular.module 'sblogApp'

PostListCtrl = ($scope, $sce, posts) ->
  for post in posts
    post.thumbnail = $sce.trustAsHtml(post.thumbnail)
  $scope.posts = posts

sblogApp.controller 'PostListCtrl', ['$scope', '$sce', 'posts', PostListCtrl]
