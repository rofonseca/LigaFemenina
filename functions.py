import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def shooting(local_path, visit_path):
    df = pd.read_csv(local_path)
    FG = df['2PA'].sum()+df['3PA'].sum()
    P3 = df['3PA'].sum()
    FGA = df['2P'].sum()+df['3P'].sum()
    offense = (FG+0.5*P3)/FGA
    df = pd.read_csv(visit_path)
    FG = df['2PA'].sum()+df['3PA'].sum()
    P3 = df['3PA'].sum()
    FGA = df['2P'].sum()+df['3P'].sum()
    defense = (FG+0.5*P3)/FGA
    return offense, defense

def turnover(local_path, visit_path):
    df = pd.read_csv(local_path)
    TOV = df['TOV'].sum()
    FTA = df['FT'].sum()
    FGA = df['2P'].sum()+df['3P'].sum()
    offense = TOV/(FGA+0.44*FTA+TOV)
    df = pd.read_csv(visit_path)
    TOV = df['TOV'].sum()
    FTA = df['FT'].sum()
    FGA = df['2P'].sum()+df['3P'].sum()
    defense = TOV/(FGA+0.44*FTA+TOV)
    return offense, defense

def rebounding(local_path, visit_path):
    df = pd.read_csv(local_path)
    df_op = pd.read_csv(visit_path)
    ORB = df['ORB'].sum()
    DRB = df['DRB'].sum()
    ORB_op = df_op['ORB'].sum()
    DRB_op = df_op['DRB'].sum()
    offense = ORB/(ORB+DRB_op)
    defense = DRB/(ORB_op+DRB)
    return offense, defense

def free_throws(local_path, visit_path):
    df = pd.read_csv(local_path)
    FT = df['FTA'].sum()
    FGA = df['FT'].sum()
    offense = FT/FGA
    df = pd.read_csv(visit_path)
    FT = df['FTA'].sum()
    FGA = df['FT'].sum()
    defense = FT/FGA
    return offense, defense

def four_factors(local_path, visit_path):
    df = pd.read_csv(local_path)
    df_op = pd.read_csv(visit_path)
    FG = df['2PA'].sum()+df['3PA'].sum()
    P3 = df['3PA'].sum()
    FGA = df['2P'].sum()+df['3P'].sum()
    TOV = df['TOV'].sum()
    FTA = df['FT'].sum()
    ORB = df['ORB'].sum()
    DRB = df['DRB'].sum()
    FT = df['FTA'].sum()

    FG_op = df_op['2PA'].sum()+df_op['3PA'].sum()
    P3_op = df_op['3PA'].sum()
    FGA_op = df_op['2P'].sum()+df_op['3P'].sum()
    TOV_op = df_op['TOV'].sum()
    FTA_op = df_op['FT'].sum()
    ORB_op = df_op['ORB'].sum()
    DRB_op = df_op['DRB'].sum()
    FT_op = df_op['FTA'].sum()

    shoot_offense = (FG + 0.5*P3)/FGA
    shoot_defense = (FG_op + 0.5*P3_op)/FGA_op
    turn_offense = TOV/(FGA+0.44*FTA+TOV)
    turn_defense = TOV_op/(FGA_op+0.44*FTA_op+TOV_op)
    rb_offense = ORB/(ORB+DRB_op)
    rb_defense = DRB/(ORB_op+DRB)
    free_offense = FT/FGA
    free_defense = FT_op/FGA_op

    return shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense

def show_four_factors(local_path, visit_path):
    [shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense] = four_factors(local_path, visit_path)

    print('shooting offensive: ', shoot_offense)
    print('shooting defensive: ', shoot_defense)
    print('turnover offensive: ', turn_offense)
    print('turnover defensive: ', turn_defense)
    print('rebounding offensive: ', rb_offense)
    print('rebounding defensive: ', rb_defense)
    print('Free throws offensive: ', free_offense)
    print('Free throws defense: ', free_defense)

def show_four_factor_tabla(array):
    data = {
    "shooting": [array[0], array[1]],
    "turnover": [array[2], array[3]],
    "rebounding": [array[4], array[5]],
    "Free throws": [array[6], array[7]]
    }
    # Crear un DataFrame de pandas con las filas 'offensive' y 'defensive'
    df = pd.DataFrame(data, index=["offensive", "defensive"])
    # Mostrar la tabla
    print(df)


