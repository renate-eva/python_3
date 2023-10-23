import PyPDF2
import pathlib
from tabulate import tabulate
import csv
from datetime import datetime

file=input("input: ")
result=0
data=[]
nordpool_prices = []
fixed_price=[]
adrese = pathlib.Path("invoices")
visi_faili=list(adrese.glob(file+".pdf"))
for f in range(len(visi_faili)):
# this part read information from pdf file and place 
# split pdf file in to two pages and extraxt page content to text variables
    if file!="":        
        row=[]
        pdf_file=PyPDF2.PdfReader(open(visi_faili[f],"rb"))
        number_of_pages=len(pdf_file.pages)
        page1=pdf_file.pages[0]
        page2=pdf_file.pages[1]

        text1=page1.extract_text()
        text2=page2.extract_text()

        pos1 = text1.find("Apmaksai:")
        pos2 = text1.find("Elektroenerģijas patēriņš kopā")

        pos3 = text2.find("EUR")
        pos4 = text2.find("Apkalpošanas maksa")

        fix = text2[pos3+38:pos4].rstrip()
        apjoms=fix[0:8].strip()
        kwh_ar_fix=fix[13:20]
        summ_ar_fix=fix[20:27]

        apjoms = float(apjoms.replace(' ', '').replace(',', '.'))
        kwh_ar_fix = float(kwh_ar_fix.replace(',', '.'))
        summ_ar_fix = float(summ_ar_fix.replace(',', '.'))

        summa = text1[pos1+10:pos2].rstrip()
        # summa = float(summa.replace(',', '.'))

        fixed_price.append(fix)
        row.append(summa)
        pos1 = text2.find("Apjoms Mērv. Cena,")
        per = text2[pos1-23:pos1]
        row.append(per)
        data.append(row)
    # print(fixed_price)
    print(apjoms)
    print(summ_ar_fix)
    print(kwh_ar_fix)

    # print(fix)
print(tabulate(data,headers=["Summa", "Periods"], tablefmt="github"))

#     # this part NORDPOOL
with open("nordpool.csv","r") as f:
    csv_reader = csv.reader(f)

    next(csv_reader)
    for row in csv_reader:
        # start_date=row[0]
        # end_date=row[1]
        # print(start_date[0:10],end_date[0:10])
        for date in row:
            if date.startswith("2023-04"):
                nordpool_prices.append(float(row[2]))
                average_price = sum(nordpool_prices) / len(nordpool_prices)
                rounded_average = round(average_price, 2)
    print(rounded_average)
    print(round(summ_ar_fix-0-(apjoms*rounded_average)))
    

        


# # print(result)
