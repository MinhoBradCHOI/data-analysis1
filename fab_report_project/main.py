from export_excel import export_excel
from preprocess import preprocess_data
from analyze import plot_with_reference
from config import save_dir

if __name__ == '__main__':
    # Excel 저장 및 경로 확인
    path = export_excel()
    print(f"✅ Excel saved to: {path}")

    # merged_df 다시 불러와서 분석
    merged_df = preprocess_data()

    # 분석용 그래프 저장
    plot_with_reference(merged_df, save_dir)
