import globalv
import utils
import noPoly

def poly_plant():
	pos_x = get_pos_x()
	pos_y = get_pos_y()
	entity_temp = globalv.poly_goal["name"]
	if entity_temp == Entities.Tree:
		if (pos_x-1, pos_y) in globalv.poly_companions and globalv.poly_companions[(pos_x-1, pos_y)] == Entities.Tree:
			entity_temp = Entities.Bush
		if (pos_x+1, pos_y) in globalv.poly_companions and globalv.poly_companions[(pos_x+1, pos_y)] == Entities.Tree:
			entity_temp = Entities.Bush
		if (pos_x, pos_y-1) in globalv.poly_companions and globalv.poly_companions[(pos_x, pos_y-1)] == Entities.Tree:
			entity_temp = Entities.Bush
		if (pos_x, pos_y+1) in globalv.poly_companions and globalv.poly_companions[(pos_x, pos_y+1)] == Entities.Tree:
			entity_temp = Entities.Bush

	if not plant(entity_temp):
		plant(Entities.Bush)
	companion, pos = get_companion()
	globalv.poly_companions[pos] = companion
	globalv.poly_companions[(pos_x, pos_y)] = entity_temp
	return True


def poly_multi(id=0):
	if id == 1:
		MOVES = utils.generate_moves_multi(max_drones(), 1)
	else:
		MOVES = utils.generate_moves_multi(max_drones(), num_drones())
	while num_items(globalv.poly_goal["item"]) < globalv.poly_goal["cost"]: 
		for dir in MOVES:
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() == globalv.poly_goal["name"]:
				if can_harvest():
					harvest()
				
			coords = (get_pos_x(), get_pos_y())
			if coords in globalv.poly_companions:
				comp = globalv.poly_companions[coords]
				plant(comp)
			else:
				poly_plant()
			utils.watering()

			move(dir)

def start_poly():
	if max_drones() == 1:
		poly_multi(1)
	else:
		for _ in range(max_drones()-1):
			spawn_drone(poly_multi)
			utils.sleep(200)
		poly_multi(1)

def start():
	if num_unlocked(Unlocks.Polyculture)==0:
		noPoly.start()
		return
	clear()
	
	if globalv.poly_goal["item"] == Items.Carrot:
		totalCarrot = globalv.poly_goal["cost"]
		needCarrot = totalCarrot - num_items(Items.Carrot) + globalv.size**2 *num_unlocked(Unlocks.Carrots)**2
		if num_items(Items.Hay)<needCarrot:
			globalv.poly_goal = {"item": Items.Hay, "cost": needCarrot, "name": Entities.Grass}
			start_poly()
		if num_items(Items.Wood)<needCarrot:
			globalv.poly_goal = {"item": Items.Wood, "cost": needCarrot, "name": Entities.Tree}
			start_poly()
		globalv.poly_goal = {"item": Items.Carrot, "cost": totalCarrot, "name": Entities.Carrot}
	elif globalv.poly_goal["item"] == Items.Hay:
		globalv.poly_goal["name"] = Entities.Grass
	elif globalv.poly_goal["item"] == Items.Wood:
		globalv.poly_goal["name"] = Entities.Tree
	else:
		return False
	start_poly()

if __name__ == "__main__":
	start()
