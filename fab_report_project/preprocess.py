import pandas as pd
import numpy as np
from config import data_path_eds, data_path_fab

def preprocess_data():
    # ✅ 1. 사용할 item_id 목록 구성
    item_ids = ['RWL', 'CWL', 'Cs', 'RBL', 'CBL', 'VTS', 'IDR', 'SWS', 'Cov', 'VFB'] + [f'ITEM{i}' for i in range(1, 88)]

    # ✅ 2. EDS 데이터 전처리
    df_eds = pd.read_csv(data_path_eds)

    df_eds = df_eds[
        (df_eds['tkout_time'] >= '2025-04-07') &
        (df_eds['line_id'] == 'PPPP') &
        (df_eds['subitem_id'].astype(int).between(1, 13)) &
        (df_eds['item_id'].isin(item_ids))
    ]

    df_eds['et_value'] = pd.to_numeric(df_eds['et_value'], errors='coerce')

    # ✅ subitem_id 매핑
    df_eds['subitem_id'] = df_eds['subitem_id'].astype(int).map({
        7: 1, 4: 2, 5: 3, 10: 4, 9: 5, 1: 6, 3: 7, 8: 8,
        12: 9, 13: 10, 11: 11, 6: 12, 2: 13
    })

    # ✅ 피벗
    pivot_table_eds = df_eds.pivot_table(
        index=['root_lot_id', 'wafer_id', 'subitem_id', 'tkout_time', 'rework_cnt'],
        columns='item_id', values='et_value', aggfunc='first', observed=True
    ).reset_index()

    # ✅ IDR 단위 변환
    pivot_table_eds['IDR'] = pivot_table_eds.get('IDR', 0) * 1e6

    # ✅ 3. FAB 데이터 전처리
    df_fab = pd.read_csv(data_path_fab)

    valid_pairs_fab = [('SK016125', 'CD1'), ('SK016125', 'CD3'), ('SK036210', 'THK1_1_TOP')]
    filtered_result_fab = df_fab[df_fab[['step_seq', 'item_id']].apply(tuple, axis=1).isin(valid_pairs_fab)]

    # 🛠️ str 접근자 오류 방지 → 문자열 변환 후 'S' 제거
    filtered_result_fab['subitem_id'] = (
        filtered_result_fab['subitem_id']
        .astype(str)
        .str.replace('S', '', regex=False)
        .astype(int)
    )

    filtered_result_fab['column_id'] = (
        filtered_result_fab['step_seq'] + '_' + filtered_result_fab['item_id']
    )

    filtered_result_fab['fab_value'] = pd.to_numeric(filtered_result_fab['fab_value'], errors='coerce')

    # ✅ 피벗
    pivot_table_fab = filtered_result_fab.pivot_table(
        index=['root_lot_id', 'wafer_id', 'subitem_id'],
        columns='column_id', values='fab_value', aggfunc='first', observed=True
    ).reset_index()

    # ✅ 4. Join을 위한 key 정렬
    join_keys = ['root_lot_id', 'wafer_id', 'subitem_id']
    pivot_table_eds[join_keys] = pivot_table_eds[join_keys].astype(str)
    pivot_table_fab[join_keys] = pivot_table_fab[join_keys].astype(str)

    # ✅ 5. Merge
    merged_df = pivot_table_eds.merge(pivot_table_fab, on=join_keys, how='left')

    # ✅ rework_cnt 기준 최신 이력 추출
    merged_df['rework_cnt'] = merged_df['rework_cnt'].astype(int)
    merged_df = merged_df.sort_values('rework_cnt', ascending=False).drop_duplicates(
        subset=['root_lot_id', 'wafer_id', 'subitem_id'], keep='first'
    )

    # ✅ wafer_id 2자리 문자열 패딩
    merged_df['wafer_id'] = merged_df['wafer_id'].astype(str).str.zfill(2)

    return merged_df
