# any move_to function can be used.
# /movement/wrapping_shortest_path/navi_to_deltalist.py
from utils import move_to, generate_moves_multi, sleep, generate_moves_multi_y
import globalv
import pumpkin


def gradient_bubble_sort(grid, rx, ry):
	global_changed = True
	while global_changed:
		global_changed = False
		for x in rx:
			gridx = grid[x]
			for y in ry:
				# Swap with right neighbor if needed.
				yp1 = y + 1
				if y < ry[-1] and gridx[y] > gridx[yp1]:
					temp = gridx[y]
					gridx[y] = gridx[yp1]
					gridx[yp1] = temp

					global_changed = True
					move_to(x, y)
					swap(North)
					offset = y - 1
					offset2 = y
					while offset2 > ry[0] and gridx[offset2] < gridx[offset]:
						move_to(x, offset2)
						swap(South)
						temp = gridx[offset2]
						gridx[offset2] = gridx[offset]
						gridx[offset] = temp

						offset += 1
						offset2 += 1
				# Swap with bottom neighbor if needed.
				xp1 = x + 1
				if x < rx[-1]:
					gridxp1 = grid[xp1]
				else:
					continue
				if gridx[y] > gridxp1[y]:
					# use temp variable to swap
					temp = gridx[y]
					gridx[y] = gridxp1[y]
					gridxp1[y] = temp

					global_changed = True
					move_to(x, y)
					swap(East)
					offset = x - 1
					offset2 = x
					while offset2 > rx[0] and grid[offset2][y] < grid[offset][y]:
						move_to(offset2, y)
						swap(West)
						gridoffset = grid[offset]
						gridoffset2 = grid[offset2]
						temp = gridoffset2[y]
						gridoffset2[y] = gridoffset[y]
						gridoffset[y] = temp

						offset += 1
						offset2 += 1


def planting(id=0):
	if id == 1:
		MOVES = generate_moves_multi(max_drones(), 1)
	else:
		MOVES = generate_moves_multi(max_drones(), num_drones())
	grid = {}
	rx = []
	ry = []
	for dir in MOVES:
		x = get_pos_x()
		y = get_pos_y()
		if x not in grid:
			grid[x] = {}
		if x not in rx:
			rx.append(x)
		if y not in ry:
			ry.append(y)
		till()
		plant(Entities.Cactus)
		grid[x][y] = measure()
		move(dir)
	gradient_bubble_sort(grid, rx, ry)


def scan(id=0,drones = globalv.cactus_drones):
	if id == 1:
		MOVES = generate_moves_multi(drones, 1)
	else:
		MOVES = generate_moves_multi(drones, num_drones())
	grid = {}
	rx = []
	ry = []
	for dir in MOVES:
		x = get_pos_x()
		y = get_pos_y()
		if x not in grid:
			grid[x] = {}
		if x not in rx:
			rx.append(x)
		if y not in ry:
			ry.append(y)
		grid[x][y] = measure()
		move(dir)
	gradient_bubble_sort(grid, rx, ry)


def scan_y(id=0):
	if id == 1:
		MOVES = generate_moves_multi_y(globalv.cactus_drones, 1)
	else:
		MOVES = generate_moves_multi_y(globalv.cactus_drones, num_drones())
	grid = {}
	rx = []
	ry = []
	for dir in MOVES:
		x = get_pos_x()
		y = get_pos_y()
		if x not in grid:
			grid[x] = {}
		if x not in rx:
			rx.append(x)
		if y not in ry:
			ry.append(y)
		grid[x][y] = measure()
		move(dir)
	gradient_bubble_sort(grid, rx, ry)


def pumpkinCheck():
	size = get_world_size()
	needCactus = globalv.cactus_goal-num_items(Items.Cactus)
	oneTurnCactus = size**4 * 2**(num_unlocked(Unlocks.Cactus)-1)
	oneTurnPumpkin = size**2 * 2**(num_unlocked(Unlocks.Cactus)-1)
	needPumpkin = (needCactus//oneTurnCactus + 1)*oneTurnPumpkin
	if num_items(Items.Pumpkin) < needPumpkin:
		globalv.pumpkin_goal = needPumpkin
		pumpkin.start()


def start():
	while num_items(Items.Cactus) < globalv.cactus_goal:
		pumpkinCheck()
		clear()
		globalv.cactus_drones = max_drones()
		if max_drones() == 1:
			planting(1)
			continue
		
		for _ in range(max_drones()-1):
			spawn_drone(planting)
			sleep(200)
		planting(1)
		while num_drones() > 1:
			sleep(200)
		for _ in range(max_drones()-1):
			spawn_drone(scan_y)
			sleep(200)
		scan_y(1)
		while num_drones() > 1:
			sleep(200)
		if max_drones() == get_world_size():
			harvest()
			continue
			
		globalv.cactus_drones = max(1, globalv.cactus_drones//2)
		while True:
			if globalv.cactus_drones == 1:
				if num_drones() == 1:
					scan(1)
					break
				else:
					sleep(200)
			else:
				for _ in range(globalv.cactus_drones-1):
					spawn_drone(scan)
					sleep(200)
				scan(1)
				while num_drones() > 1:
					sleep(200)
				for _ in range(globalv.cactus_drones-1):
					spawn_drone(scan_y)
					sleep(200)
				scan_y(1)
				while num_drones() > 1:
					sleep(200)
				#scan(1,1)
				#break
			globalv.cactus_drones = max(1, globalv.cactus_drones//4)
			sleep(400)
		harvest()
