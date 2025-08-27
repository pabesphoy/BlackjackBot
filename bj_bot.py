import random
from bj_utils import valor_mano, valor_carta

def get_random_decision(opciones, mano, carta_crupier):
    #Este algoritmo tiene éxito un 11.5% de los días
    return random.choice(opciones)

def get_simple_decision(opciones, mano, carta_crupier):
    #Este algoritmo tiene éxito un 20% de los días
    if valor_mano(mano) > 18.55:
        return opciones[1]
    else:
        return opciones[0]
    

def es_par(mano):
    return len(mano) == 2 and mano[0][0] == mano[1][0]

def es_mano_blanda(mano):
    total = valor_mano(mano)
    valores = [carta[0] for carta in mano]

    # debe haber al menos un As
    if 'A' not in valores:
        return False

    # calcular el total contando un As como 11 y los demás como 1 si es necesario
    total_sin_as = sum(10 if v in ['J','Q','K'] else int(v) for v in valores if v != 'A')
    num_ases = valores.count('A')

    # buscar si al menos un As puede contarse como 11 sin pasarse de 21
    for ases_11 in range(1, num_ases + 1):
        posibles_total = total_sin_as + ases_11 * 11 + (num_ases - ases_11) * 1
        if posibles_total <= 21:
            #print(f'Mano {mano} es una mano blanda')
            return True

    return False


def get_best_option(opciones, mano, carta_crupier):
    total = valor_mano(mano)
    dealer_valor = valor_carta(carta_crupier)  # convertir carta visible a valor numérico (A=11)

    # Pares
    if es_par(mano):
        if total in [4,6,14]:
            return "s" if dealer_valor <= 7 and "s" in opciones else "p"
        if total == 8:
            return "s" if dealer_valor in [5,6] and "s" in opciones else "p"
        if total == 10:
            return "d" if dealer_valor <= 9 and "d" in opciones else "p"
        if total == 12:
            return "s" if dealer_valor <= 6 and "s" in opciones else "p"
        if total == 16: 
            if "s" in opciones:
                return "s" 
            else:
                return "q" if dealer_valor <= 7 else "p"
        if total == 18:
            if dealer_valor == 7 or dealer_valor >= 10:
                return "q"
            elif "s" in opciones:
                return "s"
            else:
                return "q"
        if total == 20: return "q"  
        if total == 22: return "s" 

    # Manos blandas
    if es_mano_blanda(mano):
        if total in [13,14]:
            return "d" if dealer_valor in [5,6] and "d" in opciones else "p"
        if total in [15,16]:  
            return "d" if dealer_valor in [4,5,6] and "d" in opciones else "p" 
        if total == 17:   
            return "d" if dealer_valor in [3,4,5,6] and "d" in opciones else "p" 
        if total == 18:
            if dealer_valor in [2,7,8]: return "q"
            elif dealer_valor in [3,4,5,6]: return "d" if "d" in opciones else "q"
            else: return "p"
        if total >= 19:
            return "q"

    # Manos duras
    else:
        if total <= 8: return "p"
        if total == 9: return "d" if dealer_valor in [3,4,5,6] and "d" in opciones else "p"
        if total == 10: return "d" if dealer_valor in range(2,10) and "d" in opciones else "p"
        if total == 11: return "d" if dealer_valor != 11 and "d" in opciones else "p"
        if total == 12: return "q" if dealer_valor in [4,5,6] else "p"
        if 13 <= total <= 16: return "q" if dealer_valor in range(2,7) else "p"
        if total >= 17: return "q"

    # fallback
    raise Exception("No se encontró estrategia.")

