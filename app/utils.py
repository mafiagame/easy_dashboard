# coding:utf-8
import json
from app.models import Player
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def adjust_player_data(player_data):
    player_data["_id"] = ObjectId(player_data["_id"])

    # buildings
    for pos in player_data["buildings"]:
        player_data["buildings"][pos]["construct_id"] = int(player_data["buildings"][pos]["construct_id"])
        player_data["buildings"][pos]["level"] = int(player_data["buildings"][pos]["level"])

    # resource
    for resource_type in player_data["resource"]:
        if resource_type in ["updated", "diamond"]:
            player_data["resource"][resource_type] = int(player_data["resource"][resource_type])
        else:
            player_data["resource"][resource_type] = float(player_data["resource"][resource_type])

    # resource_delta
    for resource_type in player_data["resource_delta"]:
        player_data["resource_delta"][resource_type] = float(player_data["resource_delta"][resource_type])



def create_single_form_fields():
    ret = ""

    _list = {
        "name": {"type": basestring, "desc": u"名称"},
        "sex": {"type": int, "desc": u"性别"},
        "avatar": {"type": int, "desc": u"头像"},
        "officer_level": {"type": int, "desc": u"军官等级"},
        "officer_exp": {"type": int, "desc": u"军官经验"},
        "military_rank": {"type": int, "desc": u"军衔"},  # 军衔，需要策划跟进
        "combat_power": {"type": int, "desc": u"战斗力"},  # 战斗力
        "energy": {"type": int, "desc": u"体力"},  # 体力,每半小时提升一个点
        "energy_update_time": {"type": int, "desc": u"体力更新时间"},  # 体力,每半小时提升一个点
        "honors": {"type": int, "desc": u"荣誉"},
        "prestige_exp": {"type": int, "desc": u"声望经验"},  # 玩家声望经验, 用于限制科研的研究等级等
        "prestige_level": {"type": int, "desc": u"声望等级"},  # 玩家声望等级, 用于限制科研的研究等级等
        "leadership": {"type": int, "desc": u"统率力"},  # 统率力
        "created": {"type": int, "desc": u"创建时间"},
        "build_queue_limit": {"type": int, "desc": u"建筑队列上限"},
        "vip": {'type': int, 'desc': u"VIP等级"},
        "recharge_score": {'type': int, 'desc': u"充值钻石总数"},
        "total_pay_time": {"type": int, "desc": u"总支付次数"},
    }
    field_template = u'''
    <fieldset class="form-group">
        <label for="TITLE">DESC</label>
        <input type="TYPE" class="form-control" id="TITLE" ng-model="data.TITLE">
    </fieldset>
    '''
    # player = Player.player_test()
    for field in _list:
        item = _list[field]
        desc = item["desc"]
        content = field_template

        if item["type"] is basestring:
            _type = "text"
        elif item["type"] is bool:
            _type = "checkbox"
        elif item["type"] is int:
            _type = "number"
        else:
            continue

        content = content.replace("TITLE", field)
        content = content.replace("DESC", desc)
        content = content.replace("TYPE", _type)
        ret += content

    return ret


def create_double_level_fields():
    ret = ""

    _list = {
        "units": {
            "TITLE" : "units",
            "TOGGLE_ACTION" : "toggleUnits",
            "DELETE_ACTION" : "deleteUnit",
            "ADD_ACTION" : "addUnit",
            "ANGULAR_SHOW" : "unitsVis",
            "ANGULAR_FIELD" : "data.units",
            "ANGULAR_MODAL" : "unitModal",

            "TEXT_KEY" : u"士兵id",
            "TEXT_VALUE" : u"士兵数量",

            "ANGULAR_KEY" : "newUnitId",
            "ANGULAR_VALUE" : "newUnitNum",
            "DESC": u"士兵"
        },
        "techs": {
            "TITLE" : "techs",
            "TOGGLE_ACTION" : "toggleTechs",
            "DELETE_ACTION" : "deleteTech",
            "ADD_ACTION" : "addTech",
            "ANGULAR_SHOW" : "techsVis",
            "ANGULAR_FIELD" : "data.techs",
            "ANGULAR_MODAL" : "techModal",

            "TEXT_KEY" : u"科技id",
            "TEXT_VALUE" : u"科技等级",

            "ANGULAR_KEY" : "newTechId",
            "ANGULAR_VALUE" : "newTechLevel",
            "DESC": u"科技"
        },

        "skills": {
            "TITLE" : "skills",
            "TOGGLE_ACTION" : "toggleSkills",
            "DELETE_ACTION" : "deleteSkill",
            "ADD_ACTION" : "addSkill",
            "ANGULAR_SHOW" : "skillsVis",
            "ANGULAR_FIELD" : "data.skills",
            "ANGULAR_MODAL" : "skillModal",

            "TEXT_KEY" : u"技能id",
            "TEXT_VALUE" : u"技能等级",

            "ANGULAR_KEY" : "newSkillId",
            "ANGULAR_VALUE" : "newSkillLevel",
            "DESC": u"技能"
        },
        "items": {
            "TITLE" : "items",
            "TOGGLE_ACTION" : "toggleItems",
            "DELETE_ACTION" : "deleteItem",
            "ADD_ACTION" : "addItem",
            "ANGULAR_SHOW" : "itemsVis",
            "ANGULAR_FIELD" : "data.items",
            "ANGULAR_MODAL" : "itemModal",

            "TEXT_KEY" : u"物品id",
            "TEXT_VALUE" : u"物品数量",

            "ANGULAR_KEY" : "newItemId",
            "ANGULAR_VALUE" : "newItemNum",
            "DESC": u"物品"
        },
        "payments": {
            "TITLE" : "payments",
            "TOGGLE_ACTION" : "togglePayments",
            "DELETE_ACTION" : "deletePayment",
            "ADD_ACTION" : "addPayment",
            "ANGULAR_SHOW" : "paymentsVis",
            "ANGULAR_FIELD" : "data.payment_time",
            "ANGULAR_MODAL" : "paymentModal",

            "TEXT_KEY" : u"付费id",
            "TEXT_VALUE" : u"购买次数",

            "ANGULAR_KEY" : "newPaymentId",
            "ANGULAR_VALUE" : "newPaymentNum",
            "DESC": u"付费项目的购买次数"
        },
    }

    field_template = '''
    <fieldset class="form-group">
        <label for="TITLE">DESC</label>
        <a class="click-open" id="TITLE" ng-click="TOGGLE_ACTION()">data</a>
        <div ng-show = "ANGULAR_SHOW">
            <div ng-repeat="(key, value) in ANGULAR_FIELD">
                {[key]}: <input type="number" ng-model="ANGULAR_FIELD[key]">
                <a class="click-delete" ng-click="DELETE_ACTION(key)">delete</a>
            </div>
            <button type="button" class="btn-success" data-toggle="modal" data-target="#ANGULAR_MODAL">
                <span class="glyphicon glyphicon-plus"></span>
            </button>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="ANGULAR_MODAL" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="myModalLabel">new item</h4>
              </div>
              <div class="modal-body">
                  TEXT_KEY: <input type="text" ng-model="ANGULAR_KEY">
                  TEXT_VALUE: <input type="number" ng-model="ANGULAR_VALUE">
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" ng-click="ADD_ACTION()">Save changes</button>
              </div>
            </div>
          </div>
        </div>
    </fieldset>
    <hr>
    '''
    for field in _list:
        content = field_template
        substitution = _list[field]
        for item in substitution:
            content = content.replace(item, substitution[item])

        ret += content

    return ret

