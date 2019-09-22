import unittest
import json
import os 

from fwf2csv import FWF2CSV

class TestFWF2CSV(unittest.TestCase):
    # tc stands for test_case
    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    
    def setUp(self):
        self.base_test_case = {
            'f1': ['ab','AB','AAABBB_B'],
            'f2': ['cd','CD','CCC_DDD_D'],
            'f3': ['ef','EF','EFFF_FFF'],
            'f4': ['gh','GH','GHGHGHGH'],
            'f5': ['ij','IJ','IJIJIJIJ'],
            'f6': ['kl','KL','KL___KL'],
            'f7': ['mn','MN','MN123456MN'],
            'f8': ['op','OP','OPOP'],
            'f9': ['qr','QR','QRqrQRqr'],
            'f10': ['st','ST','STSTstST']
        }

        with open ('spec.json','r') as jf:
            specs_dict = json.load(jf)
        self.base_config_dict = {col_name:{'length': int(length_val), 'type': str,'default_value' : ''} 
               for (col_name,length_val) in zip(specs_dict['ColumnNames'], specs_dict['Offsets'])}

        self.base_tc_isntance = FWF2CSV(self.base_test_case,self.base_config_dict)

            
    def tearDown(self):
        print('tearDown\n')
    
    def test_fix_dict(self):
        tc_1 = {
            'f1': ['ab','AB',12345678],
            'f2': [1],
            'f3': ['ef','EF'],
        }

        config_1 = {
            'f1': {'length': 5, 'type': str, 'default_value' : ''},
            'f2': {'length': 12, 'type': int, 'default_value' : -1},
            'f3': {'length': 3, 'type': str, 'default_value' : ''}
        }

        EA_1 = {
            'f1': ['ab','AB',12345678],
            'f2': [1,-1,-1],
            'f3': ['ef','EF',''],
        }
        
        self.assertEqual(FWF2CSV.fix_dict(self,tc_1,config_1,3),EA_1)
        
    def test_fix_data_type(self):
        # type f1 from int to str, type f2 from str to int, type f3 from bool to str, 
        # length f1 should be cut to 5
        tc_2 = {
            'f1': 12345678,
            'f2': '1',
            'f3': True,
        }

        config_2 = {
            'f1': {'length': 5, 'type': str, 'default_value' : ''},
            'f2': {'length': 12, 'type': int, 'default_value' : -1},
            'f3': {'length': 6, 'type': str, 'default_value' : ''}
        }

        EA_2 = {
            'f1': '12345',
            'f2': 1,
            'f3': 'True',
        } 

        self.assertEqual(FWF2CSV.fix_data_type(FWF2CSV(tc_2,config_2),tc_2,config_2),EA_2)

    def test_fix_cols_type(self):
        # f1 is a string and can't be converted to int
        tc_3 = {
            'f1': 'ab',
            'f2': '1',
        }

        config_3_1 = {
            'f1': {'length': 5, 'type': int, 'default_value' : ''},
            'f2': {'length': 12, 'type': int, 'default_value' : -1},
        }

        self.assertRaises( (TypeError,ValueError),FWF2CSV.fix_cols_type(self,tc_3,config_3_1))

        config_3_2 = {
                    'f1': {'length': 5, 'type': float, 'default_value' : ''},
                    'f2': {'length': 12, 'type': int, 'default_value' : -1},
                }
        self.assertRaises( (TypeError,ValueError),FWF2CSV.fix_cols_type(self,tc_3,config_3_2))

    def test_fix_cols_length(self):
        # f1 should be cut to 5 letters. f2 with config_4_1 should be fine
        # but when change the length to 2, 123 can't fit into 2 spaces field, should raise error
        # same with config_4_3 in which f2 column type is float
        tc_4 = {
            'f1': 'abcdef',
            'f2': 123,
        }

        config_4_1 = {
            'f1': {'length': 5, 'type': str, 'default_value' : ''},
            'f2': {'length': 3, 'type': int, 'default_value' : -1},
        }

        EA_4 = {
            'f1': 'abcde',
            'f2': 123,
        }

        self.assertEqual( FWF2CSV.fix_cols_length(self,tc_4,config_4_1),EA_4)

        config_4_2 = {
                    'f1': {'length': 5, 'type': str, 'default_value' : ''},
                    'f2': {'length': 2, 'type': int, 'default_value' : -1},
                }
        self.assertRaises( (TypeError,ValueError),FWF2CSV.fix_cols_type(self,tc_4,config_4_2))

        config_4_3 = {
                    'f1': {'length': 5, 'type': str, 'default_value' : ''},
                    'f2': {'length': 2, 'type': float, 'default_value' : -1},
                }
        self.assertRaises( (TypeError,ValueError),FWF2CSV.fix_cols_type(self,tc_4,config_4_3))


    def test_make_new_line(self):
        # should return line in binary format
        tc_5 = {
            'f1': 'abcde',
            'f2': 123,
        }
        
        config_5= {
            'f1': {'length': 7, 'type': str, 'default_value' : ''},
            'f2': {'length': 3, 'type': int, 'default_value' : -1}
            }

        EA_5 = b'abcde  123\n'
        self.assertEqual(FWF2CSV.make_new_line(self,tc_5,config_5),EA_5)

    

    def test_break_dict(self):
        tc_6 = {
            'f1': ['ab','AB','12345'],
            'f2': [1,0,2],
            'f3': ['ef','EF','EFG'],
        }

        config_6 = {
            'f1': {'length': 5, 'type': str, 'default_value' : ''},
            'f2': {'length': 12, 'type': int, 'default_value' : -1},
            'f3': {'length': 3, 'type': str, 'default_value' : ''}
        }

        EA_6 = {'0':{'f1': 'ab', 'f2': 1, 'f3': 'ef'},
                '1':{'f1': 'AB', 'f2': 0, 'f3': 'EF'},
                '2':{'f1': '12345', 'f2': 2, 'f3': 'EFG'}
        }

        self.assertEqual(FWF2CSV.break_dict(FWF2CSV(tc_6, config_6), tc_6, config_6), EA_6)

    def test_write_file(self):
        # should write file to local directory 
        file_name = 'test_new_file.txt'
        FWF2CSV.write_file(self.base_tc_isntance,
        self.base_test_case, self.base_config_dict, file_name=file_name)
        self.assertTrue(os.path.exists(file_name))

    def test_chopper(self):
        tc_7 = '  fo   12   bar'

        config_7 = {
            'f1': {'length': 4, 'type': str, 'default_value' : ''},
            'f2': {'length': 5, 'type': int, 'default_value' : -1},
            'f3': {'length': 6, 'type': str, 'default_value' : ''}
        }
        EA_7 =['  fo','   12','   bar']
        self.assertEqual(FWF2CSV.chopper(self,tc_7,config_7),EA_7)

    def test_joiner(self):
        tc_8 = ['  fo','   12','   bar']

        EA_8 ='  fo,   12,   bar\n'
        self.assertEqual(FWF2CSV.joiner(self,tc_8),EA_8)  

    def test_fwf_2_csv_line(self):
        tc_9 = '  fo   12   bar'
        config_9 = {
            'f1': {'length': 4, 'type': str, 'default_value' : ''},
            'f2': {'length': 5, 'type': int, 'default_value' : -1},
            'f3': {'length': 6, 'type': str, 'default_value' : ''}
        }

        EA_9 ='  fo,   12,   bar\n'
        self.assertEqual(FWF2CSV.fwf_2_csv_line(FWF2CSV(tc_9,config_9),tc_9,config_9),EA_9) 

    def test_E2E(self):
        # test case with all kind of problems
        # the file should show correctly in excel while with problem in other utf-8 based apps
        tc_10 = {
            'f1': ['ab','‘’','AAABBB_B'],# big cell
            'f2': [12.3,123,True], # incompatible cell type
            'f3': ['ef','EF','EFFF_FFF'],# big cell
            'f4': ['gh','','GHGHGHGH'], # empty cell
            'f5': ['Jânis','El Niño','résumé'],
            'f6': ['kl','KL'], # missing cell
            'f7': [10,12,20], # int to float
            'f8': [12.3,1.23,2.8], # foat to int
            'f9': ['qr','QR','QRqrQRqr'],
            'f10': ['st','ST','STSTstST']
        }
        config_10 = {
            'f1': {'length': 5, 'type': str, 'default_value': ''},
            'f2': {'length': 12, 'type': str, 'default_value': ''},
            'f3': {'length': 3, 'type': str, 'default_value': ''},
            'f4': {'length': 2, 'type': str, 'default_value': ''},
            'f5': {'length': 13, 'type': str, 'default_value': ''},
            'f6': {'length': 7, 'type': str, 'default_value': ''},
            'f7': {'length': 10, 'type': float, 'default_value': ''},
            'f8': {'length': 13, 'type': int, 'default_value': ''},
            'f9': {'length': 20, 'type': str, 'default_value': ''},
            'f10': {'length': 13, 'type': str, 'default_value': ''}
        }

        file_name = 'E2E_test_new_file.txt'
        tc_10_insctance = FWF2CSV(tc_10,config_10)

        FWF2CSV.write_file(tc_10_insctance,
        tc_10, config_10, file_name=file_name)
        self.assertTrue(os.path.exists(file_name))

        
    def test_E2E_csv(self):
        tc_11 = {
            'f1': ['ab','‘’','AAABBB_B'],# big cell
            'f2': [12.3,123,True], # incompatible cell type
            'f3': ['ef','EF','EFFF_FFF'],# big cell
            'f4': ['gh','','GHGHGHGH'], # empty cell
            'f5': ['Jânis','El Niño','résumé'],
            'f6': ['kl','KL'], # missing cell
            'f7': [10,12,20], # int to float
            'f8': [12.3,1.23,2.8], # foat to int
            'f9': ['qr','QR','QRqrQRqr'],
            'f10': ['st','ST','STSTstST']
        }
        config_11 = {
            'f1': {'length': 5, 'type': str, 'default_value': ''},
            'f2': {'length': 12, 'type': str, 'default_value': ''},
            'f3': {'length': 3, 'type': str, 'default_value': ''},
            'f4': {'length': 2, 'type': str, 'default_value': ''},
            'f5': {'length': 13, 'type': str, 'default_value': ''},
            'f6': {'length': 7, 'type': str, 'default_value': ''},
            'f7': {'length': 10, 'type': float, 'default_value': ''},
            'f8': {'length': 13, 'type': int, 'default_value': ''},
            'f9': {'length': 20, 'type': str, 'default_value': ''},
            'f10': {'length': 13, 'type': str, 'default_value': ''}
        }

        tc_11_instance = FWF2CSV(tc_11,config_11)
        FWF2CSV.fwf_2_csv(tc_11_instance, config_11, 
        input_file = 'E2E_test_new_file.txt', output_file = 'E2E_test_new_utf8_file.csv', 
        input_encoding = 'cp1252', output_encoding = 'utf-8')
        self.assertTrue(os.path.exists('E2E_test_new_utf8_file.csv'))        



if __name__ == '__main__':
    unittest.main()
