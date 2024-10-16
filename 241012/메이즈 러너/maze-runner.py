import copy
from collections import deque

DEBUG=True
DEBUG=False

def print_2d_graph(text="", graph=[]):
    if DEBUG:
        print(text)
        for g in graph:
            print(g)
        print()

def print_3d_graph(text="", graph=[], idx=0):
    if DEBUG:
        print(text)
        for gr in graph:
            for g in gr:
                print(g[idx], end=' ')
            print()
        print()

def print_dict(text="", _dict={}):
    if DEBUG:
        print(text)
        for k, v in _dict.items():
            print(f'{k}: {v}')
        print()

def print_debug(*args):
    if DEBUG:
        for a in args:
            print(a)
        print()

def get_distance(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)

def in_board(r, c):
    global N
    if r <= 0 or r > N or c <= 0 or c > N:
        return False
    return True

def check_wall(r, c):
    """ 벽이 없으면 True, 벽이나 출구가 있으면 False"""
    global board, N
    if in_board(r, c) and board[r][c][0] <= 0:
        return True
    return False

def get_direction(r, c):
    """ (r, c) 위치에서 출구까지의 최단 거리가 가장 가까운 방향 리턴"""
    global exit
    er, ec = exit
    dist = get_distance(er, ec, r, c)
    ret = [0, 0]
    for dr, dc in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
        nr = r + dr
        nc = c + dc
        # 맵 밖을 벗어나거나 벽이 있으면 움직이지 않음.
        if not in_board(nr, nc) or not check_wall(nr, nc):
            continue
        cur_dist = get_distance(er, ec, nr, nc)
        if cur_dist < dist:
            dist = cur_dist
            ret = [dr, dc]
    return ret

def update_coords():
    global coords, action
    coords = []
    for r in range(1, N+1):
        for c in range(1, N+1):
            if board[r][c][1] != 0:
                coords.append([r, c])
    coords.sort(key=lambda x: x[1])
    coords.sort(key=lambda x: x[0])
    action = [[0] * (N + 1) for _ in range(N + 1)]

def move_person(idx, r, c, dr, dc):
    global board, coords, result, exit, action
    if (dr == 0 and dc == 0) or not in_board(r+dr, c+dc) or not check_wall(r+dr, c+dc):
        return
    if r+dr == exit[0] and c+dc == exit[1]:
        # coords[idx] = [0, 0]
        result += board[r][c][1]
        board[r][c][1] = 0
        return
    action[r+dr][c+dc] += board[r][c][1]
    result += board[r][c][1]
    board[r][c][1] = 0
    return

def get_bbox():
    global board, alive, exit, coords, N
    er, ec = exit
    dist = 999999
    bbox = [9999, 9999, 9999, 9999]
    for idx, coord in enumerate(coords):
        ir, ic = coord
        # 출구와 이 참가자 사이의 정사각형 한 변의 길이.
        length = max(abs(er-ir), abs(ec-ic))
        if length > dist:
            continue
        # 가장 작은 크기 정사각형 2개 이상 -> r, c 따라 우선순위.
        if ir <= er:
            ltr = er - length
            rbr = er
            if ltr <= 0:
                ltr = 1
                rbr = ltr + length
        else:
            ltr = ir - length
            rbr = ir
            if ltr <= 0:
                ltr = 1
                rbr = ltr + length
        if ic <= ec:
            ltc = ec - length
            rbc = ec
            if ltc <= 0:
                ltc = 1
                rbc = ltc + length
        else:
            ltc = ic - length
            rbc = ic
            if ltc <= 0:
                ltc = 1
                rbc = ltc + length
        if length < dist:
            dist = length
            bbox = [ltr, ltc, rbr, rbc]
        elif ltr < bbox[0]:
            bbox = [ltr, ltc, rbr, rbc]
        elif ltr == bbox[0] and ltc < bbox[1]:
            bbox = [ltr, ltc, rbr, rbc]

    return bbox

def rotate_board(r1, c1, r2, c2):
    global board, alive, exit, people
    er, ec = exit
    assert r2-r1 == c2-c1, ValueError(f"r1: {r1}, r2: {r2}, c1: {c1}, c2: {c2}")
    length = r2 - r1 + 1

    target0 = [[0] * length for _ in range(length)]
    target1 = [[0] * length for _ in range(length)]

    """
    1 2 3
    4 5 6
    7 8 9
    
    7 4 1
    8 5 2
    9 6 3
    """
    for r in range(length):
        for c in range(length):
            target0[c][length-r-1] = board[r1+r][c1+c][0]
            target1[c][length-r-1] = board[r1+r][c1+c][1]

    print_2d_graph('target0', target0)
    print_2d_graph('target1', target1)

    for r in range(length):
        for c in range(length):
            num0 = target0[r][c]
            num1 = target1[r][c]
            if num0 > 0:
                num0 -= 1
            elif num0 == -1:
                exit = [r1+r, c1+c]
            board[r1+r][c1+c][0] = num0
            board[r1+r][c1+c][1] = target1[r][c]



N, M, K = map(int, input().split())
# [r][c][0] : 벽 내구도, [r][c][1] : 사람 수
board = [[[0] * 2 for _ in range(N+1)] for _ in range(N+1)]
alive = {k: True for k in range(1, M+1)}
result = 0

miro = [list(map(int, input().split())) for _ in range(N)]
coords = [list(map(int, input().split())) for _ in range(M)]
exit = list(map(int, input().split()))
action = [[0] * (N+1) for _ in range(N+1)]
people = {}
for r in range(1, N+1):
    for c in range(1, N+1):
        board[r][c][0] = miro[r-1][c-1]

for i, c in enumerate(coords):
    cr, cc = c
    board[cr][cc][1] += 1

# board, alive, exit, coords, result, action 사용.

board[exit[0]][exit[1]][0] = -1
print_3d_graph('board0', board, 0)
print_3d_graph('board1', board, 1)
print_dict('people', people)
print_debug('exit', exit)

flag = True
# K초동안 진행.
for k in range(K):
    # 모든 참가자 이동.
    update_coords()
    if len(coords) == 0:
        print(result)
        print(exit[0], exit[1])
        flag=False
        break
    for idx, coord in enumerate(coords):
        # 현재 참가자 좌표
        cr, cc = coord
        # 현재 참가자에서 출구까지 최단거리가 가장 가까운 방향.
        dir = get_direction(cr, cc)
        move_person(idx, cr, cc, *dir)
        # print_3d_graph(f'[Time {k}, idx {idx}] board', board)
        print_debug(f'[Time {k}, idx {idx}, cr: {cr}, cc: {cc}, dir {dir}] coords', coords)
    for r in range(1, N+1):
        for c in range(1, N+1):
            if action[r][c] != 0:
                board[r][c][1] += action[r][c]

    update_coords()
    if len(coords) == 0:
        print(result)
        print(exit[0], exit[1])
        flag=False
        break
    # 보드 회전 좌표 획득
    bbox = get_bbox()
    print_debug(f'[Time {k}] bbox', bbox)
    # 보드 회전
    print_3d_graph(f'[Time {k}] before rotation board 0', board, 0)
    print_3d_graph(f'[Time {k}] before rotation board 1', board, 1)
    rotate_board(*bbox)
    print_3d_graph(f'[Time {k}] after rotation board 0', board, 0)
    print_3d_graph(f'[Time {k}] after rotation board 1', board, 1)
    print_debug(f'[Time {k} Done. ]. result: {result}, exit: {exit}, coords: {coords}')

if flag:
    print(result)
    print(exit[0], exit[1])