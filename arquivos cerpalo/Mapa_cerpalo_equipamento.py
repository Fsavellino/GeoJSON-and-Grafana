import folium
import json
import requests
import os
import webbrowser

# URL do GeoJSON com os estados do Brasil
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

# Baixar arquivo GeoJSON
response = requests.get(geojson_url)
geojson_data = response.json()

# Criar um mapa centralizado em Santa Catarina
m = folium.Map(location=[-27.2423, -50.2189], zoom_start=7)

# Adicionar a camada base de Santa Catarina
folium.GeoJson(
    geojson_data,
    name="Santa Catarina",
    style_function=lambda feature: {
        "fillColor": "lightgray",
        "color": "black",
        "weight": 1.5,
        "fillOpacity": 0.3
    }
).add_to(m)

# Definição das camadas
geojson_files = {
    "Compensador de Reativo Baixa Tensão": {"file": "UNCRMT.geojson", "color": "red"},
    "Reguladora": {"file": "UNREMT.geojson", "color": "orange"},
    "Seccionador Média tensão": {"file": "UNSEMT.geojson", "color": "blue"},
    "Trafo Média tensão": {"file": "UNTRMT.geojson", "color": "purple"},  
}

# Carregar arquivos e adicionar pontos com CircleMarker
for nome, info in geojson_files.items():
    if os.path.exists(info["file"]):
        try:
            with open(info["file"], encoding="utf-8") as f:
                geojson_data_local = json.load(f)

            camada = folium.FeatureGroup(name=nome)

            for feature in geojson_data_local["features"]:
                coords = feature["geometry"]["coordinates"]
                latitude, longitude = coords[1], coords[0]

                folium.CircleMarker(
                    location=[latitude, longitude],
                    radius=2,  # Tamanho do ponto
                    color=info["color"],
                    fill=True,
                    fill_color=info["color"],
                    fill_opacity=0.8,
                    popup=folium.Popup(f"{nome} - Ponto", parse_html=True),
                ).add_to(camada)

            camada.add_to(m)
            print(f"✅ Arquivo {info['file']} ({nome}) carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar o arquivo {info['file']}: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {info['file']}")

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Salvar o mapa como HTML
output_file = "mapa_cerpalo_equipamento.html"
m.save(output_file)

# Abrir o mapa automaticamente no navegador
webbrowser.open("file://" + os.path.abspath(output_file))

print(f"\n✅ Mapa salvo como {output_file} e aberto no navegador.")
