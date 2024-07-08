import json


def parse_table(table, websocket_response, base_ws):
    # Initialize the result dictionary
    result = {
        'columns': [],
        'order_by': None,
        'conditions_data': {},
        'page_size': None,
        'row_height': None,
        'color_conditions': {},
        'module': 'SO'
    }

    for i, row in enumerate(table):
        col_view = row['Columns View']
        ws_response = websocket_response.get(col_view)

        # Map Columns View
        if ws_response:
            result['columns'].append({
                'index': ws_response['index'],
                'sort': i
            })

        # Map Sort By
        sort_by = row['Sort By']
        if sort_by:
            result['order_by'] = {
                'direction': sort_by,
                'index': ws_response['index']
            }

        # Map Condition
        condition = row['Condition']
        if condition:
            conditions = condition.split(',')
            for cond in conditions:
                cond_type, cond_value = cond.split('=')
                result['conditions_data'].setdefault(ws_response['filter'], []).append({
                    'type': cond_type,
                    'value': cond_value
                })

        # Map Row Height
        row_height = row['Row Height']
        if row_height:
            result['row_height'] = row_height

        # Map Lines per page
        lines_per_page = row['Lines per page']
        if lines_per_page:
            result['page_size'] = lines_per_page

        # Map Highlight By
        highlight_by = row['Highlight By']
        if highlight_by:
            highlights = highlight_by.split('/')
            for highlight in highlights:
                h_parts = highlight.split('=')
                if len(h_parts) >= 2:
                    h_type = h_parts[0]
                    h_value = h_parts[1]
                    color = h_parts[2] if len(h_parts) > 2 else ''
                    result['color_conditions'].setdefault(ws_response['filter'], []).append({
                        'type': h_type,
                        'value': h_value,
                        'color': color
                    })

    # Assign defaults if not set
    result['page_size'] = result['page_size'] or ''
    result['row_height'] = result['row_height'] or ''

    return result


table = [{'Columns View': 'SO Number', 'Sort By': '', 'Highlight By': 'equals=S110=rgba(172,86,86,1)/equals=S111',
          'Condition': 'equals=S110,equals=S111', 'Row Height': '60', 'Lines per page': '25'},
         {'Columns View': 'Client PO', 'Sort By': '', 'Highlight By': 'equals=S110,equals=S111', 'Condition': '',
          'Row Height': '', 'Lines per page': ''},
         {'Columns View': 'Terms of Sale', 'Sort By': 'asc', 'Highlight By': 'equals=ToS110=rgba(172,86,86,1)',
          'Condition': '', 'Row Height': '', 'Lines per page': ''}]

websocket_response = {'Client PO': {'index': 'so_list_client_po', 'filter': 'client_po'},
                      'SO Number': {'index': 'so_list_so_number', 'filter': 'so_no'},
                      'Terms of Sale': {'index': 'so_list_terms_of_sale', 'filter': 'term_sale'}}

base_ws = {'Columns View': 'columns',
           'Sort By': 'order_by',
           'Condition': 'conditions_data',
           'Lines per page': 'page_size',
           'Row Height': 'row_height',
           'Highlight By': 'color_conditions'}

# result = {'columns': [{'index': 'so_list_so_number', 'sort': 0},
#                       {'index': 'so_list_client_po', 'sort': 1},
#                       {'index': 'so_list_terms_of_sale', 'sort': 2}],
#           'order_by': {'direction': 'asc', 'index': 'so_list_terms_of_sale'},
#           'conditions_data': {'so_no': [{'type': 'equals', 'value': 'S110'},
#                                         {'type': 'equals', 'value': 'S111'}],
#                               'client_po': [{'type': 'equals', 'value': 'P110'}]},
#           'page_size': '25',
#           'row_height': '60',
#           'color_conditions': {'so_no': [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}],
#                                'client_po': [{'type': 'equals', 'value': 'S110', 'color': ''},
#                                              {'type': 'equals', 'value': 'S111', 'color': ''}],
#                                'term_sale': [{'type': 'equals', 'value': 'S113', 'color': ''},
#                                              {'type': 'equals', 'value': 'S112', 'color': ''}]},
#           'module': 'SO'}

result = parse_table(table, websocket_response, base_ws)
print(json.dumps(result, indent=4))
