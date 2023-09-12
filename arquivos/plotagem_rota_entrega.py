import matplotlib.pyplot as plt
from arquivos.criacao_rota_entrega import waypoints

def plotagem_rota_entrega():
  plt.figure(figsize=(15, 8))
  x = []
  y = []

  for i in range(len(waypoints)):
    x.append(waypoints[i][1])
    y.append(waypoints[i][0])

  plt.scatter(x, y, color='blue', label='Waypoints', s=50, zorder=2)
  plt.plot(x, y, linestyle='-', color='gray', linewidth=2, alpha=0.7, zorder=1)

  for i, (x_val, y_val) in enumerate(zip(x, y)):
      plt.annotate(f'{i}', (x_val, y_val), textcoords="offset points", xytext=(0,10), ha='center')

  plt.title('Rota de entrega otimizada')
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.grid(True, linestyle='--', alpha=0.5)
  plt.legend()
  plt.savefig('./otimizacao_de_rota/rota_entrega_otimizada.png')