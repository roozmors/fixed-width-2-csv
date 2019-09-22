
class FWF2CSV:
    """ The methods in this class create and write a fixed-width-file and read/write it into a csv file."""
    def __init__(self,dataset,config_dict):
        self.dataset = dataset
        self.config_dict = config_dict
    

    
    def fix_dict(self,data_dict,config,max_length_data):
        """ This function fills the empty cells (end of the list) with default values from config file"""
        for field_name in data_dict:
            if len(data_dict[field_name])<max_length_data:
                extesion_list = [config[field_name]['default_value'] for i in range(max_length_data-len(data_dict[field_name])) ]
                data_dict[field_name].extend(extesion_list)
                
        return data_dict   

    def fix_data_type(self,data_dict, config):
        data_dict = self.fix_cols_type(data_dict, config)
        data_dict = self.fix_cols_length(data_dict, config)
        return data_dict

    def fix_cols_type(self,data_dict, config):
        """If col type is string, change the data to string. If int or float, try to convert"""
        for col_name in config:
            if not isinstance(data_dict[col_name],config[col_name]['type']):
                if config[col_name]['type'] is str:
                    data_dict[col_name] = str(data_dict[col_name])
                elif config[col_name]['type'] is int:
                    try:
                        data_dict[col_name] = int(data_dict[col_name])
                    except ValueError:
                        print('{} cant be converted into int format'.format(data_dict[col_name]))
                elif config[col_name]['type'] is float:
                    try:
                        data_dict[col_name] = float(data_dict[col_name])
                    except ValueError:
                        print('{} cant be converted into float format'.format(data_dict[col_name]))
                
        return data_dict

    def fix_cols_length(self,data_dict,config):
        """if length of data in a string-type column is greater than it should be (i.e. =length), pick first 'length' values. 
        If type is boolean, maybe the input is True, or 1 or yes (etc.), then change the output to 1 
        data_dict, contains one series of data. """ 
        for col_name in config:
            if config[col_name]['type'] is str:
                if len(str(data_dict[col_name])) > config[col_name]['length']:
                    data_dict[col_name] = data_dict[col_name][:config[col_name]['length'] ] # first length characters
            elif config[col_name]['type'] is bool:
                if data_dict[col_name] in {1,'yes','Yes','YES','True'}:
                    data_dict[col_name]=1
                elif data_dict[col_name] in {0,'no','No','NO','False'}:
                    data_dict[col_name]=0
                else:
                    raise ValueError("{} is not a bolean type.".format(data_dict[col_name]) )
            
            else:
                if len(str(data_dict[col_name])) > config[col_name]['length']:
                    raise ValueError("{} cannot fit into {} spaces).".format(data_dict[col_name], config[col_name]['length']))

        return data_dict

    def make_new_line(self,data_dict,config,encoding = 'utf-8'):
        """ Makes new line with provided input (data) using configuration file (config)"""
        line = "".join(['{0:{1}}'.format(data_dict[col_name],config[col_name]['length']) 
                        for col_name in config])+'\n'
        
        line = line.encode(encoding = encoding, errors ='replace')
        return line

    def break_dict(self,data_dict,config):
        # when there are more than one entry for each column in the original dictionary
        # some of fields might be empty, find the maximum length
        max_length_data = 0
        for field_name in data_dict:
            max_length_data = max(len(data_dict[field_name]),max_length_data)
        
        # fill the empty cells with default value from config 
        data_dict = self.fix_dict(data_dict,config,max_length_data)
        
        nested_dict = dict.fromkeys([f_name for f_name in config])
        new_dict = {str(i):dict(nested_dict) for i in range(max_length_data)}
        
        for field_name in config:
            for idx,_ in  enumerate(data_dict[field_name]):
                new_dict[str(idx)][field_name]= data_dict[field_name][idx]

        for col_name in new_dict:
            new_dict[col_name] = self.fix_data_type(new_dict[col_name],config)
            
        return new_dict


    def write_file(self,data_dict,config, file_name = 'new_file.txt', encoding = 'cp1252'):
    
        segregated_dict = self.break_dict(data_dict,config)
        header_line = "".join(['{0:{1}}'.format(col_name,int(config[col_name]['length'])) 
                            for col_name in config])+'\n'
        header_line=header_line.encode(encoding)
        with open(file_name,"wb") as f:
            f.write(header_line)
            for dct in segregated_dict:
                f.write(self.make_new_line(segregated_dict[dct],config,encoding = encoding))    

    def chopper(self,str_obj, config):
        position = 0
        chopped_string = []
        for field_config in config.values():
            length = field_config['length']
            chopped_string.append(str_obj[position:position + length])
            position += length
        return chopped_string

    def joiner(self,chopped_line,delimiter=','):
        return delimiter.join(chopped_line)+'\n'

    def fwf_2_csv_line(self,line, config, delimiter = ','):
        chopped_line = self.chopper(line,config)
        joined_line = self.joiner(chopped_line,delimiter)
        return joined_line

    def fwf_2_csv(self, config, input_file = 'new_file.txt', output_file = 'new_utf8_file.csv', input_encoding = 'cp1252', output_encoding = 'utf-8'):
        f_in = open(input_file,'r',encoding=input_encoding)
        f_out = open(output_file,'w',encoding= output_encoding)
        for line in f_in:
            comma_joined_line = self.fwf_2_csv_line(line, config)
            f_out.write(comma_joined_line)
        f_in.close()
        f_out.close()

    

