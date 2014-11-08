// Generated by CoffeeScript 1.8.0
(function() {
  var TagsCtrl, sblogApp;

  sblogApp = angular.module('sblogApp');

  TagsCtrl = function($scope, $http, $routeParams, data) {
    var post, tag, _i, _j, _len, _len1, _ref, _ref1;
    _ref = data.posts;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      post = _ref[_i];
      post.tagNames = {};
      _ref1 = post.tags;
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        tag = _ref1[_j];
        post.tagNames[tag.name] = true;
      }
    }
    $scope.posts = data.posts;
    $scope.tags = data.tags;
    $scope.tagSelected = $routeParams.tag ? $routeParams.tag : 'All';
    $scope.selectTag = function(tag) {
      return $scope.tagSelected = tag;
    };
    return $scope.tagPostFilter = function(value, index) {
      if ($scope.tagSelected === 'All') {
        return true;
      }
      return $scope.tagSelected in value.tagNames;
    };
  };

  sblogApp.controller('TagsCtrl', ['$scope', '$http', '$routeParams', 'data', TagsCtrl]);

}).call(this);
