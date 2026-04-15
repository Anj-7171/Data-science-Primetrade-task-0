import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_analysis(data_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(data_path)
    
    print("--- 1. Performance vs Sentiment ---")
    
    # Categorize Sentiment to Fear vs Greed broadly
    def classify_broad(sentiment):
        if 'Fear' in sentiment:
            return 'Fear'
        elif 'Greed' in sentiment:
            return 'Greed'
        return 'Neutral'
        
    df['broad_sentiment'] = df['sentiment_class'].apply(classify_broad)
    
    # Q1: Does performance differ between Fear vs Greed days?
    performance_metrics = df.groupby('broad_sentiment').agg(
        avg_daily_pnl=('daily_pnl', 'mean'),
        median_daily_pnl=('daily_pnl', 'median'),
        avg_win_rate=('win_rate', 'mean'),
        total_pnl=('daily_pnl', 'sum'),
        sample_size=('date', 'count')
    ).round(4)
    print(performance_metrics)
    performance_metrics.to_csv(os.path.join(output_dir, 'performance_by_sentiment.csv'))
    
    # Q2: Do traders change behavior based on sentiment (trade frequency, leverage, long/short bias, position sizes)?
    # Proxy for leverage might not be available directly cleanly without balance, but we have size and frequency.
    behavior_metrics = df.groupby('broad_sentiment').agg(
        avg_trades_per_day=('num_trades', 'mean'),
        avg_trade_size=('avg_trade_size', 'mean'),
        avg_long_short_ratio=('long_short_ratio', 'mean')
    ).round(4)
    print("\n--- 2. Behavior vs Sentiment ---")
    print(behavior_metrics)
    behavior_metrics.to_csv(os.path.join(output_dir, 'behavior_by_sentiment.csv'))
    
    # Plots
    sns.set_theme(style="whitegrid")
    
    # Plot 1: PnL by sentiment
    plt.figure(figsize=(8, 6))
    sns.barplot(data=performance_metrics.reset_index(), x='broad_sentiment', y='avg_daily_pnl', palette='coolwarm')
    plt.title('Average Daily PnL by Broad Sentiment')
    plt.savefig(os.path.join(output_dir, 'pnl_by_sentiment.png'))
    plt.close()
    
    # Plot 2: Win Rate by sentiment
    plt.figure(figsize=(8, 6))
    sns.barplot(data=performance_metrics.reset_index(), x='broad_sentiment', y='avg_win_rate', palette='viridis')
    plt.title('Average Win Rate by Broad Sentiment')
    plt.savefig(os.path.join(output_dir, 'win_rate_by_sentiment.png'))
    plt.close()

    # Plot 3: Long/Short Ratio by sentiment
    plt.figure(figsize=(8, 6))
    sns.barplot(data=behavior_metrics.reset_index(), x='broad_sentiment', y='avg_long_short_ratio', palette='magma')
    plt.title('Average Long/Short Trade Ratio by Broad Sentiment')
    plt.savefig(os.path.join(output_dir, 'long_short_ratio_by_sentiment.png'))
    plt.close()

    # Q3: Identify 2-3 segments
    # We already have `frequency_segment` and `volume_segment` from data prep.
    # Segment analysis: PnL on Fear vs Greed based on segments.
    segment_pnl = df.groupby(['broad_sentiment', 'frequency_segment', 'volume_segment']).agg(
        avg_daily_pnl=('daily_pnl', 'mean'),
        avg_win_rate=('win_rate', 'mean')
    ).reset_index()
    
    print("\n--- 3. Segments Performance ---")
    print(segment_pnl)
    segment_pnl.to_csv(os.path.join(output_dir, 'segment_performance.csv'))
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=segment_pnl, x='broad_sentiment', y='avg_daily_pnl', hue='frequency_segment', palette='mako')
    plt.title('Avg Daily PnL by Sentiment & Frequency Segment')
    plt.savefig(os.path.join(output_dir, 'pnl_by_frequency.png'))
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=segment_pnl, x='broad_sentiment', y='avg_daily_pnl', hue='volume_segment', palette='mako')
    plt.title('Avg Daily PnL by Sentiment & Volume Segment')
    plt.savefig(os.path.join(output_dir, 'pnl_by_volume.png'))
    plt.close()

    print("\nAnalysis complete. Outputs saved to", output_dir)

if __name__ == "__main__":
    run_analysis("merged_daily_trader_data.csv", "output")
