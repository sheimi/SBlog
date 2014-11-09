sblogApp = angular.module 'sblogApp'

PostListCtrl = ($scope, $sce, posts) ->
  $scope.posts = posts

sblogApp.controller 'PostListCtrl', ['$scope', '$sce', 'posts', PostListCtrl]
