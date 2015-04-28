sblogApp = angular.module 'sblogApp'

PostDetailsCtrl = ($scope, $rootScope, $routeParams, $sce, post) ->
  $scope.post = post.post
  $rootScope.title = post.post.title

sblogApp.controller 'PostDetailsCtrl', ['$scope', '$rootScope', '$routeParams', '$sce', 'post', PostDetailsCtrl]
