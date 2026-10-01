# Title Page

**Project title:** Do Discounts Really Drive Sales? A Visual Analysis of Amazon Electronics Products  

**Course / section:** ITEC 3310 – Data Visualization *(replace with your section code if required)*  

**Team members (name and student ID):**  
- Om Bagadia — 219273994  
- Prabhleen Luthra — 219617109  
- Lavanya Kumar — 219148790  

**Date:** March 2026  

---

# Abstract *(target: 150–250 words)*

Retailers use discounts and badges to move inventory, but shoppers often wonder whether a steep markdown means a good deal or a weak product. We study the public Kaggle dataset of Amazon U.S. electronics listings (roughly 42,000 rows after preprocessing) and ask how discount depth, price, ratings, reviews, and listing flags relate to reported monthly purchases. Work was done in Python with Plotly-first charts in a Jupyter notebook—no predictive models, only aggregation and visuals so non-technical readers can follow the story. We compare categories, plot discount against sales on a log scale with a smoothed trend, split products into discount bands, compare Best Seller versus non–Best Seller prices, and summarize relationships with a correlation heatmap. The patterns line up with a few practical takeaways: average purchases tend to peak in moderate discount bands, not at the deepest cuts; very high discounts sit with lower average ratings; Best Sellers cluster in a mid-range price band rather than at the bottom; and organic listings with strong reviews often look stronger than sponsored ones alone. Discounting appears most useful as part of a broader quality-and-trust strategy, not as a stand-alone lever.

*(Word count for the abstract paragraph above: ~230 words.)*

---

# 1. Introduction (Problem Overview)

**Domain.** Online marketplaces list huge catalogs of electronics; prices and promotions change constantly. Managers choose discount depth and placement; buyers weigh price against ratings and trust signals.

**Who the work is for.** We aimed the visuals at e-commerce and pricing staff, product managers, and analysts who need quick pattern reads without wading through model output. Marketing and ops teammates who are not coding-heavy should still be able to use the charts in meetings.

**Motivation.** It is easy to assume “bigger discount → more sales,” but that story can hide weaker products or training shoppers to wait for fire sales. We wanted a clear, picture-based read of what the Amazon snapshot actually shows.

**Objectives.** (1) Describe how categories differ in volume and satisfaction. (2) Relate discount level to sales and ratings. (3) Compare Best Seller pricing to other listings. (4) Summarize which numeric and flag variables move together with purchases. All of this is done through interactive Plotly figures linked in our notebook; the report highlights five figures (Figures 1–5) that match those goals.

---

# 2. Data Description

**Source and link.** We used the *Amazon Electronics Products Sales Dataset (2025)* on Kaggle:  
https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025/data  

**Size and grain.** The raw CSV contains on the order of 42,000+ rows—one row per product listing at scrape time. Currency is USD; the scrape is a single snapshot, not a time series.

**Key variables.** Titles and `product_category`; `product_rating` and `total_reviews`; `purchased_last_month` as a coarse sales proxy (Amazon rounds to bands such as 100 or 1,000); `original_price`, `discounted_price`, and `discount_percentage`; flags such as `is_best_seller`, `is_sponsored`, `has_coupon`, and `buy_box_availability`; timestamps and optional sustainability tags.

**Cleaning and preprocessing.** Column names were normalized. Ratings, counts, prices, and discounts were converted to numeric; bad strings became missing. We **dropped rows missing rating, either price, or category** so every remaining row supports fair comparisons.  

**Why we removed non-positive prices (zero or negative `original_price`).** A listed “original” price of zero or below is not a valid retail price in this context—it usually means missing data, a placeholder, or a malformed scrape. Keeping those rows would break sensible discount math (division by zero or nonsense percentages) and would distort histograms and correlations. Restricting to `original_price > 0` keeps the analysis focused on normal product listings.  

We also **trimmed extreme price outliers** using the 1st–99th percentile of `original_price` so a handful of extreme SKUs do not stretch every chart. **Missing `discount_percentage`** was set to **0**, treating “no discount field” as full price—consistent with many rows where list and sale price match. We added **discount buckets** (e.g., none, 1–10%, …, 50%+) and **log10 transforms** for heavily skewed counts (reviews, monthly purchases) where noted in the notebook.

After these steps the working table still contains tens of thousands of rows—enough for category-level and discount-band views without claiming row-level precision for sales.

---

# 3. Tasks / Analysis Questions

Our notebook is organized around these questions (each maps to at least one main figure):

1. **Which electronics categories show the most listings, and how do average ratings vary across them?** → Figure 1.  
2. **How does discount percentage relate to reported monthly purchases, and do Best Sellers sit in one part of that space?** → Figure 2.  
3. **Do average purchases and average ratings move together across discount bands, or do deep discounts trade volume for weaker ratings?** → Figure 3.  
4. **How do list prices differ between Best Seller and non–Best Seller products?** → Figure 4.  
5. **Which variables correlate most strongly with monthly purchases, and how strong is discount versus badges and reviews?** → Figure 5.  

Supporting plots in the notebook (e.g., sponsored versus organic, violin plots by discount band) answer follow-up questions but are not the five figures we cite in this report.

---

# 4. Solution and Design Rationale

