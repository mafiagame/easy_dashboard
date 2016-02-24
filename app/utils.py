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


def create_single_form_fields():
    ret = ""
    field_template = '''
    <fieldset class="form-group">
        <label for="TITLE">TITLE</label>
        <input type="TYPE" class="form-control" id="TITLE" ng-model="data.TITLE">
    </fieldset>
    '''
    player = Player.player_test()
    for field in player:
        title = field
        content = field_template

        if isinstance(player[field], basestring):
            _type = "text"
        elif isinstance(player[field], bool):
            _type = "checkbox"
        elif isinstance(player[field], int) or isinstance(player[field], float):
            _type = "number"
        else:
            continue

        content = content.replace("TITLE", title)
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

            "TEXT_KEY" : "unit_id",
            "TEXT_VALUE" : "unit_num",

            "ANGULAR_KEY" : "newUnitId",
            "ANGULAR_VALUE" : "newUnitNum",
        },
        "techs": {
            "TITLE" : "techs",
            "TOGGLE_ACTION" : "toggleTechs",
            "DELETE_ACTION" : "deleteTech",
            "ADD_ACTION" : "addTech",
            "ANGULAR_SHOW" : "techsVis",
            "ANGULAR_FIELD" : "data.techs",
            "ANGULAR_MODAL" : "techModal",

            "TEXT_KEY" : "tech_id",
            "TEXT_VALUE" : "tech_level",

            "ANGULAR_KEY" : "newTechId",
            "ANGULAR_VALUE" : "newTechLevel",
        },

        "skills": {
            "TITLE" : "skills",
            "TOGGLE_ACTION" : "toggleSkills",
            "DELETE_ACTION" : "deleteSkill",
            "ADD_ACTION" : "addSkill",
            "ANGULAR_SHOW" : "skillsVis",
            "ANGULAR_FIELD" : "data.skills",
            "ANGULAR_MODAL" : "skillModal",

            "TEXT_KEY" : "skill_id",
            "TEXT_VALUE" : "skill_level",

            "ANGULAR_KEY" : "newSkillId",
            "ANGULAR_VALUE" : "newSkillLevel",
        },
        "items": {
            "TITLE" : "items",
            "TOGGLE_ACTION" : "toggleItems",
            "DELETE_ACTION" : "deleteItem",
            "ADD_ACTION" : "addItem",
            "ANGULAR_SHOW" : "itemsVis",
            "ANGULAR_FIELD" : "data.items",
            "ANGULAR_MODAL" : "itemModal",

            "TEXT_KEY" : "item_id",
            "TEXT_VALUE" : "item_num",

            "ANGULAR_KEY" : "newItemId",
            "ANGULAR_VALUE" : "newItemNum",
        },
    }

    field_template = '''
    <fieldset class="form-group">
        <label for="TITLE">TITLE</label>
        <a id="TITLE" ng-click="TOGGLE_ACTION()">data</a>
        <div ng-show = "ANGULAR_SHOW">
            <div ng-repeat="(key, value) in ANGULAR_FIELD">
                <label>{[key]}</label>
                <button class="btn-danger" type="button" ng-click="DELETE_ACTION(key)"><span class="glyphicon glyphicon-remove"></span></button>
                <input type="number" class="form-control" ng-model="ANGULAR_FIELD[key]">
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
    '''
    for field in _list:
        content = field_template
        substitution = _list[field]
        for item in substitution:
            content = content.replace(item, substitution[item])

        ret += content

    return ret