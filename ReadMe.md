# 🚚 Roteirizador Logístico com Google Maps e Streamlit

Este projeto é uma aplicação web interativa para otimização de rotas logísticas, permitindo calcular a melhor ordem de visita entre uma origem e múltiplos destinos, utilizando distâncias reais por via urbana.

A aplicação é indicada para cenários como:

* entregas

* coletas

* visitas comerciais

* planejamento logístico com múltiplos pontos

---

## Tecnologias utilizadas

* Google Maps API

  * Geocoding (endereços → coordenadas)

  * Distance Matrix (distâncias reais por via)

* OR-Tools

  * Resolução do Problema do Caixeiro Viajante (TSP)

* Streamlit

  * Interface web interativa

* Folium

  * Visualização da rota no mapa

Solução para quem deseja otimizar entregas, coletas ou qualquer processo logístico com múltiplos pontos.

---

## Aplicação online
A aplicação está disponível em:

📍[Aplicativo de Roteirização](https://app-roteirizacao-mathezzz.streamlit.app/)

### Passos:
1. Acesse o site.

2. Insira a coordenada de origem no formato lat, lon (ex: -23.5505, -46.6333).

3. Informe os destinos utilizando campos individuais:

   * Clique em ➕ Adicionar destino para incluir novos pontos

   * Cada destino pode ser:

     * coordenada (lat, lon)

     * endereço textual (Em construção, estudando a API do Places)

     * ponto de interesse (Em construção, estudando a API do Places)

4. Clique em "Calcular rota".

5. Visualize:

   * a ordem otimizada de visita
   * a rota exibida no mapa interativo

Você pode limpar e recalcular quantas vezes quiser.

# 🎓 Contexto acadêmico/estudos

Trabalho feito para a disciplina de *LOGISTICA E GESTAO DE REDES DE SUPRIMENTOS 1*

Não tem a pretenção de se vender como uma ferramenta comercial, apenas mostrar um sistema simples com uma implementação do projeto do cacheiro viajante, ponto chave de estudo acadêmico dentro da área de logística e rede de suprimentos.

Para entrar em contato comigo: [Anderson Matheus - LinkedIn](https://www.linkedin.com/in/anderson-matheuzzz/)

# Contribua ou adapte!

Sinta-se à vontade para clonar, adaptar e sugerir melhorias.