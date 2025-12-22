#class config que vai ter as conf base
#class elements que vai chamar elementos visuais que eu configurar
#ambas as class vai interagir entre si
#uma Class menu que vai chamar os menu
# a ideia geral e segmentar o maximo possivel para poder simplificar
#
#15/12/25
#percebi que sou meio burro, nao tinha a necessidade de uma função config so vou fazer o config uma vez
#alem disso usar uma funçao config estava criando uma conplexidade desnecessaria
#devido a isso vou so fazer a config no inicio do main
# quero que as funçoes de formataçao recebam os textos ckmo objetos
#
#16/12/2025
#foi projetado a tecla de saida, com um simples if no menu, mas estou cogitando desenvolver as interaçoes com teclado em uma classe 
# aparte e chamalas como funçoes, nao sei se seria apropriado, aumentaria a complexidade do projeto
#
#foi feito o desenvolvimento das primeiras funçoes de formataçao
# a ideia e tranformar essa funçoes em objetos e chamalas sempre que conveniente
# a estrutura por recomendação do google gemini ficou um pouco diferente do que eu tinha planejado
#
# agora a classe elements vai conter de fato elementos e caracteristicas de formataçao
#
# anotacao mental: reurn self e algo divino
# com isso vou poder chamar minhas funcoes de elements em cascata e formatar da forma que quiser
#
#estou em um nivel proximo de ter uma erecao vendo minhas classes sendo chamadas e funcionando
# foi implementado uma funcao parar printar listas dessa forma fica mais facil de printar os menus
# nao me pergunte sobre como vou pegar qual opçao foi selecionada
# agora parando para ver, nem todo parametro precisa ser passado em init
# possa passar direto na funcao que vai usalo
# isso diminui o acesso de certas funcoes que nao precisam desse parametro
#
#
# minha primeira gambiarra: centralize_x pega o valor de self.texto
#toda via ele não reflete o tamanho dos textos de addstring_list()
# por isso sempre passar em self.texto a maior string da lista
#
#18/12/2025
#
# Mudei um pouco a ideia do projeto
# Não vai ser mais um rpg de texto mas sim um conjunto de ferramentas hackers
# Hack the Planet!
#
#parece que para fazer o input o sistema injeta objeto dentro de objeto algo que fica confuso pra mim 
#vou ter que me adaptar
#
#acabei de descobrir que a amanipulaçao de cores e uma grande bosta
#por incrivel que pareça o terminal nao me deixa colocar a cor que eu quero
# fica ai a critica pros donos dessa biblioteca de merda 
# #RUST>PYTHON
# #VOUREFATORARVOCECODIGOMALDITO
# percebi que nao precisava de um while no main do jeito que vou fazer as coisas agora, isso deixa o codigo bem melhor
#
#22/12/2025
#
#hoje decidi recomeçar do zero, ate agora o projeto foi de grande aprendizagem
#mas segui em um caminho desnecessariamente sem sentido
#realmente nao tinha necessidade de usar curses
#daria pra fazer tudo com print e input
#vai ficar bem mais legal