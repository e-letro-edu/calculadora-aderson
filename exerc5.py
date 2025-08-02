import csv , sys

with open ("clientes.csv", errors ="replace", encoding ="utf -8") as f :
    leitor = csv.reader(f)
    for i , linha in enumerate ( leitor , start =1) :
        if not linha :
            continue
        try:
            valor = int(linha[0])

        
            pass
        except Exception as e :
            print (f"[ WARN ] linha {i} ignorada : {e}")