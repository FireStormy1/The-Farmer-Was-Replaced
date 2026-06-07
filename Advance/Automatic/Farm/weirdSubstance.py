from utils import move_to,distribute_point,sleep
import globalv


def multi(id=0):
	if id == 0:
		id = num_drones()
	size = get_world_size()
	x,y = distribute_point(size,max_drones(),id)
	move_to(x,y)
	till()
	use_item(Items.Water)
	use_item(Items.Water)
	use_item(Items.Water)
	while num_items(Items.Weird_Substance) < globalv.weirdSubstance_goal:
		use_item(Items.Water)

		plant(Entities.Tree)
		if Entities.Grass in get_companion():
			if not use_item(Items.Fertilizer):
				break
		harvest()


def start():
	clear()
	if max_drones() == 1:
		multi(1)
	else:
		for _ in range(max_drones()-1):
			spawn_drone(multi)
			sleep(200)
		multi(1)
	pass
