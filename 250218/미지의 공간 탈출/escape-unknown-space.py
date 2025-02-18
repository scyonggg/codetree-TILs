from collections import deque
import math

def get_flatten_board():
    global walls, N, M
    L = 3 * M + 2
    flatten_board = [[1] * L for _ in range(L)]
    for dir, wall in enumerate(walls):
        spad = [[0] * M for _ in range(M)]
        if dir == 0:  # 동
            for r in range(M):
                for c in range(M):
                    spad[M-1-c][r] = wall[r][c]
            for r in range(M):
                for c in range(M):
                    flatten_board[M+1+r][2*M+1+c] = spad[r][c]

        elif dir == 1:  # 서
            for r in range(M):
                for c in range(M):
                    spad[c][M-1-r] = wall[r][c]
            for r in range(M):
                for c in range(M):
                    flatten_board[M+1+r][1+c] = spad[r][c]

        elif dir == 2:  # 남
            for r in range(M):
                for c in range(M):
                    spad[r][c] = wall[r][c]
            for r in range(M):
                for c in range(M):
                    flatten_board[2*M+1+r][M+1+c] = spad[r][c]

        elif dir == 3:  # 북
            for r in range(M):
                for c in range(M):
                    spad[M-1-r][M-1-c] = wall[r][c]
            for r in range(M):
                for c in range(M):
                    flatten_board[1+r][M+1+c] = spad[r][c]

        elif dir == 4:  # 윗면
            for r in range(M):
                for c in range(M):
                    flatten_board[M+1+r][M+1+c] = wall[r][c]

    #     print(f'dir: {directions[dir]}')
    #     debug_2d(wall)
    # debug_2d(flatten_board)

    return flatten_board

def get_unknown_coords():
    global board, N
    for r in range(N):
        for c in range(N):
            if board[r][c] == 3:
                return [r, c]

def add_huddles(flatten_board):
    global board, N, M, global_exit
    un_r, un_c = get_unknown_coords()
    un_r -= 1
    un_c -= 1
    L = len(flatten_board)
    for r in range(un_r, un_r+M+2):
        for c in range(un_c, un_c+M+2):
            if un_r + 1 <= r < un_r+M+1 and un_c + 1 <= c < un_c+M+1:
                continue
            if board[r][c] == 1:
                pass
            elif board[r][c] == 0:
                global_exit = [r, c]
                # 동
                if c == un_c+M+1:
                    r -= un_r+1
                    flatten_board[r+M+1][L-1] = 10
                # 서
                elif c == un_c:
                    r -= un_r+1
                    flatten_board[r+M+1][0] = 10
                # 남
                elif r == un_r+M+1:
                    c -= un_c+1
                    flatten_board[L-1][c+M+1] = 10
                # 북
                elif r == un_r:
                    c -= un_c+1
                    flatten_board[0][c+M+1] = 10
    # debug_2d(flatten_board)
    return flatten_board

def debug_2d(graph):
    for g in graph:
        print(g)
    print()
    return

def debug_3d(graph):
    for idx, i in enumerate(graph):
        print(f'Debugging {directions[idx]}')
        for g in i:
            print(g)
    print()

def bfs(flatten_board):
    L = len(flatten_board)
    visit = [[0] * L for _ in range(L)]
    r, c = 0, 0
    for i in range(L):
        for j in range(L):
            if flatten_board[i][j] == 2:
                r, c, = i, j
    q = deque()
    q.append([r, c])
    visit[r][c] = 1
    while q:
        cr, cc = q.popleft()
        for dr, dc in zip((-1, 1, 0, 0), (0, 0, 1, -1)):
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < L and 0 <= nc < L:
                # 동 -> 남 (2*M, 2*M)
                if cr == 2*M and 2*M+1 <= cc <= 3*M and dr == 1:
                    nc = 2*M
                    nr = (2*M) + ((cc) - (2*M))
                # 남 -> 동 (2*M, 2*M)
                elif cc == 2*M and 2*M+1 <= cr <= 3*M and dc == 1:
                    nr = 2*M
                    nc = (2*M) + ((cr) - (2*M))
                # 남 -> 서 (2*M, M+1)
                elif cc == M+1 and 2*M+1 <= cr <= 3*M and dc == -1:
                    nr = 2*M
                    nc = (2*M) - ((cr) - (2*M))
                # 서 -> 남 (2*M, M+1)
                elif cr == 2*M and 1 <= cc <= M and dr == 1:
                    nc = M+1
                    nr = (2*M) + ((M+1) - (cc))
                # 서 -> 북 (M+1, M+1)
                elif cr == M+1 and 1 <= cc <= M and dr == -1:
                    nc = M+1
                    nr = (M+1) - ((M+1) - (cc))
                # 북 -> 서 (M+1, M+1)
                elif cc == M+1 and 1 <= cr <= M and dc == -1:
                    nr = M+1
                    nc = (M+1) - ((M+1) - (cr))
                # 북 -> 동 (M+1, 2*M)
                elif cc == 2*M and 1 <= cr <= M and dc == 1:
                    nr = M+1
                    nc = (2*M) + ((M+1) - (cr))
                # 동 -> 북 (M+1, 2*M)
                elif cr == M+1 and 2*M+1 <= cc <= 3*M and dr == -1:
                    nc = 2*M
                    nr = (M+1) - ((cc) - (2*M))

                if flatten_board[nr][nc] != 1 and visit[nr][nc] == 0:
                    if flatten_board[nr][nc] == 10:
                        visit[nr][nc] = visit[cr][cc] + 1
                        return visit[cr][cc] + 1 - 1  # 1부터 시작했으므로 하나 빼줌.
                    else:
                        visit[nr][nc] = visit[cr][cc] + 1
                        q.append([nr, nc])
    return -1

