import pandas as pd
import numpy as np

def process_data(trader_data_path, sentiment_data_path, output_path):
    print("Loading data...")
    df_trades = pd.read_csv(trader_data_path)
    df_sentiment = pd.read_csv(sentiment_data_path)

    print("Initial trade rows/cols:", df_trades.shape)
    print("Initial sentiment rows/cols:", df_sentiment.shape)

    # 1. Date Alignment
    # The 'Timestamp IST' column looks like '02-12-2024 22:50'. We can extract date.
    df_trades['Datetime'] = pd.to_datetime(df_trades['Timestamp IST'], format='mixed', dayfirst=True)
    df_trades['date'] = df_trades['Datetime'].dt.date.astype(str)
    
    df_sentiment['date'] = pd.to_datetime(df_sentiment['date']).dt.date.astype(str)
    
    # 2. Aggregate Data per Trader per Day
    # Closed PnL might be sum-able. 
    # Notice that Closed PnL is 0 for opening trades, but we have it for closing trades.
    # We will compute daily PnL, trade counts, volume, win rates.
    
    df_trades['Is_Win'] = (df_trades['Closed PnL'] > 0).astype(int)
    df_trades['Is_Loss'] = (df_trades['Closed PnL'] < 0).astype(int)
    
    daily_trader_stats = df_trades.groupby(['date', 'Account']).agg(
        num_trades=('Transaction Hash', 'nunique'),
        daily_pnl=('Closed PnL', 'sum'),
        total_volume_usd=('Size USD', 'sum'),
        avg_trade_size=('Size USD', 'mean'),
        wins=('Is_Win', 'sum'),
        losses=('Is_Loss', 'sum')
    ).reset_index()
    
    # Calculate Win Rate based on closed trades
    daily_trader_stats['closed_trades_count'] = daily_trader_stats['wins'] + daily_trader_stats['losses']
    daily_trader_stats['win_rate'] = np.where(
        daily_trader_stats['closed_trades_count'] > 0, 
        daily_trader_stats['wins'] / daily_trader_stats['closed_trades_count'], 
        np.nan  # NaN if they didn't close any trades that day
    )
    
    # Calculate Long / Short ratio per day per account
    # Side is 'BUY' or 'SELL'
    side_counts = df_trades.groupby(['date', 'Account', 'Side']).size().unstack(fill_value=0).reset_index()
    if 'BUY' not in side_counts.columns: side_counts['BUY'] = 0
    if 'SELL' not in side_counts.columns: side_counts['SELL'] = 0
    
    side_counts['long_short_ratio'] = np.where(
        side_counts['SELL'] > 0, 
        side_counts['BUY'] / side_counts['SELL'], 
        side_counts['BUY']  # If 0 sells, ratio is just number of buys (or infinity, so we use buys as proxy)
    )
    
    daily_trader_stats = pd.merge(daily_trader_stats, side_counts[['date', 'Account', 'long_short_ratio']], on=['date', 'Account'], how='left')
    
    # 3. Merge with Sentiment
    merged_data = pd.merge(daily_trader_stats, df_sentiment[['date', 'value', 'classification']], on='date', how='inner')
    
    # Rename for clarity
    merged_data.rename(columns={'value': 'sentiment_value', 'classification': 'sentiment_class'}, inplace=True)
    
    # Segmentation Features
    # Group accounts by their total history to find frequent/infrequent and high/low volume
    account_stats = merged_data.groupby('Account').agg(
        total_days_active=('date', 'nunique'),
        avg_daily_volume=('total_volume_usd', 'mean')
    ).reset_index()
    
    # Frequent: active on > median active days
    median_days = account_stats['total_days_active'].median()
    account_stats['frequency_segment'] = np.where(account_stats['total_days_active'] > median_days, 'Frequent', 'Infrequent')
    
    # High Volume: avg daily volume > median
    median_volume = account_stats['avg_daily_volume'].median()
    account_stats['volume_segment'] = np.where(account_stats['avg_daily_volume'] > median_volume, 'High Volume', 'Low Volume')
    
    merged_data = pd.merge(merged_data, account_stats[['Account', 'frequency_segment', 'volume_segment']], on='Account', how='left')

    print("Final merged data rows/cols:", merged_data.shape)
    
    # Save the output
    merged_data.to_csv(output_path, index=False)
    print(f"Data processed and saved to {output_path}")

if __name__ == "__main__":
    process_data("historical_data.csv", "fear_greed_index.csv", "merged_daily_trader_data.csv")
