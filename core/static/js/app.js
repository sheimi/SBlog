// Generated by CoffeeScript 1.8.0
(function() {
  var defaultRoute, getResolveFunc, routes, routingFunc, sblogApp;

  sblogApp = angular.module('sblogApp', ['ngRoute', 'ngAnimate', 'ngProgress']);

  getResolveFunc = function(url, params) {
    var resolveFunc;
    if (!params) {
      params = {};
    }
    resolveFunc = function($q, $http, $location, ngProgress) {
      var defer;
      ngProgress.color('#FFB85C');
      ngProgress.start();
      defer = $q.defer();
      $http({
        url: url,
        method: 'GET',
        params: params
      }).success(function(data) {
        defer.resolve(data);
        return ngProgress.complete();
      }).error(function(data, status) {
        ngProgress.complete();
        return $location.url('/');
      });
      return defer.promise;
    };
    return resolveFunc;
  };

  routes = {
    '/': {
      templateUrl: '/static/templates/post-list.html',
      controller: 'PostListCtrl',
      resolve: {
        posts: getResolveFunc('/api/v1/posts')
      }
    },
    '/tags': {
      templateUrl: '/static/templates/tags.html',
      controller: 'TagsCtrl',
      resolve: {
        data: getResolveFunc('/api/v1/posts/tags')
      }
    },
    '/tags/:tag': {
      templateUrl: '/static/templates/tags.html',
      controller: 'TagsCtrl',
      resolve: {
        data: getResolveFunc('/api/v1/posts/tags')
      }
    },
    '/archives': {
      templateUrl: '/static/templates/post-archives.html',
      controller: 'ArchivesCtrl',
      resolve: {
        posts: getResolveFunc('/api/v1/posts/archives')
      }
    },
    '/:category/:year/:month/:day/:file': {
      templateUrl: '/static/templates/post-detail.html',
      controller: 'PostDetailsCtrl',
      resolve: {
        post: function($route, $q, $http, $location, ngProgress) {
          var params, url;
          params = {
            category: $route.current.params.category,
            year: $route.current.params.year,
            month: $route.current.params.month,
            day: $route.current.params.day,
            file: $route.current.params.file
          };
          url = "/api/v1/posts/details";
          return getResolveFunc(url, params)($q, $http, $location, ngProgress);
        }
      }
    }
  };

  defaultRoute = {
    redirectTo: '/'
  };

  routingFunc = function($routeProvider, $locationProvider) {
    var config, url;
    for (url in routes) {
      config = routes[url];
      $routeProvider.when(url, config);
    }
    $routeProvider.otherwise(defaultRoute);
    return $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
  };

  sblogApp.config(['$routeProvider', '$locationProvider', routingFunc]);

}).call(this);
// Generated by CoffeeScript 1.8.0
(function() {
  var PostDetailsCtrl, sblogApp;

  sblogApp = angular.module('sblogApp');

  PostDetailsCtrl = function($scope, $routeParams, $sce, post) {
    post.content = $sce.trustAsHtml(post.content);
    return $scope.post = post;
  };

  sblogApp.controller('PostDetailsCtrl', ['$scope', '$routeParams', '$sce', 'post', PostDetailsCtrl]);

}).call(this);
// Generated by CoffeeScript 1.8.0
(function() {
  var PostListCtrl, sblogApp;

  sblogApp = angular.module('sblogApp');

  PostListCtrl = function($scope, $sce, posts) {
    var post, _i, _len;
    for (_i = 0, _len = posts.length; _i < _len; _i++) {
      post = posts[_i];
      post.thumbnail = $sce.trustAsHtml(post.thumbnail);
    }
    return $scope.posts = posts;
  };

  sblogApp.controller('PostListCtrl', ['$scope', '$sce', 'posts', PostListCtrl]);

}).call(this);
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
// Generated by CoffeeScript 1.8.0
(function() {
  var RecentPostCtrl, sblogApp;

  sblogApp = angular.module('sblogApp');

  RecentPostCtrl = function($scope, $http) {
    $scope.willHide = 'sheimi-hide';
    return $http.get('/api/v1/posts/recent').success(function(recent_posts) {
      $scope.posts = recent_posts;
      return $scope.willHide = '';
    });
  };

  sblogApp.controller('RecentPostCtrl', ['$scope', '$http', RecentPostCtrl]);

}).call(this);
// Generated by CoffeeScript 1.8.0
(function() {
  var ArchivesCtrl, sblogApp;

  sblogApp = angular.module('sblogApp');

  ArchivesCtrl = function($scope, $http, posts) {
    return $scope.posts = posts;
  };

  sblogApp.controller('ArchivesCtrl', ['$scope', '$http', 'posts', ArchivesCtrl]);

}).call(this);
// Generated by CoffeeScript 1.8.0
(function() {
  $(document).ready(function() {
    $('.bs-tooltip').tooltip();
    $('img[alt="content image"]').each(function(index, value) {
      return $(this).addClass('img-polaroid');
    });
    $(window).on('resize', function(e) {
      return windowResize();
    });
    return windowResize();
  });

  window.windowResize = function() {
    if ($('html').height() < $(window).height()) {
      return $('.footer').addClass('fix-bottom');
    } else {
      return $('.footer').removeClass('fix-bottom');
    }
  };

}).call(this);
