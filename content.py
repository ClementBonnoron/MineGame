from enum import Enum

class Blocks(bytes, Enum):
	DIRT = (0, 50, 1)
	WOOD = (1, 30, 3)
	STONE = (2, 15, 10)
	GOLD = (3, 5, 50)

	def __new__(cls, value, prob, cost):
		super().__new__(cls, value)
		obj = bytes.__new__(cls, [value])
		obj._value_ = value
		obj.proba = prob
		obj.cost = cost
		return obj

	@classmethod
	def from_name(cls, name):
		for block_name, block in Blocks.__members__.items():
			if block_name == name:
				return block
		raise ValueError("{}'' is not a valid block name".format(name))




class Access(bytes, Enum):
	PLAIN = (1, 0, 'Plain')
	FOREST = (2, 10, 'Forest')
	MINE = (3, 25, 'Mine')
	UNDERGROUND = (4, 100, 'Underground')

	def __new__(cls, value, cost, name):
		super().__new__(cls, value)
		obj = bytes.__new__(cls, [value])
		obj._value_ = value
		obj._name_ = name
		obj.cost = cost
		obj.blocks = obj.get_blocks_from_access()
		return obj

	@classmethod
	def from_name(cls, name):
		for access_name, access in Access.__members__.items():
			if access_name == name:
				return access
		raise ValueError("{}'' is not a valid access name".format(name))

	@classmethod
	def is_access(cls, name):
		return name in Access.__members__.keys()

	@classmethod
	def next_access(cls, access):
		if access == Access.PLAIN:
			return Access.FOREST
		elif access == Access.FOREST:
			return Access.MINE
		elif access == Access.MINE:
			return Access.UNDERGROUND

	
	def get_blocks_from_access(self):
		access_blocks = {
			'Plain': [
				Blocks.DIRT
				],
			'Forest': [
				Blocks.DIRT, Blocks.WOOD
				],
			'Mine': [
				Blocks.DIRT, Blocks.WOOD, Blocks.STONE
				],
			'Underground': [
				Blocks.DIRT, Blocks.WOOD, Blocks.STONE, Blocks.GOLD
				]
		}
		return access_blocks[self.name]




def print_content():
	print(Blocks.__members__.keys())
	print(Blocks.from_name('WOOD').proba)
	print(Access.__members__.keys())
	print(Access.from_name('UNDERGROUND').cost)
