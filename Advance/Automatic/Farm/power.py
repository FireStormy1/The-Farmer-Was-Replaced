import utils
import globalv
import poly

def power_multi(id=0):
	if id == 1:
		MOVES = utils.generate_moves_multi(max_drones(), 1)
	else:
		MOVES = utils.generate_moves_multi(max_drones(), num_drones())

	while num_items(Items.Power) < globalv.power["max"]:
		for direction in MOVES:
			if get_ground_type() == Grounds.Grassland:
				till()
			while measure() != 15:
				harvest()
				if not plant(Entities.Sunflower):
					return False
			utils.watering()
			move(direction)
		for direction in MOVES:
			if can_harvest():
				harvest()
			move(direction)

def CarrotCheck():
	size = get_world_size()
	needPower = globalv.power["max"]-num_items(Items.Power)
	oneTurnPower= size**2 *8
	oneTurnCarrot = size**2 *9
	needCarrot= (needPower//oneTurnPower + 1)*oneTurnCarrot
	if num_items(Items.Carrot) < needCarrot:
		globalv.poly_goal = {"item": Items.Carrot, "cost": needCarrot}
		poly.start()

def start():
	CarrotCheck()
	clear()

	if max_drones() == 1:
		power_multi(1)
	else:
		for _ in range(max_drones()-1):
			spawn_drone(power_multi)
			utils.sleep(200)
		power_multi(1)
	utils.harvestAll()
