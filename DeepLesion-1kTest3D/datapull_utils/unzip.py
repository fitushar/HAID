import zipfile
import os
filelist= [file for file in os.listdir() if file.endswith('.zip')]
print(filelist[3:])

for rio_zim in filelist[3:]:
    print('Extraction-Start-{}'.format(rio_zim))
    with zipfile.ZipFile(rio_zim, 'r') as zip_ref:
         zip_ref.extractall('/image_data/nobackup/DeepLesion_Pull/unzip/')
         print('Extraction-Done-{}'.format(rio_zim))