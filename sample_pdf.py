import pymupdf

doc = pymupdf.open()

# Page 1
page = doc.new_page()
page.insert_text(
    (72, 72),
    "REFUND POLICY\n\nCustomers can request a refund within 7 days.\n\nRefund requests must be reviewed by support."
)

# Page 2
page = doc.new_page()
page.insert_text(
    (72, 72),
    "DELIVERY POLICY\n\nStandard delivery takes 3 to 5 business days.\n\nCustomers can track orders using their order ID."
)

doc.save("data/documents/sample.pdf")
doc.close()

print("Sample PDF created successfully!")