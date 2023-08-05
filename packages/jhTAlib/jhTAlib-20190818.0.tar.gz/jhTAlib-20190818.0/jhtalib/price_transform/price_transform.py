def AVGPRICE(df):
    """
    Average Price
    """
    avgprice_list = []
    i = 0
    while i < len(df['Close']):
        avgprice = (df['Open'][i] + df['High'][i] + df['Low'][i] + df['Close'][i]) / 4
        avgprice_list.append(avgprice)
        i += 1
    return avgprice_list

def MEDPRICE(df):
    """
    Median Price
    """
    medprice_list = []
    i = 0
    while i < len(df['Close']):
        medprice = (df['High'][i] + df['Low'][i]) / 2
        medprice_list.append(medprice)
        i += 1
    return medprice_list

def TYPPRICE(df):
    """
    Typical Price
    """
    typprice_list = []
    i = 0
    while i < len(df['Close']):
        typprice = (df['High'][i] + df['Low'][i] + df['Close'][i]) / 3
        typprice_list.append(typprice)
        i += 1
    return typprice_list

def WCLPRICE(df):
    """
    Weighted Close Price
    """
    wclprice_list = []
    i = 0
    while i < len(df['Close']):
        wclprice = (df['High'][i] + df['Low'][i] + (df['Close'][i] * 2)) / 4
        wclprice_list.append(wclprice)
        i += 1
    return wclprice_list

