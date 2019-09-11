# -*- coding: utf-8 -*-
"""
@author: DGuo
"""

"""
Converts a collection of one application data in python dictionary format into another
python dictionary which is used for other modules in deployment.

Directions
==========

The CSVParser requires 1 input file(dictionary) containing these keys: application, principal.
And also in princiapl, it must have keys 'trade_lines' and 'inquiries'.

Module
------
Input: Python Dictionary
Output: Python Dictionary

In your code import the module, instantiate the `MatrixCSVParser` class by
passing the location of the dictionary file, and execute the run method. The run
method will return a collection of python objects.

```
from matrix_csv_parser import MatrixCSVParser

parser = MatrixCSVParser(
    input_dict = {
    'application':...,
    'principal':{
            'trade_lines':[...],
            'inquiries':[...]}
)
results = parser.run()
```
"""
import sys
import datetime
import logging
from engine.Util import log_format, PROJECT_DIR, DataPrepInputCheck

class DataPrepare(object):
    VALID_LOAN_COLUMNS = {
        "application_id": {"type": "str"},
        "vehicle_type": {"type": "str"},
        "ecoa": {"type":"str"},
        "open_date": {"type": "datetime.datetime"}
    }

    VALID_INQUIRY_COLUMNS = {
        "application_id": {"type": "str"},
        "id": {"type":"str"},
        "date": {"type": "datetime.datetime"},
        "kob": {"type": "str"}
    }

    VALID_TRADE_LINE_COLUMNS = {
        "application_id": {"type": "str"},
        'tradeline_id': {"type": "str"},
        "account_type": {"type": "str"},
        "balance_amount": {"type": "int"},
        "limit": {"type": "int"},
        "open_date": {"type": "datetime.datetime"},
        "raw_balance_date":{"type": "datetime.datetime"},
        "original_amount": {"type": "int"},
        "payment_profile": {"type": "str"},
        "responsibility": {"type": "str"},
        "delinquency_over_90_days": {"type": "int"}
    }
    logger = logging.getLogger("DATAPREP")
    input_dict = DataPrepInputCheck('input_dict', logger)

    def __init__(self, input_dict):
        """
        :param loans_csv_path: (dict) dictionary of input interface.
        """
        self.input_dict = input_dict

    @staticmethod
    def checktype_convert(value, type_):
        """
        Function to cast string inputs to their respective types
        """
        if type_ == "str":
            try:
                res = str(value) if value != None else None
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                err_message = "Error happened in convert function:Line{}. Value '{}' could not be converted to string. \n {}".format(exc_tb.tb_lineno, value, e)
                raise ValueError(err_message)

        elif type_ == "int":
            try:
                res = int(value) if value != None else None
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                err_message = "Error happened in convert function:Line{}. Value '{}' could not be converted to integer. \n {}".format(exc_tb.tb_lineno, value, e)
                raise ValueError(err_message)

        elif type_ == "datetime.datetime":
            if isinstance(value, datetime.datetime):
                return value
            elif isinstance(value, datetime.date):
                return datetime.datetime.combine(value, datetime.datetime.min.time())
            else:
                try:
                    res = datetime.datetime.strptime(value, "%Y-%m-%d") if value else None
                except:
                    try:
                        res = datetime.datetime.strptime(value, "%m/%d/%Y") if value else None
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        err_message = "Error happened in convert function:Line{}. Value '{}' could not be converted to datetime. \n {}".format(exc_tb.tb_lineno, value, e)
                        raise ValueError(err_message)
        else:
            err_message = "{} is not one of the default types. Default types only have 'int', 'str' and 'datetime'. ".format(type_)
            raise ValueError(err_message)
        return res

    def check_loan_columns(self):
        # check loan columns
        loan_info = self.input_dict['application'].copy()
        valid_columns = DataPrepare.VALID_LOAN_COLUMNS
        for col in valid_columns:
            if col not in loan_info:
                DataPrepare.logger.warning("Warning: column {} in LOAN dataset is missing.".format(col))
            loan_info[col] = self.checktype_convert(loan_info.get(col, None), valid_columns[col]['type'])
        return loan_info

    def check_inquiry_columns(self):
        # check inquiry columns
        inquiry_info = self.input_dict['principal']['inquiries'].copy()
        valid_columns = DataPrepare.VALID_INQUIRY_COLUMNS
        for inquiry_record in inquiry_info:
            for col in valid_columns:
                if col not in inquiry_record:
                    DataPrepare.logger.warning("Warning: column {} in INQUIRY dataset is missing.".format(col))
                inquiry_record[col] = self.checktype_convert(inquiry_record.get(col, None), valid_columns[col]['type'])
            return inquiry_info

    def check_trade_line_columns(self):
        # check tradeline columns
        trade_line_info = self.input_dict['principal']['trade_lines'].copy()
        valid_columns = DataPrepare.VALID_TRADE_LINE_COLUMNS
        for trade_line_record in trade_line_info:
            for col in valid_columns:
                if col not in trade_line_record:
                    DataPrepare.logger.warning("Warning: column {} in TRADELINE dataset  is missing.".format(col))
                trade_line_record[col] = self.checktype_convert(trade_line_record.get(col, None), valid_columns[col]['type'])
            return trade_line_info


    def run(self):
        """
        Converts a collection of applications in CSV format into a collection
        of python objects in a similar format to the decisioning model libraries
        input format
        """
        # instantiate logger
        if (DataPrepare.logger.hasHandlers()):
            DataPrepare.logger.handlers.clear()
        log_format(PROJECT_DIR + '/logs/DataPrep', DataPrepare.logger)

        # Prepare loan data and generate log
        DataPrepare.logger.info("Extracting Loan Data From Input Interface.")
        try:
            loans = self.check_loan_columns()
        except Exception as e:
            err_message = "Error happened in LOAN data!"
            DataPrepare.logger.error(err_message)
            DataPrepare.logger.error('Exact Error Info:' + '\n' + str(e))
            raise ValueError(err_message)
        else:
            DataPrepare.logger.info("Loan Extraction Successful.")

        # Prepare tradeline data and generate log
        DataPrepare.logger.info("Extracting Tradeline Data From Input Interface.")
        try:
            trade_lines = self.check_trade_line_columns()
        except Exception as e:
            err_message = "Error happened in TRADELINE data."
            DataPrepare.logger.error(err_message)
            DataPrepare.logger.error('Exact Error Info:' + '\n' + str(e))
            raise ValueError(err_message)
        else:
            DataPrepare.logger.info("Tradeline Extraction Successful.")

        # Prepare inquiry data and generate log
        DataPrepare.logger.info("Extracting Inquiry Data From Input Interface.")
        try:
            inquiries = self.check_inquiry_columns()
        except Exception as e:
            err_message = "Error happened in INQUIRY data!"
            DataPrepare.logger.error(err_message)
            DataPrepare.logger.error('Exact Error Info:' + '\n' + str(e))
            raise ValueError(err_message)
        else:
            DataPrepare.logger.info("Inquiry Extraction Successful.")
        DataPrepare.logger.info("Dara Preparation Successfull.")
        logging.shutdown()
        return {'loans':loans, 'trade_lines':trade_lines, 'inquiries' : inquiries}

if __name__ == '__main__':
    import pickle
    input_dict = pickle.load(open(PROJECT_DIR + '/demo_data/data.pkl', "rb" ))
    input_dict_ln1 = input_dict[0]
    res = DataPrepare(input_dict_ln1).run()
