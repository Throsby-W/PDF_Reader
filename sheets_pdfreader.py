import camelot, os, sys, webbrowser, gspread
import pandas as pd
import numpy as np
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

file_path = "/Users/Throsby/Documents/GitHub/PDF_Reader/Test PDFs/330working.pdf"

# Creates name of file without filetype as tail_wo_filetype. Creates procedure as the first four letters of tail_wo_filetype
head, tail_with_filetype = os.path.split(file_path)
tail_wo_filetype = os.path.splitext(tail_with_filetype)[0]

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scope)
client = gspread.authorize(creds)

# in_file_content = open('%s.csv'%(tail_wo_filetype),'r').read()

###--------------------------------------------------------------------------###
###Reformatting staging area

###--------------------------------------------------------------------------###
def open_in_chrome(url):
    url_to_open = "https://docs.google.com/spreadsheets/d/{}".format(url.id)
    print("Opening new link to {}".format(url_to_open))
    browser = webbrowser.get('chrome')
    browser.open_new(url_to_open)

def make_sheet_up(f_path):
    ### Opens file or creates file and shares
    h,t = os.path.split(f_path)
    t_no_csv = os.path.splitext(t)[0]
    try:
        sheet = client.open("%s"%(t_no_csv))
        print("File Exists! Opening file for {}!".format(t_no_csv))
    except:
        sheet = client.create("%s"%(t_no_csv))
        sheet.share("throsbywells@gmail.com", perm_type='user', role='writer')
        print("File DNE, Creating now!")
        print("Creating file: {}".format(t_no_csv))

    worksheet = sheet.sheet1
    header = ["Index","Comments","Rapid?","PCR?","Last","First","Middle","Title","Department","Phone","Email","Location","Type"]
    df = pd.read_csv('%s.csv'%(t_no_csv),skiprows=1,names=header)
    set_with_dataframe(worksheet,df)
    open_in_chrome(sheet)

def by_filepath_make_sheet_up():
    ### Opens file or creates file and shares
    try:
        sheet = client.open("%s"%(tail_wo_filetype))
        print("File Exists! Opening file for {}!".format(tail_wo_filetype))
    except:
        sheet = client.create("%s"%(tail_wo_filetype))
        sheet.share("throsbywells@gmail.com", perm_type='user', role='writer')
        print("File DNE, Creating now!")
        print("Creating file: {}".format(tail_wo_filetype))


    worksheet = sheet.sheet1
    header = ["Index","Comments","Rapid?","PCR?","Last","First","Middle","Title","Department","Phone","Email","Location","Type"]
    df = pd.read_csv('%s.csv'%(tail_wo_filetype),skiprows=1,names=header)
    set_with_dataframe(worksheet,df)
    open_in_chrome(sheet)
