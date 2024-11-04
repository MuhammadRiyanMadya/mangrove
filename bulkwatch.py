"""
Created to scanning and extracting large excel data based on identifier keys
~MRM 08/08/2024
"""
import sys
sys.path.append('../flakes')
import flakes
import numpy as np
import collections
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
import logging
import datetime
from datetime import timedelta
        
class dataExt():

    logger = logging.getLogger(__name__)

    def __init__(self, fileName):
        self.n = 1
        self.name = fileName
        self.SaveLoc = os.getcwd()
        self.MainKey = 'Key1' #by default refers to R201, please CHANGE this accordingly !
        self.namebackup = None
        logging.basicConfig(filename = self.SaveLoc + '\\' + self.name + '.log', level = logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filemode = 'a')

        logging.info('\n')
        # test the update logger formats
        # pass! 13/10/2024
        
    def filter(self, columnLimit=2, fromFolder = False, newxlsx = False):
        """
        Default structure:
        column 1: valve opening
        column 2: flow value
        column 3: ppm hydrogen
        column n: additional parameters
        """
        path = self.SaveLoc + '\\' + self.name + '.xlsx'
        if fromFolder == False:
            df = pd.read_excel(path)
##            df = df.dropna(thresh =1).dropna(axis=0)
            df = df[df != -1].dropna()
##            df = df.replace(to_replace = 'MAS 2158', value = 1)
##            df = df.replace(to_replace = 'MAS-2158', value = 1)
##            df = df.replace(to_replace = '2158', value = 1)
##            df = df.replace(to_replace = 'MAS  2158', value = 1)
##            df = df.replace(to_replace = 2158, value = 1)
##
##            df = df.replace(to_replace = 'MAS 2159', value = 2)
##            df = df.replace(to_replace = 'MAS-2159', value = 2)
##            df = df.replace(to_replace = '2159', value = 2)
##            df = df.replace(to_replace = '2159.0', value = 2)
##
##            df = df.replace(to_replace = 'MAS 3352', value = 3)
##            df = df.replace(to_replace = 'MAS-3352', value = 3)
##            df = df.replace(to_replace = '3352', value = 3)
##            df = df.replace(to_replace = 3352, value = 3)
##
##            df = df.replace(to_replace = 'MAS 3256', value = 4)
##            df = df.replace(to_replace = 'MAS-3256', value = 4)
##            df = df.replace(to_replace = '3256', value = 4)
##            df = df.replace(to_replace = 3256, value = 4)
##
##            df = df.replace(to_replace = 'MAS 3355', value = 5)
##            df = df.replace(to_replace = 'MAS-3355', value = 5)
##            df = df.replace(to_replace = '3355', value = 5)
##            df = df.replace(to_replace = 3355, value = 5)
##            
##
##            df = df.replace(to_replace = 'MAS 3160', value = 6)
##            df = df.replace(to_replace = 'MAS-3160', value = 6)
##            df = df.replace(to_replace = '3160', value = 6)
##
##            df = df.replace(to_replace = 'MAS 5402', value = 7)
##            df = df.replace(to_replace = 'MAS-5402', value = 7)
##            df = df.replace(to_replace = '5402', value = 7)
##
##            df = df.replace(to_replace = 'MAS 5637', value = 8)
##            df = df.replace(to_replace = 'MAS-5637', value = 8)
##            df = df.replace(to_replace = '5637', value = 8)
##
##            df = df.replace(to_replace = 'MAS 7402', value = 9)
##            df = df.replace(to_replace = 'MAS-7402', value = 9)
##            df = df.replace(to_replace = '7402', value = 9)
##
##            df = df.replace(to_replace = 'MAS 7702', value = 10)
##            df = df.replace(to_replace = 'MAS-7702', value = 10)
##            df = df.replace(to_replace = '7702', value = 10)
            
            df = df.sort_values(by=[df.columns.values[0]], ignore_index = True)

            for i in range(len(df.iloc[:,2])):
                mytype = df.iloc[i,2]
                if isinstance(mytype, int) or isinstance(mytype, np.int64):
                    continue
                if 'ZN' in mytype:
                    df = df.replace(mytype, 7)
                elif 'C49' in mytype:
                    df = df.replace(mytype, 4)
                elif 'C44' in mytype or 'HRC44' in mytype:
                    dfv = df.replace(mytype,3)
                else:
                    df = df.replace(mytype, 1)

            for i in range(len(df.iloc[:,1])):
                
                if 2158 == mytype:
                    df = df.replace(mytype, 11)
                elif 2159 == mytype:
                    df = df.replace(mytype, 13)
                elif 3355 == mytype:
                    df = df.replace(mytype, 15)
                elif 3256 == mytype:
                    df = df.replace(mytype, 17)
                elif 5637 == mytype or 5402 == mytype:
                    df = df.replace(mytype, 19)
                else:
                    pass

            
