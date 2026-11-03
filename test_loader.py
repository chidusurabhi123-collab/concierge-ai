from app.ingestion.loader import load_pdf

pdf = load_pdf("data/documents/sample.pdf")

print("Filename:", pdf["filename"])

print("Total pages:", len(pdf["pages"]))

for page in pdf["pages"]:

    print("\nPage:", page["page"])

    print("Content:", page["content"])