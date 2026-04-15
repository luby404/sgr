from escpos import (
    POSPrinter,
    POSReceiptBuilder,
    POSTextBuilder,
    POSTextAlignment,
    POSQRCodeBuilder,
    POSQRCodeErrorCorrection
)

printer = POSPrinter("t1")
receipt = (
    POSReceiptBuilder()
    .set_title("Mesa 1")
    .add_component(POSTextBuilder("Scanea o codigo para receber o cardapio").set_alignment(POSTextAlignment.CENTER).build())
    
    .add_component(
        POSQRCodeBuilder("http://127.0.0.1:5000//cardapio/1")
        .set_size(10)
        .set_error_correction(POSQRCodeErrorCorrection.HIGH)
        .build()
    )
    .set_footer("Bem-Vindo")
    .build()
)

printer.print(receipt)