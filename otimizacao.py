import gurobipy as gp
import pandas as pd





#base = pd.ExcelFile('Base_de_dados_PO.xlsx')
base = pd.ExcelFile('Base_de_dados_PO_infactivel.xlsx')
#base = pd.ExcelFile('Base_de_dados_PO_grande.xlsx')
#base = pd.ExcelFile('Base_de_dados_PO_mega.xlsx')  


Distancias=pd.read_excel(base,sheet_name='Distâncias IxJ')
Pesos=pd.read_excel(base,sheet_name='"Pesos" K')
Ofertas=pd.read_excel(base,sheet_name='Oferta a(i,k)')
Demandas=pd.read_excel(base,sheet_name='Demanda b(j,k)')


I = Ofertas.shape[0]-1  # Número de distribuidoras
J = Demandas.shape[0]-1 # Número de clientes
K = Pesos.shape[0]  # Número de produtos

#print(Ofertas.shape[0]-1,' Quantidade de distribuidoras, primeiro teste foi com 4')
#print(Demandas.shape[0]-1,' Quantidade de clientes, primeiro teste foi com 8')
#print(Pesos.shape[0],' Quantidade de produtos, primeiro teste foi com 3')

#rotulos

distr=list()
client=list()
prod=list()
for i in range(I):
    distr.append(Ofertas['Distribuidora'][i])
for j in range(J):
    client.append(Demandas['Cidade Consumidora'][j])
for k in range(K):
    prod.append(Pesos['Produto'][k])
    
#dicionário de ofertas
a=dict()
for i in range(I):
    for k in range(K):
        d=distr[i]
        p=prod[k]
        a[d,p]=Ofertas.iloc[i][k+1]

#dicionário de demandas
b=dict()
for j in range(J):
    for k in range(K):
        c=client[j]
        p=prod[k]
        b[c,p]=Demandas.iloc[j][k+1]



#dicionário de custos

custos=dict()
for i in range(I):
    for j in range(J):
        for k in range(K):
            d=distr[i]
            c=client[j]
            p=prod[k]
            custos[d,c,p]=(int(Distancias.iloc[i,j+1])*int(Pesos.iloc[k,1]))
#print(custos)

#Criando o modelo 

m= gp.Model()

#variáveis de decisão
x = m.addVars(distr,client,prod, vtype= gp.GRB.INTEGER)

#Função objetivo
m.setObjective(
    gp.quicksum(x[i,j,k]*custos[i,j,k]for i in distr for j in client for k in prod),
    sense= gp.GRB.MINIMIZE)


#definição de Restrições
#vetor_teste factbilidade
factivel = {}

for k in prod:
    soma_ofertas = sum(valor for (localizacao, produto) in a.keys() if produto == k for valor in [a[(localizacao, produto)]])
    soma_demandas = sum(valor for (localizacao, produto) in b.keys() if produto == k for valor in [b[(localizacao, produto)]])
    factivel[k] = 1 if soma_ofertas > soma_demandas else 0

# Adicionar restrições usando o dicionário factivel
a1 = m.addConstrs(
    (gp.quicksum(x[i, j, k] for j in client) <= a[i, k] if factivel[k] else gp.quicksum(x[i, j, k] for j in client) == a[i, k])
    for i in distr for k in prod)

b1 = m.addConstrs(
    (gp.quicksum(x[i, j, k] for i in distr) == b[j, k] if factivel[k] else gp.quicksum(x[i, j, k] for i in distr) <= b[j, k])
    for j in client for k in prod)

#Executa o modelo

m.optimize()

print("\n")
#Informativo de onde sobrou ou faltou produtos
for k in prod:
    for i in distr:
        sobra = round(a1[i,k].Slack)
        if sobra > 0:
            print("Sobraram {} unidades de {} na distribuidora em {}".format(sobra,k,i)) 

print("\n")
for k in prod:
    for j in client:
        falta = round(b1[j,k].Slack)
        if falta > 0:
            print("Faltaram {} unidades de {} para o cliente {}".format(falta,k,j)) 
            
#transformando a saida X em tabela

resultado=[(f"{i[0]}", f"{i[1]}",f"{i[2]}",valor.x) for i, valor in x.items()]

df = pd.DataFrame(resultado,columns=['origem','Destino','produto','Valor'])

df_pivotado = df.pivot_table(index=[ 'produto','origem'], columns='Destino', values='Valor')

produtos = df_pivotado.index.get_level_values('produto').unique().tolist()

df_total = pd.DataFrame()

for produto in produtos:
    sub_df = df_pivotado[df_pivotado.index.get_level_values('produto') == produto]  # Sub-DataFrame para o produto específico
    
    # Criar uma linha de total com as somas
    total_row = sub_df.sum().to_frame().T
    
    # Adicionar informações de produto e origem à linha de total
    total_row['produto'] = produto
    total_row['origem'] = f"Total {produto}"
    
    # Concatenar a linha de total ao final do sub-DataFrame
    sub_df = pd.concat([sub_df, total_row.set_index(['produto', 'origem'])])
    
    df_total = df_total.append(sub_df)



df_total['Soma'] = df_pivotado.sum(axis=1)



df_total.to_excel('Plano_de_Transporte.xlsx', index=True)
