import bybit_queries as bq
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns


def pull_all_data(ticker_list, start_time):
    interval = bq.candle_length(start_time)
    times = bq.market_data(ticker_list[0], interval, start_time)["start_at"].tolist()
    data = [times]
    for ticker in ticker_list:
        alt = bq.market_data(ticker, interval, start_time)["close"].tolist()
        alt = [((alt[x] - alt[0]) / alt[0] * 100) for x in range(len(alt))]
        data.append(alt)
    df = pd.DataFrame(data).transpose()
    df.columns = ["time"] + ticker_list

    return df.dropna()


def plot_data(df):
    size = 8
    start = df["time"].min()
    end = df["time"].max()
    offset = (end - start) / (size * 5)
    last_values = df[["ticker", "pct_change"]][df["time"] == end]

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(size, size))
    lineplot = sns.lineplot(x="time",
                            y="pct_change",
                            data=df,
                            hue="ticker",
                            ax=ax,
                            legend=False,
                            linewidth=1)

    ax.set_xlim([start, end])
    ax.set_xlim([None, end + offset])
    ax.spines["right"].set_visible(False)
    for ticker, value in last_values.itertuples(index=False):
        ax.text(x=end + offset, y=value, s=ticker, va="center", fontsize="x-small")

    ticks_loc = lineplot.get_xticks().tolist()
    lineplot.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    lineplot.xaxis.set_major_locator(mticker.MaxNLocator(size))

    plt.show()


def main():
    tickers = bq.get_tickers(quote_currency="USDT")["name"].tolist()
    start_time = input("Enter start time (unix): ")
    df = pull_all_data(tickers, start_time)
    melted_df = pd.melt(df, id_vars=["time"], value_vars=tickers)
    melted_df = melted_df.rename(columns={"value": "pct_change", "variable": "ticker"})
    plot_data(melted_df)


if __name__ == "__main__":
    main()
