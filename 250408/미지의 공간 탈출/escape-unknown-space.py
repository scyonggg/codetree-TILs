# from collections import deque
# import math

# def get_flatten_board():
#     global walls, N, M
#     L = 3 * M + 2
#     flatten_board = [[1] * L for _ in range(L)]
#     for dir, wall in enumerate(walls):
#         spad = [[0] * M for _ in range(M)]
#         if dir == 0:  # 동
#             for r in range(M):
#                 for c in range(M):
#                     spad[M-1-c][r] = wall[r][c]
#             for r in range(M):
#                 for c in range(M):
#                     flatten_board[M+1+r][2*M+1+c] = spad[r][c]

#         elif dir == 1:  # 서
#             for r in range(M):
#                 for c in range(M):
#                     spad[c][M-1-r] = wall[r][c]
#             for r in range(M):
#                 for c in range(M):
#                     flatten_board[M+1+r][1+c] = spad[r][c]

#         elif dir == 2:  # 남
#             for r in range(M):
#                 for c in range(M):
#                     spad[r][c] = wall[r][c]
#             for r in range(M):
#                 for c in range(M):
#                     flatten_board[2*M+1+r][M+1+c] = spad[r][c]

#         elif dir == 3:  # 북
#             for r in range(M):
#                 for c in range(M):
#                     spad[M-1-r][M-1-c] = wall[r][c]
#             for r in range(M):
#                 for c in range(M):
#                     flatten_board[1+r][M+1+c] = spad[r][c]

#         elif dir == 4:  # 윗면
#             for r in range(M):
#                 for c in range(M):
#                     flatten_board[M+1+r][M+1+c] = wall[r][c]

#     #     print(f'dir: {directions[dir]}')
#     #     debug_2d(wall)
#     # debug_2d(flatten_board)

#     return flatten_board

# def get_unknown_coords():
#     global board, N
#     for r in range(N):
#         for c in range(N):
#             if board[r][c] == 3:
#                 return [r, c]

# def add_huddles(flatten_board):
#     global board, N, M, global_exit
#     un_r, un_c = get_unknown_coords()
#     un_r -= 1
#     un_c -= 1
#     L = len(flatten_board)
#     for r in range(un_r, un_r+M+2):
#         for c in range(un_c, un_c+M+2):
#             if un_r + 1 <= r < un_r+M+1 and un_c + 1 <= c < un_c+M+1:
#                 continue
#             if board[r][c] == 1:
#                 pass
#             elif board[r][c] == 0:
#                 global_exit = [r, c]
#                 # 동
#                 if c == un_c+M+1:
#                     tr = r - un_r
#                     flatten_board[M+tr][L-1] = 10
#                 # 서
#                 elif c == un_c:
#                     tr = r - un_r
#                     flatten_board[M+tr][0] = 10
#                 # 남
#                 elif r == un_r+M+1:
#                     tc = c - un_c
#                     flatten_board[L-1][M+tc] = 10
#                 # 북
#                 elif r == un_r:
#                     tc = c - un_c
#                     flatten_board[0][M+tc] = 10
#     return flatten_board

# def debug_2d(graph):
#     for g in graph:
#         print(g)
#     print()
#     return

# def debug_3d(graph):
#     for idx, i in enumerate(graph):
#         print(f'Debugging {directions[idx]}')
#         for g in i:
#             print(g)
#     print()

