PyAlgoTrade mootdx module
=========================
此项目是 PyAlgoTrade mootdx(基于 pytdx 的二次封装版本) 的一个数据源

一个简单的用法:

```
from pyalgotrade import plotter, strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.technical import ma

from pyalgotrade_mootdx import tools


class Strategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(Strategy, self).__init__(feed)

        self.__position = None
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 150)
        self.__instrument = instrument
        self.getBroker()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("买入 %.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("卖出 %.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def getSMA(self):
        return self.__sma

    def onBars(self, bars):
        # 每一个数据都会抵达这里，就像becktest中的next
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        # bar.getTyoicalPrice = (bar.getHigh() + bar.getLow() + bar.getClose())/ 3.0
        bar = bars[self.__instrument]

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # 开多头.
                self.__position = self.enterLong(self.__instrument, 100, True)

        # 平掉多头头寸.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def main():
    instruments = ["600036"]
    feeds = tools.build_feed(instruments, 2017, 2018, "histdata")

    # 3.实例化策略
    strat = Strategy(feeds, instruments[0])

    # 4.设置指标和绘图
    ratio = sharpe.SharpeRatio()
    strat.attachAnalyzer(ratio)
    plter = plotter.StrategyPlotter(strat)

    # 5.运行策略
    strat.run()
    strat.info("最终收益: %.2f" % strat.getResult())

    # 6.输出夏普率、绘图
    strat.info("夏普比率: " + str(ratio.getSharpeRatio(0)))
    # plter.plot()


if __name__ == '__main__':
    main()
```

```
2018-04-03 00:00:00 strategy [INFO] 卖出 28.86
2018-04-11 00:00:00 strategy [INFO] 买入 30.34
2018-04-17 00:00:00 strategy [INFO] 卖出 28.25
2018-05-02 00:00:00 strategy [INFO] 买入 29.98
2018-05-04 00:00:00 strategy [INFO] 卖出 29.28
2018-05-09 00:00:00 strategy [INFO] 买入 29.70
2018-05-24 00:00:00 strategy [INFO] 卖出 29.60
2018-09-25 00:00:00 strategy [INFO] 买入 29.83
2018-10-12 00:00:00 strategy [INFO] 卖出 28.70
2018-10-15 00:00:00 strategy [INFO] 买入 29.16
2018-10-19 00:00:00 strategy [INFO] 卖出 27.75
2018-10-22 00:00:00 strategy [INFO] 买入 29.53
2018-10-30 00:00:00 strategy [INFO] 卖出 28.12
2018-11-01 00:00:00 strategy [INFO] 买入 29.45
2018-11-15 00:00:00 strategy [INFO] 卖出 28.24
2018-11-19 00:00:00 strategy [INFO] 买入 28.70
2018-11-23 00:00:00 strategy [INFO] 卖出 28.29
2018-12-03 00:00:00 strategy [INFO] 买入 29.49
2018-12-11 00:00:00 strategy [INFO] 卖出 28.35
2018-12-12 00:00:00 strategy [INFO] 买入 29.00
2018-12-18 00:00:00 strategy [INFO] 卖出 28.05
2018-12-21 13:48:01,740 strategy [INFO] 最终收益: 999254.00
2018-12-21 13:48:01,740 strategy [INFO] 夏普比率: -0.6957113853538597
```
