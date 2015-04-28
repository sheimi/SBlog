sblogApp = angular.module 'sblogApp'

ArchivesCtrl = ($scope, $rootScope, $http, posts) ->
  $scope.posts = posts.posts
  $rootScope.title = "Archives"

sblogApp.controller 'ArchivesCtrl', ['$scope', '$rootScope', '$http', 'posts', ArchivesCtrl]
