sblogApp = angular.module 'sblogApp'

PostDetailsCtrl = ($scope, $routeParams, $sce, post) ->
  $scope.post = post

sblogApp.controller 'PostDetailsCtrl', ['$scope', '$routeParams', '$sce', 'post', PostDetailsCtrl]
