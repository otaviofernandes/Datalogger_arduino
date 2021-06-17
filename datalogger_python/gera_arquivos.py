import os
import time


def testa_arquivo(doc):
    teste = os.path.exists(doc) and os.path.isfile(doc)
    return teste


def monta_nome(i):
    i = i.split()
    data, hora = i[0].split("-")
    data = data.split(".")
    hora  = hora.split(".")
    nome = ''
    for i in range(len(data)-1):
        if len(data[i]) < 2:
            nome += '0' + data[i] + '.'
        else:
            nome += data[i] + '.'

    if len(data[-1]) < 2:
        nome += '0' + data[-1] + '-'
    else:
        nome += data[-1] + '-'

    for i in range(len(hora)-1):
        if len(hora[i]) < 2:
            nome += '0' + hora[i] + '.'
        else:
            nome += hora[i] + '.'

    if len(hora[-1]) < 2:
        nome += '0' + hora[-1] + '.txt'
    else:
        nome += hora[-1] + '.txt'          
    return nome


def gera_arquivos(doc):
    cont = 1
    estado = 0
    with open(doc, 'r') as f:
        leitura = f.readlines()
    print('Relação de arquivos gerados:\n')
    for i in range(len(leitura)):
        if leitura[i] == 'begin\n':
            nome_arquivo = monta_nome(leitura[i +1])
            teste = testa_arquivo("arquivos_log\\" + nome_arquivo)
            if teste:
                estado = 0
            else:
                print("Arquivo %d -> %s" % (cont, nome_arquivo))
                cont += 1
                estado = 1
                arquivo = open("arquivos_log\\" + nome_arquivo, 'w')

        elif leitura[i] != 'end\n' and estado == 1:
            arquivo.write(leitura[i])

        elif leitura[i] == 'end\n' and estado == 1:
            arquivo.close()
            estado = 0

def arquivo():
    fim = False
    doc = input('\nDigite o nome.extensão do arquivo.  ')
    teste = testa_arquivo(doc)
    if not teste:
        while teste == False:
            print('O arquivo "%s" não existe!\n' % doc)
            doc = input('Digite o nome.extensão do arquivo ou "X" para sair.  ')
            if doc == 'x' or doc == 'X':
                fim = True
                break
            else:
                teste = testa_arquivo(doc)           
    if not fim:
        gera_arquivos(doc)
        input("\nAperte qualquer tecla para sair. ")
    return
