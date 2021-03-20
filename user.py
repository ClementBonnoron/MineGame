from content import Blocks, Access
import random as rd
from datetime import datetime
import json

class UserData:

	default_access = Access.PLAIN
	default_money = 0

	def __init__(self, name, id):
		super().__init__()
		self.data = dict()
		self.name = name
		self.id = id
		self.access = UserData.default_access
		self.money = UserData.default_money
		self.date_joined = datetime.now().strftime("%d/%m/%Y, %H:%M")
		self.display_messages_mining = False
		for key in Blocks.__members__.keys():
			self.data[key] = 0

	def mine(self, name):
		if name is None:
			block = self.__get_block(self.access)
			self.__add_block(block, 1)
			return block, self.access, 1
		else:
			place = Access.from_name(name)
			block = self.__get_block(place)
			self.__add_block(block, 1)
			return block, place, 1

	def sell_block(self, block=None, quantity=None):
		block = block.upper()
		if (quantity.isdecimal() and int(quantity) <= 0) or (
				not quantity.isdecimal() and str(quantity) != "all" and block not in Blocks.__members__.keys()):
			return False, "Error with the quantity : '{}'".format(quantity)

		sales = {}
		gains = 0

		if block == "ALL":
			for name, count in self.data.items():
				nb_sold = (count if str(quantity) == "all" else (int(quantity) if int(quantity) <= count else count))
				gain_block = nb_sold * Blocks.from_name(name).cost
				gains += gain_block
				sales[name] = nb_sold, gain_block 

		elif block in self.data:
			count = self.data[block]
			nb_sold = (count if str(quantity) == "all" else (int(quantity) if int(quantity) <= count else count))
			gain_block = nb_sold * Blocks.from_name(block).cost
			gains += gain_block
			sales[block] = nb_sold, gain_block 
			
		else:
			return False, "Error with the arguments : '{}' '{}'".format(quantity, block)
		
		self.__clear_data(sales)
		self.money += gains
		return True, sales

	def upgrade_access(self):
		next_place = Access.next_access(self.access)
		if next_place.cost > self.money:
			return "You have not enough money : {} missing !".format(next_place.cost - self.money)
		self.access = next_place
		self.money -= next_place.cost
		return "You have been upgraded ! Now you are in '{}' !".format(next_place.name.capitalize())

	def __clear_data(self, sales):
		for name, counts in sales.items():
			self.data[name] -= counts[0]

	def __get_block(self, place):
		blocks = place.blocks
		checks = [block.proba for block in blocks]
		return rd.choices(blocks, weights=checks)[0]

	def __add_block(self, block, number):
		if not block.name in Blocks.__members__.keys():
			raise ValueError("'{}' is not a valid block name".format(block))
		self.data[block.name] += number

	def set_display_mining(self, value):
		self.display_messages_mining = value

	def get_profil(self):
		profil = {}
		blocks = {}
		profil["name"] = self.name
		profil["date_joined"] = self.date_joined
		profil["money"] = self.money
		for key in Blocks.__members__.keys():
			blocks[key] = self.data[key]
		profil["blocks"] = blocks
		return profil

	def verify_access(self, place):
		return self.access.value >= place.value



class Users:
	
	def __init__(self):
		super().__init__()
		self.data = dict()

	async def create_user(self, msg):
		self.data[msg.aid] = UserData(msg.aname, msg.aid)
		await msg.channel.send('Bienvenue <@!{}>, création de votre profil réussi !'.format(msg.aid))

	def get_user(self, msg):
		if not msg.aid in self.data:
			return None
		return self.data[msg.aid]

	def remove_user(self, msg):
		del self.data[msg.aid]

	def is_defined(self, msg):
		return msg.aid in self.data

	def user_mine(self, msg, name=None):
		return self.data[msg.aid].mine(name)

	def user_profil(self, msg):
		return self.data[msg.aid].get_profil()

	def user_have_access(self, msg, name):
		return self.data[msg.aid].verify_access(Access.from_name(name))

	def sell_user_block(self, msg, block, quantity):
		return self.data[msg.aid].sell_block(block, quantity)
	
	def user_display_msg(self, msg):
		return self.data[msg.aid].display_messages_mining

	def set_display_mining_user(self, msg, value):
		self.data[msg.aid].set_display_mining(value)

	def user_update_place(self, msg):
		return self.data[msg.aid].upgrade_access()

	def saveData(self, filename):
		data = self.toJson()
		json_object = json.dumps(data, indent=2)
		with open(filename, 'w') as outfile: 
			outfile.write(json_object) 

	def dropUsers(self):
		self.data.clear()

	def toJson(self):
		struct = {}
		for id, user in self.data.items():
			data = {}
			data["name"] = user.name
			data["access"] = user.access.name
			data["money"] = user.money
			data["date_joined"] = user.date_joined
			data["display_messages_mining"] = str(user.display_messages_mining)
			blocks = {}
			for block, count in user.data.items():
				blocks[block] = count
			data["data"] = blocks
			struct[str(user.id)] = data
		return struct

	def loadData(filename):
		with open(filename, 'r') as openfile: 
			data = json.load(openfile)
			return Users.decodeJson(data)

	def decodeJson(obj):
		users = Users()
		for id, infos in obj.items():
			user = UserData(infos['name'], int(id))
			user.access = Access.from_name(infos['access'])
			user.money = infos['money']
			user.date_joined = infos['date_joined']
			user.display_messages_mining = (infos['display_messages_mining'] == 'True')
			user.data = infos['data']
			users.data[int(id)] = user
		return users

