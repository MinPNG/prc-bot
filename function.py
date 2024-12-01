import time
from datetime import date,datetime,timedelta,timezone,UTC
from calendar import timegm
import json


def save_file(save):
    with open('save.txt',"w") as file:
        json.dump(save,file)
    file.close()

def load_file():
    with open('save.txt',"r") as input:
            out = json.load(input)
    input.close()
    return out

#Error default respone
error = ("reply","Something wrong, try again")

#Setting Timezone
offset = timedelta(hours=9)
jp_tzone = timezone(offset)

#Load savefile
db = load_file()
nameset = []
aliasset = []

for item in db:
    nameset.append(item["name"])
    for alias in item["alias"]:
        aliasset.append(alias)
    

def add(arg):
    if arg != []:
        option = arg.pop(0)
        match option:
            case "clone":
                name = arg.pop(0)
                if name in nameset:
                    return ("reply","This clone is already added")
                aliases = []
                if arg != []:
                    for alias in arg:
                        if alias in aliasset:
                            return ("reply",alias + " is already existed as another alias")
                        aliases.append(alias)
                db.append(
                    {
                        "name":name,
                        "alias":aliases,
                        "done":False
                    }
                )
                nameset.append(name)
            case "alias":
                name = arg.pop(0)
                for alias in arg:
                    if alias in aliasset:
                        return ("reply",alias + " is already existed as an alias")
                if arg != []:
                    for item in db:
                        if item["name"] == name:
                                item["alias"].append(alias)
                                aliasset.append(alias)
        try:
            save_file(db)
        except:
            return error
        return ("react","✅")
    return error

def remove(arg):
    if arg != []:
        option = arg.pop(0)
        match option:
            case "alias":
                if arg ==[]:
                    return error
                for alias in arg:
                    if alias not in aliasset:
                        return ("reply",alias + " not found")
                    for item in db:
                        if alias in item["alias"]:
                            item["alias"].remove(alias)
                            aliasset.remove(alias)
                save_file()
                return ("react","✅")
            case _:
                if option not in nameset:
                    return ("reply",option + " not found")
                for item in db:
                    if item["name"] == option:
                        db.remove(item)
                        nameset.remove(option)
                        save_file()
                        return ("react","✅")
    return error

def change(arg):
    if arg != []:
        return ("react","✅")
    return error

def check(arg):
    if arg == []:
        print(db)
        return ("reply", str(db))
    match arg[0]:
            case "reset":
                return ("reply","Reset daily in ||<t:" + str(get_next_reset_timestamp()) +":R>||")
            case _:
                name = arg.pop(0)
                if  name not in nameset:
                    return ("reply",name + " doesn't exist, Try again")
                if db[nameset.index(name)]["done"]:
                    return ("reply",name + " daily done")
                if not db[nameset.index(name)]["done"]:
                    return ("reply",name + " daily not done")
                
    return ("reply","Cannot check")

def do(arg):
    if arg != []:
        if len(arg) > 1:
            return ("reply","One account at a time please")
        name = arg[0]
        if name not in nameset:
            if name not in aliasset:
                return("reply", name + "not found, Please try again")
            name = get_name_from_alias(name)
        if db[nameset.index(name)]["done"]:
                return ("reply",name + " already done daily")
        if not db[nameset.index(name)]["done"]:
                db[nameset.index(name)]["done"] = True
                save_file(db)
                return ("react","✅")
    return error

def undo(arg):
    if arg != []:
        if len(arg) > 1:
            return ("reply","One account at a time please")
        name = arg[0]
        if name not in nameset:
            if name not in aliasset:
                return("reply", name + "not found, Please try again")
            name = get_name_from_alias(name)
        if not db[nameset.index(name)]["done"]:
                return ("reply",name + " already undone")
        if db[nameset.index(name)]["done"]:
                db[nameset.index(name)]["done"] = False
                save_file(db)
                return ("react","✅")
    return error

def reset(arg):
    option = "default" if arg == [] else arg.pop(0)
    match option:
        case "default":
            for item in db:
                item["done"] = False
            return ("react","✅")
        case "alias":
            if arg == []:
                return ("reply","name required")
            name = arg.pop(0)
            db[nameset.index(name)]["alias"] = []
            save_file(db)
            return ("react","✅")

    return ("reply","Work on progress")

def help(arg):
    return ("reply","Pls ping MinPNG for a clear instruction because he was too lazy to write a help command")

def get_next_reset_timestamp():
    current_time = datetime.now(jp_tzone)
    reset_time = datetime(current_time.year,current_time.month,current_time.day,5,0,0,0,tzinfo=jp_tzone)
    reset_time = timegm(reset_time.utctimetuple())
    return reset_time if reset_time > time.time() else reset_time + 86400

def get_name_from_alias(alias):
    for item in db:
        if alias in item["alias"]:
            return item["name"]
    return None


if __name__ == "__main__":
    current_time = datetime.now(jp_tzone)
    reset_time = datetime(current_time.year,current_time.month,current_time.day,5,0,0,0,tzinfo=jp_tzone)
    print(timegm(reset_time.utctimetuple()))
    load_file()