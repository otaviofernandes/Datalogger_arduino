import gera_arquivos as ga
import gera_relatorio as gr

gr.cabecalho()
opcao = input("\nEscolha:\n1-Gerar arquivos de log.\n2-Gerar relatórios.\n3-Encerrar o programa.\n\nOpção:  ")
while opcao != '1' and opcao != '2' and opcao != '3':
    gr.cabecalho()
    print("\nOpção escolhida %s é inválida!\n" %opcao)
    opcao = input("Escolha:\n1-Gerar arquivos de log.\n2-Gerar relatórios.\n3-Encerrar o programa.\n\nOpção:  ")

gr.cabecalho()
if opcao == '1':
    ga.arquivo()

elif opcao == '2':
    gr.relatorio()


