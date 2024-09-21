import copy

class LabyrinthError(Exception):
    pass

class Labyrinth:

    def __init__(self, file):
        self.filename = file
        self.digits = None
        self.height = 0
        self.width = 0
        self.gates = 0
        self.walls = 0
        self.inaccessible_inner_points = 0
        self.accessible_areas = 0
        self.culdesacs = 0
        self.trandtl = []
        self.entry_exit_paths = 0
        self.readfiletodigits()
        self.constructafoursquaregrid()
        self.constructanewgrid()
        self.countpillars()
        self.countgates()
        self.countwalls()
        self.countnoaccessibleareas()
        self.findaccessibleareas()
        self.countculdesacs()
        self.countentryexitpaths()

    def readfiletodigits(self):
        digits = []
        with open(self.filename) as file:
            for line in file:
                if line.isspace(): continue
                line_digits = list(''.join(line.split()))
                digits.append(line_digits)

        if not 2 < len(digits) <= 41:
            raise LabyrinthError('Incorrect input.')
        
        for line in digits:
            if not 2 < len(line) <= 31:
                raise LabyrinthError('Incorrect input.')
            
            if len(line) != len(digits[0]):
                raise LabyrinthError('Incorrect input.')
                
            for d in line:
                if not d.isdigit():
                    raise LabyrinthError('Incorrect input.')
                if int(d) not in (0, 1, 2, 3):
                    raise LabyrinthError('Incorrect input.')
                
            if int(line[-1]) in (1, 3):
                raise LabyrinthError('Input does not represent a labyrinth.')
            
        for d in digits[-1]:
            if int(d) in (2, 3):
                raise LabyrinthError('Input does not represent a labyrinth.')
            
        self.digits = digits
        self.new_digits = digits

    def constructafoursquaregrid(self):
        grid = []
        for row in self.digits:
            newrowtop = []
            newrowbottom = []
            for num in row:
                if num == '0':
                    newrowtop.extend([1, 0])
                    newrowbottom.extend([0, 0])
                elif num == '1':
                    newrowtop.extend([1, 1])
                    newrowbottom.extend([0, 0])
                elif num == '2':
                    newrowtop.extend([1, 0])
                    newrowbottom.extend([1, 0])
                elif num == '3':
                    newrowtop.extend([1, 1])
                    newrowbottom.extend([1, 0])
            grid.append(newrowtop)
            grid.append(newrowbottom)

        if grid:
            grid = grid[:-1]

        for i in range(len(grid)):
            grid[i] = grid[i][:-1]

        self.digits = grid

        self.height = len(self.digits)
        self.width = len(self.digits[0])

        # print("Foursquare Grid:")
        # for row in self.digits:
        #     print(row)

    def constructanewgrid(self):
        new_grid = []
        for row in self.new_digits:
            newrowtop = []
            newrowbottom = []
            for num in row:
                if num == '0':
                    newrowtop.extend([1, 0])
                    newrowbottom.extend([0, 0])
                elif num == '1':
                    newrowtop.extend([1, 1])
                    newrowbottom.extend([0, 0])
                elif num == '2':
                    newrowtop.extend([1, 0])
                    newrowbottom.extend([1, 0])
                elif num == '3':
                    newrowtop.extend([1, 1])
                    newrowbottom.extend([1, 0])
            new_grid.append(newrowtop)
            new_grid.append(newrowbottom)

        self.new_grid = new_grid
        self.new_grid_proto = copy.deepcopy(new_grid)
        self.trimmed_new_grid = [row[:-1] for row in new_grid[:-1]]

        # print("New Grid:")
        # for row in self.new_grid:
        #     print(row)

    def countgates(self):
        gates = []
        for row in range(self.height):
            for column in range(self.width):
                if row in (0, self.height - 1) or column in (0, self.width - 1):
                    if self.digits[row][column] == 0:
                        gates.append((row, column))
        self.gates = len(gates)

    def countpillars(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        pillars = []
        for row in range(self.height):
            for column in range(self.width):
                count = 0
                for d_r, d_c in directions:
                    nextrow, nextcolumn = row + d_r, column + d_c
                    if 0 <= nextrow < self.height and 0 <= nextcolumn < self.width:
                        if self.digits[nextrow][nextcolumn] == 1:
                            count += 1
                if count == 0:
                    pillars.append((row, column))

    def countwalls(self):
        visited = [[False] * self.width for _ in range(self.height)]
        walls = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def dfs(row, column):
            stack = [(row, column)]
            wallitems = False
            while stack:
                r, c = stack.pop()
                for d_r, d_c in directions:
                    nextrow, nextcolumn = r + d_r, c + d_c
                    if 0 <= nextrow < self.height and 0 <= nextcolumn < self.width:
                        if self.digits[nextrow][nextcolumn] == 1:
                            wallitems = True
                            if not visited[nextrow][nextcolumn]:
                                visited[nextrow][nextcolumn] = True
                                stack.append((nextrow, nextcolumn))
            return wallitems

        for row in range(self.height):
            for column in range(self.width):
                if self.digits[row][column] == 1 and not visited[row][column]:
                    visited[row][column] = True

                    if any(self.digits[row + d_r][column + d_c] == 1
                           for d_r, d_c in directions
                           if 0 <= row + d_r < self.height and 0 <= column + d_c < self.width):
                        if dfs(row, column):
                            walls += 1
        self.walls = walls

    def countnoaccessibleareas(self):
        visited = [[False] * self.width for _ in range(self.height)]
        countinaccessible = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def dfs(row, column):
            stack = [(row, column)]
            inaccessiblepoints = 0
            isclose = True

            while stack:
                r, c = stack.pop()
                for d_r, d_c in directions:
                    nextrow, nextcolumn = r + d_r, c + d_c
                    if 0 <= nextrow < self.height and 0 <= nextcolumn < self.width:
                        if self.digits[nextrow][nextcolumn] == 0 and not visited[nextrow][nextcolumn]:
                            visited[nextrow][nextcolumn] = True
                            stack.append((nextrow, nextcolumn))
                    else:
                        isclose = False

                if r % 2 == 1 and c % 2 == 1:
                    inaccessiblepoints += 1

            return inaccessiblepoints if isclose else 0

        for row in range(self.height):
            for column in range(self.width):
                if self.digits[row][column] == 0 and not visited[row][column]:
                    visited[row][column] = True
                    countinaccessible += dfs(row, column)
        self.inaccessible_inner_points = countinaccessible

    def findaccessibleareas(self):
        tran_trimmed = self.trimmed_new_grid
        height_trimmed = len(tran_trimmed)
        width_trimmed = len(tran_trimmed[0])

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        mark = 2  

        def dfs(row, column, mark):
            stack = [(row, column)]
            while stack:
                r, c = stack.pop()
                for d_r, d_c in directions:
                    nextrow, nextcolumn = r + d_r, c + d_c
                    if 0 <= nextrow < height_trimmed and 0 <= nextcolumn < width_trimmed:
                        if tran_trimmed[nextrow][nextcolumn] == 0:
                            tran_trimmed[nextrow][nextcolumn] = mark
                            stack.append((nextrow, nextcolumn))

        for j in range(width_trimmed):
            if tran_trimmed[0][j] == 0:
                tran_trimmed[0][j] = mark
                dfs(0, j, mark)
                mark += 1
            if tran_trimmed[height_trimmed - 1][j] == 0:
                tran_trimmed[height_trimmed - 1][j] = mark
                dfs(height_trimmed - 1, j, mark)
                mark += 1

        for i in range(height_trimmed):
            if tran_trimmed[i][0] == 0:
                tran_trimmed[i][0] = mark
                dfs(i, 0, mark)
                mark += 1
            if tran_trimmed[i][width_trimmed - 1] == 0:
                tran_trimmed[i][width_trimmed - 1] = mark
                dfs(i, width_trimmed - 1, mark)
                mark += 1

        self.accessible_areas = mark - 2

    def countculdesacs(self):
        tran_trimmed = self.new_grid
        height_trimmed = len(tran_trimmed)
        width_trimmed = len(tran_trimmed[0])

        for i in range(height_trimmed):
            tran_trimmed[i][width_trimmed - 1] = 2
        for j in range(width_trimmed):
            tran_trimmed[height_trimmed - 1][j] = 2

        visited = [[False] * width_trimmed for _ in range(height_trimmed)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def is_dead_end(r, c):
            count = 0
            for d_r, d_c in directions:
                nextr, nextc = r + d_r, c + d_c
                if 0 <= nextr < height_trimmed and 0 <= nextc < width_trimmed:
                    if (tran_trimmed[nextr][nextc] == 1 and not visited[nextr][nextc]) or \
                    (tran_trimmed[nextr][nextc] == 3):
                        count += 1
            return count >= 3

        def dfs_mark_dead_ends(r, c):
            stack = [(r, c)]
            visited[r][c] = True
            path = [(r, c)]

            while stack:
                r, c = stack[-1]

                found_next = False
                for d_r, d_c in directions:
                    nextr, nextc = r + d_r, c + d_c
                    if 0 <= nextr < height_trimmed and 0 <= nextc < width_trimmed:
                        if tran_trimmed[nextr][nextc] == 0 and not visited[nextr][nextc]:
                            stack.append((nextr, nextc))
                            visited[nextr][nextc] = True
                            path.append((nextr, nextc))
                            found_next = True
                            break

                if not found_next:
                    if is_dead_end(r, c):
                        tran_trimmed[r][c] = 3
                    else:
                        tran_trimmed[r][c] = 1
                    stack.pop()
                    path.pop()

        for i in range(height_trimmed):
            if tran_trimmed[i][0] == 0 and not visited[i][0]:
                dfs_mark_dead_ends(i, 0)
            if tran_trimmed[i][width_trimmed - 2] == 0 and not visited[i][width_trimmed - 2]:
                dfs_mark_dead_ends(i, width_trimmed - 2)

        for j in range(width_trimmed):
            if tran_trimmed[0][j] == 0 and not visited[0][j]:
                dfs_mark_dead_ends(0, j)
            if tran_trimmed[height_trimmed - 2][j] == 0 and not visited[height_trimmed - 2][j]:
                dfs_mark_dead_ends(height_trimmed - 2, j)

        for i in range(height_trimmed):
            for j in range(width_trimmed):
                if tran_trimmed[i][j] == 2:
                    tran_trimmed[i][j] = 1

        tran_trimmed = [[1] * (width_trimmed + 1)] + [[1] + r for r in tran_trimmed]

        # Count connected zeros (cul-de-sacs)
        height = len(tran_trimmed)
        width = len(tran_trimmed[0])
        visited = [[False] * width for _ in range(height)]
        connectedculdesacs = 0

        def counting(r, c):
            stack = [(r, c)]
            while stack:
                r, c = stack.pop()
                for d_r, d_c in directions:
                    nextr, nextc = r + d_r, c + d_c
                    if 0 <= nextr < height and 0 <= nextc < width:
                        if tran_trimmed[nextr][nextc] == 3 and not visited[nextr][nextc]:
                            visited[nextr][nextc] = True
                            stack.append((nextr, nextc))

        for r in range(height):
            for c in range(width):
                if tran_trimmed[r][c] == 3 and not visited[r][c]:
                    visited[r][c] = True
                    counting(r, c)
                    connectedculdesacs += 1

        self.culdesacs = connectedculdesacs
        return self.culdesacs


    def countentryexitpaths(self):
        tran_trimmed = [row[:] for row in self.new_grid_proto]
        height_trimmed = len(tran_trimmed)
        width_trimmed = len(tran_trimmed[0])

        for i in range(height_trimmed):
            tran_trimmed[i][width_trimmed - 1] = 2
        for j in range(width_trimmed):
            tran_trimmed[height_trimmed - 1][j] = 2

        visited = [[False] * width_trimmed for _ in range(height_trimmed)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def is_dead_end(r, c):
            count = 0
            for d_r, d_c in directions:
                nextrow, nextcolumn = r + d_r, c + d_c
                if 0 <= nextrow < height_trimmed and 0 <= nextcolumn < width_trimmed:
                    if (tran_trimmed[nextrow][nextcolumn] == 1 and not visited[nextrow][nextcolumn]) or \
                       (tran_trimmed[nextrow][nextcolumn] == 3):
                        count += 1
            return count >= 3

        def dfs(row, column):
            stack = [(row, column)]
            visited[row][column] = True
            path = [(row, column)]

            while stack:
                r, c = stack[-1]

                found_next = False
                for d_r, d_c in directions:
                    nextrow, nextcolumn = r + d_r, c + d_c
                    if 0 <= nextrow < height_trimmed and 0 <= nextcolumn < width_trimmed:
                        if tran_trimmed[nextrow][nextcolumn] == 0 and not visited[nextrow][nextcolumn]:
                            stack.append((nextrow, nextcolumn))
                            visited[nextrow][nextcolumn] = True
                            path.append((nextrow, nextcolumn))
                            found_next = True
                            break

                if not found_next:
                    if is_dead_end(r, c):
                        tran_trimmed[r][c] = 3
                    else:
                        tran_trimmed[r][c] = 4
                    stack.pop()
                    path.pop()

        # 从左边和右边的边界开始深度优先搜索
        for i in range(height_trimmed):
            if tran_trimmed[i][0] == 0 and not visited[i][0]:
                dfs(i, 0)
            if tran_trimmed[i][width_trimmed - 2] == 0 and not visited[i][width_trimmed - 2]:
                dfs(i, width_trimmed - 2)

        # 从上边和下边的边界开始深度优先搜索
        for j in range(width_trimmed):
            if tran_trimmed[0][j] == 0 and not visited[0][j]:
                dfs(0, j)
            if tran_trimmed[height_trimmed - 2][j] == 0 and not visited[height_trimmed - 2][j]:
                dfs(height_trimmed - 2, j)

        # 恢复边界
        for i in range(height_trimmed):
            for j in range(width_trimmed):
                if tran_trimmed[i][j] == 2:
                    tran_trimmed[i][j] = 1

        tran_trimmed = [[1] * (width_trimmed + 1)] + [[1] + row for row in tran_trimmed]
        self.trandtl = tran_trimmed

        height = len(self.trandtl)
        width = len(self.trandtl[0])
        visited = [[False] * width for _ in range(height)]
        count = 0

        def dfs_fours(r, c):
            stack = [(r, c)]
            connected_fours = [(r, c)]
            visited[r][c] = True
            while stack:
                cr, cc = stack.pop()
                for d_r, d_c in directions:
                    nr, nc = cr + d_r, cc + d_c
                    if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc] and self.trandtl[nr][nc] == 4:
                        visited[nr][nc] = True
                        stack.append((nr, nc))
                        connected_fours.append((nr, nc))

            return connected_fours

        def check_surrounding_fours(fours):
            for r, c in fours:
                four_count = 0
                for d_r, d_c in directions:
                    nr, nc = r + d_r, c + d_c
                    if 0 <= nr < height and 0 <= nc < width and self.trandtl[nr][nc] == 4:
                        four_count += 1
                if four_count >= 3:
                    return False
            return True

        for i in range(height - 1):
            for j in range(width - 1):
                if self.trandtl[i][j] == 4 and not visited[i][j]:
                    connected_fours = dfs_fours(i, j)
                    if check_surrounding_fours(connected_fours):
                        count += 1

        self.entry_exit_paths = count
        return self.entry_exit_paths


    def display_features(self):
        print('The labyrinth has', self.gates, 'gate' + ('s' if self.gates != 1 else '') + '.')
        if self.walls == 1:
            print('The labyrinth has walls that are all connected.')
        else:
            print('The labyrinth has', self.walls, 'set' + ('s' if self.walls != 1 else '') + ' of walls that are all connected.')
        if self.inaccessible_inner_points == 0:
            print('The labyrinth has no inaccessible inner point.')
        elif self.inaccessible_inner_points == 1:
            print('The labyrinth has a single inaccessible inner point.')
        else:
            print('The labyrinth has', self.inaccessible_inner_points, 'inaccessible inner points.')
        if self.accessible_areas == 1:
            print('The labyrinth has a unique accessible area.')
        else:
            print('The labyrinth has', self.accessible_areas, 'accessible area' + ('s' if self.accessible_areas != 1 else '') + '.')
        if self.culdesacs == 0:
            print('The labyrinth has no accessible cul-de-sac.')
        elif self.culdesacs == 1:
            print('The labyrinth has accessible cul-de-sacs that are all connected.')
        else:
            print('The labyrinth has', self.culdesacs, 'set' + ('s' if self.culdesacs != 1 else '') + ' of accessible cul-de-sacs that are all connected.')
        if self.entry_exit_paths == 0:
            print('The labyrinth has no entry-exit path with no intersection not to cul-de-sacs.')
        elif self.entry_exit_paths == 1:
            print('The labyrinth has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The labyrinth has', self.entry_exit_paths, 'entry-exit path' + ('s' if self.entry_exit_paths != 1 else '') + ' with no intersections not to cul-de-sacs.')

if __name__ == '__main__':
    labyrinth = Labyrinth('D:\COMP9021\ASS2\labyrinth_2.txt')
    labyrinth.display_features()