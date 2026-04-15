<<<<<<< HEAD
# Trader Performance vs Market Sentiment 📊

This repository contains the solution for the Primetrade Data Science intern project. It analyzes how Bitcoin Market Sentiment (Fear/Greed) affects trader behavior, frequency, sizing, and performance on Hyperliquid.

## Project Structure
- `data_processor.py`: The data-prep module to clean, merge, process, and aggregate the raw data into daily trader metrics.
- `analysis.py`: The analytical engine producing statistical segmentations and generating the output charts.
- `app.py`: The Streamlit dashboard to interactively visualize the findings.
- `output/`: Auto-generated folder containing the exported metrics and visualization figures (PNGs).
- `merged_daily_trader_data.csv`: The cleaned target dataset mapping trader daily PnL, volume, frequency, and sentiment indices.

## Prerequisites & Setup
1. Ensure the following packages are installed:
   ```bash
   pip install pandas numpy matplotlib seaborn streamlit
   ```
2. Place the extracted datasets (`historical_data.csv` and `fear_greed_index.csv`) in the root directory.

## Execution
1. **Prepare Data:**
   Run `python data_processor.py` (this normalizes UTC timestamps, handles duplicates/missings, and creates the metrics).
2. **Generate Analysis Report & Charts:**
   Run `python analysis.py`. This reads the merged dataset, performs segmentations, and writes charts securely into the `output/` directory.
3. **Launch the Dashboard:**
   Run `streamlit run app.py` to view an interactive breakdown of Trader Performance segmented by Sentiment, Volume, and Frequency segments.

---

## 📈 Methodology

1. **Alignment:** Converted raw Hyperliquid Unix/IST timestamps into cleanly formatted Daily UTC boundaries. Matched those with the global daily Fear/Greed classifications.
2. **Action Engineering:** 
   - `Daily PnL`: Sum of aggregated Closed PnL per trader per day.
   - `Win Rate`: Closed profitable trades divided by total closed trades.
   - `Volume`: Metric computed primarily bridging token Size USD aggregated.
   - `L/S Ratio`: Evaluated the Side column (BUY vs SELL flags).
3. **Segmentation Definition:**
   Calculated global player behavior by segregating them based on their medians:
   - **Frequency Segment**: Frequent vs Infrequent traders.
   - **Volume Segment**: High Volume vs Low Volume execution limits.

---

## 💡 Key Insights (Backed by Data)

1. **Oversizing & Panic "Dip-Buying" During Fear:**
   - **Observation:** On Fear days, the average trader executes **MORE** trades per day (47.3 vs 41.2 on Greed) and vastly increases execution **Sizes** ($8,529 vs $5,954). The Long/Short ratio spikes aggressively to 8.37 vs 5.72 on Greed days.
   - **Insight:** When the market tanks into Fear, traders engage in aggressive "dip-buying" and catch falling knives by significantly leveraging up their positions on the Long side.
2. **Choppiness Destroys Overtraders:**
   - **Observation:** Under the 'Fear' classification, High-Volume traders who trade **Frequently** underperform vastly (Avg PnL: $3,894) compared to High-Volume traders who trade **Infrequently** (Avg PnL: $17,834).
   - **Insight:** High volatility on Fear days leads to massive chop. Catching falling knives in quick succession erodes capital, whereas taking a single heavy calculated position performs roughly 4.5x better.
3. **Retail Disadvantage in Fear:**
   - **Observation:** The "Infrequent + Low Volume" (proxy for Retail) trader does awfully on Fear days (65.5% win rate, $811 daily PnL). Conversely, during Greed regimes, this exact same segment achieves a stellar **93.7% win rate**.
   - **Insight:** Lower volume traders lack the margin to survive drawdown wicks during extreme market turbulence, causing capitulation closures, whereas on Greed days, an overarching uptrend carries their generic strategies to safety.

---

## 🚀 Strategy Recommendations (Actionable Output)

**Strategy 1 (For Heavy Algorithmic / High-Volume Accounts):**
**"VIX/Fear Volume Throttling"**
*Rule of Thumb:* When the Sentiment enters 'Fear' or 'Extreme Fear', programmatically reduce trade velocity (frequency of entries per hour) by 50% but allow sizing to remain high for concentrated entries. *Rationale: Escaping the high-volatility "chop zone" prevents death-by-a-thousand cuts. The data supports infrequent, high-volume traders dominating the fear chop.*

**Strategy 2 (Risk Management for Retail / Low Accounts):**
**"Long-Only Trend Safety"**
*Rule of Thumb:* If you are a Low-Volume trader, implement a strict halt on deploying capital during Fear days. Only execute setups when the sentiment transitions into 'Greed'.
*Rationale:* Moving from a 65% win-rate knife-catching scenario to a mathematically backed 93% structural uptrend momentum scenario guarantees systemic profitability over an extended horizon. Avoid fighting extreme systemic fear.
=======
# Data-science-Primetrade-task-0
>>>>>>> 4f9b5b7033f69db88f847167d51d55d5f982e21f
