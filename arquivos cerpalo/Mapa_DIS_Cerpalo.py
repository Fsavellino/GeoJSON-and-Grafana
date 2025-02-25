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

# Definição das camadas de LINHAS (Alta, Média e Baixa Tensão)
geojson_files = {
    "Alta Tensão": {"file": "ARAT-Cerpalo.geojson", "color": "red"},
    "Média Tensão": {"file": "ARAT-Celesc.geojson", "color": "black"},
    "Baixa Tensão": {"file": "SSDBT.geojson", "color": "blue"},
}

# Verifica se os arquivos existem antes de tentar carregar
for nome, info in geojson_files.items():
    if os.path.exists(info["file"]):  # Verifica se o arquivo existe
        try:
            with open(info["file"], encoding="utf-8") as f:
                geojson_data_local = json.load(f)

            folium.GeoJson(
                geojson_data_local,
                name=nome,
                style_function=lambda feature, cor=info["color"]: {
                    "color": cor,
                    "weight": 3,  # Espessura da linha
                    "opacity": 10
                }
            ).add_to(m)

            print(f"✅ Arquivo {info['file']} ({nome}) carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar o arquivo {info['file']}: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {info['file']}")

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Salvar o mapa como HTML
output_file = "mapa_cerpalo_rede_de_distribuicao.html"
m.save(output_file)

# Abrir o mapa automaticamente no navegador
webbrowser.open("file://" + os.path.abspath(output_file))

print(f"\n✅ Mapa salvo como {output_file} e aberto no navegador.")