def get_odd_visit_board():
    global visit_board, board, odds
    for odd in odds:
        r, c, d, v = odd
        visit_board[r][c] = 0
        nr, nc = r, c
        time = 0
        while 0 <= nr < N and 0 <= nc < N:
            time += 1
            if d == 0:  # 동
                nc += 1
            elif d == 1:  # 서
                nc -= 1
            elif d == 2:  # 남
                nr += 1
            elif d == 3:  # 북
                nr -= 1
            if board[nr][nc] == 0:  # 빈 공간이 아니면 확산되지 않는다.
                visit_board[nr][nc] = time * v
            else:
                break
    return

def bfs2(r, c, time_spent):
    global N, visit_board, board, final_exit
    visit = [[0] * N for _ in range(N)]
    q = deque()
    q.append([r, c])
    visit[r][c] = time_spent
    while q:
        cr, cc = q.popleft()
        for dr, dc in zip((-1, 1, 0, 0), (0, 0, -1, 1)):
            nr, nc = dr + cr, dc + cc
            if 0 <= nr < N and 0 <= nc < N:
                if visit[nr][nc] == 0 and visit[cr][cc] + 1 < visit_board[nr][nc]:
                    if board[nr][nc] == 0 or board[nr][nc] == 4:
                        q.append([nr, nc])
                        visit[nr][nc] = visit[cr][cc] + 1
    if visit[final_exit[0]][final_exit[1]] == 0:
        return -1
    else:
        return visit[final_exit[0]][final_exit[1]]

def get_final_exit():
    global final_exit, board
    for r in range(N):
        for c in range(N):
            if board[r][c] == 4:
                final_exit = [r, c]
                return

N, M, F = map(int, input().split())  # NxN : 미지의 공간, M : 정육면체 시간의 벽, F : 시간 이상 현상 개수

board = [list(map(int, input().split())) for _ in range(N)]  # 미지의 공간 평면도. 1 : 장애물, 2 : 타임머신, 3 : 시간의 벽, 4 : 탈출구

walls = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)]  # 시간의 벽 - 동,서,남,북,윗면 단면도

odds = [list(map(int, input().split())) for _ in range(F)]  # r, c, d, v. // 0 : 동, 1 : 서, 2 : 남, 3 : 북

directions = {0: "East", 1: "West", 2: "South", 3: "North", 4: "Upper"}

visit_board = [[math.inf] * N for _ in range(N)]  # 이상 현상 확산

global_exit = []
final_exit = []
# debug_2d(board)
# debug_3d(walls)
# debug_2d(odds)

def main():
    # 1. 시간의 벽에서 내려오기.
    # 1-1. 시간의 벽 펼치기
    flatten_board = get_flatten_board()
    # 1-2. 펼친 시간의 벽에서 장애물, 탈출구1 추가하기.
    flatten_board = add_huddles(flatten_board)  # 0: 빈공간, 1: 장애물, 2: 시작 위치, 9: 패딩된 공간 (갈 수 없음), 10: 탈출구1
    # 1-3. bfs로 탈출구1까지 소요시간 찾기
    time_spent = bfs(flatten_board)
    if time_spent == -1:
        return -1

    # 2. 미지의 공간에서 이상 현상을 피해 탈출구로 나가기.
    # 2-1. visit_board에 시간에 따른 이상 현상 그리기.
    get_odd_visit_board()
    # 2-2. 탈출구1부터 최종 탈출구까지 탐색
    get_final_exit()  # 최종 탈출구 좌표 획득
    ans = bfs2(*global_exit, time_spent)
    return ans


if __name__ == '__main__':
    print(main())