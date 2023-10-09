import math
from scipy.optimize import newton
def to_sum(value):
    """Utility function to get the sum of the value if it's a list or the value itself if it's not."""
    return sum(value) if isinstance(value, (list, tuple)) else value

def assets(liabilities, equity):
    """
    Assets = Liabilities + Stockholders’ Equity
    """
    return to_sum(liabilities) + to_sum(equity)

def networking_capital(curr_assets, curr_liabilities):
    """
    Net working capital= Current Assets – Current Liabilities
    """
    return to_sum(curr_assets) - to_sum(curr_liabilities)

def income(revenue, expenses):
    """
    Income = Revenue − Expenses 
    """
    return to_sum(revenue) - to_sum(expenses)

def current_ratio(curr_assets, curr_liabilities):
    """
    Current ratio = Current assets / Current liabilities
    """
    return to_sum(curr_assets) / to_sum(curr_liabilities)

def quick_ratio(cash, market_securities, account_receivable, curr_liabilities):
    """
    Quick ratio = (Cash + Marketable securities + Accounts receivable) /Current liabilities
    """
    numerator = to_sum(cash) + to_sum(market_securities) + to_sum(account_receivable)
    return numerator / to_sum(curr_liabilities)

def cash_ratio(cash, current_liabilities, cash_equivalent=0):
    """
    Cash ratio = (Cash and cash equivalents) / Current liabilities
    """
    numerator = to_sum(cash) + to_sum(cash_equivalent)
    return numerator / to_sum(current_liabilities)

def operating_flow_ratio(operation_cash_flow, curr_liabilities):
    """
    Operating cash flow ratio = Cash flow from operations / current liabilities
    """
    return to_sum(operation_cash_flow) / to_sum(curr_liabilities)

def debt_ratio(assets, equity):
    """
    Total Debt Ratio = (Total assets –Total stockholders’ equity) Total assets
    """
    return (to_sum(assets) - to_sum(equity)) / to_sum(assets)

def equity_multiplier(assets, equity):
    """
    Equity Multiplier = Total assets / Total stockholders’ equity
    """
    return to_sum(assets) / to_sum(equity)

def interest_coverage_ratio(ebit,interest_expense):
    """
    Interest coverage ratio= EBIT / Interest expense
    """ 
    return to_sum(ebit) / to_sum(interest_expense)

def inventory_turnover(cogs,inventory):
    """
    Inventory Turnover = Cost of Goods Sold / Inventory
    """
    return to_sum(cogs) / to_sum(inventory)
    
def days_sales_in_inventory(inventory_turnover):
    """
    Days’ sales in inventory (DSI) = 365 days / Inventory turnover
    """
    return 365 / to_sum(inventory_turnover)

def asset_turnover(total_revenues, total_assets):
    """
    Total asset turnover = Total revenues / Total assets
    """
    return to_sum(total_revenues) / to_sum(total_assets)

def gross_profit_margin(gross_profit,total_revenues):
    """
    Gross profit margin = Gross Profit / Total Revenues
    """
    return to_sum(gross_profit) / to_sum(total_revenues)

def net_profit_margin(net_income,total_revenues):
    """
    Net profit margin = Net Income / Total Revenues
    """
    return to_sum(net_income) / to_sum(total_revenues)

def return_on_assets(net_income,total_assets):
    """
    Return on Assets (ROA) = Net income / Total assets
    """
    return to_sum(net_income) / to_sum(total_assets)

def return_on_equity(net_income,total_equity):
    """
    Return on Equity (ROE) = Net income / Total equity
    """
    return to_sum(net_income) / to_sum(total_equity)

def roe(net_profit_margin,total_asset_turnover,equity_multiplier):
    """
    ROE = Net Profit Margin × Total Asset Turnover × Equity Multiplier  
    """
    return to_sum(net_profit_margin) * to_sum(total_asset_turnover) * to_sum(equity_multiplier)
def price_to_earnings_ratio(curr_share_price,eps):
    """
    Price to earnings ratio (P/E ratio) = Current share price / Earnings per share
    """
    return curr_share_price / eps
