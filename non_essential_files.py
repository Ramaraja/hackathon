import os
import json
import os.path
from os import path
from nested_lookup import get_occurrence_of_key, get_occurrence_of_value

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)

    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        for file, value in subdir.items():
            subdir[file] = {"Touchstatus": False }
        subdir["Touchstatus"] = False
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    return dir

def non_essential_json(base_path, cc_id):
    paths = {"audiocollection":"audio/",
             "announcements": "audio/",
             "messagecollection": "messages/",
             "messages": "messages/",
             "grammars": "grammars/",
             "businesshours": "businessobjects/businesshours/",
             "emergencyflags": "businessobjects/emergencyflags/",
             "datatables": "businessobjects/datatables/",
             "specialdays": "businessobjects/specialdays/"
             }
    workspace = base_path + cc_id + "/workspace/" #"/Users/jjaisank/designer/repo/workspace/36969587-76bf-410a-8764-532390bbbf90/workspace/"
    print workspace
    manifest_files = find_all('manifest.json', workspace)
    base_hash = get_directory_structure(workspace)
    for manifest_file in manifest_files:
        audiocollection = []
        messagecollection = []
        with open(manifest_file) as json_file:
            data = json.load(json_file)
            for resource in paths.keys():
                #print resource, "-", data[resource]
                if data[resource] != None or data[resource]:
                    if len(data[resource]) < 1:
                        continue
                    if resource == "audiocollection" or resource == "messagecollection" :
                        if path.exists(workspace+paths[resource]+ data[resource]["id"]):
                            base_hash["workspace"][paths[resource][:-1]][data[resource]["id"]]["Touchstatus"] = True
                            base_hash["workspace"][paths[resource][:-1]][data[resource]["id"]]["dependent"] =  manifest_file
                            #print base_hash["workspace"][paths[resource][:-1]][data[resource]["id"]]
                            if resource == "audiocollection":
                                audiocollection.append(str(data[resource]["id"]))
                            else:
                                messagecollection.append(str(data[resource]["id"]))
                    if resource == "announcements" and len(audiocollection) > 0 :
                        for announcement in data["announcements"]:
                            for audiofile in audiocollection:
                                # print workspace+paths[resource]+audiofile+"/"+announcement["id"]
                                if path.exists(workspace+paths[resource]+audiofile+"/"+announcement["id"]):
                                    # update the announcement touch status parameter
                                    #print  base_hash["workspace"]["audio"][audiofile][announcement["id"]]
                                    #print base_hash["workspace"]["audio"][audiofile]
                                    base_hash["workspace"]["audio"][audiofile][announcement["id"]]["Touchstatus"] = True
                                    base_hash["workspace"]["audio"][audiofile][announcement["id"]]["dependent"] =  manifest_file
                                    #print  base_hash["workspace"]["audio"][audiofile][announcement["id"]]
                    #if resource == "messagecollection" :
                    #    if path.exists(workspace + paths[resource] + data[resource]["id"]):
                    #        base_hash["workspace"]["messages"][data[resource]["id"]]["Touchstatus"] = True
                    #        base_hash["workspace"]["messages"][data[resource]["id"]]["dependent"] = manifest_file
                    #        # print base_hash["workspace"]["messages"][data[resource]["id"]]
                    #        messagecollection.append(str(data[resource]["id"]))
                    if resource == "messages" and len(messagecollection) > 0 :
                        for messages in data["messages"]:
                            for messagefile in messagecollection:
                                # print workspace+paths[resource]+audiofile+"/"+announcement["id"]
                                if path.exists(workspace+paths[resource]+messagefile+"/"+messagefile["id"]):
                                    # update the announcement touch status parameter
                                    #print  base_hash["workspace"]["audio"][audiofile][announcement["id"]]
                                    #print base_hash["workspace"]["audio"][audiofile]
                                    base_hash["workspace"]["messages"][messagefile][messages["id"]]["Touchstatus"] = True
                                    base_hash["workspace"]["messages"][messagefile][messages["id"]]["dependent"] =  manifest_file
                                    #print  base_hash["workspace"]["audio"][audiofile][announcement["id"]]
                    if resource == "grammars":
                        if path.exists(workspace + paths[resource] + data[resource]["id"]):
                            base_hash["workspace"]["grammars"][data[resource]["id"]]["Touchstatus"] = True
                            base_hash["workspace"]["grammars"][data[resource]["id"]]["dependent"] = manifest_file
                            # print base_hash["workspace"]["messages"][data[resource]["id"]]
                    if resource == "businesshours" or resource == "emergencyflags" or resource == "datatables" or resource == "specialdays":
                        for res in data[resource]:
                            #print resource
                            #print workspace + paths[resource] + res["id"]

                            #print base_hash["workspace"]["businessobjects"][resource] [res["id"]+".json"]
                            #print base_hash["workspace"]["businessobjects"][resource]#[res["id"]]
                            #print workspace + paths[resource] + res["id"]+".json"
                            if path.exists(workspace + paths[resource] + res["id"]+".json"):
                                base_hash["workspace"]["businessobjects"][resource][res["id"]+".json"]["Touchstatus"] = True
                                base_hash["workspace"]["businessobjects"][resource][res["id"]+".json"]["dependent"] = manifest_file
                                base_hash["workspace"]["businessobjects"][resource][res["id"]+".json"]["Touchstatus"]
                            # print base_hash["workspace"][resource][data[resource]["id"]]
    return base_hash

def non_essential_count(base_path, cc_id):
    base_json = non_essential_json(base_path, cc_id)
    return {"total":get_occurrence_of_key(base_json, key="Touchstatus"),
            "essential":get_occurrence_of_value(base_json, value=True),
            "non-essential":get_occurrence_of_value(base_json, value=False)}

def find_key(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key(v, value)
            if p:
                #print p[1]
                #find_key(d, value)
                return [d, [k] + p[1]]
        elif v == value:
            d.pop(k)
            return [d, [k]]

def find_all_occurence(d,value):
    results =[]
    while get_occurrence_of_value(d, value=value) > 0:
        result = find_key(d, value)
        d = result[0]
        result = result[1]
        result.pop()
        #result.join('/')
        res = "/".join(result)
        #print res
        results.append(res)
        #print get_occurrence_of_value(d, value=value)
    return results

def list_non_essential_files(base_path, cc_id):
    base_json = non_essential_json(base_path, cc_id)
    return {
        "file": find_all_occurence(base_json, False)
    }

def list_essential_files(base_path, cc_id):
    base_json = non_essential_json(base_path, cc_id)
    return {
        "file": find_all_occurence(base_json, True)
    }

#print (json.dumps(non_essential_json(), indent=4, sort_keys=True))
#print non_essential_count()

#print list_essential_files()
#print list_non_essential_files()
#f = open("output.json", "w")
#f.write(json.dumps(base_hash, indent=4, sort_keys=True))
#f.close()