# def bfs(flatten_board):
#     L = len(flatten_board)
#     visit = [[0] * L for _ in range(L)]
#     r, c = 0, 0
#     for i in range(L):
#         for j in range(L):
#             if flatten_board[i][j] == 2:
#                 r, c, = i, j
#     q = deque()
#     q.append([r, c])
#     visit[r][c] = 1
#     while q:
#         cr, cc = q.popleft()
#         for dr, dc in zip((-1, 1, 0, 0), (0, 0, 1, -1)):
#             nr, nc = cr + dr, cc + dc
#             if 0 <= nr < L and 0 <= nc < L:
#                 # 동 -> 남 (2*M, 2*M)
#                 if cr == 2*M and 2*M+1 <= cc <= 3*M and dr == 1:
#                     nc = 2*M
#                     nr = (2*M) + ((cc) - (2*M))
#                 # 남 -> 동 (2*M, 2*M)
#                 elif cc == 2*M and 2*M+1 <= cr <= 3*M and dc == 1:
#                     nr = 2*M
#                     nc = (2*M) + ((cr) - (2*M))
#                 # 남 -> 서 (2*M, M+1)
#                 elif cc == M+1 and 2*M+1 <= cr <= 3*M and dc == -1:
#                     nr = 2*M
#                     nc = (2*M) - ((cr) - (2*M))
#                 # 서 -> 남 (2*M, M+1)
#                 elif cr == 2*M and 1 <= cc <= M and dr == 1:
#                     nc = M+1
#                     nr = (2*M) + ((M+1) - (cc))
#                 # 서 -> 북 (M+1, M+1)
#                 elif cr == M+1 and 1 <= cc <= M and dr == -1:
#                     nc = M+1
#                     nr = (M+1) - ((M+1) - (cc))
#                 # 북 -> 서 (M+1, M+1)
#                 elif cc == M+1 and 1 <= cr <= M and dc == -1:
#                     nr = M+1
#                     nc = (M+1) - ((M+1) - (cr))
#                 # 북 -> 동 (M+1, 2*M)
#                 elif cc == 2*M and 1 <= cr <= M and dc == 1:
#                     nr = M+1
#                     nc = (2*M) + ((M+1) - (cr))
#                 # 동 -> 북 (M+1, 2*M)
#                 elif cr == M+1 and 2*M+1 <= cc <= 3*M and dr == -1:
#                     nc = 2*M
#                     nr = (M+1) - ((cc) - (2*M))

#                 if flatten_board[nr][nc] != 1 and visit[nr][nc] == 0:
#                     if flatten_board[nr][nc] == 10:
#                         visit[nr][nc] = visit[cr][cc] + 1
#                         return visit[cr][cc] + 1 - 1  # 1부터 시작했으므로 하나 빼줌.
#                     else:
#                         visit[nr][nc] = visit[cr][cc] + 1
#                         q.append([nr, nc])
#     return -1

# def get_odd_visit_board():
#     global visit_board, board, odds
#     for odd in odds:
#         r, c, d, v = odd
#         visit_board[r][c] = 0
#         nr, nc = r, c
#         time = 0
#         while 0 <= nr < N and 0 <= nc < N:
#             time += 1
#             if d == 0:  # 동
#                 nc += 1
#             elif d == 1:  # 서
#                 nc -= 1
#             elif d == 2:  # 남
#                 nr += 1
#             elif d == 3:  # 북
#                 nr -= 1
#             if not (0 <= nr < N and 0 <= nc < N):
#                 break
#             if board[nr][nc] == 0:  # 빈 공간이 아니면 확산되지 않는다.
#                 visit_board[nr][nc] = time * v
#             else:
#                 break
#     return

# def bfs2(r, c, time_spent):
#     global N, visit_board, board, final_exit
#     visit = [[0] * N for _ in range(N)]
#     q = deque()
#     q.append([r, c])
#     visit[r][c] = time_spent
#     while q:
#         cr, cc = q.popleft()
#         for dr, dc in zip((-1, 1, 0, 0), (0, 0, -1, 1)):
#             nr, nc = dr + cr, dc + cc
#             if 0 <= nr < N and 0 <= nc < N:
#                 if visit[nr][nc] == 0 and visit[cr][cc] + 1 < visit_board[nr][nc]:
#                     if board[nr][nc] == 0 or board[nr][nc] == 4:
#                         q.append([nr, nc])
#                         visit[nr][nc] = visit[cr][cc] + 1
#     if visit[final_exit[0]][final_exit[1]] == 0:
#         return -1
#     else:
#         return visit[final_exit[0]][final_exit[1]]

# def get_final_exit():
#     global final_exit, board
#     for r in range(N):
#         for c in range(N):
#             if board[r][c] == 4:
#                 final_exit = [r, c]
#                 return

# N, M, F = map(int, input().split())  # NxN : 미지의 공간, M : 정육면체 시간의 벽, F : 시간 이상 현상 개수

# board = [list(map(int, input().split())) for _ in range(N)]  # 미지의 공간 평면도. 1 : 장애물, 2 : 타임머신, 3 : 시간의 벽, 4 : 탈출구

# walls = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)]  # 시간의 벽 - 동,서,남,북,윗면 단면도

