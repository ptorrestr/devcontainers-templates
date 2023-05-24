# install_certifi.py
#
# sample script to install or update a set of default Root Certificates
# for the ssl module.  Uses the certificates provided by the certifi package:
#       https://pypi.python.org/pypi/certifi
import os
import os.path
import ssl
import stat
import subprocess
import sys
STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
             | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
             | stat.S_IROTH |                stat.S_IXOTH )

def main():
    openssl_cafile = ssl.get_default_verify_paths().cafile
    print(" -- pip install --upgrade certifi")
    subprocess.check_call([sys.executable,
        "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"])
    
    import certifi
    
    # change working directory to the default SSL directory
    relpath_to_certifi_cafile = os.path.abspath(certifi.where())
    print(relpath_to_certifi_cafile)
    print(" -- removing any existing file or link")
    try:
        os.remove(relpath_to_certifi_cafile)
    except FileNotFoundError:
        pass
    print(" -- creating symlink to ssl cafile")
    os.symlink(openssl_cafile, relpath_to_certifi_cafile)
    print(" -- setting permissions")
    os.chmod(relpath_to_certifi_cafile, STAT_0o775)
    print(" -- update complete")
    


if __name__ == '__main__':
    main()
