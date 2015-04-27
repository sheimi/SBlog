sblogApp = angular.module 'sblogApp'

RecentPostCtrl = ($scope, $http) ->
  $scope.willHide = 'sheimi-hide'
  $http.get '/api/v1/posts/recent'
       .success (recent_posts) ->
         $scope.posts = recent_posts.posts
         $scope.willHide = ''

sblogApp.controller 'RecentPostCtrl', ['$scope', '$http', RecentPostCtrl]
