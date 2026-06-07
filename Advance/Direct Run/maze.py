#gives 1mil/min
def cheese():
	drones = []
	for x in range(5):
		for y in range(5):
			drones.append(make_drone(x, y))
	do_a_flip() # let drones get into position
	while True:
		plant(Entities.Bush)
		use_substance()
		while measure():
			pass # wait

			
def make_drone(x, y):
	def action():
		goto(x, y)
		while True:
			while not measure(): 
				pass # wait for maze
			counter = 0
			while measure():
				if get_entity_type() == Entities.Treasure:
					use_substance()
					counter += 1 
					if counter > 5: 
						harvest() # harvest when chest stops moving
				else:
					counter = 0
	return spawn_drone(action)


def goto(x, y):
	for _ in range(x):
		move(East)
	for _ in range(y):
		move(North)

	
def use_substance():
	n_substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, n_substance)

	
if __name__ == "__main__":
	set_world_size(5)
	goto(2,2)
	#change_hat(Hats.Golden_Gold_Hat) # not needed
	cheese()
