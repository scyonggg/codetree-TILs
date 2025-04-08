
import heapq

from select import select


def debug_2d(graph, text: str=None):
    if text:
        print(text)
    for g in graph:
        print(g)
    print()
    return

def move_player(i):
    # i번 플레이어가 바라보는 방향으로 한 칸 이동.
    cr, cc, d, s = players[i]
    dr, dc = directions[d]
    nr, nc = cr + dr, cc + dc
    if not 0 <= nr < n:
        nr = cr - dr
        d = (d + 2) % 4
    if not 0 <= nc < n:
        nc = cc - dc
        d = (d + 2) % 4

    players[i] = [nr, nc, d, s]
    return

def is_player_exist(i):
    # i번 플레이어의 위치에 다른 플레이어가 있는지 확인
    ir, ic, _, _ = players[i]

    for idx, player in enumerate(players):
        if idx == i:
            continue
        if ir == player[0] and ic == player[1]:  # 같은 위치에 있는 다른 플레이어가 있음.
            return True
    return False

def is_gun_exist(i):
    # i번 플레이어의 위치에 떨어진 총이 있는지 확인.
    r, c, _, _ = players[i]
    if guns[r][c]:
        return True
    return False

def get_strongest_dropped_gun(r, c):
    if guns[r][c]:
        return -heapq.heappop(guns[r][c])
    return

def select_gun(gun1, gun2):
    return max(gun1, gun2), min(gun1, gun2)

def pickup_gun(i):
    r, c = players[i][:2]
    s, attached_gun = equipment[i]
    if is_gun_exist(i):  # 떨어진 총 있으면 비교.
        dropped_gun = get_strongest_dropped_gun(r, c)
        if attached_gun == 0:
            pickup = dropped_gun
            equipment[i] = [s, pickup]
        else:
            pickup, drop = select_gun(attached_gun, dropped_gun)
            heapq.heappush(guns[r][c], -drop)  # 약한 총 버림
            equipment[i] = [s, pickup]
    # 떨어진 총 없으면 아무것도 하지 않음.
    return

def get_enemy(i):
    # i번째 플레이어 위치에 다른 플레이어가 있음.
    r, c, d, s = players[i]
    for idx, player in enumerate(players):
        if idx == i:
            continue
        pr, pc, pd, ps = player
        if r == pr and c == pc:
            return idx

def fight(challenger, defender):
    cs, cg = equipment[challenger]
    ds, dg = equipment[defender]

    c_sum = cs + cg
    d_sum = ds + dg
    if c_sum > d_sum:  # challenger 승리
        return challenger, defender, abs(c_sum - d_sum)
    elif c_sum < d_sum:  # defender 승리
        return defender, challenger, abs(d_sum - c_sum)
    else:
        if cs > ds:
            return challenger, defender, abs(c_sum - d_sum)
        else:
            return defender, challenger, abs(d_sum - c_sum)

def drop_gun(loser):
    # loser는 제자리에 총 버린다.
    gun = equipment[loser][1]
    if gun == 0:
        return
    r, c, _, _ = players[loser]
    heapq.heappush(guns[r][c], -gun)
    equipment[loser][1] = 0
    return

def is_player_exist_in_coord(i, r, c):
    for idx, player in enumerate(players):
        if idx == i:
            continue
        if r == player[0] and c == player[1]:
            return True
    return False

def is_inside_board(r, c):
    if 0 <= r < n and 0 <= c < n:
        return True
    return False

def move_loser(loser):
    # 본인 바라보는 방향으로 이동.
    # 해당 방향에 다른 플레이어가 있거나, 격자 밖인 경우 오른쪽 90도 회전
    r, c, d, s = players[loser]
    for i in range(4):
        nd = (d + i) % 4
        dr, dc = directions[nd]
        nr, nc = r + dr, c + dc
        if (not is_player_exist_in_coord(loser, nr, nc)) and is_inside_board(nr, nc):
            players[loser] = [nr, nc, nd, s]
            break
    return

def get_point(winner, scores, point):
    scores[winner] += point
    return scores

def action(i, scores):
    # i번 플레이어의 위치에 다른 플레이어가 없다면, 총을 주울 수 있음
    if not is_player_exist(i):
        pickup_gun(i)
    # 다른 플레이어가 있다면, 싸움
    else:
        enemy = get_enemy(i)
        winner, loser, point = fight(i, enemy)
        # 패자
        drop_gun(loser)
        move_loser(loser)
        pickup_gun(loser)
        # 승자
        pickup_gun(winner)
        scores = get_point(winner, scores, point)
    return scores

def main():
    # k 라운드 진행
    scores = [0 for _ in range(m)]
    for z in range(k):
        # m명 플레이어 진행
        for i in range(m):
            # 1. 본인의 방향으로 한 칸 이동.
            move_player(i)
            # 2. 이동한 위치에서 인터랙션 수행.
            scores = action(i, scores)
        # debug_2d(guns, f'guns')
    print(" ".join([str(s) for s in scores]))

    return

if __name__ == '__main__':
    n, m, k = map(int, input().split())
    tmp = [list(map(int, input().split())) for _ in range(n)]
    guns = [[[] for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if tmp[r][c] != 0:
                heapq.heappush(guns[r][c], -tmp[r][c])
    players = [list(map(int, input().split())) for _ in range(m)]  # r, c, d, s
    players = [[r-1, c-1, d, s] for r, c, d, s in players]
    directions = {
        0: [-1, 0],  # 상
        1: [0, 1],  # 우
        2: [1, 0],  # 하
        3: [0, -1]  # 좌
    }
    equipment = [[] for _ in range(m)]
    for i, player in enumerate(players):
        s = player[-1]
        equipment[i] = [s, 0]
    # debug_2d(guns, f'guns')
    # debug_2d(equipment, f'equipment')

    main()