##            df = df[df != 'ZN'].dropna()
##            df = df[df != 'HR--ZN'].dropna()
##            df = df[df != 'ZN--HR'].dropna()
##            df = df[df != 'HR->ZN'].dropna()
##            df = df[df != 'ZN->HR'].dropna()
##            df = df[df != 'HR'].dropna()
##            df = df[df != 'HR--ZN'].dropna()
##            df = df[df != 'ZN--HR'].dropna()
##            df = df[df != 'HR->ZN'].dropna()
##            df = df[df != 'ZN->HR'].dropna()
            
            npdata = df.values
            
        if newxlsx == True:
            newname = self.name + '_filtered'
            if os.path.exists(os.getcwd() + '\\' + newname + '.xlsx'):
                os.remove(os.getcwd() + '\\' + newname + '.xlsx')
                
            with pd.ExcelWriter(newname + '.xlsx') as writer:
                df.to_excel(writer, header = None, index = False)

        return npdata
        
    def dataV(self, npd, secondData= True):

        fig, ax1 = plt.subplots()

        ax1.plot(npd[:,0], npd[:,1], linestyle = 'dashed',linewidth = 0.5, color = 'blue', label = self.name, marker = '.', markerfacecolor ='yellow', markersize = 7)
        ax1.set_xlabel('OP, %')
        ax1.set_ylabel('H2 kg/h', color = 'b')
        ax1.tick_params('y', colors='b')
        ax1.xaxis.set_major_locator(MultipleLocator(2))
##        ax1.yaxis.set_major_locator(MultipleLocator(0.025))

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines = lines1
        labels = labels1
        if secondData == True:
            ax2 = ax1.twinx()
            ax2.plot(npd[:,0], npd[:,2], label = 'PPM', linewidth = 0.5,color = 'red', linestyle ='dashed', marker ='.', markerfacecolor =  'yellow', markersize = 7)
            ax2.set_ylabel('PPM', color='r')
            ax2.tick_params('y', colors = 'r')
            lines2, labels2 = ax2.get_legend_handles_labels()
            lines = lines1 + lines2
            labels = labels1 + labels2
        plt.legend(lines, labels, loc = 'upper right')
        plt.title(f'{self.name} Valve Trend', fontsize = 16, fontweight = 'bold')
        plt.show()
        
    def xlsxIdentifier(self, path, keys, FileErrorFlag = False):
        logging.info('Extracting Data Inside ' + path)
        print(f'Start scanning {path}')
        
        for files in os.listdir(path):
            self.foldernamebackup = files
            try:
                if '.' in files:
                    print(f'Scanning {files}')
                    filePath = path + '\\' + files
                    self.df_init = pd.read_excel(filePath)

                    #back up the date as secondary data
                    self.xlsxnamebackup = files

                    #checking
                    for j in keys:
                        idx = np.where(self.df_init == j)
                        if len(idx[0]) != 0:
                            break
                    #warning and logging
                    if len(idx[0]) == 0:
                        logging.info(files + ' Not FOUND')
                           
                    #processing - extracting and expanding
                    if len(idx[0]) != 0:
                        self.df = pd.read_excel(filePath)

                        ### preliminary look up
                        print(self.df.head(50))
                        print(self.df.iloc[0:50,13:17])
                        ###

                        if self.MainKey == 'Key1':
                            DT = self.dataBrowser(self.df, 'DATE :', 'DATE:', formatNew = 'FRONT',searchObj = 'date')
                            GR = self.dataBrowser(self.df, '1.', formatNew = 'FRONT',searchObj = 'BulkStr')
                            CATZ = self.dataBrowser(self.df, '4.', formatNew = 'FRONT')