def analisis_libres_temporada(df, fecha):
    title_general = 'Análisis de Tiros Libres por Partido hasta la fecha \n' + fecha
    plt.figure(figsize=(12, 8))
    # Título general
    plt.suptitle(title_general, fontsize=16)
    j = 0
    for i in df['Date'].unique():
        j = j+1
        df_fec = df[df['Date'] == i]
        scored = df_fec['Free throws scored'].sum()
        not_scored = df_fec['Free throws I.P.P.'].sum() - scored
        labels = ['Tiros Libres Acertados', 'Tiros Libres Errados']
        sizes = [scored, not_scored]
        colors = ['#f2231d', '#565252']
        explode = (0.1, 0)  # Solo resaltar el primer segmento
        plt.subplot(2,4,j)
        wedges, texts, autotexts = plt.pie(sizes, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
        # Personalizar los textos de los porcentajes
        for text in autotexts:
            text.set_color('white')  # Cambiar el color a blanco
            text.set_fontsize(16)    # Ajustar el tamaño de la fuente


        plt.axis('equal')
    plt.legend(wedges, labels,  loc="best",
           prop={'size': 12})
    plt.show()

def throws(df, tipo):
  if tipo=='free':
    column = 'Free throws I.P.P.'
    column_scored = 'Free throws scored'
    title = 'Tiros libres por partido'
    y_label = 'Tiros libres por partido'
  elif tipo=='double':
    column = '2P throws I.P.P.'
    column_scored = '2P throws scored'
    title = 'Dobles por partido'
    y_label = 'Dobles por partido'
  else:
    column = '3P throws I.P.P.'
    column_scored = '3P throws scored'
    title = 'Triples por partido'
    y_label = 'Triples por partido'
  plt.figure(figsize=(10, 6))
  plt.bar(df['Player'], df[column],color='grey', alpha=0.7, label='Puntos tirados')
  plt.bar(df['Player'], df[column_scored],color='red', alpha=0.7, label='Puntos convertidos')
  plt.xlabel('Jugadores')
  plt.ylabel(y_label)
  plt.title(title)
  plt.legend()
  plt.xticks(rotation=45)
  plt.show()

def variable_per_player(df, var):
    if var == 'Total points':
        y_label = 'Puntos por partido'
        title = 'Puntos por jugador'
    elif var == 'Minutes':
        y_label = 'Minutos jugados por partido'
        title = 'Minutos jugados por jugador'
    elif var == 'Total Rebound':
        y_label = 'Rebotes por partido'
        title = 'Rebotes por jugador'
    elif var == 'Asistences':
        y_label = 'Asistencias por partido'
        title = 'Asistencias por jugador'
    elif var == 'Recover':
        y_label = 'Recuperaciones por partido'
        title = 'Recuperaciones por jugador'
    elif var == 'Turnover':
        y_label = 'Pérdidas por partido'
        title = 'Pérdidas por jugador'

    plt.figure(figsize=(10, 6))
    plt.bar(df['Player'], df[var], color='red')
    plt.xlabel('Jugadores')
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()

def scored_team(df, tipo):
    if tipo == 'free':
        scored = df['Free throws scored'].sum()
        not_scored = df['Free throws I.P.P.'].sum() - scored
        labels = ['Tiros Libres Acertados', 'Tiros Libres Errados']
        title = 'Tiros Libres Acertados vs Errados'
    elif tipo == 'double':
        scored = df['2P throws scored'].sum()
        not_scored = df['2P throws I.P.P.'].sum() - scored
        labels = ['Dobles Acertados', 'Dobles Errados']
        title = 'Dobles Acertados vs Errados'
    else:
        scored = df['3P throws scored'].sum()
        not_scored = df['3P throws I.P.P.'].sum() - scored
        labels = ['Triples Acertados', 'Triples Errados']
        title = 'Triples Acertados vs Errados'
    sizes = [scored, not_scored]
    colors = ['#f2231d', '#565252']
    explode = (0.1, 0)  # Solo resaltar el primer segmento

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.title(title)
    plt.axis('equal')  # Para que el gráfico sea un círculo
    plt.show()

def all_graphs_for_match(df):
    variable_per_player(df, 'Total points')
    variable_per_player(df, 'Minutes')
    variable_per_player(df, 'Total Rebound')
    variable_per_player(df, 'Asistences')
    variable_per_player(df, 'Recover')
    variable_per_player(df, 'Turnover')
    throws(df, 'free')
    throws(df, 'double')
    scored_team(df, '3P')

def puntos_por_partido(df,fecha):

  title_general = 'Análisis de Tiros por Partido \n' + fecha
  column = 'FT'
  column_scored = 'FTA'
  title = 'Tiros libres por partido'
  plt.figure(figsize=(12, 18))
  # Título general
  plt.suptitle(title_general, fontsize=16)

  plt.subplot(3, 2, 1)
  plt.barh(df['Jugadores'], df[column], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  # Beige claro
  plt.barh(df['Jugadores'], df[column_scored], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
  plt.ylabel('Jugadores', fontsize=14)
  plt.title(title, fontsize=14)
  plt.legend()
  plt.gca().spines['top'].set_visible(False)
  plt.gca().spines['right'].set_visible(False)

  column = '2P'
  column_scored = '2PA'
  title = 'Dobles por partido'
  plt.subplot(3, 2, 3)
  plt.barh(df['Jugadores'], df[column], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  # Beige claro
  plt.barh(df['Jugadores'], df[column_scored], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
  plt.ylabel('Jugadores', fontsize=14)
  plt.title(title, fontsize=14)
  plt.legend()
  plt.gca().spines['top'].set_visible(False)
  plt.gca().spines['right'].set_visible(False)

  column = '3P'
  column_scored = '3PA'
  title = 'Triples por partido'
  plt.subplot(3, 2, 5)
  plt.barh(df['Jugadores'], df[column], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  # Beige claro
  plt.barh(df['Jugadores'], df[column_scored], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
  plt.ylabel('Jugadores', fontsize=14)
  plt.title(title, fontsize=14)
  plt.legend(loc="center right")
  plt.gca().spines['top'].set_visible(False)
  plt.gca().spines['right'].set_visible(False)

  scored = df['FTA'].sum()
  not_scored = df['FT'].sum() - scored
  labels = ['Tiros Libres Acertados', 'Tiros Libres Errados']
  title = 'Tiros Libres Acertados vs Errados'
  sizes = [scored, not_scored]
  colors = ['#f2231d', '#565252']
  plt.subplot(3, 2, 2)
  wedges, texts, autotexts = plt.pie(sizes, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
  # Personalizar los textos de los porcentajes
  for text in autotexts:
    text.set_color('white')  # Cambiar el color a blanco
    text.set_fontsize(16)    # Ajustar el tamaño de la fuente

  plt.legend(wedges, labels,  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
           prop={'size': 12})

  plt.title(title, fontsize=14)
  plt.axis('equal')

  scored = df['2PA'].sum()
  not_scored = df['2P'].sum() - scored
  labels = ['Dobles Acertados', 'Dobles Errados']
  title = 'Dobles Acertados vs Errados'
  sizes = [scored, not_scored]
  colors = ['#f2231d', '#565252']
  plt.subplot(3, 2, 4)
  wedges, texts, autotexts = plt.pie(sizes, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
  # Personalizar los textos de los porcentajes
  for text in autotexts:
    text.set_color('white')  # Cambiar el color a blanco
    text.set_fontsize(16)    # Ajustar el tamaño de la fuente

  plt.legend(wedges, labels,  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
           prop={'size': 12})

  plt.title(title, fontsize=14)
  plt.axis('equal')

  scored = df['3PA'].sum()
  not_scored = df['3P'].sum() - scored
  labels = ['Triples Acertados', 'Triples Errados']
  title = 'Triples Acertados vs Errados'
  sizes = [scored, not_scored]
  colors = ['#f2231d', '#565252']
  plt.subplot(3, 2, 6)
  wedges, texts, autotexts = plt.pie(sizes, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
  # Personalizar los textos de los porcentajes
  for text in autotexts:
    text.set_color('white')  # Cambiar el color a blanco
    text.set_fontsize(16)    # Ajustar el tamaño de la fuente

  plt.legend(wedges, labels,  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
           prop={'size': 12})

  plt.title(title, fontsize=14)
  plt.axis('equal')

  plt.tight_layout(rect=[0, 0, 1, 0.96])
  plt.show()

def por_partido(df,fecha):     

    title_general = 'Análisis por Partido \n' + fecha

    plt.figure(figsize=(16,24))
    # Título general
    plt.suptitle(title_general, fontsize=16)
    plt.subplot(4, 2, 1)
    df['Min'] = pd.to_datetime(df['Min'], format='%M:%S').dt.minute + pd.to_datetime(df['Min'], format='%M:%S').dt.second / 60
    plt.barh(df['Jugadores'], df['Min'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Minutos jugados por jugador')

    plt.subplot(4, 2, 2)
    plt.barh(df['Jugadores'], df['AST'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Asistencias por jugador')

    plt.subplot(4, 2, 3)
    plt.barh(df['Jugadores'], df['ROB'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Recuperaciones por jugador')

    plt.subplot(4, 2, 4)
    plt.barh(df['Jugadores'], df['TOV'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Pérdidas por jugador')

    plt.subplot(4, 2, 5)
    plt.barh(df['Jugadores'], df['ORB'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Rebotes ofensivos por jugador')

    plt.subplot(4, 2, 6)
    plt.barh(df['Jugadores'], df['DRB'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Rebotes defensivos por jugador')

    plt.subplot(4, 2, 7)
    plt.barh(df['Jugadores'], df['TAP'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Bloqueos hechos por jugador')


    plt.subplot(4, 2, 8)
    plt.barh(df['Jugadores'], df['FP'], color='red')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylabel('Jugadores')
    plt.title('Faltas realizadas por jugador')


    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def por_jugador(df, jugador):

    title_general = 'Análisis por Partido \n' + jugador
    df = df[df['Jugadora'] == jugador]
    plt.figure(figsize=(16, 24))
    # Título general
    plt.suptitle(title_general, fontsize=16)

    plt.subplot(5, 2, 1)
    plt.bar(df['Fecha'], df['FT'], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  
    plt.bar(df['Fecha'], df['FTA'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Tiros libres por partido')
    plt.legend()

    plt.subplot(5, 2, 2)
    plt.bar(df['Fecha'], df['2P'], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  
    plt.bar(df['Fecha'], df['2PA'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Dobles por partido')
    plt.legend()

    plt.subplot(5, 2, 3)
    plt.bar(df['Fecha'], df['3P'], color='#565252', edgecolor='black', alpha=0.7, label='Puntos tirados')  
    plt.bar(df['Fecha'], df['3PA'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Triples por partido')
    plt.legend()

    plt.subplot(5, 2, 4)
    plt.plot(df['Fecha'], df['Puntos'], 'ro-')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Puntos por partido')

    plt.subplot(5, 2, 5)
    plt.bar(df['Fecha'], df['AST'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Asistencias por partido')

    plt.subplot(5, 2, 9)
    plt.bar(df['Fecha'], df['REB'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fechas')
    plt.title('Rebotes (totales) por partido')

    plt.subplot(5, 2, 6)
    plt.bar(df['Fecha'], df['ROB'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fecha')
    plt.title('Recuperaciones por partido')

    plt.subplot(5, 2, 7)
    plt.bar(df['Fecha'], df['TOV'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fecha')
    plt.title('Pérdidas por partido')

    plt.subplot(5, 2, 8)
    plt.bar(df['Fecha'], df['FP'], color='#f2231d', edgecolor='black', alpha=1, label='Puntos convertidos')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel('Fecha')
    plt.title('Faltas cometidas por partido')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def puntos_historicos_algunos(df, jugadores):
  plt.figure(figsize=(10,6))
  # Establecer un ciclo de colores usando un colormap
  plt.gca().set_prop_cycle(color=plt.cm.tab20.colors)  # Usa hasta 20 colores diferentes
  for i in jugadores:
    df_player = df[df['Player'] == i]
    plt.plot(df_player['Date'], df_player['Total points'], 'o-', label=i)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
  plt.xlabel('Fechas')
  plt.ylabel('Puntos totales')
  plt.title('Puntos en la temporada')
  #plt.legend(title='Jugadores')
  # Agregar líneas horizontales de guía
  plt.grid(axis='y', linestyle='--', linewidth=0.5, color='gray')
  # Ajustar la leyenda para que esté fuera del gráfico, a la derecha
  plt.legend(title="Jugadores", bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()  # Ajusta la figura para que no se corte la leyenda
  plt.show

def puntos_historicos(df):
  plt.figure(figsize=(10,6))
  # Establecer un ciclo de colores usando un colormap
  plt.gca().set_prop_cycle(color=plt.cm.tab20.colors)  # Usa hasta 20 colores diferentes

  for i in df['Player'].unique():
    df_player = df[df['Player'] == i]
    plt.plot(df_player['Date'], df_player['Total points'], 'o-', label=i)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
  plt.xlabel('Fechas')
  plt.ylabel('Puntos totales')
  plt.title('Puntos en la temporada')
  #plt.legend(title='Jugadores')
  # Ajustar la leyenda para que esté fuera del gráfico, a la derecha
  plt.legend(title="Jugadores", bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()  # Ajusta la figura para que no se corte la leyenda
  plt.show

def maximo_puntos_historico(df):
  for i in df['Date'].unique():
    df_fec = df[df['Date'] == i]
    max_valor = df_fec['Total points'].max()
    pos = df_fec['Total points'].idxmax()
    jug = df_fec['Player'][pos]
    print('Fecha: ', i)
    print('Jugador con más puntos: ', jug)
    print('Puntos hechos: ', max_valor)
    print('----------------')

