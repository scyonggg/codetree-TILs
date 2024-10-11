from collections import deque

DEBUG=True
DEBUG=False

def print_debug(*args):
    if DEBUG:
        for a in args:
            print(a)
        print()

def print_2d_graph(text="", graph=[]):
    if DEBUG:
        print(text)
        for g in graph:
            print(g)
        print()

def print_dict(text='', _dict={}):
    if DEBUG:
        print(text)
        for k, v in _dict.items():
            print(f'{k}: {v}')
        print()

def in_board(r, c, h, w):
    if r <= 0 or r+h-1 > L or c <= 0 or c+w-1 > L:
        return False
    return True

def is_wall(r, c, h, w):
    if not in_board(r, c, h, w):
        return False
    flag = True
    for i in range(r, r+h):
        for j in range(c, c+w):
            if board[i][j] == 2:
                flag = False
                break
    return flag

def overlapped_knights(i, r, c, h, w):
    """r, c, h, w의 조건을 갖는 i번 기사가 다른 기사들과 겹치는지 확인."""
    others = []
    for x in range(r, r+h):
        for y in range(c, c+w):
            # i번이 아닌 기사가 있으면, 해당 기사 번호를 저장.
            if knights[x][y] != 0 and knights[x][y] != i:
                others.append(knights[x][y])

    return list(set(others))

def is_movable(i, d):
    """ i번 기사가 d 방향으로 이동가능한지 확인"""
    # i번 기사가 d 방향으로 움직일 수 있는지 확인. (벽이 있는지, 범위를 벗어나지 않는지)
    r, c, h, w, k = knight_dict[i]  # i번 기사의 정보
    if d == 0:  # 위쪽
        return in_board(r-1, c, h, w) and is_wall(r, c, h, w)
    elif d == 1:  # 오른쪽
        return in_board(r, c+1, h, w) and is_wall(r, c+1, h, w)
    elif d == 2:  # 아래쪽
        return in_board(r+1, c, h, w) and is_wall(r+1, c, h, w)
    elif d == 3:  # 왼쪽
        return in_board(r, c-1, h, w) and is_wall(r, c-1, h, w)
    else:
        raise ValueError(f"Wrong d {d} given. i: {i}, knight : {knight_dict[i]}")

def cal_damage():
    pass

def clear_knight(i):
    """ knights 에서 i번째 기사를 제거"""
    global knights
    for x in range(L+1):
        for y in range(L+1):
            if knights[x][y] == i:
                knights[x][y] = 0

def move_knight(i, d, first=False):
    # 명령을 받은 기사는 아니고, 밀려나는 기사로 가정.
    r, c, h, w, k = knight_dict[i]
    if d == 0:
        r -= 1
    elif d == 1:
        c += 1
    elif d == 2:
        r += 1
    elif d == 3:
        c -= 1

    if not is_movable(i, d):  # 밀려날 위치가 경기장을 벗어나거나, 벽이 있음.
        return False
    overlap = overlapped_knights(i, r, c, h, w)  # 겹치는 기사들에게 다시 이동 명령을 보내야함.
    movable = True
    if len(overlap) != 0:
        for over in overlap:
            movable = move_knight(over, d)
            if not movable:  # 움직일 수 없는 기사가 있으면 즉시 중단.
                return False

    # 계산된 데미지 및 위치 업데이트.
    clear_knight(i)
    for x in range(r, r+h):
        for y in range(c, c+w):
            if not first and board[x][y] == 1:  # 함정 수 만큼 데미지 계산.
                k -= 1
            knights[x][y] = i
    if k <= 0:
        clear_knight(i)
        alive[i] = False
        knight_dict[i] = [0, 0, 0, 0, k]
        return True

    knight_dict[i] = [r, c, h, w, k]
    return True

"""
board : (L+1, L+1). 0행과 0열은 사용 안함.
기사 : 1번부터 N번까지.

1. 기사 이동

2. 대결 데미지
"""

L, N, Q = map(int, input().split())
board = [[0] * (L+1)]
board += ([[0] + list(map(int, input().split())) for _ in range(L)])

knights = [[0] * (L+1) for _ in range(L+1)]
alive = {k: True for k in range(1, N+1)}

knight_dict = {k: [] for k in range(1, N+1)}
initial_info = [list(map(int, input().split())) for _ in range(N)]
commands = [list(map(int, input().split())) for _ in range(Q)]

answer = 0

for idx, (r, c, h, w, k) in enumerate(initial_info):
    knight_dict[idx+1] = [r, c, h, w, k]
    for i in range(r, r+h):
        for j in range(c, c+w):
            knights[i][j] = idx+1

print_2d_graph('board', board)
print_2d_graph('knights', knights)
print_dict('knight_dict', knight_dict)

# Q개의 명령 실행.
for command in commands:
    # 명령은 (i, d) 형태로 주어짐.
    i, d = command
    # i번 기사가 사라져있는지 확인.
    if not alive[i]:
        continue
    # i번 기사 방향 d로 이동할 수 있는지 확인. (벽 or 보드 밖 확인)
    if not is_movable(i, d):
        continue
    move_knight(i, d, True)

print_2d_graph('knights', knights)
print_dict('knights_dict', knight_dict)

for _k, _v in knight_dict.items():
    r, c, h, w, k = _v
    if not alive[_k] or k <= 0:
        continue
    answer += initial_info[_k-1][-1] - k
print(answer)