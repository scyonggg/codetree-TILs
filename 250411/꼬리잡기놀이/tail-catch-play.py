"""
3명 이상 그룹.

1. 머리사람 따라 한 칸 이동.
2. 라운드에 따라 공을 던짐. (좌->우, 하->상, 우->좌, 상->하 반복)
3. 해당 선에 사람이 있으면, 최초 만나는 사람 점수 획득.
획득 점수 : k^2
획득할 경우, 방향을 바꿈. (머리사람 꼬리사람 바꿈)
4. 1번부터 반복.

"""
from collections import deque

DEBUG=False
DEBUG=True

def debug_2d(graph, text: str=None):
    if not DEBUG:
        return
    if text:
        print(text)
    for g in graph:
        print(g)
    print()
    return

def find_head():
    # 그룹별 머리사람 찾기. board[r][c] = 1이면 머리사람.
    heads = []
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                heads.append([r, c])
    return heads

def bfs(src):
    sr, sc = src
    visit = [[False] * n for _ in range(n)]
    visit[sr][sc] = True
    q = deque()
    q.append([sr, sc, [[sr, sc]]])
    tr, tc = -1, -1
    cpath = []
    while q:
        cr, cc, cpath = q.popleft()
        for dr, dc in zip((0, 0, 1, -1), (-1, 1, 0, 0)):
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < n and 0 <= nc < n and not visit[nr][nc]:
                if board[nr][nc] == 2:  # 다음 사람
                    visit[nr][nc] = True
                    q.append([nr, nc, cpath + [[nr, nc]]])
                elif board[nr][nc] == 3:  # 꼬리 사람
                    visit[nr][nc] = True
                    tr, tc = nr, nc
    return cpath + [[tr, tc]]

def dfs(src):
    sr, sc = src
    visit = [[False] * n for _ in range(n)]
    visit[sr][sc] = True
    q = deque()
    q.append([sr, sc, [[sr, sc]]])
    tr, tc = -1, -1
    cpath = []
    while q:
        cr, cc, cpath = q.pop()
        for dr, dc in zip((0, 0, -1, 1), (-1, 1, 0, 0)):
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < n and 0 <= nc < n and not visit[nr][nc]:
                if board[nr][nc] == 2:  # 다음 사람
                    visit[nr][nc] = True
                    q.append([nr, nc, cpath + [[nr, nc]]])
                elif board[nr][nc] == 3:  # 꼬리 사람
                    visit[nr][nc] = True
                    tr, tc = nr, nc
    return cpath + [[tr, tc]]

def find_groups(heads):
    groups = []
    for head in heads:
        p = dfs(head)
        # p = bfs(head)
        groups.append(p)
    return groups

def move_head(groups):
    new_groups = []
    for i, group in enumerate(groups):
        head, tail = group[0], group[-1]
        hr, hc = head
        tr, tc = tail
        # head에서 시작. 주변에서 다음 이동할 지역을 찾음. 이 때, 꼬리사람 (3)일수도 있고 이동 선 (4)일수도 있음..
        nr, nc = -1, -1
        for dr, dc in zip((0, 0, -1, 1), (1, -1, 0, 0)):
            nr, nc = hr + dr, hc + dc
            if 0 <= nr < n and 0 <= nc < n and (board[nr][nc] == 3 or board[nr][nc] == 4):
                break
        # 이전 head 및 tail 처리
        board[hr][hc] = 2
        board[tr][tc] = 4
        # 새로운 head 및 tail 처리
        board[nr][nc] = 1
        board[group[-2][0]][group[-2][1]] = 3
        # group 업데이트
        ngroup = [[nr, nc]] + group[:-1]
        new_groups.append(ngroup)

    return new_groups

def throw_ball(i):
    i = (i + (4*n)) % (4*n)
    ball_path = []
    if 0 <= i < n:  # 좌->우
        ball_path = [[i, c] for c in range(n)]
    elif n <= i < 2*n:  # 하->상
        ball_path = [[r, i-n] for r in range(n-1, -1, -1)]
    elif 2*n <= i < 3*n:  # 우->좌
        ball_path = [[3*n-1 - i, c] for c in range(n-1, -1, -1)]
    elif 3*n <= i < 4*n:  # 상->하
        ball_path = [[r, 4*n-1 - i] for r in range(n)]
    return ball_path

