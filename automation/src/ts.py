import fitz

f = fitz.open('models\cIEF 200\\046-329_CofA_Maurice_cIEF_Cartridge_090-101_RevF.pdf')
for page in f:
    for w in page.widgets():
        print(w.field_name)
