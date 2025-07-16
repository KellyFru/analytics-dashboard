import fetch_data 

def add_metrics(df):
    df['ctr'] = df['clicks'] / df['impressions'] * 100
    df['cpc'] = df['spend'] / df['clicks']
    df['cpa'] = df['spend'] / df['conversions']
    df['revenue'] = df['conversions'] * 20
    df['roi'] = (df['revenue'] - df['spend']) / df['spend'] * 100
    return df

if __name__ == "__main__":
    df = fetch_data.fetch_campaign_data()
    df = add_metrics(df)
    print(df.head())
