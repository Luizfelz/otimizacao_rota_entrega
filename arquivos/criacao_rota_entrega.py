import googlemaps
import folium
from datetime import datetime
from arquivos.tratamento_df_completo import df_completo

def criacao_rota_entrega():
  arquivo = open('./api_key.txt')
  chave_api = str(arquivo.read())
  chave_api = chave_api.replace("'",'')
  arquivo.close()

  gmaps = googlemaps.Client(key=chave_api)

  waypoints = []
  nome_waypoints = []
  id_waypoints = []

  for linha in range(df_completo.shape[0]):
    waypoints.append((df_completo['LATITUDE'][linha], df_completo['LONGITUDE'][linha]))
    nome_waypoints.append(df_completo['NOME_INSTITUICAO'][linha])
    id_waypoints.append(df_completo['ID_INSTITUICAO'][linha])

  # Descomentar a linha abaixo fará com que somente 25 cidades sejam consideradas para otimização da rota
  # waypoints = waypoints[0:25]

  particao = 25
  directions = []
  pares_waypoints = []

  for i in range(0, len(waypoints), particao):
    chunk_waypoints = waypoints[i:i+particao]
    chunk_id_waypoints = id_waypoints[i:i+particao]
    chunk_directions = gmaps.directions(
                            origin=chunk_waypoints[0],
                            destination=chunk_waypoints[-1],
                            mode="driving",  # opções: "walking", "bicycling", "transit"
                            waypoints=chunk_waypoints[0:],
                            optimize_waypoints=True,
                            departure_time=datetime.now(),
                            )
    directions.extend(chunk_directions)
    pares_waypoints.append(list(zip(chunk_directions[0]['waypoint_order'],chunk_id_waypoints)))

  i = 0
  locais = []
  for lat, lng in waypoints:
    rotulo = nome_waypoints[i]
    locais.append((lat, lng, rotulo))
    i += 1

  m = folium.Map(location=(sum([lat for lat, _, _ in locais]) / len(locais),\
                      sum([lng for _, lng, _ in locais]) / len(locais)),\
                zoom_start=10)

  for lat, lng, rotulo in locais:
    folium.Marker([lat, lng], popup=rotulo).add_to(m)

  m.save('./otimizacao_de_rota/mapa_marcado.html')

  return pares_waypoints, waypoints

pares_waypoints, waypoints = criacao_rota_entrega()