# Blackjack en Python 🃏

Este proyecto es una implementación del clásico juego de **Blackjack** en Python, con soporte para jugar manualmente o mediante un bot con distintas estrategias de decisión. Además, incluye visualización avanzada usando la librería `rich` y registro de logs de las partidas.  

---

## Características

- Juego completo de **Blackjack** con:
  - Pedir carta
  - Quedarse
  - Doblar apuesta
  - Dividir pareja (split)
- Bot opcional con tres estrategias:
  - Aleatoria
  - Básica (pide si es menor que 18.55)
  - Estrategia avanzada (basada en mejores opciones)
- Visualización en consola con colores y paneles (`rich`)
- Registro de partidas en `blackjack.log`
- Simulación de múltiples días con seguimiento de ganancias y pérdidas

---

## Requisitos

- Python 3.10+
- Librerías:
  ```bash
  pip install rich
  ```

---

## Estructura del Proyecto

- `blackjack.py` → Archivo principal con la lógica del juego
- `bj_bot.py` → Contiene funciones de decisiones automáticas del bot
- `bj_utils.py` → Funciones auxiliares (`valor_mano`, `valor_carta`)
- `blackjack.log` → Archivo donde se registran las partidas (si se habilita el log)

---

## Uso

### Juego interactivo manual

Ejecuta el script principal:

```bash
python blackjack.py
```

Se te pedirá:

1. Cantidad de días a simular.
2. Si quieres usar un bot o jugar manualmente.
3. Apuestas y decisiones durante el juego.

### Uso de bot

Si eliges usar un bot:

1. Decide si quieres mostrar logs en consola.
2. Selecciona la estrategia:
   - `1` → Aleatoria
   - `2` → Simple (mayor que 18.55)
   - `3` → Estrategia básica

El bot jugará automáticamente siguiendo la estrategia seleccionada y registrará resultados.

---

## Funciones Principales

- `jugar_blackjack(dinero, use_log=True, funcion=None)` → Juego básico, compatible con bot.
- `jugar_blackjack_rich(dinero, use_log=False, funcion=None)` → Juego con visualización avanzada.
- `crear_baraja()` → Genera y mezcla un mazo de 52 cartas.
- `mostrar_mano(mano, ocultar_primera=False)` → Muestra la mano del jugador o del crupier.
- `set_log()` → Configura el registro de partidas en `blackjack.log`.

---

## Ejemplo de ejecución

```python
python blackjack.py
```

Salida en consola (resumida):

```
🃏 ¡Bienvenido al Blackjack! 🃏
Tu saldo: 100
¿Cuánto quieres apostar?: 10

Mano 1: [10♠] [7♥] Total: 17 | Apuesta: 10
Mano del crupier: [?] [K♦]

Elige una acción (p/q/d/s): p
...
¡Ganaste 10! 🥳
Saldo final: 110
```

---

## Licencia

Este proyecto es **libre** para uso personal y educativo.

