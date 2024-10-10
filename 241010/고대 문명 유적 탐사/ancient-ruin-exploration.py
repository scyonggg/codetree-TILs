from collections import deque
import copy

DEBUG=False
def print_2d_graph(text, graph):
    if DEBUG:
        print(text)
        for g in graph:
            print(g)
        print()


def print_dict(text, _dict):
    if DEBUG:
        print(text)
        for k, v in _dict.items():
            print(f'{k}: {v}')
        print()

# def rotate_90(src):
#     dest = [[0] * len(src[0]) for _ in range(len(src))]
#     for i in range(len(src)):
#         for j in range(len(src[0])):
#             dest[j][-i-1] = src[i][j]
#     return dest

def rotate_90(src, r, c):
    palette = [[0] * 3 for _ in range(3)]
    dest = copy.deepcopy(src)
    tmp = [dest[i][c-1: c+2] for i in range(r-1, r+2)]

    for i in range(len(tmp)):
        for j in range(len(tmp[0])):
            palette[j][-i-1] = tmp[i][j]

    for ii, i in enumerate(range(r-1, r+2)):
        for jj, j in enumerate(range(c-1, c+2)):
            dest[i][j] = palette[ii][jj]

    return dest

def rotate_180(src, r, c):
    palette = [[0] * 3 for _ in range(3)]
    dest = copy.deepcopy(src)
    tmp = [dest[i][c-1: c+2] for i in range(r-1, r+2)]

    for i in range(len(tmp)):
        for j in range(len(tmp[0])):
            palette[-i-1][-j-1] = tmp[i][j]

    for ii, i in enumerate(range(r-1, r+2)):
        for jj, j in enumerate(range(c-1, c+2)):
            dest[i][j] = palette[ii][jj]
    return dest

def rotate_270(src, r, c):
    palette = [[0] * 3 for _ in range(3)]
    dest = copy.deepcopy(src)
    tmp = [dest[i][c-1: c+2] for i in range(r-1, r+2)]

    for i in range(len(tmp)):
        for j in range(len(tmp[0])):
            palette[-j-1][i] = tmp[i][j]

    for ii, i in enumerate(range(r-1, r+2)):
        for jj, j in enumerate(range(c-1, c+2)):
            dest[i][j] = palette[ii][jj]
    return dest

K, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(5)]
nums = list(map(int, input().split()))

print_2d_graph("graph", graph)
"""
1. 유물 탐사 시작.
그래프는 0~4행, 0~4열로 가정.
3x3 회전 가능한 중심 = (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)으로 총 9개.
9개에 대해 각각 90, 180, 270도 회전한 유물조각 계산. = 27개 후보.

2. 유물 획득
    2-1. 유물 가치 계산.
        27개 후보들에 대해 모두 유물 가치 계산. 
        유물 가치 계산은 BFS로.
        우선순위에 따라 dict나 list에 저장.
        우선순위:
        1) 유물 가치 최대
        2) 회전 각도 최소
        3) 가장 작은 열, 가장 작은 행 선택.
    2-2. 유물 획득 및 새로 채우기
        우선 순위 가장 큰 후보에서 유물 획득 후, 해당 유물 제거.
        우선순위에 따라 추가 후보들을 nums에서 가져옴.
        우선순위:
        1) 가장 작은 열.
        2) 가장 큰 열.
        2-2-1. 유물 가치 계산이 추가로 가능할 경우, 가치 계산 및 2-3 반복.
        2-2-2. 유물 가치 계산이 안될경우, 1번으로 돌아가기. (회전하는 것부터)
"""

def rotate_cand(graph):
    """
    행 방향 (세로) = x, 열 방향 (가로) = y
    (1,1), ..., (3,3)의 9개에 대해 각각 90, 180, 270도 회전시킨 유물 조각 계산.
    """
    cand = []
    for idx, (c, r) in enumerate([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]):
        idx_90 = rotate_90(graph, r, c)
        cand.append(idx_90)

    for idx, (c, r) in enumerate([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]):
        idx_180 = rotate_180(graph, r, c)
        cand.append(idx_180)

    for idx, (c, r) in enumerate([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]):
        idx_270 = rotate_270(graph, r, c)
        cand.append(idx_270)


    # for _ in cand:
    #     print_2d_graph("_", _)

    return cand


