import random
from math import floor
from bj_bot import get_random_decision, get_simple_decision, get_best_option
from bj_utils import valor_mano, valor_carta
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table



def crear_baraja():
    palos = ['♠', '♥', '♦', '♣']
    valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    baraja = [(valor, palo) for valor in valores for palo in palos]
    random.shuffle(baraja)
    return baraja



def mostrar_mano(mano, ocultar_primera=False):
    if ocultar_primera:
        return "[?] " + " ".join([f"[{carta[0]}{carta[1]}]" for carta in mano[1:]])
    else:
        return " ".join([f"[{carta[0]}{carta[1]}]" for carta in mano])

def jugar_blackjack(dinero, use_log=True, funcion = None):
    out = logging.info if use_log else print

    out("\n🃏 ¡Bienvenido al Blackjack! 🃏")

    try:
        out(f'Tu saldo: {dinero}. Ingresas {floor(dinero/2)}')
        apuesta_inicial = floor(dinero/2)
        if apuesta_inicial <= 0 or apuesta_inicial > dinero:
            out("Apuesta inválida.")
            return dinero
    except ValueError:
        out("Debes ingresar un número.")
        return dinero

    baraja = crear_baraja()
    manos_jugador = [[baraja.pop(), baraja.pop()]]
    apuestas = [apuesta_inicial]
    crupier = [baraja.pop(), baraja.pop()]

    # dinero disponible para nuevas apuestas dentro de esta ronda (reservamos la apuesta inicial)
    dinero_disponible = dinero - apuesta_inicial

    # Procesar cada mano
    mano_idx = 0
    while mano_idx < len(manos_jugador):
        mano = manos_jugador[mano_idx]
        apuesta = apuestas[mano_idx]

        turno_inicial = True
        while True:
            out(f"\nMano {mano_idx + 1}: {mostrar_mano(mano)} (Total: {valor_mano(mano)}) | Apuesta: {apuesta}")
            out(f"Mano del crupier: {mostrar_mano(crupier, ocultar_primera=True)}")

            # Comprobar si se pasó
            if valor_mano(mano) > 21:
                out("¡Te pasaste! 😵")
                break

            # Opciones disponibles (sólo añadimos d/s si hay fondos reservables)
            opciones = ["p", "q"]
            can_add = turno_inicial and dinero_disponible >= apuesta
            if can_add:
                opciones.append("d")  # doblar
                if len(mano) == 2 and mano[0][0] == mano[1][0]:
                    opciones.append("s")  # split

            # Mostrar las opciones legibles
            opciones_text = []
            for o in opciones:
                if o == "p":
                    opciones_text.append("[p]edir")
                elif o == "q":
                    opciones_text.append("[q]uedar")
                elif o == "d":
                    opciones_text.append("[d]oblar")
                elif o == "s":
                    opciones_text.append("[s]plit")

            if funcion == None:
                accion = input(f'Elige una accion ({"/".join(opciones)}): {opciones_text} ').strip().lower()
            else:
                accion = funcion(opciones, mano, crupier[1])
            out(f'Elegida accion {accion}')

            if accion == 'p':  # Pedir carta
                mano.append(baraja.pop())

            elif accion == 'q':  # Quedarse
                break

            elif accion == 'd' and turno_inicial and dinero_disponible >= apuesta:  # Doblar
                # Se añade la misma cantidad de la apuesta actual al total de la apuesta
                apuestas[mano_idx] = apuesta * 2
                dinero_disponible -= apuesta  # se reserva la cantidad extra
                mano.append(baraja.pop())
                break  # en doblar se toma 1 carta y se planta

            elif (accion == 's'
                  and turno_inicial
                  and len(mano) == 2
                  and mano[0][0] == mano[1][0]
                  and dinero_disponible >= apuesta):
                # Dividir en dos manos: sacar una carta y crear la nueva mano justo tras la actual
                carta_separada = mano.pop()  # quita la segunda carta
                manos_jugador.insert(mano_idx + 1, [carta_separada, baraja.pop()])
                apuestas.insert(mano_idx + 1, apuesta)
                dinero_disponible -= apuesta  # reservar la apuesta para la nueva mano
                # completar la mano actual con una carta nueva
                mano.append(baraja.pop())
                # No rompemos el bucle: seguimos jugando la PRIMERA mano
                turno_inicial = False
                continue

            else:
                out("Opción no válida.")
                raise Exception("Opción no válida.")

            turno_inicial = False

        mano_idx += 1

    # Turno del crupier
    out("\nTurno del crupier...")
    out(f"Mano del crupier: {mostrar_mano(crupier)} (Total: {valor_mano(crupier)})")
    while valor_mano(crupier) < 17:
        crupier.append(baraja.pop())
        out(f"El crupier toma una carta: {mostrar_mano(crupier)} (Total: {valor_mano(crupier)})")

    total_crupier = valor_mano(crupier)

    # Resultados
    for i, mano in enumerate(manos_jugador):
        total_jugador = valor_mano(mano)
        apuesta = apuestas[i]
        out(f"\nResultado de Mano {i + 1}: {mostrar_mano(mano)} (Total: {total_jugador})")
        if total_jugador > 21:
            out(f"Perdiste {apuesta}.")
            dinero -= apuesta
        elif total_crupier > 21 or total_jugador > total_crupier:
            out(f"¡Ganaste {apuesta}! 🥳")
            dinero += apuesta
        elif total_jugador < total_crupier:
            out(f"Perdiste {apuesta}.")
            dinero -= apuesta
        else:
            out("Empate. 🤝")

    return dinero

