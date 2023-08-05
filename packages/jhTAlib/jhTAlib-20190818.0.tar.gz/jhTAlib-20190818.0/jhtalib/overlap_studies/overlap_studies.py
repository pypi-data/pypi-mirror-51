import jhtalib as jhta


def BBANDS(df, n, f=2):
    """
    Bollinger Bands
    """
    bbands_dict = {'midband': [], 'upperband': [], 'lowerband': []}
    tp_dict = {'tp': jhta.TYPPRICE(df)}
    sma_list = SMA(tp_dict, n, 'tp')
    stdev_list = jhta.STDEV(tp_dict, n, 'tp')
    i = 0
    while i < len(df['Close']):
        if i + 1 < n:
            midband = float('NaN')
            upperband = float('NaN')
            lowerband = float('NaN')
        else:
            midband = sma_list[i]
            upperband = midband + f * stdev_list[i]
            lowerband = midband - f * stdev_list[i]
        bbands_dict['midband'].append(midband)
        bbands_dict['upperband'].append(upperband)
        bbands_dict['lowerband'].append(lowerband)
        i += 1
    return bbands_dict

def BBANDW(df, n, f=2):
    """
    Bollinger Band Width
    """
    bbandw_list = []
    tp_dict = {'tp': jhta.TYPPRICE(df)}
    stdev_list = jhta.STDEV(tp_dict, n, 'tp')
    i = 0
    while i < len(df['Close']):
        if i + 1 < n:
            bbandw = float('NaN')
        else:
            bbandw = 2 * f * stdev_list[i]
        bbandw_list.append(bbandw)
        i += 1
    return bbandw_list

def DEMA(df, n):
    """
    Double Exponential Moving Average
    """

def EMA(df, n, price='Close'):
    """
    Exponential Moving Average
    """
    ema_list = []
    i = 0
    while i < len(df[price]):
        if i + 1 < n:
            ema = float('NaN')
        else:
            if ema != ema:
                ema = df[price][i]
            k = 2 / (n + 1)
            ema = k * df[price][i] + (1 - k) * ema
        ema_list.append(ema)
        i += 1
    return ema_list

def ENVP(df, pct=.01, price='Close'):
    """
    Envelope Percent
    """
    envp_dict = {'hi': [], 'lo': []}
    i = 0
    while i < len(df[price]):
        hi = df[price][i] + df[price][i] * pct
        lo = df[price][i] - df[price][i] * pct
        envp_dict['hi'].append(hi)
        envp_dict['lo'].append(lo)
        i += 1
    return envp_dict

def KAMA(df, n):
    """
    Kaufman Adaptive Moving Average
    """

def MA(df, n):
    """
    Moving average
    """

def MAMA(df, price='Close'):
    """
    MESA Adaptive Moving Average
    """

def MAVP(df, price='Close'):
    """
    Moving average with variable period
    """

def MIDPOINT(df, n, price='Close'):
    """
    MidPoint over period
    """
    midpoint_list = []
    i = 0
    while i < len(df[price]):
        if i + 1 < n:
            midpoint = float('NaN')
        else:
            start = i + 1 - n
            end = i + 1
            midpoint = (max(df[price][start:end]) + min(df[price][start:end])) / 2
        midpoint_list.append(midpoint)
        i += 1
    return midpoint_list

def MIDPRICE(df, n):
    """
    Midpoint Price over period
    """
    midprice_list = []
    i = 0
    while i < len(df['Close']):
        if i + 1 < n:
            midprice = float('NaN')
        else:
            start = i + 1 - n
            end = i + 1
            midprice = (max(df['High'][start:end]) + min(df['Low'][start:end])) / 2
        midprice_list.append(midprice)
        i += 1
    return midprice_list

def MMR(df, n=200, price='Close'):
    """
    Mayer Multiple Ratio
    """
    mmr_list = []
    sma_list = SMA(df, n, price)
    i = 0
    while i < len(df[price]):
        if i + 1 < n:
            mmr = float('NaN')
        else:
            mmr = df[price][i] / sma_list[i]
        mmr_list.append(mmr)
        i += 1
    return mmr_list

