from Unlock import unlockTech
import globalv
import power
import poly
import pumpkin
import maze
import cactus
import dinosaur
import weirdSubstance

while True:
	todo = unlockTech()
	if num_unlocked(Unlocks.Leaderboard)>0 and globalv.leaderboard_mode:
		break
	size = get_world_size()
	if num_unlocked(Unlocks.Sunflowers)>0 and num_items(Items.Power) < globalv.power["min"]:
		power.start()
	elif todo["item"] == Items.Hay or todo["item"] == Items.Wood or todo["item"] == Items.Carrot:
		globalv.poly_goal = todo
		poly.start()
	elif todo["item"] == Items.Pumpkin:
		globalv.pumpkin_goal = todo["cost"]
		pumpkin.start()
	elif todo["item"] == Items.Gold:
		globalv.maze_goal = todo["cost"]
		maze.start()
	elif todo["item"] == Items.Cactus:
		globalv.cactus_goal = todo["cost"]
		cactus.start()
	elif todo["item"] == Items.Bone:
		globalv.dinosaur_goal = todo["cost"]
		dinosaur.start()
	elif todo["item"] == Items.Weird_Substance:
		globalv.weirdSubstance_goal = todo["cost"]
		weirdSubstance.start()
