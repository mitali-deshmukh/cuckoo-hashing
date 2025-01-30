# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional


class CuckooHash24:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.bucket_size = 4
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
        # you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py).
        # this function randomly chooses an index from a given bucket for a given table. this ensures that the random
        # index chosen by your code and our test script match.
        #
        # for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
        # you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
        # will displace the key at index 2 in that bucket.
        rand.seed(int(str(bucket_idx) + str(table_id)))
        return rand.randint(0, self.bucket_size - 1)

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[Optional[List[int]]]]:
        # the buckets should be implemented as lists. Table cells with no elements should still have None entries.
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        table = 0
        for evictions in range(self.CYCLE_THRESHOLD + 1):
            bucket_index = self.hash_func(key, table)
            bucket = self.tables[table][bucket_index]
            if bucket is None:
                self.tables[table][bucket_index] = [key]
                return True
            elif len(bucket) == self.bucket_size:
                key_index = self.get_rand_idx_from_bucket(bucket_index, table)
                key, bucket[key_index] = bucket[key_index], key
                table = (table + 1) % len(self.tables)
            else:
                bucket.append(key)
                return True
        return False
                
                
    def lookup(self, key: int) -> bool:
        tbl = 0
        i=0
        while i in range(0,len(self.tables)):
             bucket = self.tables[tbl][self.hash_func(key, tbl)]
             if bucket is not None and key in bucket:
                 return True
             tbl = (tbl + 1) % len(self.tables)
             i+=1
        return False

    def delete(self, key: int) -> None:
        tbl = 0
        for i in range(len(self.tables)):
            bidx = self.hash_func(key, tbl)
            bkt = self.tables[tbl][bidx]
           
            if bkt is not None and key in bkt:
                bkt.remove(key)
                if not self.tables[tbl][bidx]:
                    self.tables[tbl][bidx] = None
                return
            tbl = (tbl + 1) % len(self.tables)

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1
        self.table_size = new_table_size  # do not modify this line
        original_tables = self.tables.copy()
        self.tables = [[None] * new_table_size for _ in range(2)]
        for t in original_tables:
            for b in t:
                if b is not None:
                    for key in b:
                        self.insert(key)

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define