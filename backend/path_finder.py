import numpy as np

def closest_coordinate(curr_coordinate, target_coordinates):
    min_dist = None
    closest_coordinate = None
    for coordinate in target_coordinates:
        a = np.array(coordinate)
        b = np.array(curr_coordinate)
        dist = abs(np.linalg.norm(a - b))
        if not closest_coordinate:
            min_dist = dist
            closest_coordinate = coordinate
        else:
            if min_dist > dist:
                min_dist = dist
                closest_coordinate = coordinate
    return closest_coordinate

def path_finder_v2(a, start, end, collision_block_char):
    def make_step(m, k):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    if i > 0 and m[i-1][j] == 0 and a[i-1][j] == 0:
                        m[i-1][j] = k + 1
                    if j > 0 and m[i][j-1] == 0 and a[i][j-1] == 0:
                        m[i][j-1] = k + 1
                    if i < len(m)-1 and m[i+1][j] == 0 and a[i+1][j] == 0:
                        m[i+1][j] = k + 1
                    if j < len(m[i])-1 and m[i][j+1] == 0 and a[i][j+1] == 0:
                        m[i][j+1] = k + 1

    # Convert maze to 0 (free) and 1 (collision)
    new_maze = []
    for row in a:
        new_row = []
        for j in row:
            if j == collision_block_char:
                new_row += [1]
            else:
                new_row += [0]
        new_maze += [new_row]
    a = new_maze

    m = []
    for i in range(len(a)):
        m.append([])
        for j in range(len(a[i])):
            m[-1].append(0)
    i, j = start
    m[i][j] = 1

    k = 0
    except_handle = 150
    while m[end[0]][end[1]] == 0:
        k += 1
        make_step(m, k)
        if except_handle == 0:
            break
        except_handle -= 1

    i, j = end
    k = m[i][j]
    the_path = [(i, j)]
    while k > 1:
        if i > 0 and m[i - 1][j] == k-1:
            i, j = i-1, j
            the_path.append((i, j))
            k -= 1
        elif j > 0 and m[i][j - 1] == k-1:
            i, j = i, j-1
            the_path.append((i, j))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k-1:
            i, j = i+1, j
            the_path.append((i, j))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
            i, j = i, j+1
            the_path.append((i, j))
            k -= 1

    the_path.reverse()
    return the_path

def path_finder_3(maze, start, end, collision_block_char="#"):
    # maze: 2D list of str, start/end: (x, y)
    # Convert to (row, col) for path_finder_v2
    start_rc = (start[1], start[0])
    end_rc = (end[1], end[0])
    curr_path = path_finder_v2(maze, start_rc, end_rc, collision_block_char)
    if len(curr_path) <= 2:
        return []
    else:
        a_path = curr_path[:int(len(curr_path)/2)]
        b_path = curr_path[int(len(curr_path)/2)-1:]
        b_path.reverse()
    # Convert back to (x, y)
    a_path = [(c[1], c[0]) for c in a_path]
    b_path = [(c[1], c[0]) for c in b_path]
    return a_path, b_path

def maze_to_collision_matrix(maze_obj):
    # Returns a 2D list of "#" (collision) and "0" (free)
    mat = []
    for row in maze_obj.collision_maze:
        mat.append(["#" if cell != "0" else "0" for cell in row])
    return mat
