from collections import deque


def print_2d_graph(text, graph):
    print(text)
    for g in graph:
        print(g)
    print()


def print_dict(text, _dict):
    print(text)
    for k, v in _dict.items():
        print(f'{k} : {v}')
    print()


def check_movable(r, c, direction):
    """
    Args
        r   : 정령의 행번호
        c   : 정령의 열번호
        direction   : 이동 방향.
            1 : 동
            2 : 남
            3 : 서
    """
    # 남쪽 이동 가능한지 확인
    if direction == 2:
        # 벽에 닿았는지 확인.
        if r >= R + 1:
            return False
        # 숲에 다른 골렘이 있는지 확인
        if forest[r + 1][c - 1] != 0 or forest[r + 2][c] != 0 or forest[r + 1][c + 1] != 0:
            return False
    # 서쪽 이동 가능한지 확인
    elif direction == 3:
        # 벽에 닿았는지 확인.
        if c <= 2:
            return False
        # 숲에 다른 골렘이 있는지 확인.
        if forest[r - 1][c - 1] != 0 or forest[r][c - 2] != 0 or forest[r + 1][c - 1] != 0:
            return False
    # 동쪽 이동 가능한지 확인
    elif direction == 1:
        if c >= C - 1:
            return False
        if forest[r - 1][c + 1] != 0 or forest[r][c + 2] != 0 or forest[r + 1][c + 1] != 0:
            return False
    return True


def move_golem_and_update_forest(i, direction):
    """
    Args
        i : 골렘 번호
        direction   : 이동 방향.
            1 : 동
            2 : 남
            3 : 서
    """
    global golem_coord, forest
    # 골렘의 현재 좌표
    r, c = golem_coord[i]
    # 남쪽 이동
    if direction == 2:
        # 골렘 좌표 이동
        golem_coord[i] = [r + 1, c]
        # 숲 업데이트
        forest[r - 1][c] = forest[r][c - 1] = forest[r][c + 1] = 0
        forest[r][c] = forest[r + 1][c - 1] = forest[r + 1][c] = forest[r + 1][c + 1] = forest[r + 2][c] = 1
    # 서쪽 이동
    elif direction == 3:
        golem_coord[i] = [r, c - 1]
        forest[r - 1][c] = forest[r][c + 1] = forest[r + 1][c] = 0
        forest[r][c] = forest[r - 1][c - 1] = forest[r][c - 1] = forest[r + 1][c - 1] = forest[r][c - 2] = 1
        # 골렘 출구 업데이트 (반시계)
        golem_exit[i] = (golem_exit[i] + 3) % 4
    # 동쪽 이동
    elif direction == 1:
        golem_coord[i] = [r, c + 1]
        forest[r][c - 1] = forest[r - 1][c] = forest[r + 1][c] = 0
        forest[r][c] = forest[r - 1][c + 1] = forest[r][c + 1] = forest[r + 1][c + 1] = forest[r][c + 2] = 1
        # 골렘 출구 업데이트 (시계)
        golem_exit[i] = (golem_exit[i] + 1) % 4


def is_outside_forest(r):
    if r <= 3:
        return True
    return False


def clear_forest():
    global forest, golem_coord
    forest = [[0] * (C + 1) for _ in range(R + 3)]  # 행 0,1,2는 사용하지 않음. 열 0은 사용하지 않음.
    golem_coord = {k: [1, start_list[k][0]] for k in range(K)}


def move_fairy(i):
    exit_graph = [[0] * (C + 1) for _ in range(R + 3)]
    for idx, [_r, _c] in golem_coord.items():
        if _r <= 3:
            continue
        exit_graph[_r][_c] = exit_graph[_r-1][_c] = exit_graph[_r+1][_c] = exit_graph[_r][_c-1] = exit_graph[_r][_c+1] = idx + 1
        if golem_exit[idx] == 0:
            exit_graph[_r - 1][_c] *= -1
        elif golem_exit[idx] == 1:
            exit_graph[_r][_c + 1] *= -1
        elif golem_exit[idx] == 2:
            exit_graph[_r + 1][_c] *= -1
        elif golem_exit[idx] == 3:
            exit_graph[_r][_c - 1] *= -1

    visit = [[False] * (C+1) for _ in range(R+3)]
    sr, sc = golem_coord[i]
    cand = [sr]
    q = deque()
    q.append((sr, sc, i+1))
    visit[sr][sc] = True
    while q:
        cr, cc, idx = q.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            nr = cr + dr
            nc = cc + dc
            # 같은 골렘 내부 이동.
            if nr < 3 or nr >= R+3 or nc < 1 or nc > C or visit[nr][nc] or exit_graph[nr][nc] == 0:
                continue
            if abs(exit_graph[nr][nc]) == idx or (exit_graph[cr][cc] < 0 and abs(exit_graph[nr][nc]) != idx):
                q.append((nr, nc, abs(exit_graph[nr][nc])))
                visit[nr][nc] = True
                cand.append(nr)


    # print_2d_graph("visit", visit)
    # print_2d_graph("exit_graph", exit_graph)
    # print("candidate", cand, "res", max(cand)-3)
    return max(cand)-2