console = Console()

def mostrar_mano_rich(mano, ocultar_primera=False):
    texto = ""
    for i, carta in enumerate(mano):
        if i == 0 and ocultar_primera:
            texto += "[??] "
        else:
            texto += f"[{carta[0]}{carta[1]}] "
    return texto.strip()

def jugar_blackjack_rich(dinero, use_log = False, funcion = None):
    console.clear()
    console.rule("[bold yellow]🃏 ¡Bienvenido al Blackjack! 🃏[/bold yellow]")

    console.print(f"Tu saldo: [green]{dinero}[/green]. [cyan]¿Cuánto quieres apostar?: [/cyan]")
    apuesta_inicial = int(input(''))
    if apuesta_inicial <= 0 or apuesta_inicial > dinero:
        console.print("[red]Apuesta inválida.[/red]")
        return dinero

    baraja = crear_baraja()
    manos_jugador = [[baraja.pop(), baraja.pop()]]
    apuestas = [apuesta_inicial]
    crupier = [baraja.pop(), baraja.pop()]
    dinero_disponible = dinero - apuesta_inicial

    mano_idx = 0
    while mano_idx < len(manos_jugador):
        mano = manos_jugador[mano_idx]
        apuesta = apuestas[mano_idx]

        turno_inicial = True
        while True:
            panel_mano = Panel(f"{mostrar_mano_rich(mano)}\nTotal: {valor_mano(mano)}\nApuesta: {apuesta}", title=f"Mano {mano_idx+1}", border_style="cyan")
            panel_crupier = Panel(f"{mostrar_mano_rich(crupier, ocultar_primera=True)}", title="Crupier", border_style="red")
            console.print(panel_mano)
            console.print(panel_crupier)

            if valor_mano(mano) > 21:
                console.print("[bold red]¡Te pasaste! 😵[/bold red]")
                break

            opciones = ["p", "q"]
            can_add = turno_inicial and dinero_disponible >= apuesta
            if can_add:
                opciones.append("d")
                if len(mano) == 2 and mano[0][0] == mano[1][0]:
                    opciones.append("s")
            if funcion == None:
                accion = input(f'Elige una accion ({"/".join(opciones)}): ').strip().lower()
            else:
                accion = funcion(opciones, mano, crupier[1])
            console.print(f"Acción elegida: [bold yellow]{accion}[/bold yellow]")

            if accion == 'p':
                mano.append(baraja.pop())
            elif accion == 'q':
                break
            elif accion == 'd' and can_add:
                apuestas[mano_idx] *= 2
                dinero_disponible -= apuesta
                mano.append(baraja.pop())
                break
            elif accion == 's' and can_add and len(mano) == 2:
                carta_separada = mano.pop()
                manos_jugador.insert(mano_idx+1, [carta_separada, baraja.pop()])
                apuestas.insert(mano_idx+1, apuesta)
                dinero_disponible -= apuesta
                mano.append(baraja.pop())
                turno_inicial = False
                continue
            else:
                console.print("[red]Opción no válida[/red]")
                raise Exception("Opción no válida")

            turno_inicial = False

        mano_idx += 1

    console.print("\n[bold red]Turno del crupier...[/bold red]")
    console.print(f"Mano del crupier: {mostrar_mano_rich(crupier)} (Total: {valor_mano(crupier)})")
    while valor_mano(crupier) < 17:
        crupier.append(baraja.pop())
        console.print(f"El crupier toma carta: {mostrar_mano_rich(crupier)} (Total: {valor_mano(crupier)})")

    total_crupier = valor_mano(crupier)

    for i, mano in enumerate(manos_jugador):
        total_jugador = valor_mano(mano)
        apuesta = apuestas[i]
        if total_jugador > 21:
            console.print(f"[red]Perdiste {apuesta}[/red]")
            dinero -= apuesta
        elif total_crupier > 21 or total_jugador > total_crupier:
            console.print(f"[green]¡Ganaste {apuesta}! 🥳[/green]")
            dinero += apuesta
        elif total_jugador < total_crupier:
            console.print(f"[red]Perdiste {apuesta}[/red]")
            dinero -= apuesta
        else:
            console.print("[yellow]Empate 🤝[/yellow]")

    console.print(f"\nSaldo final: [bold green]{dinero}[/bold green]")
    return dinero


