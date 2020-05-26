# coding: utf-8

# In[26]:


import pygsheets
import json
import pandas as pd
import logging


# In[88]:


class GSConnection:
    def __init__(self):
        # Create the Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler('GA_report.log')
        logger_handler.setLevel(logging.DEBUG)
        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        self.logger.info('Completed configuring logger()!')
            
    def RANGE_GS_to_DF(self,url,sheet,credenciales,crange):
        #bajar credenciales de google y nombrar en el directorio como sheets_client_secret.json para poder autorizar por primera vez
        self.gc = pygsheets.authorize(outh_file=credenciales)
        # Open spreadsheet and then worksheet
        self.sh = self.gc.open_by_url(url)
        self.wks = self.sh.worksheet_by_title(sheet)
        self.data = self.wks.range(crange,  returnas='matrix')
        #self.df = pd.Series(self.data).to_frame()
        self.df=pd.read_json(json.dumps(self.data), precise_float = True, dtype = True)
        self.df.columns = self.df.iloc[0]
        self.df = self.df[1:].reset_index(drop=True)
        self.logger.warning('Conexión con GS!')
        self.logger.info('DataFrame Creado')
        return self.df
    
    def GS_to_DF(self,url,sheet,credenciales):
        #bajar credenciales de google y nombrar en el directorio como sheets_client_secret.json para poder autorizar por primera vez
        self.gc = pygsheets.authorize(outh_file=credenciales)
        # Open spreadsheet and then worksheet
        self.sh = self.gc.open_by_url(url)
        self.wks = self.sh.worksheet_by_title(sheet)
        self.data = self.wks.get_all_records()
        self.df=pd.read_json(json.dumps(self.data), precise_float = True, dtype = True)
        self.logger.warning('Conexión con GS!')
        self.logger.info('DataFrame Creado')
        return self.df
    
    def DF_to_GS(self, df,sheet,url,credenciales):        
        # bajar credenciales de google y nombrar en el directorio como sheets_client_secret.json para poder autorizar por primera vez
        self.gc = pygsheets.authorize(outh_file=credenciales)
        self.sh = self.gc.open_by_url(url)
        # Crear el sheet en la hoja de trabajo y poner el nombre de la hoja creada
        self.wks = self.sh.worksheet_by_title(sheet)
        # Borrar Columnas  ser modificadas para evitar duplicados
        self.wks.clear(start='A1', end='C5000')
        #self.wks.delete_cols(index=0, number=3)
        self.wks.set_dataframe(df, start='A1', copy_index=False, copy_head=True, fit=False, escape_formulae=False, nan='NaN')
        self.logger.warning('Conexión con GS!')
        self.logger.info('DataFrame enviado')
