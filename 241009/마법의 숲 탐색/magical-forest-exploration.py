from collections import deque

def print_2d_graph(text="", graph: list=[[None]]):
    print(text)
    for g in graph:
        print(g)
    print()

def print_dict(text="", _dict={None: None}):
    print(text)
    for k, v in _dict.items():
        print(f'{k}: {v}')
    print()


R, C, K = map(int, input().split())
forest = [[0] * (C+1) for _ in range(R+1)]  # 0행, 0열은 사용하지 않음.

golem_info = [list(map(int, input().split())) for _ in range(K)]
golem_dict = {k: golem_info[k-1] for k in range(1, K+1)}

start_list = [[-1, golem_info[i][0]] for i in range(K)] # [R, C]
start_dict = {k: start_list[k-1] for k in range(1, K+1)}

exit_list = [golem_info[i][1] for i in range(K)] # 방향
exit_dict = {k: exit_list[k-1] for k in range(1, K+1)}

# print_2d_graph('forest', forest)
# print_dict('start', start_dict)
# print_dict('exit', exit_dict)

result = 0

def check_movable(r, c):
    global forest
    if r > R or c < 1 or c > C:
        return False
    if r >= 1 and forest[r][c] != 0:
        return False
    return True

def check_direction(r, c, dir):
    if dir == 2:
        return check_movable(r+1, c-1) and check_movable(r+2, c) and check_movable(r+1, c+1)
    elif dir == 3:
        return check_movable(r-1, c-1) and check_movable(r, c-2) and check_movable(r+1, c-1)
    elif dir == 1:
        return check_movable(r-1, c+1) and check_movable(r, c+2) and check_movable(r+1, c+1)
    else:
        return False

def move_golem(idx, r, c, dir):
    if r <= 0:
        return
    global forest
    if dir == 1:  # 동
        forest[r-1][c] = forest[r+1][c] = forest[r][c-1] = 0
        forest[r][c] = forest[r][c+1] = forest[r-1][c+1] = forest[r][c+2] = forest[r+1][c+1] = idx
        update_exit(idx, r, c+1, dir)
    elif dir == 2:  # 남
        forest[r-1][c] = forest[r][c-1] = forest[r][c+1] = 0
        forest[r][c] = forest[r+1][c] = forest[r+1][c-1] = forest[r+2][c] = forest[r+1][c+1] = idx
        update_exit(idx, r+1, c, dir)
    elif dir == 3:  # 서
        forest[r-1][c] = forest[r][c+1] = forest[r+1][c] = 0
        forest[r][c] = forest[r][c-1] = forest[r-1][c-1] = forest[r][c-2] = forest[r+1][c-1] = idx
        update_exit(idx, r, c-1, dir)


def update_exit(idx, r, c, dir):
    global forest
    cur_exit = exit_dict[idx]
    if dir == 1:  # 동쪽 = 시계
        cur_exit = (cur_exit + 1) % 4
    elif dir == 3:  # 서쪽 = 반시계
        cur_exit = (cur_exit + 3) % 4
    exit_dict[idx] = cur_exit

    if cur_exit == 0:  # 북
        forest[r-1][c] = -idx
    elif cur_exit == 1:  # 동
        forest[r][c+1] = -idx
    elif cur_exit == 2:  # 남
        forest[r+1][c] = -idx
    elif cur_exit == 3:  # 서
        forest[r][c-1] = -idx


def inForest(r):
    if r <= 1:
        return False
    return True

def clear_forest():
    global forest
    forest = [[0] * (C+1) for _ in range(R+1)]  # 0행, 0열은 사용하지 않음.

def move_fairy(idx, r, c):
    global forest
    visit = [[False] * (C+1) for _ in range(R+1)]
    q = deque()
    cand = []
    q.append((r, c, idx))
    visit[r][c] = True
    cand.append(r)
    while q:
        cr, cc, cidx = q.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            nr = cr + dr
            nc = cc + dc
            if nr < 1 or nr > R or nc < 1 or nc > C or visit[nr][nc] or forest[nr][nc] == 0:
                continue
            if abs(forest[nr][nc]) == cidx or (forest[cr][cc] < 0 and abs(forest[nr][nc]) != cidx):
                q.append((nr, nc, abs(forest[nr][nc])))
                visit[nr][nc] = True
                cand.append(nr)
    res = max(cand)
    update_result(res)

def update_result(res):
    global result
    result += res


for idx, [r, c] in start_dict.items():
    while True:
        # 남쪽 이동
        if check_direction(r, c, 2):
            move_golem(idx, r, c, 2)
            r += 1
        # 서쪽 이동시, 남쪽으로도 이동할 수 있어야함.
        elif check_direction(r, c, 3) and check_movable(r+1, c-2) and check_movable(r+2, c-1):
            move_golem(idx, r, c, 3)
            c -= 1
            # 골렘 출구 업데이트
        # 동쪽
        elif check_direction(r, c, 1) and check_movable(r+2, c+1) and check_movable(r+1, c+2):
            # print_2d_graph("move right, forest", forest)
            move_golem(idx, r, c, 1)
            c += 1
            # 골렘 출구 업데이트
        # 움직임 종료
        else:
            # 숲 밖을 벗어났는지 확인
            if not inForest(r):
                clear_forest()
            # 정령 이동
            else:
                move_fairy(idx, r, c)
            break
        # print_2d_graph("forest", forest)
print(result)