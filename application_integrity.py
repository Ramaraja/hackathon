import os
import sys
from glob import glob
from uuid import UUID
import json

class IntegrityChecker:
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
        checkmessage = workspace+"/"+collection_id+"/"+message
        if not os.path.exists(checkmessage):
            return False
        return True

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
                data = json.load(json_file)
                integrity_checker[self.ccid][app_id]["name"] = data['name']
                audiocollection = data['audiocollection']
                messagecollection = data['messagecollection']
                if audiocollection != None:
                    announcements = data['announcements']
                    for announcement in announcements:
                        if not self.validate_announcements(tenant_workspace, audiocollection, announcement):
                            integrity_checker[self.ccid][app_id]["status"] = False
                            if not "announcements" in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                                integrity_checker[self.ccid][app_id]["missingresources"]["announcements"] = []
                            integrity_checker[self.ccid][app_id]["missingresources"]["announcements"].append(announcement)
                if messagecollection != None:
                    messages = data['messages']
                    for message in messages:
                        if not self.validate_messages(tenant_workspace, messagecollection, message):
                            integrity_checker[self.ccid][app_id]["status"] = False
                            if not "messages" in integrity_checker[self.ccid][app_id]["missingresources"].keys():
                                integrity_checker[self.ccid][app_id]["missingresources"]["messages"] = []
                            integrity_checker[self.ccid][app_id]["missingresources"]["messages"].append(message)
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