def SAR(df, af_step=.02, af_max=.2):
    """
    Parabolic SAR (J. Welles Wilder)
    """
    sar_list = []
    i = 0
    while i < len(df['Close']):
        if i < 1:
            sar = float('NaN')
            sar_list.append(sar)
            is_long = True
            sar = df['Low'][i]
            ep = df['High'][i]
            af = af_step
        else:
            if is_long:
                if df['Low'][i] <= sar:
                    is_long = False
                    sar = ep
                    if sar < df['High'][i - 1]:
                        sar = df['High'][i - 1]
                    if sar < df['High'][i]:
                        sar = df['High'][i]
                    sar_list.append(sar)
                    af = af_step
                    ep = df['Low'][i]
                    sar = sar + af * (ep - sar)
#                    sar = round(sar)
                    if sar < df['High'][i - 1]:
                        sar = df['High'][i - 1]
                    if sar < df['High'][i]:
                        sar = df['High'][i]
                else:
                    sar_list.append(sar)
                    if df['High'][i] > ep:
                        ep = df['High'][i]
                        af += af_step
                        if af > af_max:
                            af = af_max
                    sar = sar + af * (ep - sar)
#                    sar = round(sar)
                    if sar > df['Low'][i - 1]:
                        sar = df['Low'][i - 1]
                    if sar > df['Low'][i]:
                        sar = df['Low'][i]
            else:
                if df['High'][i] >= sar:
                    is_long = True
                    sar = ep
                    if sar > df['Low'][i - 1]:
                        sar = df['Low'][i - 1]
                    if sar > df['Low'][i]:
                        sar = df['Low'][i]
                    sar_list.append(sar)
                    af = af_step
                    ep = df['High'][i]
                    sar = sar + af * (ep - sar)
#                    sar = round(sar)
                    if sar > df['Low'][i - 1]:
                        sar = df['Low'][i - 1]
                    if sar > df['Low'][i]:
                        sar = df['Low'][i]
                else:
                    sar_list.append(sar)
                    if df['Low'][i] < ep:
                        ep = df['Low'][i]
                        af += af_step
                        if af > af_max:
                            af = af_max
                    sar = sar + af * (ep - sar)
#                    sar = round(sar)
                    if sar < df['High'][i - 1]:
                        sar = df['High'][i - 1]
                    if sar < df['High'][i]:
                        sar = df['High'][i]
        i += 1
    return sar_list

def SAREXT(df):
    """
    Parabolic SAR - Extended
    """

def SMA(df, n, price='Close'):
    """
    Simple Moving Average
    """
    sma_list = []
    i = 0
    while i < len(df[price]):
        if i + 1 < n:
            sma = float('NaN')
        else:
            start = i + 1 - n
            end = i + 1
            sma = sum(df[price][start:end]) / n
        sma_list.append(sma)
        i += 1
    return sma_list

def T3(df, n, price='Close'):
    """
    Triple Exponential Moving Average (T3)
    """

def TEMA(df, n, price='Close'):
    """
    Triple Exponential Moving Average
    """

def TRIMA(df, n, price='Close'):
    """
    Triangular Moving Average
    """
    tma_list = []
    sma_list = []
    i = 0
    while i < len(df[price]):
        if n % 2 == 0:
            n_sma = n / 2 + 1
            start = i + 1 - n_sma
            end = i + 1
            sma = sum(df[price][start:end]) / n_sma
            sma_list.append(sma)
            n_tma = n / 2
            start = i + 1 - n_tma
            end = i + 1
        else:
            n_sma = (n + 1) / 2
            start = i + 1 - n_sma
            end = i + 1
            sma = sum(df[price][start:end]) / n_sma
            sma_list.append(sma)
            n_tma = (n + 1) / 2
            start = i + 1 - n_tma
            end = i + 1
        if i + 1 < n:
            tma = float('NaN')
        else:
            tma = sum(sma_list[start:end]) / n_tma
        tma_list.append(tma)
        i += 1
    return tma_list

def WMA(df, n, price='Close'):
    """
    Weighted Moving Average
    """

