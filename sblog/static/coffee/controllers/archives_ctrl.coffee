sblogApp = angular.module 'sblogApp'

ArchivesCtrl = ($scope, $http, posts) ->
  $scope.posts = posts.posts

sblogApp.controller 'ArchivesCtrl', ['$scope', '$http', 'posts', ArchivesCtrl]