def cal_value(rotated_graph):
    visit = [[0] * len(rotated_graph[0]) for _ in range(len(rotated_graph))]
    cand_list = []
    cnt = 0
    ret_path = []

    def bfs(_graph, _x, _y):  # x : 열, y : 행
        nonlocal visit
        global result
        q = deque()
        path = [[_x, _y]]  # 연결된 유물 좌표 기록.
        length = 1  # 연결된 유물의 개수
        q.append((_x, _y, 1))
        visit[_y][_x] = 1
        while q:
            cx, cy, num = q.popleft()
            for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                nx = cx + dx
                ny = cy + dy
                if nx < 0 or nx >= 5 or ny < 0 or ny >= 5 or visit[ny][nx] != 0:
                    continue
                if _graph[ny][nx] == _graph[cy][cx]:
                    q.append([nx, ny, num + 1])
                    visit[ny][nx] = 1
                    path.append([nx, ny])
                    length += 1
        # 연결된 유물의 개수를 visit 배열에 업데이트
        for i, j in path:
            visit[j][i] = length

        # 지나온 좌표 반환
        # if length >= 3:
        return path

    for i in range(5):
        for j in range(5):
            if visit[j][i] == 0:
                _path = bfs(rotated_graph, i, j)
                # 지나온 길이 1개 or 2개일 경우 = 아무것도 연결되지 않음.
                if len(_path) <= 2:
                    continue
                # 지나온 길이 3개 이상 = 총합 업데이트, 경로 반환. (벽면 업데이트 위해서)
                if len(_path) >= 3:
                    cnt += len(_path)
                    ret_path.extend(_path)

    # 유물 3개 이상 연결되지 않음.
    if len(ret_path) == 0:
        # 연결된 유물이 아무것도 없음. -> 턴 상관없이 전체 종료.
        global flag
        flag = False

    print_2d_graph("rotated_graph", rotated_graph)
    print_2d_graph(f"cnt: {cnt}, visit", visit)

    return cnt, ret_path

result = []
for k in range(K):
    # 27개 후보 회전.
    cands = rotate_cand(graph)
    cnt = 0
    # 27개 후보 각각 유물 가치 계산
    max_len = 0
    max_idx = 0
    max_path = []
    for idx, cand in enumerate(cands):
        cand_len, cand_path = cal_value(cand)
        if cand_len > max_len:
            max_idx = idx
            max_len = cand_len
            max_path = cand_path
    if max_len == 0:
        break
    max_path.sort(key=lambda x: x[1], reverse=True)
    max_path.sort(key=lambda x: x[0])
    # 유물 가치 업데이트.
    cnt += max_len
    # 27개 후보 중 가장 높은 유물 가치 선택.
    graph = cands[max_idx]
    while True:
        # 벽면에 써있는 숫자 업데이트
        print_2d_graph("Before updated graph", graph)
        for idx, (px, py) in enumerate(max_path):
            graph[py][px] = nums.pop(0)
        print_2d_graph("After updated graph", graph)
        # 업데이트된 유적에서 유물 가치 계산.
        cand_len, cand_path = cal_value(graph)
        # Case 1. 유물이 단 하나도 없을 때. (조각 연결 길이가 1~2일 때)
        if cand_len == 0:
            result.append(cnt)
            flag = False
            break
        # Case 2. 유물이 3개 이상 연결은 되었을 때.
        cand_path.sort(key=lambda x: x[1], reverse=True)
        cand_path.sort(key=lambda x: x[0])
        if cand_len < 3:
            result.append(cnt)
            break
        cnt += cand_len
        max_path = cand_path


for res in result:
    print(res, end=" ")