import random

# Dimensiones del laberinto
n = 5
m = 5

# Inicializar laberinto
laberinto = [[' ' for _ in range(m)] for _ in range(n)]

# Posiciones iniciales
raton_pos = (random.randint(0, n-1), random.randint(0, m-1))
gato_pos = (random.randint(0, n-1), random.randint(0, m-1))
salida_pos = (random.randint(0, n-1), random.randint(0, m-1))

# Asegurarse de que el ratón, el gato y la salida no están en la misma posición inicialmente
while gato_pos == raton_pos or gato_pos == salida_pos or raton_pos == salida_pos:
    raton_pos = (random.randint(0, n-1), random.randint(0, m-1))
    gato_pos = (random.randint(0, n-1), random.randint(0, m-1))
    salida_pos = (random.randint(0, n-1), random.randint(0, m-1))


def imprimir_laberinto():
    for i in range(n):
        for j in range(m):
            if (i, j) == raton_pos:
                print('R', end=' ')
            elif (i, j) == gato_pos:
                print('G', end=' ')
            elif (i, j) == salida_pos:
                print('S', end=' ')
            else:
                print('.', end=' ')
        print()
    print()


def mover_random(pos):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    movimiento = random.choice(movimientos)
    nueva_pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
# Verifico si la nueva posición está dentro de los límites del laberinto.
    if 0 <= nueva_pos[0] < n and 0 <= nueva_pos[1] < m:
        return nueva_pos
    else:
        return pos


def minimax(pos_raton, pos_gato, depth, is_raton_turn):
    if depth == 0 or pos_raton == pos_gato or pos_raton == salida_pos:
        if pos_raton == pos_gato:
            return -1  # El gato gana
        elif pos_raton == salida_pos:
            return 1  # El ratón gana
        else:
            return 0  # Empate o profundidad alcanzada

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if is_raton_turn:

        # Inicializo max_eval con un valor muy bajo (negativo infinito) para buscar el valor máximo posible.
        max_eval = float('-inf')
        for movimiento in movimientos:
            # Calculo la nueva posición del ratón al aplicar el movimiento actual
            nueva_pos = (pos_raton[0] + movimiento[0],
                         pos_raton[1] + movimiento[1])
            # Verifica si la nueva posición está dentro de los límites del tablero
            if 0 <= nueva_pos[0] < n and 0 <= nueva_pos[1] < m:
                # Llama recursivamente a minimax con la nueva posición del ratón
                # la posición actual del gato, una profundidad reducida en 1, y cambiando el turno al gato (False)
                eval = minimax(nueva_pos, pos_gato, depth-1, False)
                # con el valor máximo entre el valor actual y la evaluación retornada por la llamada recursiva
                max_eval = max(max_eval, eval)
        # Devuelve la evaluación máxima encontrada.
        return max_eval
    else:
        # Inicializo min_eval con un valor muy alto (positivo infinito) para buscar el valor mínimo posible
        min_eval = float('inf')
        for movimiento in movimientos:
            # Calcula la nueva posición del gato al aplicar el movimiento actual.
            nueva_pos = (pos_gato[0] + movimiento[0],
                         pos_gato[1] + movimiento[1])
            # Verifico si la nueva posición está dentro de los límites del tablero
            if 0 <= nueva_pos[0] < n and 0 <= nueva_pos[1] < m:
                # Llama recursivamente a minimax con la posición actual del ratón
                # la nueva posición del gato, una profundidad reducida en 1, y cambiando el turno al ratón (True).
                eval = minimax(pos_raton, nueva_pos, depth-1, True)
                # con el valor mínimo entre el valor actual y la evaluación retornada por la llamada recursiva.
                min_eval = min(min_eval, eval)
        # Devuelve la evaluación mínima encontrada.
        return min_eval


def mejor_movimiento(pos_raton, pos_gato, is_raton_turn):
    mejor_mov = None
    # con negativo infinito si es el turno del ratón (buscando maximizar) o
    # con positivo infinito si es el turno del gato (buscando minimizar).
    mejor_eval = float('-inf') if is_raton_turn else float('inf')
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for movimiento in movimientos:
        # Calculo la nueva posición dependiendo de si es el turno del ratón o del gato.
        nueva_pos = (pos_raton[0] + movimiento[0], pos_raton[1] + movimiento[1]
                     ) if is_raton_turn else (pos_gato[0] + movimiento[0], pos_gato[1] + movimiento[1])
        # Verifico si la nueva posición está dentro de los límites del tablero
        if 0 <= nueva_pos[0] < n and 0 <= nueva_pos[1] < m:
            # Llama a minimax para evaluar el movimiento, con una profundidad de 2 y alternando el turno.
            eval = minimax(nueva_pos, pos_gato, 2, not is_raton_turn) if is_raton_turn else minimax(
                pos_raton, nueva_pos, 2, not is_raton_turn)
            # Actualiza mejor_eval y mejor_mov si la evaluación actual
            # es mejor que la anterior (máximo para el ratón, mínimo para el gato).
            if (is_raton_turn and eval > mejor_eval) or (not is_raton_turn and eval < mejor_eval):
                #: Actualiza la mejor evaluación.
                mejor_eval = eval
                # Actualiza el mejor movimiento.
                mejor_mov = nueva_pos
    # Devuelve la mejor posición encontrada para el siguiente movimiento del ratón o el gato.
    return mejor_mov


# Ciclo principal del juego
max_movimientos = 100  # Limitar el número de movimientos para evitar bucles infinitos
contador_movimientos = 0

while contador_movimientos < max_movimientos:
    imprimir_laberinto()

    if raton_pos == gato_pos:
        print("¡El gato atrapó al ratón! El gato gana.")
        break
    elif raton_pos == salida_pos:
        print("¡El ratón encontró la salida! El ratón gana.")
        break

    # Estrategia inteligente
    nueva_raton_pos = mejor_movimiento(raton_pos, gato_pos, True)
    if nueva_raton_pos:
        raton_pos = nueva_raton_pos

    nueva_gato_pos = mejor_movimiento(raton_pos, gato_pos, False)
    if nueva_gato_pos:
        gato_pos = nueva_gato_pos

    contador_movimientos += 1

if contador_movimientos >= max_movimientos:
    print("El juego ha terminado en un empate debido al límite de movimientos.")