def update_result(res):
    global result
    result += res


"""
1. 남쪽으로 이동 가능한지 확인.
    1-1. 가능하면) 골렘 이동
    1-2. 불가능하면) 골렘이 숲 밖으로 빠져나와있는지 확인
        1-2-1. 빠져나왔으면) 모든 골렘 숲 밖으로 제거.
        1-2-2. 아니면) 2번으로 이동.
2. 서쪽으로 이동 가능한지 확인.
    2-1. 가능하면) 골렘 이동 & 출구 회전
    2-2. 불가능하면) 3번.
3. 동쪽으로 이동 가능한지 확인.
    3-1. 가능하면) 골렘 이동 & 출구 회전
    3-3. 불가능하면) 4번.
4. 현재 골렘에서 최남단 행 번호와 출구에 인접한 골렘이 있다면 해당 골렘의 최남단 행 번호 비교.
    -> DFS, BFS 필요할듯?
5. 다음 골렘 시작.
    5-1) 모든 골렘이 다 돌았으면 6번으로.
    5-2) 모든 골렘이 다 돌지 않았으면 1번으로.
6. 


R=6
X 0
X 1
X 2
1 3
2 4
3 5
4 6
5 7
6 8 = R+2
"""

R, C, K = map(int, input().split())
start_list = [list(map(int, input().split())) for _ in range(K)]  # c, d

# 골렘이 있으면 1, 없으면 0
forest = [[0] * (C + 1) for _ in range(R + 3)]  # 행 0,1,2는 사용하지 않음. 열 0은 사용하지 않음.
# 정령의 좌표. (행 r, 열 c)
golem_coord = {k: [1, start_list[k][0]] for k in range(K)}
# 골렘의 출구.  # 0: 북 // 1: 동 // 2: 남 // 3: 서
golem_exit = {k: start_list[k][1] for k in range(K)}
# 결과
result = 0

# print_2d_graph('start_list:', start_list)
# print_2d_graph('forest:', forest)
# print_dict('golem_coord:', golem_coord)
# print_dict('golem_exit:', golem_exit)

for i in range(K):
    movable = True
    ## 어디로든 이동 가능한 경우 계속 반복.
    while movable:
        r, c = golem_coord[i]
        ## 최남단에 도착하면 정지 후 다음 골렘 이동.
        if r >= R + 1:
            movable = False
            ## 정령 최남단 이동 (DFS 필요)
            res = move_fairy(i)
            ## 결과 업데이트 (행 번호 누적)
            update_result(res)
        ## 남쪽 이동 가능한지 확인.
        elif check_movable(r, c, 2):
            ## 골렘 좌표, 출구, 숲 상황 업데이트
            move_golem_and_update_forest(i, 2)
        ## 서쪽으로 이동한 다음에 남쪽으로 갈 수 있어야 함.
        elif check_movable(r, c, 3):
            ## 골렘 좌표, 출구, 숲 상황 업데이트
            move_golem_and_update_forest(i, 3)
            if not check_movable(r, c - 1, 2):
                move_golem_and_update_forest(i, 1)
                movable = False
                ## 정령 최남단 이동 (DFS 필요)
                res = move_fairy(i)
                ## 결과 업데이트 (행 번호 누적)
                update_result(res)
        ## 동쪽으로 이동한 다음에 남쪽으로 갈 수 있어야 함.
        elif check_movable(r, c, 1):
            ## 골렘 좌표, 출구, 숲 상황 업데이트
            move_golem_and_update_forest(i, 1)
            if not check_movable(r, c + 1, 2):
                move_golem_and_update_forest(i, 3)
                movable = False
                ## 정령 최남단 이동 (DFS 필요)
                res = move_fairy(i)
                ## 결과 업데이트 (행 번호 누적)
                update_result(res)

        ## 아무곳도 이동 불가능한 상황.
        else:
            ## 숲 밖으로 빠져나왔는지 확인.
            if is_outside_forest(r):
                ## 모든 골렘 빼내기.
                clear_forest()
                ## 다음 골렘부터 다시 시작
                movable = False
            else:
                ## 이동 중단.
                movable = False
                ## 정령 최남단 이동 (DFS 필요)
                res = move_fairy(i)
                ## 결과 업데이트 (행 번호 누적)
                update_result(res)

print(result)