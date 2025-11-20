#Script para correção de procedimentos de Preventivo e alteração de Chave Verificadora do BPA-I.
import time, datetime

def geradorNovaChave(lista:list,chaveInicial) -> list:
    #Gera uma nova chave de verificação para o BPA seguindo o layout de importação do MS.
    soma = 0
    numProcedimentos = 0

    # Contador de quantas linhas iniciam com 03 indicando ser uma linha de procedimento.
    for i in lista:
        if i[0:2] == "03":
            numProcedimentos += 1
            soma += int(i[49:59])
    
    # 1. Encontrar o resto da seguinte divisão:
    # [(somatório das quantidades de procedimentos) + (somatório dos códigos de procedimento)] dividido por 1111 (mil cento e onze);
    # 2. Somar 1111 (mil cento e onze) ao resto.
    novaChave = ((numProcedimentos + soma) % 1111) + 1111

    valor = str(lista[0]).replace(str(chaveInicial),str(novaChave))
    lista[0] = valor


    return novaChave


def corretorProcedimentos(lista:list) -> list:
    # Corrige as inconsistências de procedimentos em idades incompatíveis.
    novaLista = lista
    print("\n************* ANALISANDO LINHAS *************")
    erros = 0
    for indice, valor in enumerate(novaLista):

        #Verifica em cada linha se existe resgistro com procedimento 0203010086 para pacientes fora da faixa etária 25 a 64 anos.
        if valor[49:59] == "0203010086" and (int(valor[85:88]) < 25 or int(valor[85:88]) > 64):
            print(f"Procedimento: {valor[49:59]} Idade: {valor[85:88]} ----> Procedimento Incompatível")
            valor = str(valor).replace("0203010086","0203010019")
            novaLista[indice] = valor
            erros += 1

    print(f"Erros localizados: {erros}")   

    if erros == 0:
        input("\nPressione qualquer tecla para sair...")
        exit()
    return novaLista

# Solicita o nome do arquivo BPA-I a ser lido, o arquivo deve estar na mesma pasta do script.
nomeArquivo = input("Digite o nome do arquivo: ")

# Divide o arquivo recebido em linhas e adiciona a uma lista
lista = []
with open(nomeArquivo, "r") as arquivo:
    conteudo = arquivo.read()
    for linha in conteudo.split("\n"):
        lista.append(linha)


# Chave inicial de verificação do BPA posicionada nos índices 23 a 27 da primeira linha do arquivo BPA-I.
chaveInicial = lista[0][23:27]

lista = corretorProcedimentos(lista)
novaChave = geradorNovaChave(lista,chaveInicial)

# Exibe a nova chave após o cálculo
print(f"\nChave inicial: {chaveInicial} // Nova Chave: {novaChave}")

# Solicita o nome do novo arquivo BPA-I a ser salvo na mesma pasta do script
novoNomeArquivo = input("\nDigite o nome do novo arquivo a ser salvo: ")
with open(novoNomeArquivo,"a") as novoArquivo:
    for linha in lista:
        novoArquivo.write(str(linha))

input("\nPressione qualquer tecla para sair...")