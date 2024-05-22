class constant:
    MANAGER_SESSION = 'manager_session_0'

def getItemName(itemId):
    if itemId == 0:
        return '코카콜라'
    elif itemId == 1:
        return '칠성사이다'
    elif itemId == 2:
        return '레쓰비'
    elif itemId == 3:
        return '칸쵸'
    elif itemId == 4:
        return '빼빼로'
    elif itemId == 5:
        return '고소미'
    elif itemId == 6:
        return '스니커즈'
    elif itemId == 7:
        return '짜파게티'
    else:
        return '알 수 없음'

def getItemPrice(itemId):
    if itemId == 0:
        return 1700
    elif itemId == 1:
        return 1500
    elif itemId == 2:
        return 1000
    elif itemId == 3:
        return 1200
    elif itemId == 4:
        return 1400
    elif itemId == 5:
        return 1100
    elif itemId == 6:
        return 800
    elif itemId == 7:
        return 1800
    else:
        return -1