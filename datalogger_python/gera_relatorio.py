import matplotlib.pyplot as plt
import numpy as np
import os
import time
from fpdf import FPDF


def escolhe_arquivo():
    listarquivos = os.listdir("arquivos_log")
    listatxt = []
    for i in listarquivos:
        if (i[-3]+i[-2]+i[-1]) in ['txt']:
            listatxt.append(i)
    listatxt.append('sair')
    print('\n')
    if len(listatxt) == 1:
        print('Não existem arquivos de log no formato .txt.\nInsira o arquivo que deseja visualizar na pasta "arquivos_log"!')
        return 'sair'
    else:
        print('Arquivos encontrados no diretório %s\n' % (os.getcwd()))
        for i in range(len(listatxt)):
            print('%s -> %s' %((i+1), listatxt[i]))
        while True:
            try:
                escolha = int(input(('\nDigite o número do arquivo que deseja visualizar ou o número da opção SAIR para encerrar o programa: ')))
                escolha = listatxt[escolha-1]
                return escolha
            except Exception:
                return 'sair'


def ajusta_colunas(arquivo):
    saida = []
    with open(arquivo, 'r') as f:
        leitura = f.readlines()
    for i in leitura:
        i = i.split()
        data,hora = i[0].split("-")
        data = data.split(".")
        hora  = hora.split(".")
        umd = i[1]
        temp = i[2]
        
        linha = ''
        for i in range(len(data)-1):
            if len(data[i]) < 2:
                linha += '0' + data[i] + '.'
            else:
                linha += data[i] + '.'
        if len(data[-1]) < 2:
            linha += '0' + data[-1] + '-'
        else:
            linha += data[-1] + '-'

        for i in range(len(hora)-1):
            if len(hora[i]) < 2:
                linha += '0' + hora[i] + '.'
            else:
                linha += hora[i] + '.'
        if len(hora[-1]) < 2:
            linha += '0' + hora[-1]
        else:
            linha += hora[-1]
        saida.append(linha + " " + umd + " " + temp + '\n')
        doc = open(arquivo, 'w')
        doc.writelines(saida)   
        doc.close()
        log_inicio = leitura[0].split()
        log_fim = leitura[-1].split()
    return log_inicio[0], log_fim[0]


def gera_pdf(log_inicio, log_fim, arquivo):
    x = []
    umid = []
    temp = []

    with open(arquivo, 'r') as f:
        leitura = f.readlines()

    for i in range(len(leitura)):
        linha = leitura[i].split()
        x.append(i+1)
        umid.append(float(linha[1]))
        temp.append(float(linha[2]))
        
    plt.subplot(211)
    plt.plot(x, umid, 'r-')
    plt.ylabel('Valores de Umidade (%)')
    
    plt.subplot(212)
    plt.plot(x, temp, 'b-')
    plt.ylabel('Valores de Temperatura (°C)')

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.20, right=0.95, hspace=0.25, wspace=0.35)
    plt.suptitle("LEITURAS - de %s a %s" %(log_inicio, log_fim))
    plt.savefig('relatorio\\grafico.png')
    plt.close()
    
    titulo = 'Logs do arquivo ' + arquivo[13:] + '. Total de registros: ' + str(len(leitura))
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(280, 10, titulo, 0, 0, 'C')
    pdf.image('relatorio\\grafico.png', x = 0, y = 25, w = 297, h = 180)
    pdf.add_page(orientation = 'P')
    pdf.set_font('Arial', 'B', 12)

    pdf.set_fill_color(r = 224, g = 224, b = 224)
    pdf.cell(125, 6, ' {:^25}|{:^20}|{:^25} '.format('Data/hora', 'Umidade (%)', 'Temperatura (°C)'), 1, 2, fill = True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(190, 0.5, '', 0, 2)
    cont = 0
    for i in leitura:
        cel = i.split()
        pdf.set_fill_color(r = 204, g = 255, b = 255)        
        if cont == 0:
            pdf.cell(125, 4, '{:^26}|{:^34}|{:^42}'.format(cel[0], cel[1], cel[2]), 1, 2, fill = cont)            
            cont = 1
        elif cont == 1:
            pdf.cell(125, 4, '{:^26}|{:^34}|{:^42}'.format(cel[0], cel[1], cel[2]), 1, 2, fill = cont)
            cont = 0
    nome_relatorio = 'relatorio\\' + arquivo[13:32] + '.pdf'
    pdf.output(nome_relatorio, 'F')
    pdf.close()
    os. chdir('relatorio\\')
    os.system(arquivo[13:32] + '.pdf')
    return


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    return


def cabecalho():
    cls()
    print('╔' + '═' * 100 + '╗')
    print('║ {:^98} ║'.format('--PROJETO DATALOGGER--  (versão 1.0)'))
    print('╚' + '═' * 100 + '╝')
    return


def relatorio():
    arquivo = escolhe_arquivo()
    log_inicio, log_fim = ajusta_colunas("arquivos_log\\" + arquivo)
    gera_pdf(log_inicio, log_fim, "arquivos_log\\" + arquivo)
