var playerApp = angular.module("playerApp", [])
playerApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

playerApp.controller("playerController", function($scope, $http){
  $scope.onlyNumbers = /^\d+$/;

  var bindShowHide = function(_param, _click){
    $scope[_param] = false;
    $scope[_click] = function(){
      $scope[_param] = $scope[_param] ? false:true
    };
  };
//搜索按钮
  $scope.searchAction = function(){
    $http.get("/player-search-name", {params: {name: $scope.searchName}}).then(function(response){
      if(response.data == ""){
        $scope.mainVis = false;
        alert("Player not found!")
      }else{
        $scope.data = response.data;
        $scope.mainVis = true;
        $scope.buildingVis = {};
        for(key in $scope.data.buildings){
          $scope.buildingVis[key] = false;
        };
        $scope.mapCollVis = {};
      }
    });
  };
//修改信息提交事件
  $scope.submit = function(){
    var postData = $scope.data;
    $http.post('player-search-name', postData
    ).success(function(data, status, headers, config) {
      alert("信息修改成功！")
    }).error(function(data, status, headers, config) {
      alert("信息修改失败！")
    });
  };

//save button
  $scope.singleSave = function(key){
    if(!$scope.data[key] && $scope.data[key]!=0){
      alert("输入错误!");
      return;
    }
    var postData = {
      "_id": $scope.data._id,
      "key": key,
      "value": $scope.data[key]
    };

    $http.post('player-single-save', postData
    ).success(function(data, status, headers, config) {
      $scope.data = data;
      alert("信息修改成功！")
    }).error(function(data, status, headers, config) {
      alert("信息修改失败！")
    });
  };

//save building button
  $scope.buildingLevelSave = function(key){
    var postData = {
      "_id": $scope.data._id,
      "building_pos": key,
      "building_lv": $scope.data.buildings[key]["level"]
    };

    $http.post('player-building-save', postData
    ).success(function(data, status, headers, config) {
      $scope.data = data;
      alert("信息修改成功！")
    }).error(function(data, status, headers, config) {
      alert("信息修改失败！")
    });
  };
//******************buildings*******************
//添加建筑事件
  $scope.addBuilding = function(){
    var pos = $scope.newBuildingPos.toString();
    if(pos in $scope.data.buildings){
      alert("该建造位已被占");
    }else{
      $scope.data.buildings[pos] = {
        "construct_id": $scope.newBuildingId,
        "level": $scope.newBuildingLevel
      };
      $('#buildingModal').modal('hide');
    }
  };

//删除建筑事件
  $scope.deleteBuilding = function(key){
    delete $scope.data.buildings[key]
  }

//显示隐藏buildings逻辑
  bindShowHide("buildingsVis", "toggleBuildings");
  $scope.toggleBuilding = function(key){
    $scope.buildingVis[key] = $scope.buildingVis[key] ? false:true
  };

//******************resource*******************
//显示隐藏resource逻辑
  bindShowHide("resourceVis", "toggleResource");


//******************units*******************
//添加建筑事件
  $scope.addUnit = function(){
    var unit_id = $scope.newUnitId
    if(!unit_id || !$scope.newUnitNum){
      alert("输入错误！");
    }else if(unit_id in $scope.data.units){
      alert("该单位已存在");
    }else{
      $scope.data.units[unit_id] = $scope.newUnitNum;
      $('#unitModal').modal('hide');
    }
  };

//删除建筑事件
  $scope.deleteUnit = function(key){
    delete $scope.data.units[key]
  }
//显示隐藏units逻辑
  bindShowHide("unitsVis", "toggleUnits");

//


//******************techs*******************
//添加科技事件
  $scope.addTech = function(){
    var tech_id = $scope.newTechId
    if(!tech_id || !$scope.newTechLevel){
      alert("输入错误！");
    }else if(tech_id in $scope.data.techs){
      alert("该单位已存在");
    }else{
      $scope.data.techs[tech_id] = $scope.newTechLevel;
      $('#techModal').modal('hide');
    }
  };

//删除科技事件
  $scope.deleteTech = function(key){
    delete $scope.data.techs[key]
  }
//显示隐藏科技逻辑
  bindShowHide("techsVis", "toggleTechs");

//

//******************skills*******************
//添加技能事件
  $scope.addSkill = function(){
    var skill_id = $scope.newSkillId
    if(!skill_id || !$scope.newSkillLevel){
      alert("输入错误！");
    }else if(skill_id in $scope.data.skills){
      alert("该单位已存在");
    }else{
      $scope.data.skills[skill_id] = $scope.newSkillLevel;
      $('#skillModal').modal('hide');
    }
  };

//删除技能事件
  $scope.deleteSkill = function(key){
    delete $scope.data.skills[key]
  }
//显示隐藏技能逻辑
  bindShowHide("skillsVis", "toggleSkills");

//


//******************items*******************
//添加技能事件
  $scope.addItem = function(){
    var item_id = $scope.newItemId
    if(!item_id || !$scope.newItemNum){
      alert("输入错误！");
    }else if(item_id in $scope.data.items){
      alert("该单位已存在");
    }else{
      $scope.data.items[item_id] = $scope.newItemNum;
      $('#itemModal').modal('hide');
    }
  };

//删除技能事件
  $scope.deleteItem = function(key){
    delete $scope.data.items[key]
  }
//显示隐藏技能逻辑
  bindShowHide("itemsVis", "toggleItems");

//

//******************payment_time*******************
//添加技能事件
  $scope.addPayment = function(){
    var payment_id = $scope.newPaymentId
    if(!payment_id || !$scope.newPaymentNum){
      alert("输入错误！");
    }else if(payment_id in $scope.data.payment_time){
      alert("该单位已存在");
    }else{
      $scope.data.payment_time[payment_id] = $scope.newPaymentNum;
      $('#paymentModal').modal('hide');
    }
  };

//删除技能事件
  $scope.deletePayment = function(key){
    delete $scope.data.payment_time[key]
  }
//显示隐藏技能逻辑
  bindShowHide("paymentsVis", "togglePayments");

//


//******************map_collections*******************
//添加map_collections事件
  $scope.addMapColl = function(){
    $scope.data.map_collections.push({
      "name": $scope.newMapCollName,
      "category": $scope.newMapCollCat,
      "x": $scope.newMapCollX,
      "y": $scope.newMapCollY,
      "type": $scope.newMapCollType,
      "lv": $scope.newMapCollLv,
    });
    $('#mapCollModal').modal('hide');

  };

//删除map_collections事件
  $scope.deleteMapColl = function(_index){
    $scope.data.map_collections.splice(_index, 1);
  }
//显示隐藏map_collections逻辑
  bindShowHide("mapCollsVis", "toggleMapColls");
  $scope.toggleMapColl = function(key){
    $scope.mapCollVis[key] = $scope.mapCollVis[key] ? false:true
  };

});




var showPlayerInfo = function(_scope, _data){

}