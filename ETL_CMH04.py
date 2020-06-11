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
    if ".csv" in filename:
        print('Getting ' + filename)
        sio = BytesIO()
        ftp.retrbinary(f"RETR {filename}", callback=handle_binary)
        sio.seek(0) # Go back to the startdpd.read_csv(sio, header=None, skiprows= 8, nrows = 3)
        df = pd.read_csv(sio, header = None, skiprows= 8, nrows = 3)
        df_list.append(df.copy())
    
ftp.quit()
#combine all files in the list
df = pd.concat(df_list)
data = df.rename(columns={0: "record_number", 1: "date", 2: "time", 3: "sensor n", 4: "pressure", 5: "temp_C", 6: "level_ft"})
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'], dayfirst=True)


#merge each parameter to create merged dataframe
CMH04_private = data.loc[:, ["date", "time", "datetime", "level_ft", "temp_C", "pressure"]]
CMH04_private['level_ft'] = pd.to_numeric(CMH04_private['level_ft'], errors='coerce')
CMH04_private.dropna(subset = ["level_ft"], inplace=True)
CMH04_private['rounded_time'] = CMH04_private['datetime'].dt.floor('h')
CMH04_private['rounded_time'] = CMH04_private['rounded_time'].astype(str)
CMH04_public = CMH04_private.groupby("rounded_time").mean()

#Calculate flow for CMH04 using rating curve (CMH04: flow=37.319*(stage-853.55)^1.7061)
CMH04_public['flow'] = CMH04_public['level_ft']-853.55
CMH04_public['flow']=np.power(CMH04_public['flow'], 1.7061)
CMH04_public['flow']= CMH04_public['flow'] * 37.319


ftp = FTP('213.190.6.111')
ftp.login(user='u948444459', passwd = 'MCWD2020')

ftp.cwd('/public_html/')

# text buffer
buffer = StringIO()

# saving a data frame to a buffer (same as with a regular file):
CMH04_private.to_csv(buffer, sep=',', encoding = 'utf-8', mode ='r', index=True)
text = buffer.getvalue()
bio = BytesIO(str.encode(text))
bio.seek(0)
ftp.storbinary('STOR '+ 'private_CMH04.csv', bio)

# text buffer
public = StringIO()

# saving a data frame to a buffer (same as with a regular file):
CMH04_public.to_csv(public, sep=',', encoding = 'utf-8', mode ='r', index=True)
public_text = public.getvalue()
public_bio = BytesIO(str.encode(public_text))
public_bio.seek(0)
ftp.storbinary('STOR '+ 'public_CMH04.csv', public_bio)

ftp.quit()