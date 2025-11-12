import requests
import pandas as pd
import streamlit as st



def fazer_request(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"erro no request: {e}")
        resultado = None
    else:
        resultado = resposta.json()
    return resultado


def pegar_nome_por_decada(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    params = {
        'groupBy':'UF',
    }
    dados_decadas = fazer_request(url=url)
    if not dados_decadas:
        return {}
    dict_decadas = {}
    for dados in dados_decadas[0]['res']:
        decada = dados['periodo'].replace('[','')
        quantidade = dados['frequencia']
        dict_decadas[decada] = quantidade
    return dict_decadas


def main():
    st.title('web App nomes')
    st.write('dados do ibge ')

    nome = st.text_input('consulte um nome: ')
    if not nome:
        st.stop()

    dict_decadas = pegar_nome_por_decada(nome)
    if not dict_decadas:
        st.warning(f'nenhum dado encontrado para o nome {nome}')
        st.stop()
        
    df = pd.DataFrame.from_dict(dict_decadas,orient="index")

    col1, col2 = st.columns([0.3,0.7])
    with col1 :
        st.write('frequencia por decada')
        st.dataframe(df)
    with col2:
        st.write('Evolução no tempo')
        st.line_chart(df)
    

if __name__ == '__main__':
    main()