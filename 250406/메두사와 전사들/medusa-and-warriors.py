from collections import deque

def get_distance(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)

def bfs():
    visit = [[-1] * N for _ in range(N)]
    visit[sr][sc] = 0
    q = deque()
    q.append([sr, sc, []])
    while q:
        cr, cc, cpath = q.popleft()
        for dr, dc in zip((-1, 1, 0, 0), (0, 0, -1, 1)):  # 상하좌우
            nr, nc = cr + dr, cc + dc
            if 0 <= nr <= N-1 and 0 <= nc <= N-1 and visit[nr][nc] == -1 and roads[nr][nc] == 0:
                visit[nr][nc] = visit[cr][cc] + 1
                if nr == er and nc == ec:  # 출구에 도착
                    return cpath + [[nr, nc]], visit
                q.append([nr, nc, cpath + [[nr, nc]]])
    # 출구에 도착할 수 없음.
    return [], visit

def medusa_view(r, c, dir):
    """
    x+y=r+c
    x-y=-r+c
    """
    board = [[0] * N for _ in range(N)]
    stoned_warriors = []
    for br in range(N):
        for bc in range(N):
            if board[br][bc] == 1:
                continue
            if dir == 0 and 0 <= br < r:  # 상
                if br - r + c <= bc < c:  # 상좌
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [0, 2]])
                    board[br][bc] = 1
                elif bc == c : # 상
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [0, 0]])
                    board[br][bc] = 1
                elif c < bc <= -br + r + c:  # 상우
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [0, 3]])
                    board[br][bc] = 1
            elif dir == 1 and r < br <= N-1:  # 하
                if -br + r + c <= bc < c:  # 하좌
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [1, 2]])
                    board[br][bc] = 1
                elif bc == c:  # 하
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [1, 1]])
                    board[br][bc] = 1
                elif c < bc <= br - r + c:  # 하우
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [1, 3]])
                    board[br][bc] = 1
            elif dir == 2 and 0 <= bc < c:  # 좌
                if bc + r - c <= br < r:  # 좌상
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [2, 0]])
                    board[br][bc] = 1
                elif br == r:  # 좌좌
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [2, 2]])
                    board[br][bc] = 1
                elif r < br <= -bc + r + c:  # 좌하
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [2, 1]])
                    board[br][bc] = 1
            elif dir == 3 and c < bc <= N-1:  # 우
                if -bc + r + c <= br < r:  # 우상
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [3, 0]])
                    board[br][bc] = 1
                elif br == r:  # 우우
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [3, 3]])
                    board[br][bc] = 1
                elif r < br <= bc + r - c:  # 우하
                    if [br, bc] in warriors:
                        stoned_warriors.append([br, bc, [3, 1]])
                    board[br][bc] = 1
    return board, stoned_warriors

def warrior_view(medusa_pov, stoned_warriors):
    for stoned_warrior in stoned_warriors:
        r, c, wd = stoned_warrior
        for wr in range(N):
            for wc in range(N):
                if medusa_pov[wr][wc] == 0:
                    continue
                
                if wd == [0, 0]:  # 상상
                    if 0 <= wr < r and wc == c:
                        medusa_pov[wr][wc] = 0
                elif wd == [0, 2]:  # 상좌
                    if 0 <= wr < r and wr - r + c <= wc <= c:
                        medusa_pov[wr][wc] = 0
                elif wd == [0, 3]:  # 상우
                    if 0 <= wr < r and c <= wc <= -wr + r + c:
                        medusa_pov[wr][wc] = 0
                elif wd == [1, 1]:  # 하하
                    if r < wr <= N-1 and wc == c:
                        medusa_pov[wr][wc] = 0
                elif wd == [1, 2]:  # 하좌
                    if r < wr <= N-1 and -wr + r + c <= wc <= c:
                        medusa_pov[wr][wc] = 0
                elif wd == [1, 3]:  # 하우
                    if r < wr <= N-1 and c <= wc <= wr - r + c:
                        medusa_pov[wr][wc] = 0
                elif wd == [2, 2]:  # 좌좌
                    if 0 <= wc < c and wr == r:
                        medusa_pov[wr][wc] = 0
                elif wd == [2, 0]:  # 좌상
                    if 0 <= wc < c and wc + r - c <= wr <= r:
                        medusa_pov[wr][wc] = 0
                elif wd == [2, 1]:  # 좌하
                    if 0 <= wc < c and r <= wr <= -wc + r + c:
                        medusa_pov[wr][wc] = 0
                elif wd == [3, 3]:  # 우우
                    if c < wc <= N-1 and wr == r:
                        medusa_pov[wr][wc] = 0
                elif wd == [3, 0]:  # 우상
                    if c < wc <= N-1 and -wc + r + c <= wr <= r:
                        medusa_pov[wr][wc] = 0
                elif wd == [3, 1]:  # 우하
                    if c < wc <= N-1 and r <= wr <= wc + r - c:
                        medusa_pov[wr][wc] = 0
    return medusa_pov

def get_stoned_warriors(medusa_pov):
    stoned_warriors = []
    for warrior in warriors:
        r, c = warrior
        if medusa_pov[r][c] == 1:
            stoned_warriors.append([r, c])
    return stoned_warriors

