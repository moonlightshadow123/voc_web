import requests
import json
import re
from utils import try_deco
from saver import Saver
dict_key = "28807962-c095-4619-9eab-47b83f2e88c9"
thes_key = "5ad3d92b-b84a-474a-b498-1627051c0b60"
dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}"
thes_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{}?key={}"
audi_url = "https://media.merriam-webster.com/soundc11/{}/{}.wav"
temp_name = "temp.wav"

def searchKey(data, skey):
    # res = None
    if type(data) == list:
        for each in data:
            subres = searchKey(each, skey)
            if subres != None:
                return subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                return val
            else:
                subres = searchKey(val, skey)
                if subres != None:
                    return subres
    return None

def searchAll(data, skey):
    # print("hello")
    res = []
    if type(data) == list:
        for each in data:
            subres = searchAll(each, skey)
            if subres != None:
                res += subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                # print(val)
                res.append(val)
            subres = searchAll(val, skey)
            if subres != None:
                res += subres
    return res
 
def searchAllPS(data, skey, psdata, pskey):
    # print("hello")
    res = []
    if type(data) == list:
        for each in data:
            subres = searchAllPS(each, skey, psdata, pskey)
            if subres != None:
                res += subres
    if type(data) == dict:
        for key,val in data.items():
            if key == skey:
                # print(val)
                if type(val) == dict: val[pskey] = psdata
                elif type(val) == list: val.append([pskey, psdata]) 
                res.append(val)
            elif key == pskey:
                psdata = val
            subres = searchAllPS(val, skey, psdata, pskey)
            if subres != None:
                res += subres
    return res

class MWapi:
    def __init__(self, temp_dir, temp_url):
        # self.temp_dir = temp_dir
        # self.temp_url = temp_url
        self.saver = Saver(temp_dir, temp_url)

    @try_deco
    def lookup(self, word, mode="cmd"):
        # requests
        dict_data = self.getDict(word)
        thes_data = self.getThes(word)
        hasaudio, audiourl = self.downAudio(word, searchKey(dict_data, "audio"))
        # print(dict_data)
        # data process
        res = {}
        defs = self.getDefs(dict_data)
        stems = self.getStems(dict_data)
        syns = self.getSyns(thes_data)
        ants = self.getAnts(thes_data)
        res["word"] = word
        res["defs"] = defs 
        res["stems"] = stems
        res["syns"] = syns
        res["ants"] = ants
        if hasaudio: res["audio"] = audiourl
        # print("Definitions:")
        if mode == "cmd":
            return None
        if mode == "json":
            with open("data.json", "w") as f:
                json.dump(res, f, indent=4)
            return res

    def processStr(self, string):
        # print(string)
        string = re.sub(r"\{([^\|]*?)\}", r"", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        string = re.sub(r"\{([^\|]*?)\|([^\|]*?)\|([^\|]*?)\|([^\|]*?)\}", r"\g<2>", string)
        return string

    '''Requests related'''

    '''
    @try_deco
    def downAudio(self, audio):
        if not audio: return False
        subd = ""
        if re.match(r"bix.*", audio):
            subd = "bix"
        elif re.match(r"gg.*", audio):
            subd = "gg"
        elif re.match(r"[^a-zA-Z].*", audio):
            subd = "number"
        else:
            subd = audio[0]
        url = audi_url.format(subd, audio)
        res = requests.get(url)  
        with open(temp_name, 'wb') as f:
            f.write(res.content)
        return True
    '''
    @try_deco
    def downAudio(self, word, audio):
        if not audio: return False, ""
        subd = ""
        if re.match(r"bix.*", audio):
            subd = "bix"
        elif re.match(r"gg.*", audio):
            subd = "gg"
        elif re.match(r"[^a-zA-Z].*", audio):
            subd = "number"
        else:
            subd = audio[0]
        url = audi_url.format(subd, audio)
        file_url = self.saver.save(word, url)
        # return True, file_url
        return True, url

    @try_deco
    def getDict(self, word):
        url = dict_url.format(word, dict_key)
        res = requests.get(url)
        json_data = json.loads(res.text)
        return json_data

    @try_deco
    def getThes(self, word):
        url = thes_url.format(word,thes_key)
        res = requests.get(url)
        json_data = json.loads(res.text)
        return json_data

    '''From Dict'''

    def getDefs(self, data):
        data = searchAllPS(data, "dt", "", "fl")
        res = []
        for eachDt in data:
            cur_dict = {"text":"", "vis":"", "fl":""}
            for item in eachDt:
                if len(item) < 2:
                    continue
                if item[0] == "text":
                    cur_dict["text"] = self.processStr(item[1])
                elif item[0] == "vis":
                    cur_dict["vis"] = self.processStr(item[1][0]["t"])
                elif item[0] == "fl":
                    cur_dict["fl"] = self.processStr(item[1])
            if cur_dict["text"] != "" : res.append(cur_dict)
        return res

    def getStems(self, data):
        data = searchKey(data, "stems")
        return data if data else None

    ''' From Thes'''

    def getSyns(self, data):
        data = searchKey(data, "syns")
        return data[0] if data else None

    def getAnts(self, data):
        data = searchKey(data, "ants")
        return data[0] if data else None


if __name__ == "__main__":
    mw = MWapi()
    print(mw.lookup("after", "json"))