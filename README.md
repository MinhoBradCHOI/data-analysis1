## Fab data analysis project
#1. Work Purpose
- Analyze the relationship between EDS data and FAB data, and suggest a direction for yield improvement and process optimization.

#2. Methods
- Imports EDS and FAB data stored on the company server
- Conducts trend analysis for each EDS item
- Analyzes inter-item relationships
- Applies basic machine learning models using Scikit-learn

```## 📁 Code Structure
fab_report_project/
├── main.py
├── config.py
├── preprocess.py
├── export_excel.py
├── analyze.py
├── data/
│   └── raw/ (server data in reality)
│       ├── fake_eds_dataset.csv
│       └── fake_fab_dataset.csv
└── PythonSave/
```
#4. Main Results (saved as the excel file (Tables) and HTML (Graphs)
 1) Trend analysis of major EDS items such as Bitline(BL) Resistance (RBL) and Capacitance (CBL)

 2) Correlation analysis between RBL and CBL

 3) Exploratory analysis of RBL (EDS) and BL-related FAB data

 4) Conclusion & Recommendation:
  RBL and CBL show strong correlation within EDS data.
  However, the R² between RBL (EDS) and GBL CD (FAB data) is low.
  This suggests that RBL cannot be fully explained by FAB data alone.
  Additional analysis such as vertical structural review (TEM) is recommended.
 
#5. Version
   - python 3.12.7
   - pandas 2.2.2
   - numpy 1.26.4
   - sklearn 1.5.1
   - openpyxl 3.1.5
   - plotly 5.24.1
