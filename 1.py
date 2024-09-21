class LabyrinthError(Exception):
    def __init__(self, message):
        self.message = message


class Labyrinth:
    def __init__(self, filename):
        self.filename = filename
        self.grid = []
        self.to_grid()
        self.searched_point = set()
        self.analyse()

    def to_grid(self):
        with open(self.filename, 'r') as file:
            for line in file:
                new_line = line.replace(' ', '').strip()
                if len(new_line) != 0:
                    self.grid.append(list(new_line))

        if len(self.grid) < 2 or len(self.grid) > 41:
            raise LabyrinthError('Incorrect input.')

        length = []
        for y in self.grid:
            length.append(len(y))
            if len(y) < 2 or len(y) > 31 or len(set(length)) != 1:
                raise LabyrinthError('Incorrect input.')
            for digits in y:
                if digits not in {'0', '1', '2', '3'}:
                    raise LabyrinthError('Incorrect input.')

        last_row = self.grid[-1]
        for i in last_row:
            if i == '2' or i == '3':
                raise LabyrinthError('Input does not represent a labyrinth.')

        last_col = []
        for rows in self.grid:
            last_col.append(rows[-1])

        for j in last_col:
            if j == '1' or j == '3':
                raise LabyrinthError('Input does not represent a labyrinth.')

    def analyse(self):
        self.gate_position()
        self.point_direction()
        self.all_function()

        if self.num_gate() == 0:
            print('The labyrinth has no gate.')
        if self.num_gate() == 1:
            print('The labyrinth has a single gate.')
        if self.num_gate() > 1:
            print(f'The labyrinth has {self.num_gate()} gates.')

        if self.walls() == 0:
            print('The labyrinth has no wall.')
        if self.walls() == 1:
            print('The labyrinth has walls that are all connected.')
        if self.walls() > 1:
            print(f'The labyrinth has {self.walls()} sets of walls that are all connected.')

        self.inaccessible_count = (len(self.grid)-1)*(len(self.grid[0])-1) - len(self.searched_point)
        if self.inaccessible_count == 0:
            print('The labyrinth has no inaccessible inner point.')
        if self.inaccessible_count == 1:
            print('The labyrinth has a unique inaccessible inner point.')
        if self.inaccessible_count > 1:
            print(f'The labyrinth has {self.inaccessible_count} inaccessible inner points.')

        if self.accessible_area == 0:
            print('The labyrinth has no accessible area.')
        if self.accessible_area == 1:
            print('The labyrinth has a unique accessible area.')
        if self.accessible_area > 1:
            print(f'The labyrinth has {self.accessible_area} accessible areas.')

        if self.cul_de_sacs_counts == 0:
            print('The labyrinth has no accessible cul-de-sac.')
        if self.cul_de_sacs_counts == 1:
            print('The labyrinth has accessible cul-de-sacs that are all connected.')
        if self.cul_de_sacs_counts > 1:
            print(f'The labyrinth has {self.cul_de_sacs_counts} sets of accessible cul-de-sacs that are all connected.')

        if len(self.final_entry_exit_path) == 0:
            print('The labyrinth has no entry-exit path with no intersection not to cul-de-sacs.')
        if len(self.final_entry_exit_path) == 1:
            print('The labyrinth has a unique entry-exit path with no intersection not to cul-de-sacs.')
        if len(self.final_entry_exit_path) > 1:
            print(f'The labyrinth has {len(self.final_entry_exit_path)} entry-exit paths with no intersections not to cul-de-sacs.')

    def num_gate(self):
        first_row = self.grid[0]
        last_row = self.grid[-1]
        first_col = []
        last_col = []
        for col in self.grid:
            first_col.append(col[0])
            last_col.append(col[-1])

        row_gates = 0
        col_gates = 0
        for i in range(len(self.grid[0])):
            if first_row[i] in {'0', '2'}:
                row_gates += 1
            if last_row[i] in {'0', '2'}:
                row_gates += 1
        row_gates = row_gates - 2

        for j in range(len(self.grid)):
            if first_col[j] in {'1', '0'}:
                col_gates += 1
            if last_col[j] in {'1', '0'}:
                col_gates += 1
        col_gates = col_gates - 2
        grid_gates = col_gates + row_gates

        return grid_gates

    def gate_position(self):
        self.gate_positions = []
        num_row = len(self.grid)
        num_col = len(self.grid[0])
        for col in range(num_col-1):
            if self.grid[0][col] == '0' or self.grid[0][col] == '2':
                self.gate_positions.append((-1, col))
            if self.grid[-1][col] == '0' or self.grid[-1][col] == '2':
                self.gate_positions.append((num_row - 1, col))

        for row in range(num_row-1):
            if self.grid[row][0] == '1' or self.grid[row][0] == '0':
                self.gate_positions.append((row, -1))
            if self.grid[row][-1] == '1' or self.grid[row][-1] == '0':
                self.gate_positions.append((row, num_col - 1))

    def walls(self):
        walls = 0
        visited = []
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[0])):
                if self.grid[row_index][col_index] != '0' and (row_index, col_index) not in visited:
                    walls += 1
                    self.dfs_walls(row_index, col_index, visited)

        return walls

    def dfs_walls(self, row_index, col_index, visited, con=None):
        if con is None:
            con = ['1', '2', '3']
        if row_index < 0 or row_index >= len(self.grid):
            return None
        if col_index < 0 or col_index >= len(self.grid[0]):
            return None
        if (row_index, col_index) in visited:
            return None
        if self.grid[row_index][col_index] not in con:
            return None

        visited.append((row_index, col_index))

        if self.grid[row_index][col_index] == '1':
            self.dfs_walls(row_index, col_index + 1, visited, ['1', '2', '3'])
            self.dfs_walls(row_index, col_index - 1, visited, ['1', '3'])
            self.dfs_walls(row_index - 1, col_index, visited, ['2', '3'])
            self.dfs_walls(row_index - 1, col_index + 1, visited, ['2', '3'])

        if self.grid[row_index][col_index] == '2':
            self.dfs_walls(row_index, col_index - 1, visited, ['1', '3'])
            self.dfs_walls(row_index - 1, col_index, visited, ['2', '3'])
            self.dfs_walls(row_index + 1, col_index, visited, ['1', '2', '3'])
            self.dfs_walls(row_index + 1, col_index - 1, visited, ['1', '3'])

        if self.grid[row_index][col_index] == '3':
            self.dfs_walls(row_index, col_index + 1, visited, ['1', '2', '3'])
            self.dfs_walls(row_index, col_index - 1, visited, ['1', '3'])
            self.dfs_walls(row_index - 1, col_index, visited, ['2', '3'])
            self.dfs_walls(row_index + 1, col_index, visited, ['1', '2', '3'])
            self.dfs_walls(row_index - 1, col_index + 1, visited, ['2', '3'])
            self.dfs_walls(row_index + 1, col_index - 1, visited, ['1', '3'])

    def all_function(self):
        self.accessible_area()
        self.search_points()
        self.cul_de_sacs()
        self.entry_exit_path()

    def accessible_area(self):
        self.entry_exit_paths = []
        self.accessible_area = 0
        self.visited_gate = []

        for gate in self.gate_positions:
            if gate in self.visited_gate:
                continue
            self.accessible_area += 1

            first_point = None
            if gate[0] == -1:
                first_point = (0, gate[1])
            elif gate[1] == -1:
                first_point = (gate[0], 0)
            elif gate[0] == len(self.grid) - 1:
                first_point = (gate[0]-1, gate[1])
            elif gate[1] == len(self.grid[0]) - 1:
                first_point = (gate[0], gate[1]-1)

            current_path = [gate]
            paths = []
            exit_gates = []

            current_path_copy = []
            for point in current_path:
                current_path_copy.append(point)

            exit_gates = self.get_exit_gates(paths, first_point, current_path_copy)

            if len(exit_gates) == 1 and len(paths) == 1:
                special_path = paths[0]
                for i in range(1, len(paths)):
                    if len(paths[i]) < len(special_path):
                        special_path = paths[i]
                self.entry_exit_paths.append(special_path)

            for exit_gate in exit_gates:
                self.visited_gate.append(exit_gate)

    def search_points(self):
        for gate in self.gate_positions:
            if gate[0] == -1:
                first_point = (0, gate[1])
            if gate[1] == -1:
                first_point = (gate[0], 0)
            if gate[0] == len(self.grid) - 1:
                first_point = (gate[0]-1, gate[1])
            if gate[1] == len(self.grid[0]) - 1:
                first_point = (gate[0], gate[1]-1)

            current_path = [gate]
            self.get_exit_gates([], first_point, current_path.copy())

    def get_exit_gates(self, paths, current_point, current_path):
        if current_point in self.gate_positions and current_point != current_path[0]:
            current_path.append(current_point)
            path_copy = []
            for point in current_path:
                path_copy.append(point)
            paths.append(path_copy)
            return [current_point]

        current_path.append(current_point)
        self.searched_point.add(current_point)
        neighbors = self.neighbors(current_point)

        exit_gates = []
        for next_point in neighbors:
            if next_point in self.searched_point or next_point in current_path:
                continue

            current_path_copy = []
            for point in current_path:
                current_path_copy.append(point)

            next_exit_gates = self.get_exit_gates(paths, next_point, current_path_copy)

            for gate in next_exit_gates:
                gate_exists = False
                for exit_gate in exit_gates:
                    if gate == exit_gate:
                        gate_exists = True
                        break
                if not gate_exists:
                    exit_gates.append(gate)

        return exit_gates

    def neighbors(self, current_point):
        available_directions = self.point_direction[current_point[0]][current_point[1]]
        neighbors = []

        for direc_index in range(4):
            if available_directions[direc_index] == 1 and direc_index == 0:
                neighbor = (current_point[0] - 1, current_point[1])
                neighbors.append(neighbor)

            if available_directions[direc_index] == 1 and direc_index == 1:
                neighbor = (current_point[0] + 1, current_point[1])
                neighbors.append(neighbor)

            if available_directions[direc_index] == 1 and direc_index == 2:
                neighbor = (current_point[0], current_point[1] - 1)
                neighbors.append(neighbor)

            if available_directions[direc_index] == 1 and direc_index == 3:
                neighbor = (current_point[0], current_point[1] + 1)
                neighbors.append(neighbor)

        return neighbors

    def cul_de_sacs(self):
        self.cul_de_sacs_counts = 0
        self.cul_de_sacs_axis = []
        self.test_direction = []

        for row in range(len(self.grid) - 1):
            test_line = []
            for col in range(len(self.grid[0]) - 1):
                direction = []
                for d in self.point_direction[row][col]:
                    direction.append(d)
                test_line.append(direction)

                direc_count = 0
                for d in self.point_direction[row][col]:
                    if d == 0:
                        direc_count += 1

                if direc_count == 3:
                    self.cul_de_sacs_counts += 1
                    self.cul_de_sacs_axis.append((row, col))

            self.test_direction.append(test_line)

        while True:
            for point in self.cul_de_sacs_axis:
                point_direc = self.test_direction[point[0]][point[1]]
                if point_direc.count(0) == 4:
                    continue

                index = point_direc.index(1)
                if index == 0:
                    next_row = point[0] - 1
                    next_col = point[1]
                    next_index = 1

                if index == 1:
                    next_row = point[0] + 1
                    next_col = point[1]
                    next_index = 0

                if index == 2:
                    next_row = point[0]
                    next_col = point[1] - 1
                    next_index = 3

                if index == 3:
                    next_row = point[0]
                    next_col = point[1] + 1
                    next_index = 2

                if (next_row, next_col) in self.gate_positions:
                    continue
                self.test_direction[point[0]][point[1]][index] = 0
                self.test_direction[next_row][next_col][next_index] = 0

            new_points = []

            for point in self.searched_point:
                if point not in self.cul_de_sacs_axis:
                    if self.test_direction[point[0]][point[1]].count(0) == 3:
                        new_points.append(point)

            if len(new_points) > 0:
                for point in new_points:
                    self.cul_de_sacs_axis.append(point)
                    pre_direction = self.point_direction[point[0]][point[1]]
                    count_ones = 0
                    for direction in pre_direction:
                        if direction == 1:
                            count_ones += 1
                    self.cul_de_sacs_counts -= (count_ones - 2)
            else:
                break

        for point in reversed(self.cul_de_sacs_axis):
            if point not in self.searched_point:
                self.cul_de_sacs_counts -= 1
                self.cul_de_sacs_axis.remove(point)

    def entry_exit_path(self):
        self.final_entry_exit_path = []
        for path in self.entry_exit_paths:
            is_valid = True

            for point in path[1:-1]:
                count_ones = 0
                for direction in self.test_direction[point[0]][point[1]]:
                    if direction == 1:
                        count_ones += 1

                if count_ones != 2:
                    is_valid = False
                    break

            if is_valid is True:
                self.final_entry_exit_path.append(path)

    def point_direction(self):
        points_direction = []
        for x in range(len(self.grid) - 1):
            row_direction = []
            for y in range(len(self.grid[0]) - 1):
                up, down, left, right = 0, 0, 0, 0
                if self.grid[x][y + 1] not in ['2', '3']:
                    right = 1
                if self.grid[x + 1][y] not in ['1', '3']:
                    down = 1
                if self.grid[x][y] not in ['2', '3']:
                    left = 1
                if self.grid[x][y] not in ['1', '3']:
                    up = 1
                row_direction.append([up, down, left, right])
            points_direction.append(row_direction)

        self.point_direction = points_direction

    def display_features(self):
        print('Labyrinth analysis complete.')
        print(f'The labyrinth has {self.num_gate()} gate(s).')
        print(f'The labyrinth has {self.walls()} set(s) of walls that are all connected.')
        if self.inaccessible_count == 0:
            print('The labyrinth has no inaccessible inner point.')
        elif self.inaccessible_count == 1:
            print('The labyrinth has a unique inaccessible inner point.')
        else:
            print(f'The labyrinth has {self.inaccessible_count} inaccessible inner points.')
        if self.accessible_area == 0:
            print('The labyrinth has no accessible area.')
        elif self.accessible_area == 1:
            print('The labyrinth has a unique accessible area.')
        else:
            print(f'The labyrinth has {self.accessible_area} accessible areas.')
        if self.cul_de_sacs_counts == 0:
            print('The labyrinth has no accessible cul-de-sac.')
        elif self.cul_de_sacs_counts == 1:
            print('The labyrinth has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The labyrinth has {self.cul_de_sacs_counts} sets of accessible cul-de-sacs that are all connected.')
        if len(self.final_entry_exit_path) == 0:
            print('The labyrinth has no entry-exit path with no intersection not to cul-de-sacs.')
        elif len(self.final_entry_exit_path) == 1:
            print('The labyrinth has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The labyrinth has {len(self.final_entry_exit_path)} entry-exit paths with no intersections not to cul-de-sacs.')

