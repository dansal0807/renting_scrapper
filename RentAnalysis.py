import pandas as pd

rents = pd.read_csv("imoveis_dataset.csv", sep=";")

rents['endereco'] = rents['endereco'].apply(lambda x: x.split('-'))

rents['rua'] = rents['endereco'].apply(lambda x: x[0])
rents['bairro'] = rents['endereco'].apply(lambda x: x[1])

rents['bairro'] = rents['bairro'].apply(lambda x: x.split(',')[0].strip())

print(rents['bairro'])

for bairros in rents['bairro']:
    print(bairros)