# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 10:51:03 2023

@author: huangrunchen
"""

import re
import math
import pandas as pd

def numberextractor(input_string): #chip size "1.65mmx 1.75mm x 1.00mm"
    pattern = r'\d+\.\d+'
    matches = re.findall(pattern, input_string)
    numbers = [float(match) for match in matches]
    if len(numbers) == 3:
        return numbers
    else:
        raise ValueError("Expected exactly three numbers in the input string.")
def remove_space_lower(input_string):
    input_string=input_string.replace(" ", "")
    input_string=input_string.lower()
    return input_string
def extract_num_text(input_string):
    input_string=input_string.replace(" ", "")
    number_pattern = r'\d+\.\d+|\d+'
    numbers = re.findall(number_pattern, input_string)
    numbers = [num for num in numbers if num]
    # Split the input string by commas and plus signs
    text = re.split(r',|\+', input_string)   
    return numbers, text
def extract_number(input_string):
    extracted_number = int(''.join([c for c in input_string if c.isdigit()]))
    return extracted_number
def extract_MSL_reflow(input_string):
    input_string=input_string.replace(" ", "")
    pattern = r'\d+'
    matches = re.findall(pattern, input_string)
    if len(matches) >= 2:
        MSL_level = int(matches[0])
        reflow_number = int(matches[1])
        return MSL_level, reflow_number
    else:
        return None

def generate_result(row):
    attribute = row["Attribute"]
    ##########0) Package)##############################
    if attribute == "Package name" or attribute == "Basic type":
        return "NA"
    
    elif attribute == "QRC":
        if row["Reference"] == row["Target"]:
            return "Can be referenced"
        elif row["Reference"] == "Automotive":
            return "Cannot be referenced"
        elif row["Reference"] == "Standard":
            return "Can be referenced"
        elif row["Target"] == "Automotive":
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "AEC quality Grade (in case automotive)":
        if extract_number(row["Reference"]) >= extract_number(row["Target"]):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Mission profile (within QRC standards)":
        if row["Reference"].lower() == "yes" and row["Target"].lower()=="yes":
            return "Can be referenced"
        else:
            return "Cannot be referenced"
    
    
    elif attribute == "Packing":
        if (extract_MSL_reflow(row["Reference"])[0] <= extract_MSL_reflow(row["Target"])[0] #MSL level
            and extract_MSL_reflow(row["Reference"])[1] >= extract_MSL_reflow(row["Target"])[1]): #Number of MSL reflow
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Package Outline":
        if extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]:
            return "Can be referenced"
        else:
            return "Cannot be referenced"
    ###########################1) Chip #####################################    
    elif attribute == "Chip Size":
        x_Ref=numberextractor(row["Reference"])[0]
        y_Ref=numberextractor(row["Reference"])[1]
        z_Ref=numberextractor(row["Reference"])[2]
        x_Tar=numberextractor(row["Target"])[0]
        y_Tar=numberextractor(row["Target"])[1]
        z_Tar=numberextractor(row["Target"])[2]
        diagonal_Ref = math.sqrt(x_Ref**2+y_Ref**2)
        diagonal_Tar = math.sqrt(x_Tar**2+y_Tar**2)
        if (y_Tar/x_Tar <= 2.5 
            and (diagonal_Tar-diagonal_Ref)/diagonal_Ref <= 0.15
            and (diagonal_Tar-diagonal_Ref)/diagonal_Ref >= -0.5 
            and 0.85*z_Ref <= z_Tar <= 1.15*z_Ref):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
    
        
    elif attribute == "FSM":
        # Compare Reference and Target when the attribute is "FSM"
        if (extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]
           and  extract_num_text(row["Reference"])[1][1] == extract_num_text(row["Target"])[1][1]
           and  extract_num_text(row["Reference"])[1][3] == extract_num_text(row["Target"])[1][3]
           and  extract_num_text(row["Reference"])[1][5] == extract_num_text(row["Target"])[1][5]
           ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
    elif attribute == "BSM":
        # Define rules for another attribute here

        if (extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]
           and  extract_num_text(row["Reference"])[1][1] == extract_num_text(row["Target"])[1][1]
           and  extract_num_text(row["Reference"])[1][3] == extract_num_text(row["Target"])[1][3]
           and  extract_num_text(row["Reference"])[1][5] == extract_num_text(row["Target"])[1][5]
           ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Passivation":
        # Define rules for another attribute here
        if (extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]
           and  extract_num_text(row["Reference"])[1][1] == extract_num_text(row["Target"])[1][1]
           and  extract_num_text(row["Reference"])[1][3] == extract_num_text(row["Target"])[1][3]
           ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "BPO":
        BPO_x_r=float(extract_num_text(row["Reference"])[0][0])
        BPO_y_r=float(extract_num_text(row["Reference"])[0][1])
        BPO_dia_r=math.sqrt(BPO_x_r**2+BPO_y_r**2)
        BPO_x_t=float(extract_num_text(row["Target"])[0][0])
        BPO_y_t=float(extract_num_text(row["Target"])[0][1])
        BPO_dia_t=math.sqrt(BPO_x_t**2+BPO_y_t**2)
        if (0.85*BPO_dia_r <= BPO_dia_t <= 1.15 * BPO_dia_r):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "BPP":
        BPP_r=float(extract_num_text(row["Reference"])[0][0])
        BPP_t=float(extract_num_text(row["Target"])[0][0])
        if  BPP_t>= BPP_r:
            return "Can be referenced"
        else:
            return "Cannot be referenced"     
####################2) Carrier#############################
    elif attribute == "Die paddle":
        x_Ref=numberextractor(row["Reference"])[0]
        y_Ref=numberextractor(row["Reference"])[1]
        z_Ref=numberextractor(row["Reference"])[2]
        x_Tar=numberextractor(row["Target"])[0]
        y_Tar=numberextractor(row["Target"])[1]
        z_Tar=numberextractor(row["Target"])[2]
        diagonal_Ref = math.sqrt(x_Ref**2+y_Ref**2)
        diagonal_Tar = math.sqrt(x_Tar**2+y_Tar**2)
        if (z_Ref == z_Tar
            and 0.85*diagonal_Ref  <= diagonal_Tar <= 1.15*diagonal_Ref ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "E-pad":
        EPAD_x_r=float(extract_num_text(row["Reference"])[0][0])
        EPAD_y_r=float(extract_num_text(row["Reference"])[0][1])
        EPAD_dia_r=math.sqrt(EPAD_x_r**2+EPAD_y_r**2)
        EPAD_x_t=float(extract_num_text(row["Target"])[0][0])
        EPAD_y_t=float(extract_num_text(row["Target"])[0][1])
        EPAD_dia_t=math.sqrt(EPAD_x_t**2+EPAD_y_t**2)
        if (0.85*EPAD_dia_r <= EPAD_dia_t <= 1.15 * EPAD_dia_r):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Lead post (non-fuse)" or attribute == "Lead post (fuse)":
        x_r=float(extract_num_text(row["Reference"])[0][0])
        y_r=float(extract_num_text(row["Reference"])[0][1])
        area_r=x_r*y_r
        x_t=float(extract_num_text(row["Target"])[0][0])
        y_t=float(extract_num_text(row["Target"])[0][1])
        area_t=x_t*y_t
        if (0.5 * area_r <= area_t <= 1.5 *area_r):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Leadingframe top plating thickness":
        if (extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]
           and  extract_num_text(row["Reference"])[1][1] == extract_num_text(row["Target"])[1][1]
           and  extract_num_text(row["Reference"])[1][3] == extract_num_text(row["Target"])[1][3]
           and  extract_num_text(row["Reference"])[1][5] == extract_num_text(row["Target"])[1][5]
           ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
        
    elif attribute == "Leadingframe bottom plating thickness":
        if (extract_num_text(row["Reference"])[0] == extract_num_text(row["Target"])[0]
           and  extract_num_text(row["Reference"])[1][1] == extract_num_text(row["Target"])[1][1]
           ):
            return "Can be referenced"
        else:
            return "Cannot be referenced"
    
    elif attribute == "Lead pitch":
        ref = float(extract_num_text(row["Reference"])[0][0])
        tar = float(extract_num_text(row["Target"])[0][0])
        if tar >= ref :
            return "Can be referenced"
        else:
            return "Cannot be referenced"
####################4.1) Interconnect###############################
    elif attribute == "Number of down bonds (chip to die pad)" or attribute == "Number of chip to chip bonds" :
        ref = float(row["Reference"])
        tar = float(row["Target"])
        if tar <= ref :
            return "Can be referenced"
        else:
            return "Cannot be referenced"  
        
    elif attribute == "Number of ground bonds (chip to ground ring)" or attribute == "Number of ground bonds (Lead to ground ring)" :
        ref = float(row["Reference"])
        tar = float(row["Target"])
        if 0.7*ref <= tar <= 1.3* ref :
            return "Can be referenced"
        else:
            return "Cannot be referenced"  
        
    elif attribute == "Wire diameter":
        ref = float(extract_num_text(row["Reference"])[0][0])
        tar = float(extract_num_text(row["Target"])[0][0])
        if tar == ref :
            return "Can be referenced"
        else:
            return "Cannot be referenced"    
#################7,8,9) Pre-assembly/FEOL/BEOL Process########################        
    elif attribute == "Pre-Assembly Process" or attribute == "FEOL process" or attribute == "BEOL process" :
        if row["Target"].lower()=="yes" :
            return "Can be referenced"
        else:
            return "Cannot be referenced" 

    else:
        # Default rule for other attributes
        if remove_space_lower(row["Reference"]) == remove_space_lower(row["Target"]):
            return "Can be referenced"
        else:
            return "Cannot be referenced"

       
def generate_test(row):
    attribute = row["Attribute"]
    result = row["Result"]
    if result == "NA" :
        return pd.Series({'TC': None, 
                          'HTSL': None, 'HTRB': None,'HTGB': None,
                          'THB': None,'HAST': None, 'H3TRB': None, 
                          'PTC': None,'IOL': None, 
                          'UHAST': None})
#######################0) Package ##############################         
    elif attribute == "Assembly Location":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})        
    elif attribute == "Package type":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': 'X', 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': None, 
                              'PTC': 'X','IOL': None, 
                              'UHAST': 'X'})
    elif attribute in ["Number of die","Q006 requirement (in case automotive)"]:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})         
    elif attribute == "Packing":
        if (extract_MSL_reflow(row["Reference"])[0] > extract_MSL_reflow(row["Target"])[0] #MSL level
            and extract_MSL_reflow(row["Reference"])[1] >= extract_MSL_reflow(row["Target"])[1]): #Number of MSL reflow
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None}) 
        elif extract_MSL_reflow(row["Reference"])[1] < extract_MSL_reflow(row["Target"])[1]:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': 'X'})
        else:
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})          
    elif attribute == "Package Outline":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL':  None, 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': None, 
                              'PTC':  None,'IOL': None, 
                              'UHAST':  None})         
#######################1) Chip ##############################       
    elif attribute == "Wafer material":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': None,'HAST': '△', 'H3TRB': None, 
                              'PTC': '■','IOL': '■', 
                              'UHAST': '△'})
    elif attribute == "Pre-assembly method":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': 'X'})  
        
    elif attribute == "Pre-assembly site":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': 'X' ,'IOL': None, 
                              'UHAST': None})
    elif attribute == "BOAA(YES/No)":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': '■' ,'IOL': '■', 
                              'UHAST': None})
    elif attribute == "Chip Size":
        z_Ref=numberextractor(row["Reference"])[2]
        z_Tar=numberextractor(row["Target"])[2]
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        elif z_Tar > 1.15*z_Ref or z_Tar < 0.85*z_Ref:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': 'X'}) 
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': None})     
    elif attribute == "FSM":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})
    elif attribute == "BSM":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': None})    
    elif attribute in ["BPO", "BPP"]:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': '△',  
                              'PTC': None ,'IOL': None, 
                              'UHAST': None}) 
########################2) Carrier##################################
    elif attribute == "Leadframe Material":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': None ,'IOL': None, 
                              'UHAST': 'X'}) 
    elif attribute == "Heat sink Material(if applicable)": 
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None}) 
    elif attribute == "E-pad/non E-pad": 
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})  
    elif attribute in ["Die paddle","E-pad"]: 
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None,
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})   
    elif attribute in ["Lead post (non-fuse)","Lead post (fuse)"]: 
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None,
                              'PTC': None,'IOL': None, 
                              'UHAST': None})  
    elif attribute == "Lead pitch": 
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})     
##########################2.2) Carrier (substrate)#################
    elif attribute == "Core material":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': None})
    elif attribute in ["Solder Resist","Plating material"]:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST':  None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': '△'})  
    elif attribute == "Substrate thickness":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})     
#########################3) Die Attach##########################   
#########################4) Interconnect######################### 
    elif attribute == "Wire diameter":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': 'X', 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': None, 
                              'PTC': '■','IOL': '■',  
                              'UHAST': 'X'})   
    elif attribute == "Wire bond method":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': '■','IOL': '■',  
                              'UHAST': 'X'}) 
    elif attribute == "Clip":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': None,'HAST': '△', 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': '△'})
    elif attribute == "Pre-assembly bump site":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': 'X','HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None ,'IOL': None, 
                              'UHAST': 'X'})
    elif attribute == "Bump thickness":
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': None ,'IOL': None, 
                              'UHAST': None}) 
    elif attribute in ["Material Name", "Solder ball size"]:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': 'X', 'HTRB': None,'HTGB': None,
                              'THB': '△','HAST': '△', 'H3TRB': None, 
                              'PTC': 'X' ,'IOL': None, 
                              'UHAST': None})  
    elif attribute in ["Encapsulant", "Adhesion promoter"]:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': None})     
    else:
        if result == "Can be referenced":
            return pd.Series({'TC': None, 
                              'HTSL': None, 'HTRB': None,'HTGB': None,
                              'THB': None,'HAST': None, 'H3TRB': None, 
                              'PTC': None,'IOL': None, 
                              'UHAST': None})
        else:
            return pd.Series({'TC': 'X', 
                              'HTSL': '○', 'HTRB': '○','HTGB': '○',
                              'THB': '△','HAST': '△', 'H3TRB': '△', 
                              'PTC': '■','IOL': '■', 
                              'UHAST': 'X'})