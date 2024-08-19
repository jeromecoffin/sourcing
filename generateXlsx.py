import xlsxwriter
from io import BytesIO
import read

def generate_xlsx(doc_type, doc_data):
    # Create a BytesIO buffer for the workbook
    output = BytesIO()
    
    # Create an Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Define formats for styling
    bold_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    normal_format = workbook.add_format({'border': 1})
    title_format = workbook.add_format({'bold': True, 'font_size': 16})
    title_format.set_align('center')
    section_title_format = workbook.add_format({'bold': True, 'font_size': 14})
    section_title_format.set_align('center')
    
    # Define column widths
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 50)

    # Write the title
    worksheet.merge_range('A1:B1', f"{doc_type} Document", title_format)

    # Write subheader
    worksheet.merge_range('A3:B3', "Generated with Avanta Sourcing", normal_format)

    # Write header data
    worksheet.write('A5', 'Title', bold_format)
    worksheet.write('B5', doc_data['title'], normal_format)

    worksheet.write('A6', 'Reference', bold_format)
    worksheet.write('B6', doc_data['reference'], normal_format)

    worksheet.write('A7', 'Location', bold_format)
    worksheet.write('B7', doc_data['location'], normal_format)

    # Write timeline data
    worksheet.write('A9', 'Request Date', bold_format)
    worksheet.write('B9', doc_data['requestDate'], normal_format)

    worksheet.write('A10', 'Request Due Date', bold_format)
    worksheet.write('B10', doc_data['requestDueDate'], normal_format)

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

    # Write Product Information
    worksheet.merge_range('A43:B43', "PRODUCT INFORMATION", section_title_format)
    worksheet.write('A44', 'Product Name', bold_format)
    worksheet.write('B44', doc_data["productName"], normal_format)
    worksheet.write('A45', 'Quantity', bold_format)
    worksheet.write('B45', doc_data["quantity"], normal_format)
    worksheet.write('A46', 'Material', bold_format)
    worksheet.write('B46', doc_data["material"], normal_format)
    worksheet.write('A47', 'Size', bold_format)
    worksheet.write('B47', doc_data["size"], normal_format)
    worksheet.write('A48', 'Color', bold_format)
    worksheet.write('B48', doc_data["color"], normal_format)
    worksheet.write('A49', 'Accessory', bold_format)
    worksheet.write('B49', doc_data["accessory"], normal_format)
    worksheet.write('A50', 'Packaging', bold_format)
    worksheet.write('B50', doc_data["packaging"], normal_format)
    worksheet.write('A51', 'Carton Size (LxWxH)', bold_format)
    worksheet.write('B51', doc_data["size"], normal_format)

    # Write Logistics Information
    worksheet.merge_range('A53:B53', "LOGISTICS INFORMATION", section_title_format)
    worksheet.write('A54', 'Product Name', bold_format)
    worksheet.write('B54', '', normal_format)
    worksheet.write('A55', 'Quantity', bold_format)
    worksheet.write('B55', '', normal_format)
    worksheet.write('A56', 'Weight per Carton', bold_format)
    worksheet.write('B56', '', normal_format)
    worksheet.write('A57', 'FOB port', bold_format)
    worksheet.write('B57', '', normal_format)
    worksheet.write('A58', 'Delivery Time', bold_format)
    worksheet.write('B58', '', normal_format)
    worksheet.write('A59', 'Payment Term', bold_format)
    worksheet.write('B59', '', normal_format)
    worksheet.write('A60', 'Other', bold_format)
    worksheet.write('B60', '', normal_format)

    # Write additional information or comments based on doc_type
    if doc_type == "RFI":
        worksheet.write('A62', 'Information', bold_format)
        worksheet.write('B62', doc_data['information'], normal_format)
    elif doc_type == "RFQ":
        worksheet.write('A62', 'Quotation', bold_format)
        worksheet.write('B62', doc_data['quotationContent'], normal_format)

    worksheet.write('A64', 'Comment', bold_format)
    worksheet.write('B64', doc_data['comment'], normal_format)

    # Close the workbook and return the BytesIO buffer
    workbook.close()
    output.seek(0)
    
    return output
