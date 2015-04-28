sblogApp = angular.module 'sblogApp'

PostListCtrl = ($scope, $rootScope, $sce, posts) ->
  $scope.posts = posts.posts
  $rootScope.title = ""

sblogApp.controller 'PostListCtrl', ['$scope', '$rootScope', '$sce', 'posts', PostListCtrl]
