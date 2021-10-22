import csv 

class KVCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = dict()

    def get(self, key):
        if (key not in self.cache):
            return -1
        
        return self.cache[key]
    
    def put(self, key, value):
        if (key not in self.cache):
            file_contents = self.read_file_contents()
            if (key not in file_contents):
                print("key not found. adding new key")
                self.cache[key] = value
                print(self.cache)
                self.write_to_file(key, value)
            else:
                print(file_contents[key])
                if (file_contents[key] == '-1'):
                    print("writing key: " + str(key) + " value: " + str(value))
                    self.write_to_file(key, value)
                    file_contents[key] = value
                self.cache = file_contents
        else:
            print("Key: " + str(key) + " present in cache")
    
    def update(self, key, value):
        if (key not in self.cache):
            file_contents = self.read_file_contents()
            if (key not in file_contents):
                self.put(key, value)
        else:
            self.cache[key] = value
            self.write_to_file(key, value)

    def delete(self, key):
        if (key in self.cache):
            del self.cache[key]
            self.write_to_file(key, -1)
        else:
            file_contents = self.read_file_contents()
            self.write_to_file(key, -1)

    
    def print_contents(self):
        for key, value in self.cache.items():
            print("Key:" + str(key) + " Value: " + str(value))
    
    def write_to_file(self, key, value):
        with open('data.csv','a') as f:
            w = csv.writer(f)
            w.writerow([key,value])
    
    def read_file_contents(self):
        with open('data.csv', mode ='r')as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            mydict = dict((int(rows[0]),rows[1]) for rows in csvFile)
            return mydict

    




# cache = KVCache(10)
# cache.put(1,'abc')
# cache.put(2,'xyz')
# cache.update(1,'qwe')
# cache.delete(1)
# cache.put(1, 'efg')
# cache.put(3, 'jkl')
# cache.update(3, 'opq')
# cache.delete(3)
# cache.print_contents()
# cache.delete(1)
# cache.print_contents()

# cache.put(2,'def')
# cache.put(2,'def')
# cache.update(2,'xyz')
# cache.print_contents()

# cache.read_file_contents()