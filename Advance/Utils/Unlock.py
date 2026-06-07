from data import techData
from data import techList
from data import techUnlock



def unlockTech():
	for i in range(len(techUnlock)):
		if not techUnlock[i]["finished"]:
			tech = techData[techUnlock[i]["name"]]["object"]
			if num_unlocked(tech) < techUnlock[i]["level"]:
				cost = get_cost(tech)
				for item in cost:
					if num_items(item) < cost[item]:
						return {"item": item, "cost": cost[item]}
				techUnlock[i]["finished"] = unlock(tech)
				
			else:
				techUnlock[i]["finished"] = True
	return {"item": Items.Hay , "cost": 999999999}