# odds = [list(map(int, input().split())) for _ in range(F)]  # r, c, d, v. // 0 : 동, 1 : 서, 2 : 남, 3 : 북

# directions = {0: "East", 1: "West", 2: "South", 3: "North", 4: "Upper"}

# visit_board = [[math.inf] * N for _ in range(N)]  # 이상 현상 확산

# global_exit = []
# final_exit = []
# # debug_2d(board)
# # debug_3d(walls)
# # debug_2d(odds)

# def main():
#     # 1. 시간의 벽에서 내려오기.
#     # 1-1. 시간의 벽 펼치기
#     flatten_board = get_flatten_board()
#     # 1-2. 펼친 시간의 벽에서 장애물, 탈출구1 추가하기.
#     flatten_board = add_huddles(flatten_board)  # 0: 빈공간, 1: 장애물, 2: 시작 위치, 9: 패딩된 공간 (갈 수 없음), 10: 탈출구1
#     # 1-3. bfs로 탈출구1까지 소요시간 찾기
#     time_spent = bfs(flatten_board)
#     if time_spent == -1:
#         return -1

#     # 2. 미지의 공간에서 이상 현상을 피해 탈출구로 나가기.
#     # 2-1. visit_board에 시간에 따른 이상 현상 그리기.
#     get_odd_visit_board()
#     # 2-2. 탈출구1부터 최종 탈출구까지 탐색
#     get_final_exit()  # 최종 탈출구 좌표 획득
#     ans = bfs2(*global_exit, time_spent)
#     return ans


# if __name__ == '__main__':
#     print(main())


"""
공간 : N x N (5 <= N <= 20)
시간의 벽 : M x M (2 <= M <= min(N-2, 10)

빈 공간 : 0, 장애물 : 1, 타임머신 : 2, 시간의 벽 : 3, 탈출구 : 4

시간 이상 현상 : F개 (1 <= F <= 10)
장애물과 탈출구가 없는 빈 공간으로만 확산. 더 이상 확산할 수 없을 경우 멈춤.
(r, c)에서 v속도로 d방향 이동. (1 <= v <= 1000)
d = 0 : 동, 1 : 서, 2 : 남, 3 : 북

타임머신이 시작점에서 탈출구까지 이동하는 데 필요한 최소 시간 출력. 탈출할 수 없으면 -1 출력.
"""
from collections import deque

DEBUG=False

def debug_2d(graph, text: str=None):
    if not DEBUG:
        return
    if text:
        print(text)
    for g in graph:
        print(g)
    print()
    return

def flatten_walls():
    # 0 // 1 ~ M // M+1 ~ 2M // 2M+1 ~ 3M // 3M+1
    L = 3 * M + 2
    new_walls = [[9] * L for _ in range(L)]
    for c in range(M+1, 2*M+1):
        new_walls[0][c] = 1
        new_walls[-1][c] = 1
    for r in range(M+1, 2*M+1):
        new_walls[r][0] = 1
        new_walls[r][-1] = 1
    # 동
    src = walls[0]  # MxM
    ltr, rbr = M+1, 2*M
    ltc, rbc = 2*M+1, 3*M
    for r in range(M):
        for c in range(M):
            new_walls[rbr-c][ltc+r] = src[r][c]

    # 서
    src = walls[1]
    ltr, rbr = M+1, 2*M
    ltc, rbc = 1, M
    for r in range(M):
        for c in range(M):
            new_walls[ltr+c][rbc-r] = src[r][c]
    # 남
    src = walls[2]
    ltr, rbr = 2*M+1, 3*M
    ltc, rbc = M+1, 2*M
    for r in range(M):
        for c in range(M):
            new_walls[ltr+r][ltc+c] = src[r][c]
    # 북
    src = walls[3]
    ltr, rbr = 1, M
    ltc, rbc = M+1, 2*M
    for r in range(M):
        for c in range(M):
            new_walls[rbr-r][rbc-c] = src[r][c]

    # 윗면
    src = walls[4]
    ltr, ltc, rbr, rbc = M+1, M+1, 2*M+1, 2*M+1
    # 타임머신 위치
    tm_coord_in_new_walls = []
    for r in range(M):
        for c in range(M):
            new_walls[ltr+r][ltc+c] = src[r][c]
            if src[r][c] == 2:
                tm_coord_in_new_walls = [ltr+r, ltc+c]

    debug_2d(new_walls, 'new_walls:')
    for i in range(5):
        debug_2d(walls[i], f'walls[{dicts[i]}]:')

    return new_walls, tm_coord_in_new_walls

