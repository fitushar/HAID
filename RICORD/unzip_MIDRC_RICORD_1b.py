import zipfile38 as zipfile
#import zipfile
with zipfile.ZipFile('MIDRC_RICORD_1b.zip', 'r') as zip_ref:
    zip_ref.extractall('/image_data2/COVID_19_Publicdata/MIDRC_RICORD/MIDRC_RICORD_1b/')