# fab_report_project/analyze.py (SK016125_CD1 vs RBL 추가)

import pandas as pd
import os
import plotly.graph_objects as go
import plotly.io as pio
from config import target_root_lot_id, target_wafer_ids
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def generate_single_plot(df, item, target_root_lot_id):
    df['value'] = pd.to_numeric(df[item], errors='coerce')
    fig = go.Figure()

    sorted_lots = sorted(df['root_lot_id'].dropna().unique())

    for lot in sorted_lots:
        lot_df = df[df['root_lot_id'] == lot]
        fig.add_trace(go.Scatter(
            x=lot_df['tkout_time'],
            y=lot_df['value'],
            mode='markers',
            name=lot,
            marker=dict(
                size=8,
                color='navy' if lot == target_root_lot_id else None,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            customdata=lot_df[['root_lot_id', 'wafer_id', 'subitem_id']].values,
            hovertemplate="root_lot_id: %{customdata[0]}<br>wafer_id: %{customdata[1]}<br>"
                          "subitem_id: %{customdata[2]}<br>tkout_time: %{x}<br>value: %{y:.3f}"
        ))

    mv_tg_dict = {
        "RBL": {"med": 154200, "tol": 15420.0},
        "CBL": {"med": 28.4, "tol": 2.84},
    }
    ref_med = mv_tg_dict[item]['med']
    ref_tol = mv_tg_dict[item]['tol']

    fig.add_hline(y=ref_med, line_color="red", line_dash="dash",
                  annotation_text=f"MED={ref_med}", annotation_position="top right")
    fig.add_hline(y=ref_med + ref_tol, line_color="gray", line_dash="dot",
                  annotation_text=f"+Tol={ref_med + ref_tol}", annotation_position="top right")
    fig.add_hline(y=ref_med - ref_tol, line_color="gray", line_dash="dot",
                  annotation_text=f"-Tol={ref_med - ref_tol}", annotation_position="top right")

    unit = "Ω" if item == "RBL" else "fF"
    fig.update_layout(
        title=f"{item} vs tkout_time",
        xaxis_title="tkout_time",
        yaxis_title=f"{item}, {unit}",
        height=500,
        width=700,
        legend_title="root_lot_id"
    )
    return fig


def generate_correlation_plot(df, x_col, y_col, x_label, y_label, title, target_root_lot_id):
    df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
    df = df.dropna(subset=[x_col, y_col])

    X = df[x_col].values.reshape(-1, 1)
    y = df[y_col].values
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    fig = go.Figure()

    sorted_lots = sorted(df['root_lot_id'].dropna().unique())
    for lot in sorted_lots:
        lot_df = df[df['root_lot_id'] == lot]
        fig.add_trace(go.Scatter(
            x=lot_df[x_col],
            y=lot_df[y_col],
            mode='markers',
            name=lot,
            marker=dict(
                size=8,
                color='navy' if lot == target_root_lot_id else None,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            customdata=lot_df[['root_lot_id', 'wafer_id', 'subitem_id']].values,
            hovertemplate=f"root_lot_id: %{{customdata[0]}}<br>wafer_id: %{{customdata[1]}}<br>"
                          f"subitem_id: %{{customdata[2]}}<br>{x_label}: %{{x:.3f}}<br>{y_label}: %{{y:.3f}}"
        ))

    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=y_pred,
        mode='lines',
        name='Linear Fit',
        line=dict(color='red', dash='dash')
    ))

    x_max = df[x_col].max()
    y_max = y_pred[df[x_col].argmax()]

    fig.add_annotation(
        x=x_max,
        y=y_max - (y_max * 0.05),
        text=f"R² = {r2:.4f}",
        showarrow=False,
        font=dict(size=14, color="red"),
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500,
        width=700,
        legend_title="root_lot_id",
    )
    return fig


def plot_with_reference(merged_df, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    merged_df['tkout_time'] = pd.to_datetime(merged_df['tkout_time'], errors='coerce')
    df_all = merged_df.copy()

    fig_rbl = generate_single_plot(df_all.copy(), "RBL", target_root_lot_id)
    fig_cbl = generate_single_plot(df_all.copy(), "CBL", target_root_lot_id)
    fig_corr = generate_correlation_plot(df_all.copy(), "CBL", "RBL", "CBL, fF", "RBL, Ω", "RBL vs CBL", target_root_lot_id)
    fig_cd1 = generate_correlation_plot(df_all.copy(), "SK016125_CD1", "RBL", "GBL CD, nm", "RBL, Ω", "RBL vs GBL CD", target_root_lot_id)

    html_rbl = pio.to_html(fig_rbl, include_plotlyjs='cdn', full_html=False)
    html_cbl = pio.to_html(fig_cbl, include_plotlyjs=False, full_html=False)
    html_corr = pio.to_html(fig_corr, include_plotlyjs=False, full_html=False)
    html_cd1 = pio.to_html(fig_cd1, include_plotlyjs=False, full_html=False)

    html_combined = f"""
    <html>
    <head><title>RBL, CBL & Correlation Plot</title></head>
    <body>
    <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
        <div style="margin: 10px">{html_rbl}</div>
        <div style="margin: 10px">{html_cbl}</div>
        <div style="margin: 10px">{html_corr}</div>
        <div style="margin: 10px">{html_cd1}</div>
    </div>
    </body>
    </html>
    """

    output_path = os.path.join(save_dir, "plot_RBL_CBL_separated.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_combined)

    print(f"✅ 분리된 RBL/CBL/Correlation 그래프 저장 완료: {output_path}")