##                            TC222 = self.dataBrowser(self.df, '15.', formatNew = 'FRONT', searchObj = 'Bulk')
##                            FI222 = self.dataBrowser(self.df, '15.', formatNew = 'FRONT', searchObj = 'Bulk2')
                            
                            TC3 = self.dataBrowser(self.df, '7.', formatNew = 'FRONT', searchObj = 'Bulk2')
                            TD = self.dataBrowser(self.df, '8.', formatNew = 'FRONT', searchObj = 'Bulk2')
                            FlowDonor = self.dataBrowser(self.df, '9.', formatNew = 'FRONT', searchObj = 'Bulk2')
                            FlowTeal = self.dataBrowser(self.df, '10.', formatNew = 'FRONT', searchObj = 'Bulk2')
                            MIL = self.dataBrowser(self.df, 'Ton pp/Kg cat', formatNew = 'FRONT', searchObj = 'Bulk4')
                            OGPurge = self.dataBrowser(self.df, 'Tons', ' Tons', searchObj = 'Bulk4')
                            OGRec = self.dataBrowser(self.df, 'Kg/Hr', 'Kg / Hr', ' Kg / Hr',searchObj = 'Bulk4')
                            Rate = self.dataBrowser(self.df, ' Ton / Hr','Ton/Hr', formatNew = 'FRONT', searchObj = 'Bulk4')
                        
                        mydict = {'Date': DT[0], 'GRADE': GR[0], 'CATZ': CATZ[0], 'TC3': np.average(TC3), 'TD': np.average(TD), 'FlowDonor': np.average(FlowDonor), 'FlowTeal': np.average(FlowTeal), \
                                  'MIL': np.average(MIL), 'OGPurge': np.average(OGPurge), 'OGRec': np.average(OGRec), 'Rate': np.average(Rate)}

                        print(mydict)
              
                        self.autobackup(self.name + '.xlsx', **mydict)
                        
                        logging.info(files + f' {self.name}:-> INDEX {self.n}')
                        self.n += 3
                        
