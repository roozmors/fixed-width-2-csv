# fixed-width-2-csv parser
This repo first generate a fixed-with-file (FWF) and then transforms it to a delimited file (like csv). The initial data is provided as a dictionary of lists. Most of the code check the initial data to match the configuration criteria. The configurations for FWF are provided with a dictionary. In configuration, we have name of the columns, length of each column, its type and a default value to fill missing entries. 

The FWF is encoded in cp1252 which is a windows specific encoding. Then the data is read line by line and written into a csv file. The encoding for csv file is utf-8. That's why the resulted output might not be displayed correctly in Microsoft Excel; some characters may be displayed as a strange sign in MS Excel. 



For easy, explatory read, please use the html file. You can also download .ipynb file as well and run the cells if you have Jupyter Notebook. No extra library is required, only json module is used which is a Python native library. 

Also, the codes are condenced in fwf2csv.py file. Corresponding tests are also provided in test_fwf2csv.py. 