def get_first_exit(new_walls):
    ltr, ltc = -1, -1
    flag = True
    for r in range(N):
        if not flag:
            break
        for c in range(N):
            if spaces[r][c] == 3:
                ltr, ltc = r, c
                flag = False
                break

    roi_r, roi_c = ltr-1, ltc-1
    first_exit_in_spaces = []
    first_exit_in_new_walls = []
    for c in range(roi_c+1, roi_c+M+1):
        # 벽 윗줄
        if spaces[roi_r][c] == 0:
            first_exit_in_spaces = [roi_r, c]
            first_exit_in_new_walls = [0, M+c-roi_c]
            new_walls[0][M+c-roi_c] = 0
        # 벽 아랫줄
        elif spaces[roi_r+M+1][c] == 0:
            first_exit_in_spaces = [roi_r+M+1, c]
            first_exit_in_new_walls = [3*M+2 - 1, M+c-roi_c]
            new_walls[-1][M+c-roi_c] = 0
    for r in range(roi_r+1, roi_r+M+1):
        # 벽 왼쪽줄
        if spaces[r][roi_c] == 0:
            first_exit_in_spaces = [r, roi_c]
            first_exit_in_new_walls = [M+r-roi_r, 0]
            new_walls[M+r-roi_r][0] = 0
        # 벽 오른쪽 줄
        elif spaces[r][roi_c+M+1] == 0:
            first_exit_in_spaces = [r, roi_c+M+1]
            first_exit_in_new_walls = [M+r-roi_r, 3*M+2 - 1]
            new_walls[M+r-roi_r][-1] = 0

    debug_2d(spaces, f'first_exit_in_spaces : {first_exit_in_spaces}, spaces:')
    debug_2d(new_walls, f'first_exit_in_new_walls: {first_exit_in_new_walls}, new_walls:')
    return first_exit_in_spaces, first_exit_in_new_walls, new_walls

def get_next_coord(cr, cc, dr, dc):
    # 북 : [1 ~ M, M+1 ~ 2*M]
    # 동 : [M+1 ~ 2*M, 2*M+1 ~ 3*M]
    # 남 : [2*M+1 ~ 3*M, M+1 ~ 2*M]
    # 서 : [M+1 ~ 2*M, 1 ~ M]

    # 0 // 1 ~ M // M+1 ~ 2M // 2M+1 ~ 3M // 3M+1
    """
    0
    1 ~ M
    M+1 ~ 2*M
    2*M+1 ~ 3*M
    3*<+1
    """
    nr, nc = cr + dr, cc + dc
    # 북 -> 동
    if cc == 2*M and 1 <= cr <= M and dc == 1:
        nr = M+1
        nc = 2*M+1 + abs((2*M) - (cr))
    # 동 -> 북
    elif cr == M+1 and 2*M+1 <= cc <= 3*M and dr == -1:
        nc = 2*M
        nr = M - abs((cc) - (2*M+1))
    # 동 -> 남
    elif cr == 2*M and 2*M+1 <= cc <= 3*M and dr == 1:
        nc = 2*M
        nr = 2*M+1 + abs((2*M+1) - (cc))
    # 남 -> 동
    elif cc == 2*M and 2*M+1 <= cr <= 3*M and dc == 1:
        nr = 2*M
        nc = 2*M+1 + abs((2*M+1) - (cr))
    # 남 -> 서
    elif cc == M+1 and 2*M+1 <= cr <= 3*M and dc == -1:
        nr = 2*M
        nc = M - abs((2*M+1) - (cr))
    # 서 -> 남
    elif cr == 2*M and 1 <= cc <= M and dr == 1:
        nc = M+1
        nr = 2*M+1 + abs((M) - (cc))
    # 서 -> 북
    elif cr == M+1 and 1 <= cc <= M and dr == -1:
        nc = M+1
        nr = M - abs((M) - (cc))
    # 북 -> 서
    elif cc == M+1 and 1 <= cr <= M and dc == -1:
        nr = M+1
        nc = M - abs((M) - (cr))

    return [nr, nc]