def move_warriors(medusa_pov, medusa_r, medusa_c, stoned_warriors, ans_per_turn):
    global warriors
    new_warriors = []
    for warrior in warriors:
        if warrior in stoned_warriors:
            new_warriors.append(warrior)
            continue
        r, c = warrior
        if 0 <= r-1 <= N-1 and get_distance(medusa_r, medusa_c, r-1, c) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r-1][c] == 0:  # 상으로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r-1, c])
        elif 0 <= r+1 <= N-1 and get_distance(medusa_r, medusa_c, r+1, c) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r+1][c] == 0:  # 하로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r+1, c])
        elif 0 <= c-1 <= N-1 and get_distance(medusa_r, medusa_c, r, c-1) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r][c-1] == 0:  # 좌로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r, c-1])
        elif 0 <= c+1 <= N-1 and get_distance(medusa_r, medusa_c, r, c+1) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r][c+1] == 0:  # 우로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r, c+1])
        else:
            new_warriors.append(warrior)
    warriors = new_warriors
    return ans_per_turn

def move_warriors_2nd(medusa_pov, medusa_r, medusa_c, stoned_warriors, ans_per_turn):
    global warriors
    new_warriors = []
    for warrior in warriors:
        if warrior in stoned_warriors:
            new_warriors.append(warrior)
            continue
        r, c = warrior
        if 0 <= c-1 <= N-1 and get_distance(medusa_r, medusa_c, r, c-1) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r][c-1] == 0:  # 좌로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r, c-1])
        elif 0 <= c+1 <= N-1 and get_distance(medusa_r, medusa_c, r, c+1) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r][c+1] == 0:  # 우로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r, c+1])
        elif 0 <= r-1 <= N-1 and get_distance(medusa_r, medusa_c, r-1, c) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r-1][c] == 0:  # 상으로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r-1, c])
        elif 0 <= r+1 <= N-1 and get_distance(medusa_r, medusa_c, r+1, c) < get_distance(medusa_r, medusa_c, r, c) and medusa_pov[r+1][c] == 0:  # 하로 갈 수 있는 경우.
            ans_per_turn[0] += 1
            new_warriors.append([r+1, c])
        else:
            new_warriors.append(warrior)
    warriors = new_warriors
    return ans_per_turn

def attack_warriors(medusa_r, medusa_c, ans_per_turn):
    global warriors
    new_warrior = []
    for warrior in warriors:
        if warrior == [medusa_r, medusa_c]:
            ans_per_turn[2] += 1
        else:
            new_warrior.append(warrior)
    warriors = new_warrior
    return ans_per_turn

def main():
    # 0. 메두사 최단 경로 계산
    shortest_path, shortest_visit = bfs()
    if len(shortest_path) == 0:
        print(-1)
        return
    # <--- 매 턴 loop
    for t in range(len(shortest_path)):
        ans_per_turn = [0, 0, 0]  # [모든 전사 이동거리 합, 돌이 된 전사 수, 공격한 전사 수]
        max_stoned_warriors = []
        max_medusa_pov = []
        max_dir = -1
        if t == len(shortest_path) - 1:
            print(0)
            return
        # 1. 최단 경로를 따라 메두사 이동
        medusa_r, medusa_c = shortest_path[t]
        # 이동한 곳에 전사 있으면 제거. (메두사가 공격했으므로 카운트하지 않음)
        attack_warriors(medusa_r, medusa_c, [0,0,0])

        # 2. 메두사 시선 계산
        for d in range(4):
            ## 각 방향에 대한 메두사 시선
            medusa_pov, stoned_warriors = medusa_view(medusa_r, medusa_c, d)
            ## 전사에 의해 가려진 메두사 시선
            medusa_pov = warrior_view(medusa_pov, stoned_warriors)
            ## 가려진 메두사 시선에서 굳은 전사의 수
            stoned_warriors = get_stoned_warriors(medusa_pov)
            if len(stoned_warriors) > len(max_stoned_warriors):
                max_stoned_warriors = stoned_warriors
                max_medusa_pov = medusa_pov
                max_dir = d
        ans_per_turn[1] += len(max_stoned_warriors)
        # 3. 전사 이동.
        ans_per_turn = move_warriors(max_medusa_pov, medusa_r, medusa_c, max_stoned_warriors, ans_per_turn)
        # 4. 전사 공격
        ans_per_turn = attack_warriors(medusa_r, medusa_c, ans_per_turn)
        # 전사 이동 한 번 더.
        ans_per_turn = move_warriors_2nd(max_medusa_pov, medusa_r, medusa_c, max_stoned_warriors, ans_per_turn)
        # 전사 공격 한 번 더.
        ans_per_turn = attack_warriors(medusa_r, medusa_c, ans_per_turn)
        print(' '.join(map(str, ans_per_turn)))

    return

if __name__ == '__main__':
    global N, M, sr, sc, er, ec, warriors, roads
    N, M = map(int, input().split())
    sr, sc, er, ec = map(int, input().split())
    tmp = list(map(int, input().split()))
    warriors = [tmp[i: i+2] for i in range(0, len(tmp), 2)]
    roads = [list(map(int, input().split())) for _ in range(N)]
    main()