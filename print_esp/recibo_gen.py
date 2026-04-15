from escpos import (
    POSPrinter,
    POSReceiptBuilder,
    POSTextBuilder,
    POSPrintStyle,
    POSTextAlignment,
    POSBarcodeBuilder,
    POSBarcodeType,
    POSQRCodeBuilder,
    POSQRCodeSize,
    POSQRCodeErrorCorrection
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


printer = POSPrinter("t1")

produtos = [
    ("cocacola", 2, 100) for i in range(7)
]

receipt = POSReceiptBuilder()
receipt.add_component(text_center("Cramer"))
receipt.add_component(text_center("931617941"))
receipt.add_component(text_center("Recibbo de pagamento\n\n"))


for produto in produtos:
    receipt.add_item_styled(f"{produto[0]} x{produto[1]}", produto[2])


receipt.add_item("Mesa:", 1)
receipt.add_item("Pedido", 10)
receipt.add_item_styled("Total", 2500)


receipt.set_footer("\n\nEste Recibo não serve como fatura")
receipt.set_footer("Obrigado!")



printer.print(receipt.build())