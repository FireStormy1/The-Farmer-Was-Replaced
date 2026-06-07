import globalv
import utils


def go():
	MOVES = None
	if num_unlocked(Unlocks.Expand) == 1:
		MOVES = [North, North, North]
	else:
		MOVES = utils.generate_moves()

	if num_unlocked(Unlocks.Plant) == 0:
		while num_items(Items.Hay) < globalv.poly_goal["cost"]:
			if not MOVES:
				if num_unlocked(Unlocks.Speed) > 0:
					if can_harvest():
						harvest()
				else:
					harvest()
			else:
				for dir in MOVES:
					if can_harvest():
						harvest()
					move(dir)
	else:
		while num_items(globalv.poly_goal["item"]) < globalv.poly_goal["cost"]:
			if not MOVES:
				if can_harvest():
					harvest()
				plant(globalv.poly_goal["name"])
			else:
				for dir in MOVES:
					if can_harvest():
						harvest()
					if globalv.poly_goal["name"] == Entities.Carrot:
						if get_ground_type() == Grounds.Grassland:
							till()
					if globalv.poly_goal["name"] == Entities.Tree:
						if (get_pos_x()+get_pos_y()) % 2 == 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Bush)
					else:
						plant(globalv.poly_goal["name"])

					move(dir)


def start():
	if globalv.poly_goal["item"] == Items.Carrot:
		totalCarrot = globalv.poly_goal["cost"]
		needCarrot = totalCarrot - num_items(Items.Carrot) + globalv.size**2 * num_unlocked(Unlocks.Carrots)**2
		if num_items(Items.Hay) < needCarrot:
			globalv.poly_goal = {"item": Items.Hay,
								 "cost": needCarrot, "name": Entities.Grass}
			go()
		if num_items(Items.Wood) < needCarrot:
			globalv.poly_goal = {"item": Items.Wood,
								 "cost": needCarrot, "name": Entities.Tree}
			if num_unlocked(Unlocks.Trees) > 0:
				globalv.poly_goal["name"] = Entities.Tree
			else:
				globalv.poly_goal["name"] = Entities.Bush
			go()
		globalv.poly_goal = {"item": Items.Carrot,
							 "cost": totalCarrot, "name": Entities.Carrot}
	elif globalv.poly_goal["item"] == Items.Hay:
		globalv.poly_goal["name"] = Entities.Grass
	elif globalv.poly_goal["item"] == Items.Wood:
		if num_unlocked(Unlocks.Trees) > 0:
			globalv.poly_goal["name"] = Entities.Tree
		else:
			globalv.poly_goal["name"] = Entities.Bush
	else:
		return False
	go()
