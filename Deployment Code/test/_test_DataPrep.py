import unittest
import pickle
import datetime
from engine import DataPrepare
from engine.Util import PROJECT_DIR

class TestDataPrep(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        demo_path1 = PROJECT_DIR + '/demo_data/data.pkl'
        input_dict1 = pickle.load(open(demo_path1, "rb" ))
        self.VALID_LOAN_COLUMNS = DataPrepare.VALID_LOAN_COLUMNS
        self.VALID_INQUIRY_COLUMNS = DataPrepare.VALID_INQUIRY_COLUMNS
        self.VALID_TRADE_LINE_COLUMNS = DataPrepare.VALID_TRADE_LINE_COLUMNS
        
        self.example1 = DataPrepare(input_dict1[0])
        self.loan1, self.tradeline1, self.inquiry1 = self.example1.run().values()
        self.expect_result1 = {
        'loans': {'application_id': '115732a2527c01cb9f42975ea31a5691',
          'vehicle_type': None,
          'ecoa': '1',
          'open_date': datetime.datetime(2015, 5, 3, 0, 0),
          'vehicle_condition': None},
         'trade_lines': [{'application_id': '115732a2527c01cb9f42975ea31a5691',
           'tradeline_id': '2aca5bafc0679d076ff493513912da93',
           'account_type': '18',
           'balance_amount': 0,
           'raw_balance_date': datetime.datetime(2015, 7, 24, 0, 0),
           'delinquency_over_90_days': 0,
           'limit': 6000,
           'open_date': datetime.datetime(1999, 10, 21, 0, 0),
           'original_amount': 0,
           'payment_profile': '0C0CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
           'responsibility': '1'}],
         'inquiries': [{'application_id': '115732a2527c01cb9f42975ea31a5691',
           'date': datetime.datetime(2014, 9, 25, 0, 0),
           'id': '225331_v4',
           'kob': 'BM'}]
    }      
        demo_path2 = PROJECT_DIR + '/demo_data/2 sample record/data.pkl'
        input_dict2 = pickle.load(open(demo_path2, "rb" ))
        
        self.example2 = DataPrepare(input_dict2[0])
        self.loan2, self.tradeline2, self.inquiry2 = self.example2.run().values()
        self.expect_result2 = {
        'loans': {'application_id': 'fba59f15208e96978895775bbe324d01',
          'vehicle_type': 'atv',
          'ecoa': '1',
          'open_date': datetime.datetime(2017, 7, 29, 0, 0),
          'vehicle_condition': None},
        'trade_lines': [{'application_id': 'fba59f15208e96978895775bbe324d01',
            'tradeline_id': '8a16f6b0b1eead743afc7b3568128ade',
            'account_type': '31',
            'balance_amount': 0,
            'delinquency_over_90_days': 0,
            'limit': None,
            'open_date': datetime.datetime(2012, 12, 27, 0, 0),
            'raw_balance_date': datetime.datetime(2016, 3, 9, 0, 0),
            'original_amount': 867,
            'payment_profile': 'GG',
            'responsibility': '1'},\
             {'application_id': 'fba59f15208e96978895775bbe324d01',
            'tradeline_id': '5d203347a50346722817b99ed04caeb6',
            'account_type': '7',
            'balance_amount': 0,
            'delinquency_over_90_days': 0,
            'limit': 0,
            'open_date': datetime.datetime(2011, 1, 21, 0, 0),
            'raw_balance_date':datetime.datetime(2012, 12, 26, 0, 0),
            'original_amount': 0,
            'payment_profile': 'L-----0C----CC--CCCCCCCC------------------00000000000000000',
            'responsibility': '1'},
              {'application_id': 'fba59f15208e96978895775bbe324d01',
            'tradeline_id': '45a4e2ff068eb41e0c971e791f059805',
            'account_type': '18',
            'balance_amount': 3542,
            'delinquency_over_90_days': 0,
            'limit': 7000,
            'open_date': datetime.datetime(2004, 8, 20, 0, 0),
            'raw_balance_date': datetime.datetime(2017, 7, 2, 0, 0),
            'original_amount': 0,
            'payment_profile': 'CCCCCCCCCCCCCCC0CCCCCCCCCCCCCCCCCCCCCCCCCCC0CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
            'responsibility': '3'}
              ],
        'inquiries': [{'application_id': 'fba59f15208e96978895775bbe324d01',
            'id': '10501_v5', 
            'date': datetime.datetime(2017, 2, 3, 0, 0),
            'kob': 'BB'},\
          {'application_id': 'fba59f15208e96978895775bbe324d01',
            'id': '10501_v5', 
            'date': datetime.datetime(2017, 7, 27, 0, 0),
            'kob': 'ZF'}]
          }
        
    def test_loans_data1(self):
        for col, val in self.VALID_LOAN_COLUMNS.items():
            # check if columns exist
            self.assertIn(col, self.loan1)
            # check if column types match
            if self.loan1[col]:
                self.assertIsInstance(self.loan1[col], eval(val['type']))
            # check if values of each column are correct
            self.assertEqual(self.loan1[col], self.expect_result1['loans'][col])
    def test_trade_lines_data1(self):
        for idx, tradeline in enumerate(self.tradeline1):
            for col, val in self.VALID_TRADE_LINE_COLUMNS.items():
                # check if columns exist
                self.assertIn(col, tradeline)
                # check if column types match
                if tradeline[col]:
                    self.assertIsInstance(tradeline[col], eval(val['type']))
                # check if values of each column are correct
                self.assertEqual(tradeline[col], self.expect_result1['trade_lines'][idx][col])            

    def test_inquiries_data1(self):
        for idx, inquiry in enumerate(self.inquiry1):
            for col, val in self.VALID_INQUIRY_COLUMNS.items():
                # check if columns exist
                self.assertIn(col, inquiry)
                # check if column types match
                if inquiry[col]:
                    self.assertIsInstance(inquiry[col], eval(val['type']))
                # check if values of each column are correct
                self.assertEqual(inquiry[col], self.expect_result1['inquiries'][idx][col])            
    def test_final_output1(self):
        a = self.example1.run()
        self.assertEqual(a, self.expect_result1)
        
    def test_loans_data2(self):
        for col, val in self.VALID_LOAN_COLUMNS.items():
            # check if columns exist
            self.assertIn(col, self.loan2)
            # check if column types match
            if self.loan2[col]:
                self.assertIsInstance(self.loan2[col], eval(val['type']))
            # check if values of each column are correct
            self.assertEqual(self.loan2[col], self.expect_result2['loans'][col])

    def test_trade_lines_data2(self):
        print(self.tradeline2)
        for idx, tradeline in enumerate(self.tradeline2):
            for col, val in self.VALID_TRADE_LINE_COLUMNS.items():
                # check if columns exist
                self.assertIn(col, tradeline)
                # check if column types match
                if tradeline[col]:
                    self.assertIsInstance(tradeline[col], eval(val['type']))
                # check if values of each column are correct
                self.assertEqual(tradeline[col], self.expect_result2['trade_lines'][idx][col])    
                
    def test_inquiries_data2(self):
        for idx, inquiry in enumerate(self.inquiry2):
            for col, val in self.VALID_INQUIRY_COLUMNS.items():
                # check if columns exist
                self.assertIn(col, inquiry)
                # check if column types match
                if inquiry[col]:
                    self.assertIsInstance(inquiry[col], eval(val['type']))
                # check if values of each column are correct
                self.assertEqual(inquiry[col], self.expect_result2['inquiries'][idx][col])            
    def test_final_output2(self):
        a = self.example2.run()
        self.assertEqual(a, self.expect_result2)                
if __name__ == '__main__':
    unittest.main(verbosity = 2)