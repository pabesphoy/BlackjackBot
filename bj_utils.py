def valor_mano(mano):
    valor = 0
    ases = 0
    for carta in mano:
        if carta[0] in ['J', 'Q', 'K']:
            valor += 10
        elif carta[0] == 'A':
            ases += 1
            valor += 11
        else:
            valor += int(carta[0])
    while valor > 21 and ases:
        valor -= 10
        ases -= 1
    return valor

def valor_carta(carta):
    valor = carta[0] 
    if valor in ['J', 'Q', 'K']:
        return 10
    elif valor == 'A':
        return 11
    else:
        return int(valor)