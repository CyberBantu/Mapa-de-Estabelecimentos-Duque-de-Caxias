import streamlit as st
import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
import plotly.express as px

def main():
    # Carregar dados
    st.title('Analise espacial de estabelecimentos e moradias no Municipio de Duque de Caxias')
    end = pd.read_csv('base_completa_estabelecimento.csv', sep=';')
    caxias = geopandas.read_file('mapa_caxias.shp')

    # Converter dados de endereço em GeoDataFrame
    geometry = [Point(xy) for xy in zip(end['LONGITUDE'], end['LATITUDE'])]
    end = GeoDataFrame(end, geometry=geometry)

    # Adicionar um filtro para a coluna COD_ESPECIE ---------------------
    # Mapemamento de estabelecimentos
    cod_especie_map = {
        1: 'Domicílio Particular',
        2: 'Domicílio Coletivo',
        3: "Estabelecimento agropecuário",
        4: "Estabelecimento de ensino",
        5: "Estabelecimento de saúde",
        6: "Estabelecimento de outras finalidades",
        7: "Edificação em construção ou reforma",
        8: "Estabelecimento religioso"
    }

    cod_tipo_domicilio = {
        101:'Casa',
        102: 'Casa de vila ou em condomínio',
        103: 'Apartamento',
        104: 'Outros',
    }
    # Distritos
    localidades = {
        330170210: "Campos Elysios",
        330170220: "Xerém",
        330170215: "Imbariê",
        330170205: "Centro"
    }

    # Mapear os códigos para as descrições
    end['COD_ESPECIE_DESC'] = end['COD_ESPECIE'].map(cod_especie_map)
    end['COD_TIPO_ESPECIE_DESC'] = end['COD_TIPO_ESPECI'].map(cod_tipo_domicilio)
    end['COD_DISTRITO_DESC'] = end['COD_DISTRITO'].map(localidades)



    # Criação dos elementos da barra lateral com a opção inicial inclusa
    especie = st.sidebar.selectbox("Selecione o Tipo de Domicílio ou Estabelecimento:", list(end['COD_ESPECIE_DESC'].unique()))


    # Filtrar os dados baseado na seleção
    end_filtered = end[end['COD_ESPECIE_DESC'] == especie]
    end_filtered['COD_TIPO_ESPECIE_DESC'].fillna('Não se aplica', inplace=True)
    end_filtered['DSC_ESTABELECIMENTO'].fillna('Não se aplica', inplace=True)

    # Cri o plot
    fig = px.scatter_mapbox(end_filtered,
                            lat=end_filtered.geometry.y,
                            lon=end_filtered.geometry.x,
                            hover_name="DSC_LOCALIDADE",  
                            hover_data={"DSC_LOCALIDADE": False, 'NOM_SEGLOGR': False},
                            color='COD_TIPO_ESPECIE_DESC',  
                            color_continuous_scale=px.colors.qualitative.Plotly,  
                            custom_data=['DSC_LOCALIDADE', 'COD_DISTRITO_DESC','NOM_SEGLOGR', 'DSC_ESTABELECIMENTO'],
                            labels={'COD_TIPO_ESPECIE_DESC': 'Tipo de Moradia'},
                            zoom=10,
                            height=700,
                            width = 1000)

    fig.update_traces(hovertemplate="<b>Bairro:</b> %{customdata[0]}<br>Distrito: %{customdata[1]}<br>Nome da Rua ou Bairro: %{customdata[2]} <br>Nome de Estabelecimento: %{customdata[3]}")
    # Atualizar layout do mapa para adicionar o shapefile
    fig.update_layout(mapbox_style="carto-darkmatter",  # Estilo do mapa
                    mapbox_layers=[
                        {
                            "sourcetype": "geojson",
                            "source": caxias.__geo_interface__,
                            "type": "line",
                            "color": "lightgrey",
                            "line": {"width": .15}
                        }
                    ])
    # Adicionar título
    fig.update_layout(title_text='Distribuição de Estabelecimentos e Moradias em Duque de Caxias em 2022')

    # Mostrar o mapa no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Fonte: IBGE, 2022 - Produzido por Chrisitan Basilio ")

    st.sidebar.title('Filtros')
    st.sidebar.markdown("""
    **Utilizem os filtros acima para possibilitar novas visualizações.**

    Este mapa foi elaborado utilizando dados sobre **estabelecimentos e moradias** fornecidos pelo **Instituto Brasileiro de Geografia e Estatística (IBGE)**. 
    Além disso, foram empregados dados de _shapefile_ para a delimitação dos setores censitários, proporcionando uma visão detalhada e geograficamente precisa das áreas analisadas.
    **Elaborado por [Christian Basilio](https://www.linkedin.com/in/christianbasilioo/).** 
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Metodologia
    Este mapa foi elaborado utilizando dados sobre a extensão territorial de Duque de Caxias, incluindo seus respectivos setores censitários. Para a visualização, empregamos um gráfico de dispersão (scatterplot) que permite georreferenciar estabelecimentos e moradias na cidade. O objetivo deste projeto é facilitar a interação e o acesso a informações gerais sobre construções no município, destacando características geográficas e urbanísticas de maneira interativa.
    O Objetivo é visualização, deixando a analise a cargo do leitor. 
    Espero que tenha gostado! Obrigado

    """)


if __name__ == "__main__":
    main()