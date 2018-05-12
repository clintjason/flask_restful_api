//Initialize an Angularjs Application
var app = angular.module('myApp', ['ui.router','ngResource', 'myApp.controllers', 'myApp.services', 'toaster']);

// Create a User Resource Object using the resource service
angular.module('myApp.services', []).factory('User', function($resource) {
 return $resource('api/v1/users/:id.json', { id:'@users.id' }, {
	 update: {
	 method: 'PATCH',
	 }
 	}, {
 	stripTrailingSlashes: false
 	});
});


// Create routes with UI-Router and display the appropriate HTML file for listing, adding or updating users
angular.module('myApp').config(function($stateProvider, $urlRouterProvider) {
 //
	 // For any unmatched url, redirect to /state1
	 $urlRouterProvider.otherwise("/");
	 
	 $stateProvider
	 .state('users', { 
	 // https://github.com/angular-ui/ui-router/wiki/Nested-States-and-Nested-Views
	 abstract: true,
	 url: '/',
	 title: 'Users',
	 template: '&lt;ui-view/&gt;'
	 })
	 .state('users.list', {
	 url: 'list',
	 templateUrl: 'list.html',
	 controller: 'UserListController',
	 })
	 .state('users.add', {
	 url: 'add',
	 templateUrl: 'add.html',
	 controller: 'UserCreateController',
	})
	 .state('users.edit', {
	 url: ':id/edit',
	 templateUrl: 'update.html',
	 controller: 'UserEditController',
	 
	 })
});

// Define CRUD controllers to make the add, update and delete calls using the User resource we defined earlier
angular.module('myApp.controllers', []).controller('UserListController', function($scope, User, $state, toaster) {
 User.get(function(data) {// Get all the users. Issues a GET to /api/v1/users.json
 
 $scope.users = [];
 angular.forEach(data.data, function(value, key)
 {
	 this.user = value.attributes;
	 this.user['id'] = value.id;
	 this.push(this.user);
 }, $scope.users); 
 
 },
 function(error){
 	