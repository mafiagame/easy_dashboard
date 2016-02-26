var announceApp = angular.module("announceApp", ['ngRoute'])
announceApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

announceApp.controller("announceController", function($scope, $http, $route){
    $scope.announceSubmit = function(){
        if(!$scope.announceTitle || !$scope.announceContent){
          alert("输入错误!");
          return;
        }
        var postData = {
          "announce_title": $scope.announceTitle,
          "announce_content": $scope.announceContent,
        };

        $http.post('announce-send', postData
        ).success(function(data, status, headers, config) {
            alert("公告发送成功！")
            window.location.reload()
        }).error(function(data, status, headers, config) {
          alert("公告发送失败！")
        });
    };
});