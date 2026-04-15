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

printer = POSPrinter("t1")

receipt = (
    POSReceiptBuilder()
    .set_title("ESC/POS PYTHON DEMO")
    .add_component(POSTextBuilder("Left").set_alignment(POSTextAlignment.LEFT).build())
    .add_component(POSTextBuilder("Center").set_alignment(POSTextAlignment.CENTER).build())
    .add_component(POSTextBuilder("Right").set_alignment(POSTextAlignment.RIGHT).build())
    .add_component(POSTextBuilder("Bold").set_style(POSPrintStyle.BOLD).build())
    .add_component(POSTextBuilder("Underlined").set_style(POSPrintStyle.UNDERLINE).build())
    .add_item("Item A", 3.5)
    .add_item("Item B", 5.0)
    .add_component(
        POSBarcodeBuilder("123456789012")
        .set_type(POSBarcodeType.JAN13_EAN13)
        .build()
    )
    .add_component(
        POSQRCodeBuilder("https://example.com")
        .set_size(POSQRCodeSize.LARGE)
        .set_error_correction(POSQRCodeErrorCorrection.HIGH)
        .build()
    )
    .set_footer("Thank you!")
    .build()
)

printer.print(receipt)