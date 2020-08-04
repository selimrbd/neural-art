#!/usr/bin/python3
from pathlib import Path
import urllib.request
import tarfile

path_model_folder = Path('app/model')
path_model_tar = path_model_folder/'magenta_arbitrary-image-stylization-v1-256_2.tar.gz'
nst_model_download_link = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed'

####################

if not path_model_folder.exists():
    path_model_folder.mkdir()

## download nst model
urllib.request.urlretrieve(nst_model_download_link, path_model_tar)

## decompress nst model
def untar(fpath):
    fpath= Path(fpath)
    if str(fpath).endswith("tar.gz"):
        tar = tarfile.open(fpath, "r:gz")
        tar.extractall(fpath.parent)
        tar.close()
    elif str(fpath).endswith("tar"):
        tar = tarfile.open(fpath, "r:")
        tar.extractall(fpath.parent)
        tar.close()
untar(path_model_tar) ## decompress
