# Do Discounts Really Drive Sales?

**Course:** ITEC 3310 – Data Visualization (York University)  
**Team:** Om Bagadia, Prabhleen Luthra, Lavanya Kumar  
**Stack:** Python · pandas · Plotly · Jupyter

Visual analysis of a public Kaggle Amazon U.S. electronics listings dataset. Relates **discount depth, price, ratings, reviews, and listing flags** to reported monthly purchases—aggregation and interactive Plotly charts (no predictive models).

## Findings (short)

- Average purchases tend to peak in **moderate** discount bands, not the deepest cuts.
- Very high discounts often sit with **lower** average ratings.
- Best Sellers cluster in a **mid-range** price band.
- Organic listings with strong reviews often look stronger than sponsored ones alone.

## What’s in this slim package

| File | Role |
|------|------|
| `Amazon_Upgraded_Final.ipynb` | Full Plotly-first analysis notebook |
| `amazon_products_sales_data_cleaned.csv` | **Sample** (~2k rows) for offline demo |
| `amazon_products_sales_data_sample.csv` | Same sample, explicit name |
| `final_report.md` / `.pdf` / `.docx` | Written report |
| `export_report_to_*.py` | Report export helpers |
| `requirements.txt` | Python dependencies |

> The full cleaned table is ~37 MB / ~42k rows and is **not** included (GitHub browser upload limit). Charts from the original analysis remain in the notebook outputs and report.

## Reproduce (sample data)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook Amazon_Upgraded_Final.ipynb
```

The notebook loads `amazon_products_sales_data_cleaned.csv` (sample in this package). Figures will match the report directionally but not the full-dataset numbers.

## Full dataset (optional)

1. Download [Amazon Electronics Products Sales Dataset (2025) on Kaggle](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025/data).
2. Run the notebook’s cleaning cells (or replace the sample CSV with your cleaned full file named `amazon_products_sales_data_cleaned.csv`).

## License / academic use

Course group project packaged for portfolio demonstration. Respect Kaggle dataset terms when redistributing data.
