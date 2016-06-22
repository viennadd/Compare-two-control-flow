import os
import json
import pymongo

source_path = "/root/ToAlexClean"
cfg_path = "/root/cfg"
client = pymongo.MongoClient()
source = client.fyp.source

if __name__ == "__main__":

    def insert(filename):
        
        q = 'uncategorized'
        for x in 'abcdefghijk':
            if ('q1' + x) in filename:
                q = 'q1' + x

        if not os.path.isfile(cfg_path + '/' + filename + '.cfg.json'):
            return

        with open(source_path + "/" + filename, 'r') as f:
            source_code = f.read()    

        with open(cfg_path + '/' + filename + '.cfg.json', 'r') as f:
            cfg_json = f.readline() # read first line
            if not len(cfg_json) > 2:
                return 
            print("decoding %s" % cfg_json)
            decoded = json.loads(cfg_json)

        record = {"filename": filename,
                    "source_code": source_code,
                    "cfg_json": decoded,
                    "q": q
                    }

        # print("inserting %s" % record)
        object_id = source.insert_one(record)
        print(object_id)

    def main():
        inserts = []
        for (x, y, filenames) in os.walk(source_path):
            for f in filenames:
                if f[0] != '.': 
                    insert(f)

    main()     

    