def set_log():
    logging.basicConfig(
        filename="./blackjack.log",
        filemode="w",       # "w" sobreescribe en cada ejecución, "a" para append
        level=logging.INFO, # Nivel mínimo (INFO, DEBUG, WARNING...)
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8" 
    )
    

if __name__ == "__main__":
    set_log()
    
    use_log = False
    estrategia = None
    dias_exitosos = 0
    dias_fallidos = 0
    dias = int(input('¿Cuantos días quieres simular? '))
    bot = input('¿Quieres simular una estrategia? (s/n)') == 's'
    if bot:
        use_log = input('¿Quieres imprimir los logs por pantalla? (s/n)') != 's'
        estrategia = input('¿Qué estrategia quieres que utilice el bot? \n 1:Random \n 2:Mayor que 18.55 \n 3:Estrategia básica \n')
        if estrategia == '1':
            estrategia = get_random_decision
        elif estrategia == '2':
            estrategia = get_simple_decision
        else:
            estrategia = get_best_option
    
    out = logging.info if use_log else print
    juego = jugar_blackjack if bot else jugar_blackjack_rich

    cuenta_bancaria = 100

    for i in range(dias):
        manos_ganadas  = 0
        manos_perdidas = 0
        jugar = True
        cuenta_bancaria = cuenta_bancaria - 10

        dinero = 10
        while dinero > 1 and jugar:
            dinero_result = juego(dinero, use_log, estrategia)
            if dinero_result > dinero:
                manos_ganadas += 1
            elif dinero_result < dinero:
                manos_perdidas += 1
            dinero = dinero_result
            if dinero <= 1:
                out("\nTe quedaste sin dinero. 💸")
                out(f'Día {i+1}: Manos perdidas: {manos_perdidas}, Manos ganadas: {manos_ganadas}')
                dias_fallidos += 1
                jugar = False
            elif dinero >= 20:
                out("\n¡Doblaste tu dinero!. 💸💸💸")
                out(f'Día {i+1}: Manos perdidas: {manos_perdidas}, Manos ganadas: {manos_ganadas}')
                dias_exitosos += 1
                jugar = False
            if not bot: input('Pulsa Enter para continuar...')
        cuenta_bancaria = cuenta_bancaria + dinero

        # Mostrar progreso cada 1%
        if (i + 1) % max(1, dias // 100) == 0:
            progreso = round((i + 1) * 100 / dias, 2)
            print(f"Progreso: {progreso}%, cuenta bancaria: {cuenta_bancaria}")

    logging.info(f'Fin de la simulación: Días exitosos: {100*dias_exitosos/dias}%, cuenta bancaria: {cuenta_bancaria}')
    print(f'Fin de la simulación: Días exitosos: {100*dias_exitosos/dias}%, cuenta bancaria: {cuenta_bancaria}')

