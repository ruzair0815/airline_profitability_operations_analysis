import pandas as pd

df = pd.read_csv('../data/flights.csv')

#keep only the financially useful columns
financial_columns = [
    'FL_DATE',
    'AIRLINE',
    'ORIGIN',
    'DEST',
    'DEP_DELAY',
    'ARR_DELAY',
    'CANCELLED',
    'AIR_TIME',
    'DISTANCE',
    'DELAY_DUE_CARRIER',
    'DELAY_DUE_WEATHER',
    'DELAY_DUE_NAS',
    'DELAY_DUE_LATE_AIRCRAFT'
]

df = df[financial_columns]

delay_columns = [
    'DELAY_DUE_CARRIER',
    'DELAY_DUE_WEATHER',
    'DELAY_DUE_NAS',
    'DELAY_DUE_LATE_AIRCRAFT'
]

df[delay_columns] = df[delay_columns].fillna(0)

# est $0.18 cents per mile ticket pricing, 120 estimated passengers per flight
df['ESTIMATED_REVENUE'] = df['DISTANCE'] * 0.18 * 120

# estimated $5.20 operating fuel cost per mile
df['FUEL_COST'] = df['DISTANCE'] * 5.2

#negative or zero delay = 0, positive delay values stay the same
# estimated $75 cost per minute of arrival delay
df['DELAY_COST'] = df['ARR_DELAY'].clip(lower=0) * 75

# calculate profit
df['PROFIT'] = (
    df['ESTIMATED_REVENUE']
    - df['FUEL_COST']
    - df['DELAY_COST']
)

airline_summary = df.groupby('AIRLINE')[[
    'ESTIMATED_REVENUE',
    'FUEL_COST',
    'DELAY_COST',
    'PROFIT'
]].sum()


pd.options.display.float_format = '{:,.2f}'.format
print(airline_summary.sort_values(by='PROFIT', ascending=False))

df['ROUTE'] = df['ORIGIN'] + ' -> ' + df['DEST']

route_summary = df.groupby('ROUTE')[[
    'ESTIMATED_REVENUE',
    'FUEL_COST',
    'DELAY_COST',
    'PROFIT'
]].sum()

route_summary = route_summary.sort_values(
    by='PROFIT',
    ascending=False
)

df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])

df['MONTH'] = df['FL_DATE'].dt.to_period('M')

monthly_summary = df.groupby('MONTH')[[
    'ESTIMATED_REVENUE',
    'FUEL_COST',
    'DELAY_COST',
    'PROFIT'
]].sum()

print("\nMONTHLY FINANCIAL SUMMARY\n")
print(monthly_summary.head(12))

airline_summary.to_csv('/Users/rehmauzair/Documents/airline_financial_analysis/output/airline_summary.csv')
route_summary.to_csv('/Users/rehmauzair/Documents/airline_financial_analysis/output/route_summary.csv')
monthly_summary.to_csv('/Users/rehmauzair/Documents/airline_financial_analysis/output/monthly_summary.csv')
df.to_csv('/Users/rehmauzair/Documents/airline_financial_analysis/output/cleaned_flight_data.csv', index=False)