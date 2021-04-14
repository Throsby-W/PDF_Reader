import gspread
from datetime import datetime
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import sys

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scope)
client = gspread.authorize(creds)

# print ("{} {}-{}".format(sys.argv[1],datetime.today().month,datetime.today().day+1))
content = open('output.csv','r').read()


sheet = client.open("{} {}-{}".format("fitting",datetime.today().month,datetime.today().day+1))
# sheet.share("throsbywells@gmail.com", perm_type='user', role='writer')
sheet = client.import_csv(sheet.id,content)
# worksheet = sheet.sheet1
#
# df = pd.read_csv("./output.csv")
# print (df.columns.values.tolist())
# worksheet.update([df.columns.values.tolist()] + df.values.tolist())
