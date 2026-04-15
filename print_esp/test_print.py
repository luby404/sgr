from escpos import POSPrinter, POSReceiptBuilder

produtos = [
    
]

printer = POSPrinter("t1")  # nome do sistema

receipt = POSReceiptBuilder()

receipt.set_title("Restaurante Maneger")
for produto in produtos:
    receipt.add_item_styled()


doc = receipt.build()
printer.print(doc)