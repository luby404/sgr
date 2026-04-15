"""python
def add_item(self, name: str, price: float):
    line = f"{name.ljust(20)} {format(price, '.2f').rjust(10)}"
    self.receipt.add_component(POSTextBuilder(line).build())
    return self
"""


lista_dados = [
    ("Cocacola viste oomo", 2,  100, 200) for i in range(4)
]

header = f"{'nome'.ljust(10)} qtd {'preço'.rjust(10)}"
print(header)
for nome, qtd, price, subtotal in lista_dados:
    line = f"{nome.ljust(10)} {qtd} {format(price, '.2f').rjust(10)}"
    
    print(line)


