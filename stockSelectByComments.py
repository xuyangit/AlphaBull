# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import pandas as pd


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.days = 0
    context.period_days = 1
    context.change = {}


def period_passed(context):
    return context.days % context.period_days == 0


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    his = history(10, '1d', 'close')['000001.XSHG']

    if period_passed(context):
        if his[9] / his[8] < 0.97:
            if len(context.portfolio.positions) > 0:
                for stock in context.portfolio.positions.keys():
                    order_target_percent(stock, 0)
            return

    if not period_passed(context):
        return
    context.days += 1
    rebalance(context, bar_dict)
    update_universe(context.stocks)
    # plot('cash', context.portfolio.cash/(context.portfolio.market_value+context.portfolio.cash))


def rebalance(context, bar_dict):
    a = xueqiu.top_stocks('total_followers', count=3000)
    b = xueqiu.top_stocks('new_followers', count=3000)
    df = pd.merge(a, b, on='order_book_id')
    df.total_followers = df.total_followers + 1
    df['ratio'] = df.new_followers / df.total_followers
    df = df.sort_values(['ratio'], ascending=False)

    security = list(df.order_book_id)
    context.stocks = []
    stop = 0;
    for stock in security:

        if bar_dict[stock].is_trading and not is_st_stock(stock):
            stop += 1
            context.stocks.append(stock)
        if stop == 10:
            break

    # sell
    for stock in context.portfolio.positions:
        if stock not in context.stocks and bar_dict[stock].is_trading and not low_limit(stock, bar_dict):
            order_target_percent(stock, 0)

    if len(context.stocks) == 0:
        return

    weight = update_weights(context, context.stocks)

    # buy
    logger.info("today: " + str(context.now) + "buy stocks: " + str(context.stocks))
    for stock in context.stocks:
        Vol = history(2, '1d', 'volume')[stock]
        ratio = Vol.ix[1] / Vol.ix[0]
        if weight != 0 and stock in context.stocks and not high_limit(stock, bar_dict) and ratio < 0.8:
            order_target_percent(stock, weight)


def update_weights(context, stocks):
    if len(stocks) == 0:
        return 0
    else:

        weight = .99 / len(stocks)
        return weight


def high_limit(stock, bar_dict):
    price = history(2, '1d', 'close')[stock].ix[0]
    # logger.info("yesterday close: " + str(price) + " today close: " + str(bar_dict[stock].close))
    pricenow = bar_dict[stock].open
    pct_change = (pricenow - price) / price
    return pct_change > 0.099


def low_limit(stock, bar_dict):
    price = history(2, '1d', 'close')[stock].ix[0]
    # logger.info("yesterday close: " + str(price) + " today close: " + str(bar_dict[stock].close))
    pricenow = bar_dict[stock].open
    pct_change = (pricenow - price) / price
    return pct_change < -0.099