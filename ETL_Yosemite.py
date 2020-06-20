from ftplib import FTP
from io import StringIO
from io import BytesIO
import numpy as np
import pandas as pd

#open connection to MCWD ftp server
ftp = FTP('96.88.31.129')
ftp.login(user='MCWD', passwd = 'MCWD2020ftp')

#create working directory for ftp server
ftp.cwd('')

#create empty list to be filled with csv filenames
df_list = []

#loop through filenames and append df_list
def handle_binary(more_data):
    sio.write(more_data)


for filename in ftp.nlst():
    if "Yosemite" in filename:
        try:
            sio = BytesIO()
            ftp.retrbinary(f"RETR {filename}", callback=handle_binary)
            sio.seek(0) # Go back to the start
            df = pd.read_csv(sio, header = None, skiprows= 8, nrows = 3)
            df_list.append(df.copy())
            print('Successfully grabbed' + filename)
        except:
            print('Error in loading files from FTP')
    
ftp.quit()
#combine all files in the list
df = pd.concat(df_list)
data = df.rename(columns={0: "record_number", 1: "date", 2: "time", 3: "sensor n", 4: "pressure", 5: "temp_C", 6: "level_ft"})
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'], dayfirst=True)


#merge each parameter to create merged dataframe
Yosemite_private = data.loc[:, ["date", "time", "datetime", "level_ft", "temp_C", "pressure"]]
Yosemite_private['level_ft'] = pd.to_numeric(Yosemite_private['level_ft'], errors='coerce')
Yosemite_private.dropna(subset = ["level_ft"], inplace=True)
Yosemite_private['rounded_time'] = Yosemite_private['datetime'].dt.floor('h')
Yosemite_private['rounded_time'] = Yosemite_private['rounded_time'].astype(str)
Yosemite_public = Yosemite_private.groupby("rounded_time").mean()

#Calculate flow for Yosemite using rating curve (Yosemite: flow=37.319*(stage-853.55)^1.7061)
Yosemite_public['flow'] = Yosemite_public['level_ft']-853.55
Yosemite_public['flow']=np.power(Yosemite_public['flow'], 1.7061)
Yosemite_public['flow']= Yosemite_public['flow'] * 37.319


ftp = FTP('213.190.6.111')
ftp.login(user='u948444459', passwd = 'MCWD2020')

ftp.cwd('/public_html/')

# text buffer
buffer = StringIO()

# saving a data frame to a buffer (same as with a regular file):
Yosemite_private.to_csv(buffer, sep=',', encoding = 'utf-8', mode ='r', index=True)
text = buffer.getvalue()
bio = BytesIO(str.encode(text))
bio.seek(0)
ftp.storbinary('STOR '+ 'private_Yosemite.csv', bio)

# text buffer
public = StringIO()

# saving a data frame to a buffer (same as with a regular file):
Yosemite_public.to_csv(public, sep=',', encoding = 'utf-8', mode ='r', index=True)
public_text = public.getvalue()
public_bio = BytesIO(str.encode(public_text))
public_bio.seek(0)
ftp.storbinary('STOR '+ 'public_Yosemite.csv', public_bio)

ftp.quit()