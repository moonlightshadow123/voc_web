import requests
from pathlib import Path
import os, time, threading

class Saver:
    def __init__(self, save_dir="./", root_url="./", span=30):
        self.save_dir = save_dir
        self.span = span
        self.root_url = root_url

    def save(self, word, ori_url):
        file_path,file_url = self.getName(word)
        res = requests.get(ori_url)  
        with open(file_path, 'wb') as f:
            f.write(res.content)
        t = threading.Thread(target=self.gc, args=(file_path,self.span))
        t.start()
        return file_url

    def getName(self, word):
        file_name = word + ".wav"
        file_path = self.save_dir + file_name
        while Path(file_path).exists():
            word += "_"
            file_name = word + ".wav"
            file_path = self.save_dir + file_name
        return file_path, self.root_url+file_name

    def gc(self, file, span):
        time.sleep(span)
        try:
            os.remove(file)
        except OSError:
            pass