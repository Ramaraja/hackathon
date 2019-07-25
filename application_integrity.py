import os
import sys
from glob import glob
from uuid import UUID
import json

class IntegrityChecker:
    GROUPS = ["announcements", "messages", "grammars", "businesshours", "calendars", "emergencyflags", "datatables", "specialdays" ]
    BUSINESS_OBJECTS = [ "businesshours", "calendars", "emergencyflags", "datatables", "specialdays"]

    def __init__(self, workspace, ccid):
        self.workspace = workspace
        self.ccid = ccid


    def validate_uuid(self, uuid_string):
        try:
            val = UUID(uuid_string, version=4)
            if str(val) == uuid_string:
              return True
            else:
                return False
        except ValueError as e:
            return False

    def validate_announcements(self, workspace, collection_id, announce):
        checkannouncement = workspace+"/"+collection_id+"/"+announce
        if not os.path.exists(checkannouncement):
            return False
        return True

    def validate_messages(self, workspace, collection_id, message):
        basepath = workspace+"/"+collection_id
        checkmessage = basepath+"/"+message
        found = False
        if not os.path.exists(checkmessage):
            if not os.path.exists(basepath+"/messages.json"):
                return False
            else:
                with open(basepath+"/messages.json") as json_file:
                    datas = json.load(json_file)
                    for data in datas:
                        resources = data['resources']
                        for resouce in resources:
                            if resouce['id'] == message:
                                found = True
        return found

    def validate_businessobjects(self, workspace, btype, businessobject):  
        checkfile = workspace+"/businessobjects"+"/"+btype+"/"+businessobject+".json"
        if not os.path.exists(checkfile):
            return False
        return True

    def validate_grammar(self, workspace, grammar):  
        checkgrammar = workspace+"/grammars"+"/"+grammar
        if not os.path.exists(checkgrammar):
            return False
        return True


    def validate_tenant_apps(self):
        tenant = self.workspace+"/"+self.ccid
        integrity_checker = {}
        integrity_checker[self.ccid] = {}
        tenant_workspace = tenant+"/workspace"
        applications = glob(tenant_workspace+"/*")
        for app in applications:
            app_id = app.split("/")[-1]
            if not len(app_id.split("-")) == 5:
                continue
            integrity_checker[self.ccid][app_id] = {} 
            integrity_checker[self.ccid][app_id]["status"] = True
            integrity_checker[self.ccid][app_id]["missingresources"] = {}
            with open(app+'/manifest.json') as json_file:
                #print app_id
                data = json.load(json_file)
                integrity_checker[self.ccid][app_id]["name"] = data['name']
                audiocollection = data['audiocollection']
                messagecollection = data['messagecollection']
                announcements = data['announcements']
                for announcement in announcements:
                    if type(announcement) == dict:
                        collection = announcement["collection"]
                        annc = announcement["id"]
                    else:
                        annc = announcement
                    if audiocollection != None:
                        collection = audiocollection['id']
                    if not self.validate_announcements(tenant_workspace, collection, annc):
                        integrity_checker[self.ccid][app_id]["status"] = False
                        if not "announcements" in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                            integrity_checker[self.ccid][app_id]["missingresources"]["announcements"] = []
                        integrity_checker[self.ccid][app_id]["missingresources"]["announcements"].append(annc)
                    
                messages = data['messages']
                for message in messages:
                    if type(message) == dict:
                        #print message
                        collection = message["collection"]
                        msg = message["id"]
                        #print msg
                    else:
                        msg = message
                    if messagecollection != None:
                        collection = messagecollection['id']
                    #print msg
                    if not self.validate_messages(tenant_workspace, collection, msg):
                        integrity_checker[self.ccid][app_id]["status"] = False
                        if not "messages" in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                            integrity_checker[self.ccid][app_id]["missingresources"]["messages"] = []
                        integrity_checker[self.ccid][app_id]["missingresources"]["messages"].append(msg)

                for businessobject in IntegrityChecker.BUSINESS_OBJECTS:
                    if businessobject in data.keys() and data[businessobject] != []:
                        for bobject in data[businessobject]:
                            if not self.validate_businessobjects(tenant_workspace, businessobject, bobject):
                                integrity_checker[self.ccid][app_id]["status"] = False
                                if not businessobject in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                                    integrity_checker[self.ccid][app_id]["missingresources"][businessobject] = []
                                integrity_checker[self.ccid][app_id]["missingresources"][businessobject].append(bobject)
                if data['grammars'] != []:
                    for grammar in grammars:
                        if not self.validate_grammar(tenant_workspace, grammar):
                            integrity_checker[self.ccid][app_id]["status"] = False
                            if not "grammars" in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                                integrity_checker[self.ccid][app_id]["missingresources"]["grammars"] = []
                            integrity_checker[self.ccid][app_id]["missingresources"]["grammars"].append(grammar)
        return integrity_checker


    def list_of_fails(self):
        fails = []
        data = self.validate_tenant_apps()
        apps = data[self.ccid]
        for app_id in apps.keys():
            failed_app = {}
            app = apps[app_id]
            if not app['status']:
                failed_app['name'] = app['name']
                failed_app["missing"] = []
                missing = app['missingresources']
                for group in self.GROUPS:
                    if group in missing.keys():
                        failed_app["missing"].append(str(len(missing[group]))+" "+ str(group))
            if failed_app != {}:
                fails.append(failed_app)

        return fails