def bfs(src, dst, board):
    L = 3 * M + 2
    visit = [[0] * L for _ in range(L)]
    q = deque()
    q.append(src)
    visit[src[0]][src[1]] = 1
    while q:
        cr, cc = q.popleft()
        for dr, dc in zip((0, 0, 1, -1), (1, -1, 0, 0)):
            nr, nc = get_next_coord(cr, cc, dr, dc)
            if 0 <= nr < L and 0 <= nc < L and visit[nr][nc] == 0 and board[nr][nc] == 0:
                if nr == dst[0] and nc == dst[1]:
                    return visit[cr][cc]
                visit[nr][nc] = visit[cr][cc] + 1
                q.append([nr, nc])
    return -1


def declimb_walls():
    # 1. 시간의 벽을 펼치기. 펼친 맵은 (3M+2) x (3M+2)이고, 맨 바깥쪽 패딩에는 모두 1, 유일하게 0 한개 있음.
    new_walls, tm_coord_in_new_walls = flatten_walls()
    # 2. 유일하게 하나 있는 0을 찾기.
    first_exit_in_spaces, first_exit_in_new_walls, new_walls = get_first_exit(new_walls)
    # new_walls에 대해, tm_coord_in_new_walls에서 first_exit_in_new_walls로 BFS
    turns = bfs(tm_coord_in_new_walls, first_exit_in_new_walls, new_walls)
    if turns == -1:
        return -1
    return turns, first_exit_in_spaces

def update_odds():
    visit = [[-1] * N for _ in range(N)]
    for odd in odds:
        r, c, d, v = odd
        visit[r][c] = 0
        if d == 0:  # 동
            for t, nc in enumerate(range(c+1, N), start=1):
                if spaces[r][nc] == 0:
                    visit[r][nc] = t*v
                else:
                    break
        elif d == 1:  # 서
            for t, nc in enumerate(range(c-1, -1, -1), start=1):
                if spaces[r][nc] == 0:
                    visit[r][nc] = t*v
                else:
                    break
        elif d == 2:  # 남
            for t, nr in enumerate(range(r+1, N), start=1):
                if spaces[nr][c] == 0:
                    visit[nr][c] = t*v
                else:
                    break
        elif d == 3:  # 북
            for t, nr in enumerate(range(r-1, -1, -1), start=1):
                if spaces[nr][c] == 0:
                    visit[nr][c] = t*v
                else:
                    break
    debug_2d(visit, f'Odds visit:')
    return visit

def final_escape(src, odd_visit, turns):
    sr, sc = src
    visit = [[-1] * N for _ in range(N)]
    q = deque()
    q.append(src)
    visit[sr][sc] = turns
    while q:
        cr, cc = q.popleft()
        for dr, dc in zip((0, 0, 1, -1), (-1, 1, 0, 0)):
            nr, nc = cr + dr, cc + dc
            if not (0 <= nr < N and 0 <= nc < N) or visit[nr][nc] != -1:
                continue
            if spaces[nr][nc] == 4:
                return visit[cr][cc] + 1
            if spaces[nr][nc] != 0:
                continue
            if odd_visit[nr][nc] == -1 or visit[cr][cc] + 1 < odd_visit[nr][nc]:
                q.append([nr, nc])
                visit[nr][nc] = visit[cr][cc] + 1
    debug_2d(visit, f'final_escape visit:')
    return -1


def main():
    # 1. 시간의 벽에서 장애물을 피해 내려오기
    turns, first_exit_in_spaces = declimb_walls()
    # 2. 시간 이상 현상 업데이트
    visit = update_odds()
    # 3. 미지의 공간에 대해, first_exit_in_spaces에서 탈출구 (4)로 탈출하기. 이 때 시간 이상 현상 고려할 것.
    ret = final_escape(first_exit_in_spaces, visit, turns)
    print(ret)
    return

if __name__ == '__main__':
    N, M, F = map(int, input().split())
    spaces = [list(map(int, input().split())) for _ in range(N)]
    walls = [[], [], [], [], []]  # 동, 서, 남, 북, 윗면
    for i in range(5):
        walls[i] = [list(map(int, input().split())) for _ in range(M)]
    odds = [list(map(int, input().split())) for _ in range(F)]  # r, c, d, v
    dicts = {
        0: 'East',
        1: 'West',
        2: 'South',
        3: 'North',
        4: 'Top'
    }

    main()