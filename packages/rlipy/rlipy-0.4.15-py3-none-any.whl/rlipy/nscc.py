#!/usr/local/bin/python
from io import StringIO
import subprocess

import pandas as pd

from . import util


def nscc_raw_file(trade_date):
	return '/data/market/bamlnscc/%s_bamlnscc.txt' % (trade_date)


HEADER_RECORD_TYPE = '02'
HEADER_RECORD_LENGTH = 250

HEADER_FORMAT = pd.DataFrame(
							[
							['record_type', 1, 2, 'str'],  # Record_Type
							['etf_cusip', 3, 9, 'str'],  # ETF_Trading_CUSIP
							['etf_isin', 12, 12, 'str'],  # ETF_Trading_ISIN
							['portfolio_id', 24, 9, 'str'],  # NSCC_Portfolio_ID
							['etf_description', 33, 60, 'str'],  # ETF_Description
							['trade_date', 93, 8, 'int'],  # Portfolio_Trade_Date
							['etf_agent', 101, 8, 'int'],  # ETF_Agent
							['comp_count', 109, 8, 'int'],  # Component_Count
							['est_t-1_cash_amt_per_cu', 117, 14, 'float'],  # Estimated_T-1_Cash_Amount_Per_Creation_Unit
							['sign_est_t-1_cash_amt_per_cu', 131, 1, 'str'],  # Sign_field_for_Estimated_T-1_Cash_Amount_Per_Creation_Unit
							['nav_per_cu', 132, 17, 'float'],  # Net_Asset_Value_Per_Creation_Unit
							['sign_nav_per_cu', 149, 1, 'str'],  # Sign_field_for_Net_Asset_Value_Per_Creation_Unit
							['est_cash_per_etf_t-1', 150, 14, 'float'],  # Estimated_T-1_Cash_Amount_Per_ETF
							['sign_est_cash_per_etf_t-1', 164, 1, 'str'],  # Sign_field_for_Estimated_T-1_Cash_Amount_Per_ETF
							['nav_per_etf', 165, 17, 'float'],  # Net_Asset_Value_Per_ETF
							['sign_nav_per_etf', 182, 1, 'str'],  # Sign_field_for_Net_Asset_Value_Per_ETF
							['total_cash_amt_per_cu', 183, 14, 'float'],  # Total_Cash_Amount_Per_Creation_Unit
							['sign_total_cash_amt_per_cu', 197, 1, 'str'],  # Sign_field_for_Total_Cash_Amount_Per_Creation_Unit
							['total_shares_outstanding_per_etf_t-1', 198, 12, 'int'],  # Total_Shares_Outstanding_Per_ETF_on_T-1
							['div_per_etf_t-1', 210, 14, 'float'],  # Dividend_Amount_Per_ETF_on_T-1
							['sign_div_per_etf_t-1', 224, 1, 'str'],  # Sign_field_for_Dividend_Amount_Per_ETF_on_T-1
							['est_value_of_cash-in-lieu_comp_per_cu', 225, 14, 'float'],  # Estimated_Value_of_cash-in-lieu_Components_per_Creation_Unit
							['cash_only_ind', 239, 1, 'str'],  # Cash_Only_Indicator
							['etf_expense_ratio_t-1', 240, 3, 'str'],  # ETF_Expense_Ratio_on_T-1
							['total_asset_value_of_etf_fund_t-1', 243, 17, 'float'],  # Total_Asset_Value_of_ETF_Fund_on_T-1
							['etf_shares_per_cu', 260, 9, 'int'],  # ETF_Shares_PerCreate/Redeem_Unit
							['etf_symbol', 269, 15, 'str'],  # ETF_Symbol
							['cns_eligibility_ind', 284, 1, 'str'],  # CNS_Eligibility_Indicator
							['etf_create_redeem_ID', 285, 1, 'str'],  # ETF_Create_Redeem_Identifier
							['prior_day_portfolio_being_used', 286, 1, 'str'],  # Prior_Day's_Portfolio_being_used
							['custom_or_standard', 287, 1, 'str'],  # Custom_or_Standard
							['foreign_or_domestic', 288, 1, 'str'],  # Foreign_or_Domestic
							['nscc_new_portfolio', 289, 1, 'str'],  # NSCC_New_Portfolio
							['etf_classification_code', 290, 6, 'str'],  # ETF_Classification_Code

							],
								columns = ['NAME', 'Start', 'LEN', 'TYPE'])
