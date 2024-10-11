DEBUG=True
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

def sort_santas(_santas_list):
    # 우선 순위 : 1) r좌표 큰 산타, 2) c좌표 큰 산타.
    ret = sorted(_santas_list, key=lambda x: x[2], reverse=True)
    ret.sort(key=lambda x: x[1], reverse=True)

    return ret

def in_board(r, c):
    global N
    if r <= 0 or r > N or c <= 0 or c > N:
        return False
    return True

def get_distance(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

def get_closest_santa():
    """ 현재 루돌프로부터 가장 가까운 산타의 idx 값을 반환. """
    global santas_list, board, Rr, Rc
    # print("before sorted_santas_list", santas_list)
    sorted_santas_list = sort_santas(santas_list)
    # print("sorted_santas_list", sorted_santas_list)
    closest_dist = 9999
    closest_idx = 0
    for Si, Sr, Sc in sorted_santas_list:
        if Si == 0 or not alive[Si]:
            continue
        if not in_board(Sr, Sc) or not alive[Si]:
            continue
        dist = get_distance(Rr, Rc, Sr, Sc)
        if dist < closest_dist:
            closest_dist = dist
            closest_idx = Si

    return closest_idx

def get_direction(idx):
    """ 루돌프가 idx 번째 산타를 공격할 경우, 방향을 반환. """
    global santas_list, Rr, Rc
    _, Sr, Sc = santas_list[idx]
    assert _ == idx, f"{_}, {idx} mismatch"
    dr = dc = 0
    # 산타가 루돌프보다 아래에 있을 경우
    if Sr > Rr:
        dr = 1
    elif Sr < Rr:
        dr = -1
    # 산타가 루돌프보다 오른쪽에 있을 경우
    if Sc > Rc:
        dc = 1
    elif Sc < Rc:
        dc = -1
    return dr, dc

def get_direction_santa(idx):
    """idx 산타가 루돌프로 가기 위한 방향 리턴"""
    global Rr, Rc
    _, Sr, Sc = santas_list[idx]
    dr = dc = 0
    # dr, dc 방향에 비어있거나 루돌프가 있으면 됨.
    if Rr < Sr and board[Sr-1][Sc] <= 0:  # 상
        # 상으로 움직여도 루돌프에게 가까워질 수 있음.
        return -1, 0
        # 상으로 움직이더라도, 루돌프 방향으로 가까워질 수 없으면 움직이지 않음.
    if Rc > Sc and board[Sr][Sc+1] <= 0:  # 우
        return 0, 1
    if Rr > Sr and board[Sr+1][Sc] <= 0:  # 하
        return 1, 0
    if Rc < Sc and board[Sr][Sc-1] <= 0:  # 좌
        return 0, -1
    return dr, dc

def get_direction_santa_v1(idx):
    """idx 산타가 루돌프로 가기 위한 방향 리턴"""
    global Rr, Rc
    _, Sr, Sc = santas_list[idx]
    dr = dc = 0
    # dr, dc 방향에 비어있거나 루돌프가 있으면 됨.
    if Rr < Sr and board[Sr-1][Sc] <= 0:  # 상
        # 상으로 움직여도 루돌프에게 가까워질 수 있음.
        Sr -= 1
        # 루돌프와 겹침.
        if (Rr == Sr and Rc == Sc) or \
            (Rr < Sr and board[Sr-1][Sc] <= 0) or \
            (Rc > Sc and board[Sr][Sc+1] <= 0) or \
            (Rc < Sc and board[Sr][Sc-1] <= 0):
            return -1, 0
        Sr += 1
        # 상으로 움직이더라도, 루돌프 방향으로 가까워질 수 없으면 움직이지 않음.
    if Rc > Sc and board[Sr][Sc+1] <= 0:  # 우
        Sc += 1
        if (Rr == Sr and Rc == Sc) or \
            (Rr < Sr and board[Sr-1][Sc] <= 0) or \
                (Rc > Sc and board[Sr][Sc+1] <= 0) or \
                (Rr > Sr and board[Sr+1][Sc] <= 0):
            return 0, 1
        Sc -= 1
    if Rr > Sr and board[Sr+1][Sc] <= 0:  # 하
        Sr += 1
        if (Rr == Sr and Rc == Sc) or \
            (Rc < Sc and board[Sr][Sc-1] <= 0) or \
                (Rc > Sc and board[Sr][Sc+1] <= 0) or \
                (Rr > Sr and board[Sr+1][Sc] <= 0):
            return 1, 0
        Sr -= 1
    if Rc < Sc and board[Sr][Sc-1] <= 0:  # 좌
        Sc -= 1
        if (Rr == Sr and Rc == Sc) or \
            (Rc < Sc and board[Sr][Sc-1] <= 0) or \
                (Rr < Sr and board[Sr-1][Sc] <= 0) or \
                (Rr > Sr and board[Sr+1][Sc] <= 0):
            return 0, -1
        Sc += 1

    return dr, dc

def move_rudolph(m, idx, dr, dc):
    # 루돌프 dr, dc 방향으로 이동.
    global board, Rr, Rc, C
    # 루돌프 원래 있던 자리 제거.
    board[Rr][Rc] = 0
    nr = Rr + dr
    nc = Rc + dc
    # 움직여야할 다음 자리에 산타가 있음.
    if board[nr][nc] != 0:
        # 산타 충돌 (점수 획득, 산타 위치 변경)
        collision(m, idx, dr, dc, C)
    # 루돌프 다음 자리 업데이트
    board[nr][nc] = -1
    Rr = nr
    Rc = nc
    return

def move_santa(m, idx, dr, dc):
    """ idx 산타가 dr, dc 방향으로 이동. """
    global santas_list, board, Rr, Rc, D
    _, Sr, Sc = santas_list[idx]
    board[Sr][Sc] = 0
    nr = Sr + dr
    nc = Sc + dc
    # 다음 자리에 산타가 있을 경우, 움직이지 않음.
    if board[nr][nc] > 0:
        return
    santas_list[idx] = [idx, nr, nc]
    # 움직여야할 자리에 루돌프 있음. -> 충돌.
    if board[nr][nc] == -1:
        # 충돌 후 맵 밖으로 밀려나면 탈락.
        if not in_board(nr-dr*D, nc-dc*D):
            alive[idx] = False
            score[idx] += D
            santas_list[idx] = [idx, -1, -1]
            return
        # 루돌프 충돌 (점수 획득, 산타 위치 변경. 단, 산타가 움직인 방향과 반대방향으로 움직임)
        collision(m, idx, -dr, -dc, D)
        santas_list[idx] = [idx, nr-dr*D, nc-dc*D]
        board[nr-dr*D][nc-dc*D] = idx
    else:
        # 움직여야할 자리에 아무도 없음, 산타 업데이트
        board[nr][nc] = idx
        santas_list[idx] = [idx, nr, nc]
    return

def collision(m, idx, dr, dc, power):
    """
    idx 번째 산타에게 루돌프가 [dr, dc] 방향으로 와서 충돌했음.
    산타 원래 위치 초기화 및 밀려난 위치 업데이트.
    """
    # idx 산타는 power 점수 획득
    global score, santas_list, board, stun, alive
    score[idx] += power
    # idx 산타는 dr, dc 방향으로 power칸만큼 밀려남.
    _, Sr, Sc = santas_list[idx]
    assert _ == idx, f'collision. {_} and {idx} mismatch.'

    # 밀려난 자리가 맵 밖인지 확인.
    if in_board(Sr + dr * power, Sc + dc * power):
        # 밀려난 자리 (Sr + dr*power, Sc + dc*power)에 다른 산타가 있을 시, 상호작용.
        if board[Sr + dr * power][Sc + dc * power] != 0:
            interaction(Sr + dr * power, Sc + dc * power, dr, dc)
        # 밀려난 자리로 산타 업데이트.
        santas_list[idx] = [idx, Sr + dr * power, Sc + dc * power]
        board[Sr + dr * power][Sc + dc * power] = idx
        stun[idx] = [True, m + 1]  # m+1까지 스턴.
    # 맵 밖으로 밀려났으면 게임 탈락.
    else:
        santas_list[idx] = [idx, -1, -1]
        alive[idx] = False

    return

def interaction(Sr, Sc, dr, dc):
    """
    Sr, Sc 칸에 위치한 산타가 상호작용 당하는 함수.
    Sr+dr, Sc+dc 방향에 산타가 있으면 재귀로 상호작용.
    """
    global santas_list, board, alive
    # 산타 번호 획득 및 위치 업데이트
    idx = board[Sr][Sc]
    board[Sr][Sc] = 0
    # 이 산타는 밀려나면 탈락.
    if not in_board(Sr+dr, Sc+dc):
        santas_list[idx] = [idx, -1, -1]
        alive[idx] = False
        return

    # 다음 칸 (Sr+dr, Sc+dc)에 다른 산타가 있는지 확인
    if board[Sr+dr][Sc+dc] != 0:
        # 밀려날 자리에 다른 산타가 있을 시, 다시 상호작용 호출.
        interaction(Sr+dr, Sc+dc, dr, dc)

    # 상호작용하여 밀려날 자리가 게임판 안이고, 그 자리에 아무도 없음.
    santas_list[idx] = [idx, Sr+dr, Sc+dc]
    board[Sr+dr][Sc+dc] = idx
    return

"""
산타 정렬 : sort_santas
탈락한 산타 : alive에 저장.
"""

N, M, P, C, D = map(int, input().split())
Rr, Rc = map(int, input().split())
board = [[0] * (N+1) for _ in range(N+1)]
board[Rr][Rc] = -1

santas_list = [[0, -1, -1]]  # [idx, r, c]
for _ in range(P):
    Pn, Sr, Sc = map(int, input().split())
    santas_list.append([Pn, Sr, Sc])
# print(santas_list)

stun = {k: [False, 0] for k in range(1, P+1)}
alive = {k: True for k in range(1, P+1)}
score = {k: 0 for k in range(1, P+1)}

for Si, Sr, Sc in santas_list:
    board[Sr][Sc] = Si

# M턴 반복.
# for m in range(M):
for m in range(M):
    for k, [v1, v2] in stun.items():
        if v1 and m > v2:
            stun[k] = [False, 0]

    # 1. 루돌프 이동
    ## 루돌프와 가장 가까운 산타의 idx 확인
    closest_idx = get_closest_santa()
    ## idx 산타로 가기 위한 방향 계산
    dr, dc = get_direction(closest_idx)
    ## 루돌프가 idx 산타로 공격.
    move_rudolph(m, closest_idx, dr, dc)  # 루돌프 이동 완료, 산타 연쇄 충돌 완료.

    print_2d_graph(f"[Turn {m}], After rudolph", board)
    # print(f'[Turn {m}, Rudolph], alive: \n {alive} \n , stun: \n {stun}\n, score: \n {score}\n, santas_list: \n {santas_list} \n')
    # 2. 1번부터 P번까지 산타 이동
    for p in range(1, P+1):
        # 탈락하거나 기절 중인 산타는 스킵
        if not alive[p] or (stun[p][0] and m <= stun[p][1]):
            continue
        ## 루돌프 방향 계산
        dr, dc = get_direction_santa(p)
        # print(f'santa {p}, dr : {dr}, dc : {dc}')
        ## idx 산타가 루돌프로 공격.
        move_santa(m, p, dr, dc)
        print_2d_graph(f"[Turn {m}], After santa {p}", board)
        # print(f'[Turn {m}, santa {p}], alive: \n {alive} \n , stun: \n {stun}\n, score: \n {score}\n, santas_list: \n {santas_list} \n' )

    for k, v in score.items():
        if alive[k]:
            score[k] += 1
    # print(f'[Turn {m} done.], alive: \n {alive} \n , stun: \n {stun}\n, score: \n {score}\n, santas_list: \n {santas_list} \n')

for k, v in score.items():
    print(v, end=' ')