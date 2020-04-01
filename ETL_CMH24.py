from ftplib import FTP
from io import StringIO
from io import BytesIO
import pandas as pd

#open connection to MCWD ftp server
ftp = FTP('96.88.31.129')
ftp.login(user='MCWD', passwd = 'MCWD2020ftp')

#create working directory for ftp server
ftp.cwd('/CMH24/')

#identify csv files within the ftp server
filematch='*csv'
#create empty list to be filled with csv filenames
df_list = []

#loop through filenames and append df_list
def handle_binary(more_data):
    sio.write(more_data)


for filename in ftp.nlst():
    try:
        sio = BytesIO()
        ftp.retrbinary(f"RETR {filename}", callback=handle_binary)
        sio.seek(0) # Go back to the start
        df = pd.read_csv(sio, header=None)
        df_list.append(df.copy())
        print('Successfully grabbed all files from ftp')
    except:
        print('Error in loading files from FTP')
    
ftp.quit()
#combine all files in the list
df = pd.concat(df_list)
df = df.rename(columns={0: "date", 1: "time", 2: "parameter", 3: "value", 4: "unit", 5: "QC"})
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

#seperate df by level, temp, and cond
level_df=df[df['parameter'] == "Level"]
temp_df=df[df['parameter'] == "Temp"]
cond_df=df[df['parameter'] == "Conduct"] 

#merge each parameter to create merged dataframe
merged_df = pd.merge(level_df, temp_df, on="datetime", how="left" )
merged_df = pd.merge(merged_df, cond_df, on = "datetime", how="left")
merged_df['rounded_time'] = merged_df['datetime'].dt.floor('h')


cleaned_combined = merged_df.loc[:, ["date_x", "datetime", "rounded_time", "value_y", "QC_y", "value_x", "QC_x", "value", "QC"]]
CMH24_private = cleaned_combined.rename(columns={"date_x":"date", "datetime": "CMH24_datetime", "value_y": "temp_C", "QC_y": "QC_temp", "value_x": 
                                        "level_ft", "QC_x": "QC_level", "value": "cond_uS", "QC": "QC_cond"})

CMH24_private['rounded_time'] = CMH24_private['rounded_time'].astype(str)
CMH24_public = CMH24_private.groupby("rounded_time").mean()

ftp = FTP('213.190.6.111')
ftp.login(user='u948444459', passwd = 'MCWD2020')

ftp.cwd('/public_html/')

# text buffer
buffer = StringIO()

# saving a data frame to a buffer (same as with a regular file):
CMH24_private.to_csv(buffer, sep=',', encoding = 'utf-8', mode ='r', index=True)
text = buffer.getvalue()
bio = BytesIO(str.encode(text))
bio.seek(0)
ftp.storbinary('STOR '+ 'private_CMH24.csv', bio)

# text buffer
public = StringIO()

# saving a data frame to a buffer (same as with a regular file):
CMH24_public.to_csv(public, sep=',', encoding = 'utf-8', mode ='r', index=True)
public_text = public.getvalue()
public_bio = BytesIO(str.encode(public_text))
public_bio.seek(0)
ftp.storbinary('STOR '+ 'public_CMH24.csv', public_bio)

ftp.quit()
