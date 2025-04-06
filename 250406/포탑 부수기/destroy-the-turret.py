from collections import deque

DEBUG=False

def debug_2d(graph, text: str=None):
    if not DEBUG:
        return
    if text is not None:
        print(text)
    for g in graph:
        print(g)
    print()
    return

def get_attacker():
    """
    공격자 선정.
    """
    # 1. 공격력이 가장 낮은 포탑 찾기
    min_val = 9999999999
    min_towers = []
    for r in range(N):
        for c in range(M):
            # 부서진 포탑은 생략
            if 0 < boards[r][c] <= min_val:
                if boards[r][c] == min_val:
                    min_towers.append([r, c])
                else:
                    min_towers = [[r, c]]
                min_val = boards[r][c]
    if len(min_towers) == 1:
        return min_towers[0]
    # 2. 공격력 가장 낮은 포탑이 2개 이상
    ## 가장 최근에 공격한 포탑 찾기
    min_val = 9999999999
    ret_towers = []
    for tower in min_towers:
        r, c = tower
        if attacks[r][c] <= min_val:
            if attacks[r][c] == min_val:
                ret_towers.append([r, c])
            else:
                ret_towers = [[r, c]]
            min_val = attacks[r][c]
    if len(ret_towers) == 1:
        return ret_towers[0]
    # 3. 행과 열의 합이 가장 큰 포탑 찾기
    min_val = 9999999999
    min_towers = ret_towers
    ret_towers = []
    for tower in min_towers:
        sums = sum(tower)
        if sums <= min_val:
            if sums == min_val:
                ret_towers.append(tower)
            else:
                ret_towers = [tower]
            min_val = sums
    if len(ret_towers) == 1:
        return ret_towers[0]
    # 4. 열 값이 가장 큰 포탑 찾기
    return max(ret_towers, key=lambda x: x[1])

def attacker_update(attacker, k):
    r, c = attacker
    # 공격 시점 업데이트
    attacks[r][c] = k
    # 핸디캡 업데이트
    boards[r][c] += (N + M)
    return

def get_target():
    """
    타겟 설정.
    """
    # 1. 공격력 가장 높은 포탑
    val = -1
    max_towers = []
    for r in range(N):
        for c in range(M):
            if boards[r][c] <= 0:
                continue
            if boards[r][c] >= val:
                if boards[r][c] == val:
                    max_towers.append([r, c])
                else:
                    max_towers = [[r, c]]
                val = boards[r][c]
    if len(max_towers) == 1:
        return max_towers[0]
    # 2. 공격한지 가장 오래된 포탑
    val = 99999999
    ret_towers = []
    for tower in max_towers:
        r, c = tower
        if boards[r][c] <= 0:
            continue
        if attacks[r][c] <= val:
            if attacks[r][c] == val:
                ret_towers.append([r, c])
            else:
                ret_towers = [[r, c]]
            val = attacks[r][c]
    if len(ret_towers) == 1:
        return ret_towers[0]
    # 행과 열의 합이 가장 작은 포탑
    val = 9999999999
    old_towers = ret_towers
    ret_towers = []
    for tower in old_towers:
        r, c = tower
        if r + c <= val:
            if r+c == val:
                ret_towers.append([r, c])
            else:
                ret_towers = [[r, c]]
            val = r + c
    if len(ret_towers) == 1:
        return ret_towers[0]
    # 4. 열 값이 가장 작은 포탑
    return min(ret_towers, key=lambda x: x[1])

def raser_path(attacker, target):
    ar, ac = attacker
    tr, tc = target
    visit = [[-1] * M for _ in range(N)]
    visit[ar][ac] = 0
    q = deque()
    q.append([ar, ac, [[ar, ac]]])
    while q:
        cr, cc, cpath = q.popleft()
        for dr, dc in zip((0, 1, 0, -1), (1, 0, -1, 0)):  # 우하좌상
            nr, nc = cr + dr, cc + dc
            nr = (nr + N) % N
            nc = (nc + M) % M
            if boards[nr][nc] > 0 and visit[nr][nc] == -1:
                if nr == tr and nc == tc:
                    return cpath + [[nr, nc]]
                q.append([nr, nc, cpath + [[nr, nc]]])
                visit[nr][nc] = visit[cr][cc] + 1
    return []

def raser_attack(path, attacker):
    ar, ac = attacker
    ap = boards[ar][ac]
    l = len(path)
    # 타겟까지 경로에 있는 포탑
    for i in range(1, l-1):
        r, c = path[i]
        boards[r][c] -= ap // 2
    # 타겟 포탑
    tr, tc = path[-1]
    boards[tr][tc] -= ap
    return

def cannon_attack(attacker, target):
    ar, ac = attacker
    tr, tc = target
    ap = boards[ar][ac]
    # 타겟 포탑
    boards[tr][tc] -= ap
    related_towers = []
    # 주변 8개 포탑
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            r = (tr + i + N) % N
            c = (tc + j + M) % M
            if boards[r][c] <= 0:
                continue
            related_towers.append([r, c])
            # 타겟 포탑 및 공격자 포탑은 생략
            if (i == 0 and j == 0) or (i == ar and j == ac):
                continue
            boards[r][c] -= ap // 2

    if not attacker in related_towers:
        related_towers.append(attacker)
    return related_towers

def check_alive():
    cnt = 0
    for r in range(N):
        for c in range(M):
            if boards[r][c] <= 0:
                boards[r][c] = 0
            else:
                cnt += 1
    if cnt == 0:
        raise ValueError(f"check_alive(), cnt is {cnt}.")
    return cnt

def repair_towers(path):
    """
    :param path: 공격에 관련된 포탑
    """
    for r in range(N):
        for c in range(M):
            if boards[r][c] > 0 and [r, c] not in path:
                boards[r][c] += 1
    return

def play_one_turn(k) -> bool:
    debug_2d(boards, f'Before turn #{k}, boards:')
    # 1. 공격자 선정
    attacker = get_attacker()
    # 공격자 핸디캡 부여 및 공격시점 업데이트
    attacker_update(attacker, k)
    # 2. 공격자 공격 (타겟 선정)
    target = get_target()
    # 레이저 공격 시도.
    path = raser_path(attacker, target)
    if len(path) > 0:
        raser_attack(path, attacker)
    else:  # 포탄 공격 시도
        path = cannon_attack(attacker, target)
    # 3. 포탑 부서짐 (포탑 생존 확인)
    num_alive = check_alive()
    # 부서지지 않은 포탑이 1개이면 즉시 중지.
    if num_alive == 1:
        return False
    # 4. 포탑 정비
    repair_towers(path)

    debug_2d(boards, f'After turn #{k}, attacker : {attacker}, target : {target}, path: {path}')
    debug_2d(attacks, "attack_times")
    return True

def get_strongest_attack():
    max_val = -1
    for r in range(N):
        for c in range(M):
            if boards[r][c] > max_val:
                max_val = boards[r][c]
    return max_val

def main():
    for k in range(1, K+1):
        playable = play_one_turn(k)
        if not playable:
            break

    # 남아있는 포탑 중 가장 강한 포탑 공격력 출력
    print(get_strongest_attack())
    return

if __name__ == '__main__':
    N, M, K = map(int, input().split())
    boards = [list(map(int, input().split())) for _ in range(N)]
    attacks = [[0] * M for _ in range(N)]  # 각 타워가 마지막으로 공격한 턴 수
    main()