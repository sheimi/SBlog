sblogApp = angular.module 'sblogApp'

PostDetailsCtrl = ($scope, $routeParams, $sce, post) ->
  post.content = $sce.trustAsHtml(post.content)
  $scope.post = post

sblogApp.controller 'PostDetailsCtrl', ['$scope', '$routeParams', '$sce', 'post', PostDetailsCtrl]