**Tooling.** Analysis runs in **Python** with **pandas** and **numpy**; plots use **Plotly Express** and **Plotly Graph Objects** so users can hover, zoom, and inspect outliers. **Matplotlib/Seaborn** appear only for light exploration. The full workflow lives in `Amazon_Upgraded_Final.ipynb`; this report does not paste code blocks—see the notebook for implementation detail.

**Figure 1 (categories).** Horizontal bars show the top categories by **count** of products, with **color encoding average rating** (RdYlGn-style scale). That pairing lets a reader see at once where inventory piles up versus where satisfaction is higher—bar length for volume, color for quality.

**Figure 2 (discount vs sales).** Scatter of **discount %** versus **log10(purchased_last_month)** with points colored by Best Seller badge. A **LOWESS-style trendline** (via Plotly’s trendline option, which relies on **statsmodels** for LOWESS) highlights non-linear shape without forcing a straight line. Log scale tames heavy-tailed purchase counts.

**Figure 3 (discount buckets).** Side-by-side **bar charts** of mean purchases and mean rating by discount bucket give a simple read of “sweet spot” bands versus the heaviest markdowns.

**Figure 4 (price distributions).** **Overlapping histograms** of `original_price` for Best Seller vs not, with **median markers**, show where mass sits without assuming normality.

**Figure 5 (correlations).** A **heatmap** of Pearson correlations among prices, discount, rating, reviews, purchases, and binary flags gives one compact view of which signals line up with sales in this snapshot.

We chose Plotly for interactivity and for consistent styling (white background, readable fonts) when presenting live; static exports for the report preserve the same encodings.

---

# 5. Insights and Findings *(with figure references)*

**Insight 1 — Category size is not the same as “best” ratings.** Figure 1 shows that the categories with the most products are not always the highest-rated; niche categories can show strong average ratings with fewer SKUs.

**Insight 2 — Moderate discounts line up with stronger typical sales than the deepest cuts.** Figures 2 and 3 together suggest a peak in average purchases around mid-range discount bands rather than at 50%+ off; the trendline in Figure 2 bends accordingly.

**Insight 3 — Heavy discount bands carry weaker average ratings.** Figure 3’s rating bars dip in the highest discount bucket; supplementary violin plots in the notebook reinforce that pattern—aggressive markdowns often sit with lower star averages.

**Insight 4 — Best Sellers are not simply “the cheapest.”** Figure 4 shows overlapping price distributions with medians that do not pin Best Sellers to the bottom of the price range; many sit in a mid-range band buyers treat as fair for trusted items.

**Insight 5 — Purchases track badges and reviews more than discount alone.** Figure 5 shows stronger correlations for variables like Best Seller flag and review volume with `purchased_last_month` than for discount percentage alone; sponsored status is only modestly related in this data.

**Insight 6 — Sponsored placement is no guarantee of higher median volume.** Notebook comparisons (grouped boxes and bar summaries) show organic Best Sellers often outperform sponsored listings on median purchases—paid placement does not replace product strength.

---

# 6. Limitations and Future Work

**Limitations.** `purchased_last_month` is **bucketed and rounded** by Amazon, so fine-grained sales differences disappear. The data are a **single cross-section**—no seasonality or causal identification. We have **no cost or margin**, so we cannot say which discount policy maximizes profit. **Filtering** (missing fields, positive prices, percentile trim) may drop atypical listings; results describe the retained population. **Correlation is not causation**—brand, search rank, and ads are unobserved.

**Future work.** A longitudinal scrape would show how discounts and ranks co-move over time. Combining with **revenue** or **margin** data would support pricing decisions. Text features from titles or review sentiment could add context beyond numeric fields.

---

# 7. Conclusion

We used a notebook-driven, visualization-heavy workflow on a large Amazon electronics extract to ask whether discounts “drive” sales. The answer is nuanced: **moderate** discounts show up more often alongside stronger typical purchase levels than **extreme** markdowns, while very deep discounts align with **lower average ratings**. Best Sellers concentrate in a sensible mid-price range, and **trust signals** (reviews, badges) show up strongly in the correlation view. For the course contribution, the main payoff is a reproducible story—Figures 1–5—that managers can walk through without reading equations, plus explicit data rules (including **dropping invalid zero/negative list prices**) so others can judge what the charts represent.

---

# References

1. **Dataset (primary data source).** Ikram Shah. *Amazon Products Sales Dataset – 42k+ Items (2025).* Kaggle.  
   https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025/data  

2. **Python Software Foundation.** Python Programming Language. https://www.python.org/  

3. **pandas development team.** pandas: data structures for relational data. https://pandas.pydata.org/  

4. **Plotly Technologies Inc.** Plotly graphing libraries (Plotly Express, Graph Objects). https://plotly.com/python/  

5. **Project Jupyter.** Jupyter Notebook / JupyterLab. https://jupyter.org/  

6. **Seaborn.** Statistical data visualization for Python. https://seaborn.pydata.org/  

7. **Matplotlib.** Visualization with Python. https://matplotlib.org/  

8. **statsmodels** (used by Plotly for LOWESS trendlines in scatter plots). https://www.statsmodels.org/  

*(If your course requires APA or IEEE style, reformat these entries accordingly; links above are stable enough for a data-viz project report.)*

---

*End of main report body (excluding this note). Target length when pasted into Word with figures: roughly 6–8 pages excluding references and any appendix; add your five figures with captions and in-text “Figure n” references as you layout the document.*
