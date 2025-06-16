def create_summary_sheet(ws3, indexed_table_df, target_wafer_ids):
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.styles import Font, Alignment
    import pandas as pd

    target_items = ['RWL', 'CWL', 'Cs', 'RBL', 'CBL', 'VTS', 'IDR', 'Cov', 'VFB']
    rename_items = {'CCAP@5K': 'Cs', 'CBL_ALL_(Cell)': 'CBL'}
    med_columns = [f"MED_{wafer_id}" for wafer_id in target_wafer_ids]
    summary_columns = ['ITEM', 'ITEM_ID', 'MV T/G MED', 'MV T/G Tol.'] + med_columns

    raw_summary_df = indexed_table_df[indexed_table_df['ITEM'].isin(target_items)][summary_columns].copy()
    raw_summary_df['ITEM'] = raw_summary_df['ITEM'].replace(rename_items)

    sort_order = [rename_items.get(i, i) for i in target_items]
    raw_summary_df['__order__'] = pd.Categorical(raw_summary_df['ITEM'], categories=sort_order, ordered=True)
    summary_df = raw_summary_df.sort_values('__order__').drop(columns='__order__')

    for row in dataframe_to_rows(summary_df, index=False, header=True):
        if any(cell != "" and cell is not None for cell in row):
            ws3.append(row)

    for cell in ws3[1]:
        cell.font = Font(bold=True, size=9)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    for row in ws3.iter_rows(min_row=2):
        for cell in row:
            col_name = ws3.cell(row=1, column=cell.column).value
            cell.font = Font(size=9)
            if isinstance(col_name, str) and col_name.startswith("Rate_"):
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '0.0%'
                    cell.value = round(cell.value, 3)
            elif isinstance(col_name, str) and col_name.startswith("Tol_"):
                try:
                    if isinstance(cell.value, float):
                        if abs(cell.value) >= 10000 or abs(cell.value) < 0.0001:
                            cell.number_format = '0.00E+00'
                        else:
                            cell.number_format = '0.00'
                except:
                    pass
            if col_name not in ['ITEM', 'ITEM_ID']:
                cell.alignment = Alignment(horizontal='center', vertical='center')