COMPONENT_RECORD_TYPE = '03'
COMPONENT_RECORD_LENGTH = 400
COMPONENT_FORMAT = pd.DataFrame(
							[
							['record_type', 1, 2, 'str'],  # Record_Type
							['etf_cusip', 3, 9, 'str'],  # ETF_Trading_CUSIP
							['etf_isin', 12, 12, 'str'],  # ETF_Trading_ISIN
							['portfolio_id', 24, 9, 'str'],  # NSCC_Portfolio_ID
							['trade_date', 33, 8, 'int'],  # Portfolio_Trade_Date
							['comp_id_code', 41, 2, 'str'],  # Component_ID_Code
							['comp_id', 43, 25, 'str'],  # Component_ID
							['comp_quantity', 68, 13, 'int'],  # Component_Quantity
							['sign_comp_quantity', 81, 1, 'str'],  # Sign_Field_for_Component_Quantity
							['new_security_ind', 82, 1, 'str'],  # New_Security_Indicator
							['cash_in_lieu_ind', 83, 1, 'str'],  # Cash_In_Lieu_Indicator
							['comp_symbol', 84, 15, 'str'],  # Component_Symbol
							['comp_wi_ind', 99, 1, 'str'],  # Component_WI_Indicator
							['comp_undergoing_corporate_action', 100, 1, 'str'],  # Component_undergoing_corporate_action
							['comp_nscc_eligibility_ind', 101, 1, 'str'],  # Component_NSCC_eligibility_ind
							['comp_cns_ind', 102, 1, 'str'],  # Component_CNS_Indicator
							['external_settlement_date', 103, 8, 'int'],  # External_Settlement_Date
							['comp_description', 111, 60, 'str'],  # Component_Description
							],
							columns = ['NAME', 'Start', 'LEN', 'TYPE'])


def get_nscc_basket(raw_file):
	buf = subprocess.check_output('egrep "^02" ' + raw_file, shell = True).decode('UTF-8', errors = 'ignore')
	baskets = pd.read_fwf(StringIO(buf), widths = HEADER_FORMAT['LEN'].tolist(),
						names = HEADER_FORMAT['NAME'].tolist())
	baskets['est_t-1_cash_amt_per_cu'] = baskets['est_t-1_cash_amt_per_cu'] * 0.01 * (baskets['sign_est_t-1_cash_amt_per_cu'].apply(lambda x:-1 if x == '-' else 1))
	baskets['nav_per_cu'] = baskets['nav_per_cu'] * 0.00001 * (baskets['sign_nav_per_cu'].apply(lambda x:-1 if x == '-' else 1))
	baskets['nav_per_etf'] = baskets['nav_per_etf'] * 0.00001 * (baskets['sign_nav_per_etf'].apply(lambda x:-1 if x == '-' else 1))
	baskets['total_cash_amt_per_cu'] = baskets['total_cash_amt_per_cu'] * 0.01 * (baskets['sign_total_cash_amt_per_cu'].apply(lambda x:-1 if x == '-' else 1))
	baskets = baskets[baskets['custom_or_standard'] == 'S']
	return baskets


def __get_isin(s):
	id_code = util.num(s['comp_id_code'])
	if(id_code == 3):
		return s['comp_id']
	elif(id_code == 4):
		return s['comp_id'][0:12]
	else:
		return None


def __get_sedol(s):
	id_code = util.num(s['comp_id_code'])
	if(id_code == 2):
		return s['comp_id']
	elif(id_code == 4):
		return s['comp_id'][-7:]
	else:
		return None


def __get_cusip(s):
	id_code = util.num(s['comp_id_code'])
	if(id_code == 1):
		return s['comp_id']
	else:
		return None


def get_nscc_component(raw_file):
	buf = subprocess.check_output('egrep "^03" ' + raw_file , shell = True).decode('UTF-8', errors = 'ignore')
	components = pd.read_fwf(StringIO(buf),
							widths = COMPONENT_FORMAT['LEN'].tolist(),
							names = COMPONENT_FORMAT['NAME'].tolist(),
							)
	components['comp_isin'] = components.apply(__get_isin, axis = 1)
	components['comp_cusip'] = components.apply(__get_cusip, axis = 1)
	components['comp_sedol'] = components.apply(__get_sedol, axis = 1)
	return components


if __name__ == '__main__':
	raw_file = '/data/market/bamlnscc/20170802_bamlnscc.txt'
	baskets = get_nscc_basket(raw_file)
	baskets.to_csv('/home/VERITIONFUND/rli/pub/basket.csv', index = False, float_format = '%.4f')
	components = get_nscc_component(raw_file)
	components.to_csv('/home/VERITIONFUND/rli/pub/components.csv', index = False, float_format = '%.4f')

