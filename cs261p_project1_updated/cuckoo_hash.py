# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10
		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		table = 0
		for removal in range(self.CYCLE_THRESHOLD + 1):  
			idx = self.hash_func(key, table)
			if self.tables[table][idx] is None:
				self.tables[table][idx] = key
				return True
			else:
				key, self.tables[table][idx] = self.tables[table][idx], key
				table = (table + 1) % len(self.tables)
		return False
	
	def lookup(self, key: int) -> bool:
		return (
			self.tables[1][self.hash_func(key, 1)] == key or
            self.tables[0][self.hash_func(key, 0)] == key
            
        )


	def delete(self, key: int) -> None:
		for i in range(2):
			sub = self.hash_func(key,i)
			if self.tables[i][sub] == key:
				self.tables[i][sub] = None
				break


	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; 
		self.table_size = new_table_size # do not modify this line
		original_table = self.tables.copy()
		self.tables = [[None] * new_table_size for _ in range(2)]
		for tbl in original_table:
			for k in tbl:
				if k is not None:
					self.insert(k)

		

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


