import os


path = os.path.abspath(__file__.replace("sanitycheck.py", ""))
outputPath = os.path.join(path, "final_output")


def getAllPngs(path):
    allFiles = os.listdir(path=path)
    for i in range(len(allFiles)):
        splitFileName = allFiles[i].split(".")
        fileExtension = splitFileName[len(splitFileName)-1]
        if str.lower(fileExtension) != "png":
            allFiles.pop(i)
        else:
            allFiles[i] = int(splitFileName[0])
    return allFiles


class HashTable:
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    def set(self, key, val):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    def get(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            return record_val
        else:
            return "No record found"

    def delete(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    def __str__(self):
        return "".join(str(item) for item in self.hash_table)


def main():
    missingCount = 0
    files = getAllPngs(outputPath)
    files.sort()
    ids = HashTable(8765)
    for i in range(1, 8766):
        ids.set(i, False)
    for i in range(len(files)):
        ids.set(files[i], True)
    for i in range(1, 8766):
        if ids.get(i) == False:
            missingCount += 1
            print("missing id: " + str(i))
    print("\nmissing: " + str(missingCount) + " images")


main()