##                    self.dfGrade = pd.read_excel(filePath)
##                    grade = self.dataBrowser(self.dfGrade, 'GRADE PROD', searchObj = 'Grade')
##                    
##                    mydict = {'OP': grade, 'PV': grade, 'PPM': grade}
##                    self.dataPool(self.name + '.xlsx', **mydict)
##
##                    logging.info(filePath + ':-> INDEX {}'.format(self.n))
##                    self.n += 3
                    
                    
                elif '.' not in files:
                    self.xlsxIdentifier(path + '\\' + files, keys)
                else:
                    FileErrorFlag = True
            except Exception as e:
                print('\n\n "WARNING FILE ERROR" \n {}\{} \n *-------------------* \n'.format(path, files))
                logging.info('\nERROR\n! ' + files + f' Err Msg: {e}\n')
                continue
            
        print('END')
        logging.info('END \n')
            
    def dataBrowser(self, file: pd.DataFrame, *args, formatNew = None, searchObj = 'standard', opIdx = 0):
        dataBlock = np.array([])
        for i in args:
            IdxKey = np.where(file == i)
            print('IDXKey',IdxKey)
            if len(IdxKey[0]) != 0:
                break
            
        if len(IdxKey[0]) != 0:
            elemNum = len(IdxKey[0])
            if elemNum > 2:
                print("WARNING: Three identical identifiers are FOUND !")
                
            if formatNew == None:
                FCrow = IdxKey[0][-1]
                FCcol = IdxKey[1][-1]
                    
            elif formatNew == 'FRONT' :
                FCrow = IdxKey[0][0]
                FCcol = IdxKey[1][0]
            elif formatNew == 'MID':
                FCrow = IdxKey[0][-2]
                FCcol = IdxKey[1][-2]

            print(FCrow)
            print(FCcol)
            
            if searchObj == 'standard':
                for z in range(1,5):
                    dt = file.iloc[FCrow, FCcol + 13]
                    dataBlock = np.append(dataBlock,dt)

            if searchObj == 'Bulk1':
                for z in range(0,12,3):
                    dt = file.iloc[FCrow+1, FCcol + 13 + z]
                    print(dt)
                    if isinstance(dt, str):
                        dt = -1
                    dataBlock = np.append(dataBlock,dt)

            if searchObj == 'Bulk2':
                for z in range(0,12,3):
                    dt = file.iloc[FCrow, FCcol + 13 + z]
                    print(dt)
                    if isinstance(dt, str):
                        dt = -1
                    dataBlock = np.append(dataBlock,dt)
                    
            if searchObj == 'BulkStr':
                for z in range(0,12,3):
                    dt = file.iloc[FCrow, FCcol + 13 + z]
                    dataBlock = np.append(dataBlock,dt)

            if searchObj == 'Bulk3':
                for z in range(0,12,3):
                    dt = file.iloc[FCrow+1, FCcol + 15 + z]
                    print(dt)
                    if isinstance(dt, str):
                        dt = -1
                    dataBlock = np.append(dataBlock,dt)

            if searchObj == 'Bulk4':
                for z in range(0,12,3):
                    dt = file.iloc[FCrow, FCcol + 2 + z]
                    if isinstance(dt, str):
                        dt = None
                    dataBlock = np.append(dataBlock,dt)
                    
            if searchObj == 'string':
                for z in range(2,5):
                    dt = file.iloc[FCrow+z, FCcol+opIdx]
                    dataBlock = np.append(dataBlock,dt)

            if searchObj == 'string2':
                for z in range(1,7):
                    dt = file.iloc[FCrow+z, FCcol+opIdx]
                    if dt == dt:
                        dataBlock = np.append(dataBlock,dt)

            if searchObj == 'string3':
                for z in range(1,4):
                    dt = file.iloc[FCrow+z, FCcol+opIdx]
                    if (dt == 'STOP') or (dt != dt) or (dt == 'STOPED'):
                        dataBlock = np.append(dataBlock,1)
                    else:
                        dataBlock = np.append(dataBlock,2)
                            
            if searchObj == 'date':
                time = [[6,0],[14,0],[22,0],[24,0]]
                for z in range(1,5):
                    dt = file.iloc[FCrow, FCcol + 2]
                    if dt == isinstance(dt, pd._libs.tslibs.timestamps.Timestamp):
                        dt = dt.to_pydatetime()
                    if dt != None and not isinstance(dt,str) and not isinstance(dt,int) and not isinstance(dt,float):
                        dt = dt + timedelta(hours=time[z-1][0], minutes=time[z-1][1])
                        dataBlock = np.append(dataBlock,dt)
                    elif isinstance(dt,str):
                        init_day = int(dt.split(' ')[0])
                        init_month = dt.split(' ')[1].upper()
                        init_year = int(dt.split(' ')[-1])
                        try:
                            months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OKT','NOV','DES']
                            monthdex = months.index(init_month) + 1
                            dt = datetime.datetime(init_year,monthdex, init_day)
                            if z <= 3:
                                dt = dt + timedelta(hours=time[z-1][0], minutes=time[z-1][1])
                            else:
                                dt = dt + timedelta(hours=time[z-1][0], minutes=time[z-1][1])
                                print(dt)
                            dataBlock = np.append(dataBlock, dt)
                        except:
                            try:
                                months = ['JANUARI','FEBRUARI','MARET','APRIL','MEI','JUNI','JULI','AGUSTUS','SEPTEMBER','OKTOBER','NOVEMBER','DESEMBER']
                                monthdex = months.index(init_month) + 1
                                if z <= 3:
                                    dt = dt + timedelta(hours=time[z-1][0], minutes=time[z-1][1])
                                else:
                                    dt = dt + timedelta(hours=time[z-1][0], minutes=time[z-1][1])
                                    print(dt)
                                dataBlock = np.append(dataBlock, dt)
                            except Exception as e:
                                dataBlock = np.append(dataBlock, None)
                                print('\n\n "DATE ERROR" \n {} \n *-------------------* \n', self.xlsxnamebackup)
                                logging.info('\nERROR\n! ' + self.xlsxnamebackup + f' Err Msg: {e}\n')
                                    
                    else:
                        dataBlock = np.append(dataBlock, None)
                
        return dataBlock

    def autobackup (self, filename, appending = True, **kwargs):
        
        FirstFileFlag = False
        if not appending:
            if os.path.exists(os.getcwd() + '\\' + filename):
                os.remove(os.getcwd() + '\\' + filename)
                
        all_data = tuple([i for i in kwargs.values()])
        all_keys =[i for i in kwargs.keys()]
                         
        datadf_input = pd.DataFrame(np.vstack(all_data).T, columns = all_keys)

        try:
            datadf_excel = pd.read_excel(filename)
            lastrow = len(datadf_excel.iloc[:,0])
        except Exception as e:
            FirstFileFlag = True
            with pd.ExcelWriter(filename) as writer:
                datadf_input.to_excel(writer, header = 1, index = False)
            datadf_excel = pd.read_excel(filename)
            lastrow = len(datadf_excel.iloc[:,0])
            
        if FirstFileFlag != True:
            with pd.ExcelWriter(filename,
                                mode = 'a',
                                if_sheet_exists = 'overlay'
                                ) as writer:
                datadf_input.to_excel(writer, header = None, index = False, startrow = lastrow + 1)


