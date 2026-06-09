import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

master = pd.read_csv('data/master.csv')

ols = smf.ols(formula='gap_index ~ mh_provider_rate + pct_uninsured + pct_unemployed + pct_children_poverty + avg_mentally_unhealthy_days', data=master)

results = ols.fit()
print(results.summary())

print(master[['pct_uninsured', 'pct_unemployed', 'pct_children_poverty', 'avg_mentally_unhealthy_days']].corr())
# Correct for heteroscedasticity
results_hc3 = ols.fit(cov_type='HC3')
print (results_hc3.summary())

# Drop pct_unemployed (it is providing high multicollinearity but low coefficient)
ols = smf.ols(formula='gap_index ~ mh_provider_rate + pct_uninsured + pct_children_poverty + avg_mentally_unhealthy_days', data=master)

results_noump = ols.fit(cov_type = 'HC3')
print(results_noump.summary())

# Drop pct_uninsured (it is providing high multicollinearity but low coefficient)
ols = smf.ols(formula='gap_index ~ mh_provider_rate + pct_children_poverty + avg_mentally_unhealthy_days', data=master)

results_rev = ols.fit(cov_type = 'HC3')
print(results_rev.summary())
# Found that this improves the model (lower AIC and condition no.)

# 