import pandas as pd

def fetch_campaign_data():
    df = pd.read_csv('./data/campaign_data.csv')
    return df

if __name__ == "__main__":
    df = fetch_campaign_data()
    print(df.head())
