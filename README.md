# Mali Education Risk Monitoring System (2026)

An advanced analytical toolkit for visualizing conflict incidents and identifying educational infrastructure at risk across Mali.

## 🔗 Project Links
- **Interactive Map:** [Conflict & Risk Map](https://entaganzwa.github.io/Exam/conflict_map.html)
- **Facility Analysis:** [School Impact Map](https://entaganzwa.github.io/Exam/school_map.html)
- **Comprehensive Dashboard:** [Advanced Metrics Dashboard](https://entaganzwa.github.io/Exam/comprehensive_dashboard.html)

---

## 🚀 The Project Process

This project follows a data-driven workflow to transform raw conflict and geographical data into actionable insights for educational protection in Mali.

### 1. Data Collection
We utilized two primary open-source datasets:
- **Conflict Data:** [UCDP GED (Global Events Dataset) v25.1](https://ucdp.uu.se/downloads/index.html#ged) - Providing precise geolocation and details of organized violence.
- **Education Facilities:** [Humanitarian OpenStreetMap Team (HOTOSM)](https://data.humdata.org/organization/hot) - Comprehensive mapping of schools and educational centers in Mali.

### 2. Data Filtering & Cleaning
Using Python, we isolated relevant events:
- `scripts/filter_mali.py`: Filters the global GED dataset specifically for Mali events.
- `scripts/extract_advanced_metrics.py`: Aggregates statistics by region, violence type, and year for dashboarding.

### 3. Spatial Risk Analysis
We performed distance-based calculations to identify schools in proximity to conflict:
- `scripts/identify_schools_near_conflicts.py`: Uses the Haversine formula to calculate the distance between every school and every conflict event.
- **Risk Definition:** Schools within a **1km radius** of a conflict event are flagged as "At-Risk".

### 4. Interactive Visualization
- **Leaflet.js:** Used for the interactive maps with clustering and risk-zone overlays.
- **D3.js & Bootstrap:** Powering the comprehensive dashboard for statistical insights.

---

## 📂 Repository Structure

```
/
├── data/
│   ├── raw/        # Original datasets (GeoJSON/CSV)
│   └── processed/  # Filtered and analyzed data
├── scripts/        # Python processing scripts
├── js/             # Data files formatted for web visualization
├── index.html      # Project landing page
├── conflict_map.html
├── school_map.html
└── comprehensive_dashboard.html
```

## 🛠️ How to Run
1. **Prerequisites:** Python 3.x
2. **Setup:**
   ```bash
   git clone https://github.com/entaganzwa/Exam.git
   cd Exam
   ```
3. **Run Analysis:**
   ```bash
   python3 scripts/filter_mali.py
   python3 scripts/identify_schools_near_conflicts.py
   ```
4. **View Results:** Open `index.html` in any modern web browser.

---
© 2026 Mali Conflict Risk Project • Developed for educational protection monitoring.