def map_people(groups):
    tmp = [[-1] * n for _ in range(n)]
    for i, group in enumerate(groups):
        for r, c in group:
            tmp[r][c] = i
    return tmp

def get_group_order(i, r, c, groups):
    group = groups[i]
    for n, (gr, gc) in enumerate(group, start=1):
        if r == gr and c == gc:
            return n
    return 0

def cal_score(i, r, c, groups):
    global scores
    order = get_group_order(i, r, c, groups)
    scores += order ** 2
    return

# def get_group_order(r, c, groups):
#     for group in groups:
#         for i, (gr, gc) in enumerate(group, start=1):
#             if r == gr and c == gc:
#                 return i
#     return 0
#
# def cal_score(r, c, groups):
#     global scores
#     order = get_group_order(r, c, groups)
#     scores += order ** 2

def change_direction(i, groups):
    group = groups[i]
    hr, hc = group[0]
    tr, tc = group[-1]
    # board 업데이트
    board[hr][hc] = 3
    board[tr][tc] = 1
    # group 업데이트
    group[0], group[-1] = group[-1], group[0]
    return

# def change_direction(r, c, groups):
#     for group in groups:
#         if [r, c] in group:
#             hr, hc = group[0]
#             tr, tc = group[-1]
#             group[0], group[-1] = group[-1], group[0]
#             board[hr][hc] = 3
#             board[tr][tc] = 1
#             return
#     return

def check_hit(ball_path, groups):
    # ball_path에 사람이 맞는지 확인. 맞았다면 점수 획득, 방향 전환 수행.
    # n x n에 그룹원 번호 매핑
    tmp = map_people(groups)
    for path in ball_path:  # path는 공의 진행 방향 순서.
        r, c = path
        for i, group in enumerate(groups):
            if [r, c] in group:
                cal_score(i, r, c, groups)
                change_direction(i, groups)
                return
        # if tmp[r][c] != -1:  # 던진 공에 사람 맞았음.
        #     # 점수 획득
        #     cal_score(tmp[r][c], r, c, groups)
        #     # cal_score(r, c, groups)
        #     # 방향 전환
        #     change_direction(tmp[r][c], groups)
    return
#
# def check_hit(ball_path, groups):
#     # ball_path에 사람이 맞는지 확인. 맞았다면 점수 획득, 방향 전환 수행.
#     # n x n에 그룹원 번호 매핑
#     tmp = map_people(groups)
#     for path in ball_path:  # path는 공의 진행 방향 순서.
#         r, c = path
#         if tmp[r][c] != -1:  # 던진 공에 사람 맞았음.
#             # 점수 획득
#             cal_score(tmp[r][c], r, c, groups)
#             # cal_score(r, c, groups)
#             # 방향 전환
#             change_direction(tmp[r][c], groups)
#             return
#     return

def play_round(i):
    # i번째 라운드 진행.
    # 각 그룹별 머리사람 탐색
    heads = find_head()
    # 각 그룹원 탐색
    groups = find_groups(heads)  # groups: 그룹 정보, visits: 그룹내 멤버의 순서 정보.
    # 1. 모든 그룹 머리사람 따라 한 칸 이동
    groups = move_head(groups)
    # 2. 공을 던짐
    ball_path = throw_ball(i)
    # 3. 던진 공에 사람이 맞는지 확인.
    check_hit(ball_path, groups)

    return

def main():
    # k 라운드만큼 반복
    for i in range(k):
        play_round(i)

    print(scores)
    return


if __name__ == '__main__':
    # n: 3~20, m: 1~5, k: 1~1,000
    n, m, k = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]  # 0: 빈칸, 1: 머리사람, 2: 나머지, 3: 꼬리사람, 4: 이동 선
    scores = 0
    main()