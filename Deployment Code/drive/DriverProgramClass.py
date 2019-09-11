# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:40:56 2019

@author: DGuo
"""
import logging
from engine import DataPrepare
from engine.Util import log_format, PROJECT_DIR
#char_logic_path = PROJECT_DIR + '/docs/Characteristics Logic.xlsm'
#char_logic_table = pd.read_excel(char_logic_path)
# This is the driver program for development
# But it can not be run for now, since we have not completed all modules.
# It is simply used to show pipelines.
class DriverProgram():
    CHARATERISTICS_NAME = ['TL_original_amount_sum', 'IQ_num_inq_lst_12',
       'TL_num_rev_util_ge_75', 'TL_min_mths_dlq', 'LN_vehicle_type',
       'LN_ecoa', 'TL_limit_max', 'TL_oldest_trade_mob_cards_ind',
       'TL_num_pl_open_lst12_ng', 'TL_min_mths_pay_rpt_cards',
       'TL_num_Recreational_merchandise_loan', 'TL_sum_odbal',
       'IQ_num_Auto_financing_companies', 'TL_num_auto_amtospct_ge_90',
       'TL_delinquency_over_90_days_sum', 'TL_num_sec_dlq_lst12_30']
    def __init__(self, input_dict):
        self.input_dict = input_dict
    def run_driver(self):
        # instantiate logger
        logger = logging.getLogger("DRIVERPROGRAM")
        if (logger.hasHandlers()):
            logger.handlers.clear()
        log_format(PROJECT_DIR + '/logs/Driver Log', logger)
        output_dict = {'LN_application_id':None, 'SPID':None, 'ScrID':None, 'ExclID':None, 'Characteristics':None, 'Weights':None, 'raw score':None, 'score': None}
        for var_name in DriverProgram.CHARATERISTICS_NAME:
            output_dict[var_name] = None
            output_dict['Weight_' + var_name] = None
        #### Run each part respectively, and output log. ######
        ## Run DataPrep
        logger.info("Start to prepare the data.")
        try:
            data_prep = DataPrepare(self.input_dict).run()
        except:
            err_message = "Error happened in Data Preparation Part!"
            logger.error(err_message)
            raise ValueError(err_message)
        else:
            logger.info("Data Preparation complete.")
        # fill application id
        output_dict['LN_application_id'] = data_prep['loans']['application_id']
#        
#        ## Code below is only a template, it will be finished later.
#        ## Run Exclusion Design
#        logger.info("Start to design exclusion.")
#        try:
#            excl_des_id = ExclusionDesign(data_prep).run()
#        except:
#            err_message = "Error happened in Exclusion-Design Part!"
#            logger.error(err_message)
#            raise ValueError(err_message)
#        else:
#            logger.info("Data Preparation complete.")
#        # fill exclusion id
#        output_dict['ExclID'] = excl_des_id
#
#        ## Run Charateristics Creation
#        logger.info("Start to create characteristics.")
#        try:
#            char_create = CharacteristicsCreation(excl_des_id).run()
#        except:
#            err_message = "Error happened in Characteristics Creation Part!"
#            logger.error(err_message)
#            raise ValueError(err_message)
#        else:
#            logger.info("Characteristics Creation complete.")
#            
#        # fill Charcteristics Value
#        output_dict.update(char_create)    
#        
#        ## Run Score Deployment
#        logger.info("Start to generate score.")
#        try:
#            char_create = CharacteristicsCreation(char_create).run()
#        except:
#            err_message = "Error happened in Characteristics Creation Part!"
#            logger.error(err_message)
#            raise ValueError(err_message)
#        else:
#            logger.info("Score Deployment complete.")
#
#        output_dict['DeployScore'] = excl_des_id
#
#        # shutdown running logs
#        logging.shutdown()
#        # Generate data table for this loan application
#        output_df = pd.DataFrame([output_dict])
        return output_dict

if __name__ == '__main__':
    import pickle
    input_dict = pickle.load(open(PROJECT_DIR + '/demo_data/data.pkl', "rb" ))
    res = DriverProgram(input_dict[0]).run_driver()
