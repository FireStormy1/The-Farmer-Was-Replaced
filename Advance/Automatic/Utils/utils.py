def generate_moves_multi(
	drones=1,
	id=1
):
	size_x = get_world_size()
	base = size_x // drones
	rem = size_x % drones

	if id <= rem:
		size_y = base + 1
		y_min = (id - 1) * (base + 1)
	else:
		size_y = base
		y_min = (id - 1) * base + rem
	y_max = y_min + size_y - 1

	moves = []
	pos_x = get_pos_x()
	pos_y = get_pos_y()

	move_to(pos_x, y_min)
	pos_y = y_min
	moved = True
	dir_S = False
	for _ in range(size_x*size_y):
		if pos_y == y_max and not moved:
			moves.append(East)
			pos_x = (pos_x + 1) % size_x
			dir_S = True
			moved = True
		elif pos_y == y_min and not moved:
			moves.append(East)
			pos_x = (pos_x + 1) % size_x
			dir_S = False
			moved = True
		elif  y_min == y_max:
			moves.append(East)
			pos_x = (pos_x + 1) % size_x
		else:
			if dir_S:
				pos_y -=1
				moves.append(South)
			else:
				pos_y +=1
				moves.append(North)
			moved = False
	return moves
def generate_moves_multi_y(
	drones=1,
	id=1
):
	size_y = get_world_size()
	base = size_y // drones
	rem = size_y % drones

	if id <= rem:
		size_x = base + 1
		x_min = (id - 1) * (base + 1)
	else:
		size_x = base
		x_min = (id - 1) * base + rem
	x_max = x_min + size_x - 1

	moves = []
	pos_x = get_pos_x()
	pos_y = get_pos_y()

	move_to(x_min, pos_y)
	pos_x = x_min
	moved = True
	dir_W = False
	for _ in range(size_x*size_y):
		if pos_x == x_max and not moved:
			moves.append(North)
			pos_y = (pos_y + 1) % size_y
			dir_W = True
			moved = True
		elif pos_x == x_min and not moved:
			moves.append(North)
			pos_y = (pos_y + 1) % size_y
			dir_W = False
			moved = True
		elif  x_min == x_max:
			moves.append(North)
			pos_y = (pos_y + 1) % size_y
		else:
			if dir_W:
				pos_x -=1
				moves.append(West)
			else:
				pos_x +=1
				moves.append(East)
			moved = False
	return moves
def move_to(goal_x, goal_y, current_x=get_pos_x(), current_y=get_pos_y(), ws=get_world_size()):
	hws = ws // 2
	# Calculate the shortest x direction
	dx = (goal_x - current_x + hws) % ws - hws
	# Calculate the shortest y direction
	dy = (goal_y - current_y + hws) % ws - hws

	# Move in x direction
	for _ in range(dx):
		move(East)
	for _ in range(-dx):
		move(West)

	# Move in y direction
	for _ in range(dy):
		move(North)
	for _ in range(-dy):
		move(South)


def generate_moves(
		n = get_world_size()**2,
		world_size = get_world_size(),
		pos_x = 0,
		pos_y = 0
	):
	moves = []
	if n > world_size**2:
		world_moves = generate_moves(world_size**2, world_size, pos_x, pos_y)
		for i in range(n // world_size**2):
			moves += world_moves
		n %= world_size**2

	for i in range(n):
		if pos_x % world_size == pos_y % world_size:
			pos_x -= 1
			moves.append(West)
		else:
			pos_y += 1
			moves.append(North)
	return moves

def watering():
	if num_unlocked(Unlocks.Watering)>0:
		while get_water() < 0.7 and num_items(Items.Water)>1:
			use_item(Items.Water)

def harvestAll():
	def ha(id=0):
		if id == 1:
			MOVES = generate_moves_multi(max_drones(), 1)
		else:
			MOVES = generate_moves_multi(max_drones(), num_drones())
		for dir in MOVES:
			if can_harvest():
				harvest()
			move(dir)
		
	if max_drones() == 1:
		ha(1)
	else:
		for _ in range(max_drones()-1):
			spawn_drone(ha)
			sleep(200)
		ha(1)
	while num_drones()>1:
		do_a_flip()
	clear()



def distribute_point(size, n, id):

	# 估算列数
	cols = n ** 0.5 // 1
	if cols * cols < n:
		cols += 1

	# 行数（向上取整）
	rows = (n + cols - 1) // cols

	# 整数步长（至少 1）
	step_x = max(1, size // cols)
	step_y = max(1, size // rows)

	# id → index
	idx = id - 1
	r = idx // cols
	c = idx % cols

	# 计算整数坐标（居中）
	x = c * step_x + step_x // 2
	y = r * step_y + step_y // 2

	# 边界保护
	if x >= size:
		x = size - 1
	if y >= size:
		y = size - 1

	return x, y

def sleep(ops=3):
	list(range(ops-3))

	
