"""
사람 : 1 ~ m번. (1 <= m <= 30)
각각 1분, 2분, ..., m분에 출발하여 편의점으로 이동.
격자 크기 : n x n. (2 <= n <= 15)

최단거리 이동 : 상 좌 우 하
베이스캠프 : 1) 최단거리, 2) 행이 작은 순서, 3) 열이 작은 순서
"""
from collections import deque

def debug_2d(graph, text: str=None):
    if text:
        print(text)
    for g in graph:
        print(g)
    print()
    return

def get_dist(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)

def get_shortest_dist(src):
    # src와 가장 가까운 베이스캠프 리턴
    sr, sc = src
    visit = [[False] * n for _ in range(n)]
    visit[sr][sc] = True
    q = deque()
    q.append([sr, sc, 0])
    candidate = []
    min_len = 9999999999
    while q:
        cr, cc, cd = q.popleft()
        for dr, dc in zip((0, 0, 1, -1), (1, -1, 0, 0)):
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < n and 0 <= nc < n and not visit[nr][nc] and boards[nr][nc] != -1:
                if boards[nr][nc] == 1:
                    if cd + 1 == min_len:
                        candr, candc = candidate
                        if nr < candr:
                            candidate = [nr, nc]
                        elif nr == candr and nc < candc:
                            candidate = [nr, nc]
                    elif cd + 1 < min_len:
                        candidate = [nr, nc]
                        min_len = cd + 1
                visit[nr][nc] = True
                q.append([nr, nc, cd + 1])
    return candidate

def get_shortest_path(src, dst):
    sr, sc = src
    destr, destc = dst
    visit = [[False] * n for _ in range(n)]
    visit[sr][sc] = True
    q = deque()
    q.append([sr, sc, [[sr, sc]]])
    while q:
        cr, cc, cpath = q.popleft()
        for dr, dc in zip((-1, 0, 0, 1), (0, -1, 1, 0)):
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < n and 0 <= nc < n and not visit[nr][nc] and boards[nr][nc] != -1:
                if nr == destr and nc == destc:
                    return cpath[1] if len(cpath) > 1 else [nr, nc] # 바로 다음 경로 리턴
                visit[nr][nc] = True
                q.append([nr, nc, cpath + [[nr, nc]]])
    return []

def move_people():
    global movable_people
    new_people = {}
    for k, v in movable_people.items():
        pi, pr, pc = k, v[0], v[1]
        next_path = get_shortest_path([pr, pc], stores[pi])
        new_people[k] = next_path
    movable_people = new_people
    return

def check_arrived():
    for i, store in enumerate(stores):
        if i == 0:
            continue
        if i in movable_people and movable_people[i] == store:  # 편의점에 도착
            del movable_people[i]  # 이동 가능한 사람 명단에서 제거
            boards[store[0]][store[1]] = -1  # 해당 편의점 이동 불가
            done[i] = True
    return

def check_finished():
    for v in done.values():
        if not v:
            return False
    return True

def get_closest_basecamp(t):
    target = get_shortest_dist(stores[t])  # stores[t]에서 최단거리의 베이스캠프
    boards[target[0]][target[1]] = -1  # 해당 베이스캠프 이동 불가
    return target

def goto_basecamp(t):
    target = get_closest_basecamp(t)  # 타겟 베이스캠프
    movable_people[t] = target  # 이동 가능 사람 명단에 추가
    return

def main():
    time = 0
    while time < 1_000_000:
        time += 1
        # 1. 격자에 있는 사람 편의점으로 이동
        ## m분이 지났고 (모든 사람이 베이스캠프 입장), 움직일 사람이 더이상 없으면 모두가 편의점에 도착한 것.
        if check_finished():
            print(time)
            return time

        ## 움직일 사람 있으면, 모두 움직임
        move_people()
        # 2. 편의점에 도착했는지 확인. 도착했다면 해당 편의점 이동 불가 표시
        check_arrived()
        # 모든 사람들이 다 편의점에 도착했는지 확인. 모두 다 도착했다면 리턴
        if check_finished():
            print(time)
            return time
        # 3. t번 사람은 가고싶은 편의점과 가장 가까운 베이스캠프로 들어감. 해당 베이스캠프 이동 불가.
        if time <= m:
            goto_basecamp(time)
    return

if __name__ == '__main__':
    n, m = map(int, input().split())
    boards = [list(map(int, input().split())) for _ in range(n)]  # 0: 빈공간, 1: 베이스캠프
    stores = [list(map(int, input().split())) for _ in range(m)]  # [행, 열]
    stores = [[r-1, c-1] for r, c in stores]
    stores = [[-1, -1]] + stores
    movable_people = {}  # 번호 : [행, 열]
    done = {k: False for k in range(1, m+1)}
    # debug_2d(boards)
    # debug_2d(stores)
    main()
