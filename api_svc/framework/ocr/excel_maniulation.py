import openpyxl
from openpyxl.styles import Alignment, Font

def fct_create_excel_file(data, nrFac, furnizor, delegat):
    file1 = "/Users/sofianurobert/Projects/go_rect_inv_app/NIR---ui-backend-miscorservices/api_svc/services/ocr_svc/images/nir_1.xlsx"

    workbook = openpyxl.Workbook()

    worksheet = workbook.active

    worksheet.row_dimensions[8].height = 75
    worksheet.row_dimensions[1].height = 27

    worksheet.column_dimensions['A'].width = 20
    worksheet.column_dimensions['B'].width = 5
    worksheet.column_dimensions['C'].width = 10
    worksheet.column_dimensions['I'].width = 10

    cell_d1 = worksheet['D1']
    cell_d1.value = "NOTA DE RECEPTIE"
    font_style = Font(size=18, bold=True)
    cell_d1.font = font_style

    worksheet['A1'] = 'S.C.'
    worksheet['B1'] = 'PROTOSOF S.R.L.'
    worksheet['H1'] = 'Nr.'
    worksheet['J1'] = 'Din'
    worksheet['K1'] = data

    worksheet['B2'] = 'Protopopesti'
    worksheet['A2'] = 'Localitatea'

    worksheet['D3'] = 'Furnzor'
    worksheet['D4'] = 'Nr. si data facturii sau avizului de expediere'
    worksheet['D5'] = 'Numele si prenumele delegatului'
    worksheet['D6'] = 'B.l. Seria …...... nr. ….......... eliberat de Politia ...................................'

    worksheet['I1'] = 12
    worksheet['I3'] = furnizor
    worksheet['I4'] = nrFac
    worksheet['I5'] = delegat

    cell = worksheet['I1']
    cell.value = 12
    cell.alignment = Alignment(
        horizontal='left', vertical='bottom')

    cell = worksheet['A8']
    cell.value = "Denumire Produs"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['B8']
    cell.value = "U/M"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['C8']
    cell.value = "Dupa factura sau aviz"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['D8']
    cell.value = "La receptie"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['E8']
    cell.value = "Pret Furnizor"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['F8']
    cell.value = "Valoare furnizor col. 3 x 4"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['G8']
    cell.value = "T.V.A. Incasat de furnizor"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['H8']
    cell.value = "Total valoare factura col. 5 + 6"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['I8']
    cell.value = "Pret cu adasul practicat %"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['J8']
    cell.value = "Valoare la pret cu adaos col. 3 x 8"
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['K8']
    cell.value = "Pret cu adaos si T.V.A."
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')

    cell = worksheet['L8']
    cell.value = "Valoare la pret cu adaos si T.V.A."
    cell.alignment = Alignment(
        wrap_text=True, horizontal='center', vertical='center')


    workbook.save(file1)
    workbook.close()

fct_create_excel_file("/path/to/data", "12345", "Furnizor X", "Delegat Y")