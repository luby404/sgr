from escpos import *

from datetime import datetime

from utils import (
    NOME,
    TELEFONE,
    NIF
)

def text_center(text):
    return POSTextBuilder(f"{text}").set_style(
            POSPrintStyle.BOLD
        ).set_alignment(
            POSTextAlignment.CENTER
        ).build()

def text_left(text):
    return POSTextBuilder(f"{text}").set_style(
            POSPrintStyle.BOLD
        ).set_alignment(
            POSTextAlignment.LEFT
        ).build()



class Print():
    def __init__(self, name="t1"):
        self.printer = POSPrinter(name)
        
        self.nome = NOME
        self.phone = TELEFONE
        self.nif = NIF
    
    
    def print_recibo_qr_mesa(self, url, num_mesa):
        receipt = (
            POSReceiptBuilder()
            .set_title(f"Mesa {num_mesa}")
            .add_component(POSTextBuilder("Scanea o codigo para receber o cardapio").set_alignment(POSTextAlignment.CENTER).build())
            
            .add_component(
                POSQRCodeBuilder(str(url))
                .set_size(6)
                .set_error_correction(POSQRCodeErrorCorrection.HIGH)
                .build()
            )
            .set_footer("Bem-Vindo")
            .build()
        )

        self.printer.print(receipt)
    
    def print_recibo_pedido(self, produtos:list, cozinha:bool=False, total:str=0, mesa=0, pedido=0):
        receipt = POSReceiptBuilder()
        if not cozinha:
            receipt.add_component(text_center(self.nome))
            receipt.add_component(text_center(self.phone))
            receipt.add_component(text_center(f"NIF: {self.nif}"))
            receipt.add_component(text_center(datetime.now().strftime("%d/%m/%Y %H:%M")))
            receipt.add_component(text_center("Recibo de pagamento\n\n"))
            
        else:
            receipt.add_component(text_center(datetime.now().strftime("%d/%m/%Y %H:%M")))
            receipt.add_component(text_center("Recibo Para Cozinha\n\n"))
        
        


        for produto in produtos:
            receipt.add_item_styled(f"{produto[0]} x{produto[1]}", produto[2])


        receipt.add_component(text_left("-"*32))
        if mesa: receipt.add_component(text_left(f"Mesa: {mesa}"))
        receipt.add_component(text_left(f"Pedido: {pedido}"))
        receipt.add_component(text_left(f"Total: {total}"))
        

        if not cozinha:
            receipt.set_footer("\n\nEste Documento nao serve como fatura")
            receipt.set_footer("Obrigado!")
        else:
            receipt.set_footer("\n\nEste Documento serve apenas para cozinha")
            
        self.printer.print(receipt.build())
    
    
    