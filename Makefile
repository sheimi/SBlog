compile:
	coffee -o core/static/js -c core/static/coffee
	cat core/static/js/gist.js >> core/static/js/app.js
	cat core/static/js/controllers/post_details_ctrl.js >> core/static/js/app.js
	cat core/static/js/controllers/post_list_ctrl.js >> core/static/js/app.js
	cat core/static/js/controllers/tags_ctrl.js >> core/static/js/app.js
	cat core/static/js/controllers/recent_post_ctrl.js >> core/static/js/app.js
	cat core/static/js/controllers/archives_ctrl.js >> core/static/js/app.js
	cat core/static/js/global.js >> core/static/js/app.js
	cat core/static/bower_components/jquery/dist/jquery.js > core/static/js/lib.js
	cat core/static/bower_components/bootstrap/dist/js/bootstrap.min.js >> core/static/js/lib.js
	cat core/static/bower_components/angular/angular.js >> core/static/js/lib.js
	cat core/static/bower_components/angular-animate/angular-animate.js  >> core/static/js/lib.js
	cat core/static/bower_components/angular-route/angular-route.js >> core/static/js/lib.js
	cat core/static/bower_components/ngprogress/build/ngProgress.min.js >> core/static/js/lib.js
	sass core/static/sass/app.sass > core/static/css/app.css
	cat core/static/sass/fontello.css >> core/static/css/app.css
	cat core/static/bower_components/ngprogress/ngProgress.css >> core/static/css/app.css
