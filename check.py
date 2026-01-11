import sys
import hashlib
import base64
import subprocess
import re

if len(sys.argv) > 1:
    oib = sys.argv[1]
    val = f"9934:{oib}".encode('utf-8')
    hashed = base64.b32encode(hashlib.sha256(val).digest()).decode('utf-8').rstrip('=')
    domain = f"{hashed}.iso6523-actorid-upis.prod.ams.porezna-uprava.hr"

    try:
        output = subprocess.check_output(["dig", "+short", "@dns1.hitronet.hr", "NAPTR", domain], universal_newlines=True)
        match = re.search(r'https?://[^!"]+', output)
        if match:
            print(match.group(0))
    except:
        pass
