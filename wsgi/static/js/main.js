var app = angular.module('myApp', []);

function groupBy(list, fn) {
	var groups = {};
	for (var i = 0; i < list.length; i++) {
		var group = JSON.stringify(fn(list[i]));
		if (group in groups) {
			groups[group].data.push(list[i]);
			groups[group].amount += list[i].amounts.reduce(function(previousValue, currentValue) {
				return previousValue + currentValue;
			}, 0.0);
		} else {
			groups[group] = {
				visible: false,
				data: [list[i]],
				amount: 0.0
			};
		}
	}
	return groups;
}

// TODO: improve groups generation
function groupYearMonth(list) {
	var result = {};
	var years = groupBy(list, function(item) {
		return item.date.substr(0, 4);
	});
	for (var key in years) {
		result[key] = {
			visible: years[key].visible,
			data: groupBy(years[key].data, function(item) {
				return item.date.substr(5, 2);
			}),
			amount: years[key].amount,
		};
	}
	return result;
}

app.controller('mainController', function($scope, $http) {

	// TODO: add dialog showing when reloading
	$scope.reload = function() {
		$http({
			method: 'GET',
			url: '/data.json'
		}).success(function(data, status, headers, config) {
			$scope.debtor = data.summary.slice(-1).pop();
			$scope.members = data.members;
			$scope.sumary = groupYearMonth(data.summary);

		}).error(function(data, status, headers, config) {
		});
	};

	$scope.reload();
});

app.filter('unQuote', function() {
	return function( input ) {
		return input.replace(/^"|"$/g, '');
	};
});
