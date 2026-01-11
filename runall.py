import sqlite3
import hashlib
import base64
import subprocess
import re

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT id, oib FROM taxpayers WHERE posrednik IS NULL AND active = 1")
rows = cursor.fetchall()

for row_id, oib in rows:
    if not oib: continue
    
    try:
        val = f"9934:{oib.strip()}".encode('utf-8')
        hashed = base64.b32encode(hashlib.sha256(val).digest()).decode('utf-8').rstrip('=')
        domain = f"{hashed}.iso6523-actorid-upis.prod.ams.porezna-uprava.hr"

        output = subprocess.check_output(
            ["dig", "+short", "@dns1.hitronet.hr", "NAPTR", domain], 
            universal_newlines=True
        )
        
        match = re.search(r'https?://[^!"]+', output)
        if match:
            url = match.group(0)
            cursor.execute("UPDATE taxpayers SET posrednik = ? WHERE id = ?", (url, row_id))
            print(f"{oib} -> {url}")
            conn.commit()
        else:
            print(f"{oib} -> Not found")
            
    except Exception:
        print(f"{oib} -> Error")

conn.close()
