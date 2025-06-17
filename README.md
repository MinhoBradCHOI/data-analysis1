# 📊 Fab Data Analysis Project

## #1. Work Purpose

Analyze the relationship between **EDS data** and **FAB data**, and suggest a direction for **yield improvement** and **process optimization**.

---

## #2. Methods

- Import **EDS** and **FAB** data stored on the company server  
- Conduct **trend analysis** for each EDS item  
- Analyze **inter-item correlations**  
- Apply basic **machine learning models** using `Scikit-learn`

---

## #3. 📁 Code Structure
```fab_report_project/
├── main.py
├── config.py
├── preprocess.py
├── export_excel.py
├── analyze.py
├── data/
│ └── raw/ (server data in reality)
│ ├── fake_eds_dataset.csv
│ └── fake_fab_dataset.csv
└── PythonSave/
```

---

## #4. Main Results  
📁 **Saved as:**  
- Excel (`.xlsx`) for tables
[LOT3_W01_W02_W03_20250617.xlsx](https://github.com/user-attachments/files/20774410/LOT3_W01_W02_W03_20250617.xlsx)

- HTML (`.html`) for interactive graphs

### ✅ Key Outcomes

1. **Trend analysis** of major EDS items:  
   - Bitline Resistance (**RBL**)  
   - Bitline Capacitance (**CBL**)

2. **Correlation analysis** between **RBL** and **CBL**

3. **Exploratory analysis** of **RBL (EDS)** and **BL-related FAB data**

4. **Conclusion & Recommendation**:
   - Strong correlation observed between **RBL** and **CBL** in EDS data
   - However, the **R² between RBL (EDS)** and **GBL CD (FAB data)** is low  
   → This indicates that **RBL cannot be fully explained by FAB data alone**  
   → Further analysis using **vertical structural review (e.g., TEM)** is recommended
![RBLvs tTKOUT](https://github.com/user-attachments/assets/42b0c3b0-f55b-4c78-a261-95d936c781fd)
![CBLvs tTKOUT](https://github.com/user-attachments/assets/cef3d79b-488f-46b5-b20c-f32b365bda30)
![RBLvsCBL](https://github.com/user-attachments/assets/09f05967-3e80-4326-83ea-3443b4ffef44)
![RBLvsGBL_CD](https://github.com/user-attachments/assets/cfe947c7-4551-4d57-a93c-6125312af13a)

---

## #5. Version Info

| Package      | Version |
|--------------|---------|
| Python       | 3.12.7  |
| pandas       | 2.2.2   |
| numpy        | 1.26.4  |
| scikit-learn | 1.5.1   |
| openpyxl     | 3.1.5   |
| plotly       | 5.24.1  |

