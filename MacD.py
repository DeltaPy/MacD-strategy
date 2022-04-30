from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MacD(IStrategy):
    # This strategy does not use crossovers but just enters/exits trades
    # when 'is above' / 'is under' conditions are met.
    timeframe = "1m"  #1m, 5m, 1h, 1d
    stoploss = -1
    minimal_roi = {"0": 100.0}

 # --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            'signal': {'color': 'blue'},
        },
        'subplots': {
            "macd": {
                'macd': {'color': 'orange'},
            },
            "hist": {
                'hist': {'color': 'green'},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["macd"] = ta.MACD(dataframe.apply(lambda x: x.argmax(), axis=1).values, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["signal"] = ta.SMA(dataframe['macd'], timeperiod=9)
        dataframe["hist"] = dataframe['macd'] - dataframe['signal']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Buy when close price > sma and rsi > rsi_bline (no crossover signal, just above...)
                (dataframe['close'] == dataframe['signal'])
            ), 'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Sell when close price < sma and rsi < rsi_sline (no crossover signal, just below...)
                (dataframe['close'] <= dataframe['signal'])
            ), 'sell'] = 1

        return dataframe
