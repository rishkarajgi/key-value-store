import csv 
import json
import os
import sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = os.path.join(__location__, 'data.csv')

DELETED_FLAG = '-1'

class KVStore:
    def __init__(self):
        self.cache = dict()

    def get(self, key):
        # Ik key not present in memory fetch from file
        if (key not in self.cache):
            self.read_file_to_cache()

            if (key not in self.cache):
                return 404, "Key not found!"
        value = json.loads(self.cache[key])
        return 200, value
    
    def put(self, payload):
        for key, value in payload.items():
            if (isinstance(key, (bytes, bytearray))):
                key = str(key.decode("utf-8"))
            value = json.dumps(value)
            if (key not in self.cache):
                self.read_file_to_cache()
                if (key not in self.cache):
                    print("Key not found! Adding new key...")
                    self.cache[key] = value
                    self.write_to_file(key, value)
                else:
                    if (self.cache[key] == '-1'):
                        print("writing key: " + str(key) + " value: " + str(value))
                        self.write_to_file(key, value)
                        self.cache[key] = value
            else:
                print("Key: ({}) present in cache".format(str(key)))
    
    def update(self, payload):
        for key, value in payload.items():
            if (isinstance(key, (bytes, bytearray))):
                key = str(key.decode("utf-8"))
            value = json.dumps(value)
            self.read_file_to_cache()
            if (key not in self.cache):
                return 404, "Key not found!"
            else:
                self.cache[key] = value
                self.write_to_file(key, value)
                return 200, "Success"

    def delete(self, key):
        self.read_file_to_cache()
        if key not in self.cache:
            return 404, "Key not found!"
        if (key in self.cache):
            del self.cache[key]
            self.write_to_file(key, -1)
        else:
            self.write_to_file(key, -1)
        return 200, "Key deleted successfully"
    
    def write_to_file(self, key, value):
        with open(file_path,'a') as f:
            w = csv.writer(f)
            w.writerow([key,value])
    
    def read_file_to_cache(self):
        with open(file_path, mode ='r')as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            mydict = dict((rows[0], rows[1]) for rows in csvFile)
            for key, value in mydict.items():
                if(key not in self.cache and value != DELETED_FLAG):
                    self.cache[key] = value
    
    def flush_file(self):
        fileObject = open(file_path, "w+")
        fileObject.close()
        self.cache = {}

    