def price_to_earnings_ratio(curr_share_price,shares_outstanding):
    """
    Market capitalization (market cap) = Current price per share × Shares outstandin
    """
    return curr_share_price * shares_outstanding

def wacc(equity, debt, total_value, cost_of_equity, cost_of_debt, tax_rate):
    """
    WACC (Weighted Average Cost of Capital) = (Equity / Total value) × Cost of equity + (Debt / Total value) × Cost of debt × (1 − Tax rate)
    """
    equity_weight = to_sum(equity) / to_sum(total_value)
    debt_weight = to_sum(debt) / to_sum(total_value)
    return equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)

def capm(risk_free_rate, market_return, beta):
    """
    CAPM (Capital Asset Pricing Model) = Risk free rate + Beta(the only thing that changes from company to company) × (Market return − Risk free rate)
    """
    return risk_free_rate + beta * (market_return - risk_free_rate)

def ebit(revenues, operating_expenses):
    """
    EBIT (Earnings Before Interest and Taxes) = Revenues − Operating expenses
    """
    return to_sum(revenues) - to_sum(operating_expenses)

def ebitda(ebit, depreciation, amortization):
    """
    EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) = EBIT + Depreciation + Amortization
    """
    return to_sum(ebit) + to_sum(depreciation) + to_sum(amortization)

def entrepreneurial_value(net_operating_profit, wacc):
    """
    Entrepreneurial Value (also known as Enterprise Value) = NOP (Net Operating Profit after Taxes) / WACC (Weighted Average Cost of Capital)
    """
    return net_operating_profit / wacc

def operational_expense(revenues, gross_profit):
    """
    Operational Expense = Revenues - Gross Profit
    """
    return to_sum(revenues) - to_sum(gross_profit)


def future_value(present_value,rate,periods):
    """
    Future value: 𝐹𝑉 = 𝑃𝑉 × (1 + 𝑟)^𝑇
    """
    return present_value * ((1 + rate)**periods)

def present_value(future_value,rate,periods):
    """
    Present value: 𝑃𝑉 = 𝐹𝑉 / (1+𝑟)𝑇  
    """
    return future_value / ((1+rate)**periods)

def to_sum(value):
    """Utility function to get the sum of the value if it's a list or return the value itself if it's not."""
    return sum(value) if isinstance(value, (list, tuple)) else value

def npv(initial_investment, cash_flows, rate):
    """
    Net Present Value (NPV)
    NPV = C0 + sum(Ct / (1 + r) ** t) for t = 1 to T
    """
    npv_value = -to_sum(initial_investment)  # Initial investment is usually a negative cash flow
    for t, ct in enumerate(cash_flows, start=1):
        npv_value += ct / (1 + rate) ** t
    return npv_value

def irr(initial_investment, cash_flows):
    """
    Internal Rate of Return (IRR)
    0 = C0 + sum(Ct / (1 + IRR) ** t) for t = 1 to T
    """
    def npv_eq(irr_rate):
        return npv(initial_investment, cash_flows, irr_rate)
    return newton(npv_eq, 0.05)  # Starting estimate is 5%

def ear(r, m):
    """
    Effective Annual Rate (EAR)
    EAR = (1 + r/m) ** m - 1
    """
    return (1 + r/m) ** m - 1

def future_value_continuous_compounding(pv, r, t):
    """
    Future Value based on continuous compounding
    FV = PV * e^(rT)
    """
    return pv * math.exp(r * t)

def perpetuity(c, r):
    """
    Perpetuity
    PV = C/r
    """
    return c / r

def growing_perpetuity(c, r, g):
    """
    Growing Perpetuity
    PV = C/(r-g)
    """
    return c / (r - g)

def annuity(c, r, t):
    """
    Annuity
    PV = C/r * [1 - 1/((1 + r) ** t)]
    """
    return c/r * (1 - 1/((1 + r) ** t))

def growing_annuity(c, r, g, t):
    """
    Growing Annuity
    PV = C/(r-g) * [1 - (1+g)/(1+r) ** t]
    """
    return c / (r - g) * (1 - (1 + g) / (1 + r) ** t)
