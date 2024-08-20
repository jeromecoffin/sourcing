import xlsxwriter
from io import BytesIO
import read

def generate_xlsx_rfi(rfi):
    # Create a BytesIO buffer for the workbook
    output = BytesIO()
    
    # Create an Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Define formats for styling
    bold_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'text_wrap': True})
    normal_format = workbook.add_format({'border': 1})
    title_format = workbook.add_format({'bold': True, 'font_size': 16})
    title_format.set_align('center')
    section_title_format = workbook.add_format({'bold': True, 'font_size': 14})
    section_title_format.set_align('center')

    # Add a text wrap format.
    text_wrap_format = workbook.add_format({'text_wrap': True})
    
    # Define column widths
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 50)

    # Write the title
    worksheet.merge_range('A1:B1', f"RFI Document", title_format)

    # Write subheader
    worksheet.merge_range('A3:B3', "Generated with Avanta Sourcing", normal_format)

    # Write header data
    worksheet.write('A5', 'Title', bold_format)
    worksheet.write('B5', rfi['title'], normal_format)

    worksheet.write('A6', 'Reference', bold_format)
    worksheet.write('B6', rfi['reference'], normal_format)

    # Write timeline data
    worksheet.write('A9', 'Request Date', bold_format)
    worksheet.write('B9', rfi['requestDate'], normal_format)

    worksheet.write('A10', 'Request Due Date', bold_format)
    worksheet.write('B10', rfi['requestDueDate'], normal_format)

    # Write Requesting Party Information
    worksheet.merge_range('A12:B12', "REQUESTING PARTY INFORMATION", section_title_format)
    agent = read.agent()
    worksheet.write('A13', 'Requesting Party Name', bold_format)
    worksheet.write('B13', agent['name'], normal_format)
    worksheet.write('A14', 'Requesting Party Lastname', bold_format)
    worksheet.write('B14', agent['lastname'], normal_format)
    worksheet.write('A15', 'Requesting Party Address', bold_format)
    worksheet.write('B15', agent['address'], normal_format)
    worksheet.write('A16', 'Requesting Party Email', bold_format)
    worksheet.write('B16', agent['email'], normal_format)
    worksheet.write('A17', 'Requesting Party Phone', bold_format)
    worksheet.write('B17', agent['phone'], normal_format)

    # Write General Information
    worksheet.merge_range('A19:B19', "GENERAL INFORMATION", section_title_format)
    worksheet.write('A20', 'SUPPLIER NAME', bold_format)
    worksheet.write('B20', '', normal_format)

    # Write Contact Details Information
    worksheet.write('A22', 'CONTACT DETAILS INFORMATION', bold_format)
    worksheet.write('A23', 'Address', bold_format)
    worksheet.write('B23', '', normal_format)
    worksheet.write('A24', 'City', bold_format)
    worksheet.write('B24', '', normal_format)
    worksheet.write('A25', 'Province', bold_format)
    worksheet.write('B25', '', normal_format)
    worksheet.write('A26', 'ZIP Code', bold_format)
    worksheet.write('B26', '', normal_format)
    worksheet.write('A27', 'Contact Person', bold_format)
    worksheet.write('B27', '', normal_format)
    worksheet.write('A28', 'Job Title', bold_format)
    worksheet.write('B28', '', normal_format)
    worksheet.write('A29', 'Email', bold_format)
    worksheet.write('B29', '', normal_format)
    worksheet.write('A30', 'Phone Number', bold_format)
    worksheet.write('B30', '', normal_format)
    worksheet.write('A31', 'Fax Number', bold_format)
    worksheet.write('B31', '', normal_format)
    worksheet.write('A32', 'Website', bold_format)
    worksheet.write('B32', '', normal_format)

    # Write Business Information
    worksheet.merge_range('A34:B34', "BUSINESS INFORMATION", section_title_format)
    worksheet.write('A35', 'Which year your company was founded?', bold_format)
    worksheet.write('B35', '', normal_format)
    worksheet.write('A36', 'Ownership', bold_format)
    worksheet.write('B36', '', normal_format)
    worksheet.write('A37', 'Capital in million VND', bold_format)
    worksheet.write('B37', '', normal_format)
    worksheet.write('A38', 'What is the workfloor size?', bold_format)
    worksheet.write('B38', '', normal_format)
    worksheet.write('A39', 'How many employees do you have?', bold_format)
    worksheet.write('B39', '', normal_format)
    worksheet.write('A40', 'Do you have export license?', bold_format)
    worksheet.write('B40', '', normal_format)
    worksheet.write('A41', '% of turnover exported to UE, USA, Others', bold_format)
    worksheet.write('B41', '', normal_format)

    cell = 43
    for idx, x in enumerate(rfi["additional_fields"]):
        cell += idx
        worksheet.write('A{}'.format(cell), x, bold_format)

    # Write additional information or comments based on doc_type
    cell += 2
    worksheet.write('A{}'.format(cell), 'Information', bold_format)
    worksheet.write('B{}'.format(cell), rfi['information'], normal_format)
    cell += 2
    worksheet.write('A{}'.format(cell), 'Comment', bold_format)
    worksheet.write('B{}'.format(cell), rfi['comment'], normal_format)

    # Close the workbook and return the BytesIO buffer
    workbook.close()
    output.seek(0)
    
    return output
