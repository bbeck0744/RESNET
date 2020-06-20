from ftplib import FTP
from io import StringIO
from io import BytesIO
import pandas as pd

ftp = FTP('213.190.6.111')
ftp.login(user='u948444459', passwd = 'MCWD2020')

ftp.cwd('/public_html/')

#create empty list to be filled with csv filenames

df_list = []

def handle_binary(more_data):
    sio.write(more_data)

for filename in ftp.nlst():
    if "public" in filename:
        print('Getting ' + filename)
        sio = BytesIO()
        ftp.retrbinary(f"RETR {filename}", callback=handle_binary)
        sio.seek(0) # Go back to the startdpd.read_csv(sio, header=None, skiprows= 8, nrows = 3)
        df = pd.read_csv(sio)
        df = df.loc[:, ["rounded_time", "level_ft", "temp_C", "flow"]]
        df['site']=filename[7:12]
        df_list.append(df.copy())
    
ftp.quit()

#combine all files in the list
df = pd.concat(df_list)


#create connection to ftp site
ftp = FTP('213.190.6.111')
ftp.login(user='u948444459', passwd = 'MCWD2020')

ftp.cwd('/public_html/')

# text buffer
buffer = StringIO()

# saving a data frame to a buffer (same as with a regular file):
df.to_csv(buffer, sep=',', encoding = 'utf-8', mode ='r', index=True)
text = buffer.getvalue()
bio = BytesIO(str.encode(text))
bio.seek(0)
ftp.storbinary('STOR '+ 'combined_data.csv', bio)

ftp.quit()