# LIST OF KEYS in PT PP LOGSHEET

## GRADE KEYS
gradeKey2161 = ['MAS 2161']
gradeKey2161 = ['MAS 2162']
gradeKey2158 = ['MAS-2158', 'MAS 2158', 'MAS2158', 'MAS - 2158']
gradeKey2159 = ['MAS-2159', 'MAS 2159', 'MAS2159', 'MAS~2159']
gradeKey3355 = ['MAS-3355', 'MAS 3355', 'MAS3355', 'MAS~3355']
gradeKey3352 = ['MAS-3352', 'MAS 3352', 'MAS3352', 'MAS~3352']
gradeKey2345 = ['MAS-2345', 'MAS 2345', 'MAS2345', 'MAS~2345']
gradeKey5637 = ['MAS-5637', 'MAS 5637', 'MAS5637', 'MAS~5637']
gradeKey5402 = ['MAS-5402', 'MAS 5402', 'MAS5402', 'MAS~5402']
gradeKey7402 = ['MAS-7402', 'MAS 7402', 'MAS7402', 'MAS~7402']
gradeKey7702 = ['MAS-7702', 'MAS 7702', 'MAS7702', 'MAS~7702']

gradeKeyLowOne = gradeKey2159 + gradeKey2158 + gradeKey2161+ gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKeyLowTwo = gradeKey2159 + gradeKey2158 + gradeKey2161+ gradeKey3355 + gradeKey3352 + gradeKey2345 + gradeKey5637 + gradeKey5402

gradeKeyHighOne =  gradeKey5637 + gradeKey5402 + gradeKey7402 + gradeKey7702
gradeKeyHighTwo =  gradeKey7402 + gradeKey7702

#YEAR GRADE KEYS - FOR HYDROGEN LOW-HIGH ANALYSIS

gradeKey_2008 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2010 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2012 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2014 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2016 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2018 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2019 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2020 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2021 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2022 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2023 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345
gradeKey_2024 = gradeKey2158 + gradeKey2161 + gradeKey2159 + gradeKey3355 + gradeKey3352 + gradeKey2345

## CATZ KEYS
catzKeyHR = ['HR', 'hr', 'Hr', 'hR', 'H R']
catzKeyZN = ['ZN', 'zn', 'Zn', 'zN', 'Z N'] 
All = ['HR', 'hr', 'Hr', 'hR', 'H R','ZN', 'zn', 'Zn', 'zN', 'Z N']
UniversalKey = ['GROUP', 1,'']
UniversalKeyBulk = ['NO', 'No',1,'']

myd = dataExt('BulkPerformance_Okctober_2024')
myd.MainKey = 'Key1'
myd.xlsxIdentifier(r'C:\Users\mrm\OneDrive - Polytama Propindo\Bulk\Operations\2024\BULK\10~OKT', UniversalKeyBulk)

##m = myd.filter(newxlsx = True)
##print(m)
####myd.dataV(m, secondData = True)
##
