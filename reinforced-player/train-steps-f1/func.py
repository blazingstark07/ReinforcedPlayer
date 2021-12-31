
def distance(x, y, x1, y1):
    ret = ((x-x1)**2+(y-y1)**2)**0.5
    return ret

def sign(x):
    if x == 0: return 0
    return x/abs(x)

    
def is_tch(crd, tail, dr):
    x, y = crd
    tx, ty = tail
    dx = tx - x
    dy = ty - y

    if sign(dx) != dr[0] or sign(dy) != dr[1]: return False
    
    if dr[1]==0: a, b, c = 0, 1, -y
    elif dr[0] == 0: a, b, c = 1, 0, -x
    else: a, b, c = -dr[1], dr[0], -dr[0]*y + dr[1]*x

    dst = abs(a*tx + b*ty + c)/(a**2 + b**2)**0.5
    if dst <= 1: return True