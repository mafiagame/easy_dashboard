var compensateApp = angular.module("compensateApp", [])
compensateApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

compensateApp.controller("compensateController", function($scope, $http){
    $scope.formSubmit = function(){
        if(!$scope.comment){
          alert("请填写补偿备注!");
          return;
        }

        var postData = {
          "comment": $scope.comment,
          "diamond": $scope.diamond,
          "units": $scope.units,
          "items": $scope.items,
        };

        $http.post('compensate-send', postData
        ).success(function(data, status, headers, config) {
            alert("公告发送成功！");
            window.location.reload();
        }).error(function(data, status, headers, config) {
            alert("公告发送失败！");
        });
    };

//添加units事件
    $scope.units = {}
    $scope.addUnit = function(){
        var unit_id = $scope.newUnitId
        if(!unit_id || !$scope.newUnitNum){
            alert("输入错误！");
        }else if(unit_id in $scope.units){
            alert("该单位已存在");
        }else{
            $scope.units[unit_id] = $scope.newUnitNum;
            $('#unitModal').modal('hide');
        }
    };

//删除units事件
    $scope.deleteUnit = function(key){
        delete $scope.units[key]
    }

//添加items事件
    $scope.items = {}
    $scope.addItem = function(){
        var item_id = $scope.newItemId
        if(!item_id || !$scope.newItemNum){
            alert("输入错误！");
        }else if(item_id in $scope.items){
            alert("该单位已存在");
        }else{
            $scope.items[item_id] = $scope.newItemNum;
            $('#itemModal').modal('hide');
        }
    };

//删除items事件
    $scope.deleteItem = function(key){
        delete $scope.items[key]
    }
});