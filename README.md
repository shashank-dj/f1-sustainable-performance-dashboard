# 🌱 Sustainable Performance Optimization in Formula 1 🏎️  
### A Data-Driven Sustainability & Performance Analysis Dashboard

This project analyzes Formula 1 race telemetry and lap data to evaluate how tyre management, degradation patterns, and pit stop strategy affect both race performance and sustainability efficiency. Using real telemetry data from the 2024 Formula 1 season, this dashboard compares any two drivers within a selected race and calculates a new **Sustainability Performance Score** to assess tyre usage efficiency and resource optimization.

The goal is to demonstrate how the right combination of race strategy and tyre management can contribute to **Formula 1’s Net Zero 2030 target**, where more efficient use of tyres and pit operations directly reduce environmental resource impact.

---

## 🎯 Project Goals
- Analyze F1 race telemetry data at lap-level detail
- Understand performance patterns influenced by tyre degradation & pit timing
- Engineer sustainability-focused metrics and build a sustainability score
- Visualize driver performance insights through an interactive dashboard
- Showcase how sustainable strategy can coexist with competitive performance

---

## 🧠 Sustainability Metrics Introduced
### **Sustainability Performance Score (Custom Metric)**
Formula:

SustainabilityScore = (AverageStintLength / MeanDegradationRate) – PitStopLossTime



| Parameter | Meaning |
|----------|---------|
| Average Stint Length | Duration between pit stops |
| Mean Degradation Rate | Tyre wear impact on performance |
| Pit Stop Loss Time | Time lost per pit stop relative to average racing pace |

⚡ **Higher score = better tyre efficiency, longer stints, fewer wasted resources**

---

## 📊 Dashboard Features
| Feature | Description |
|--------|-------------|
| Race Selector | Choose any Grand Prix dataset |
| Driver Selector | Compare any two drivers side-by-side |
| Lap Time Graph | Lap-by-lap pace comparison |
| Tyre Degradation Visualization | Efficiency in tyre wear |
| Pit Stop Detection | Automatic pit lap identification |
| Sustainability Score Table | Data-driven efficiency summary |
| Final Conclusion Message | Highlights the more sustainable driver |

---

## 🔍 Key Insights Example (Bahrain GP: VER vs HAM)
- **VER** shows stronger raw pace but more degradation variability
- **HAM** has smoother degradation control and lower pit loss time
- **HAM scores higher on sustainability**, indicating better resource efficiency
- Sustainable racing is not only about speed — it’s about **smart tyre and strategy management**

---

## 🌍 Alignment with F1 Net Zero 2030 Strategy
This project demonstrates sustainability analytics relevant to motorsport engineering:

♻ Reduced tyre usage → lower tyre production emissions  
⚙ Efficient pit strategies → reduced operations & logistics load  
🔋 Controlled degradation → lower energy & waste footprint  

---

## 🚀 Live Dashboard (Streamlit)
🔗 (https://f1-sustainable-performance-dashboard-shashank.streamlit.app/)

---

## 📦 Dataset Source
Kaggle – Formula 1 Telemetry Dataset

