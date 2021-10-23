import csv 
import json

class KVStore:
    def __init__(self):
        self.cache = dict()

    def get(self, key):
        if (key not in self.cache):
            self.read_file_to_cache()
            print(self.cache)
            if (key not in self.cache):
                return -1
        print("Type: ({})".format(type(self.cache[key])))
        value = json.loads(self.cache[key])
        print(type(value))
        return value
    
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
        print("INSIDE UPDATE")
        for key, value in payload.items():
            if (isinstance(key, (bytes, bytearray))):
                key = str(key.decode("utf-8"))
            value = json.dumps(value)
            self.read_file_to_cache()
            if (key not in self.cache):
                self.put({key: value})
            else:
                self.cache[key] = value
                self.write_to_file(key, value)

    def delete(self, key):
        if (key in self.cache):
            del self.cache[key]
            self.write_to_file(key, -1)
        else:
            self.read_file_to_cache()
            self.write_to_file(key, -1)
    
    def write_to_file(self, key, value):
        with open('data.csv','a') as f:
            w = csv.writer(f)
            w.writerow([key,value])
    
    def read_file_to_cache(self):
        with open('data.csv', mode ='r')as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            mydict = dict((rows[0], rows[1]) for rows in csvFile)
            for key, value in mydict.items():
                if(key not in self.cache):
                    self.cache[key] = value

    