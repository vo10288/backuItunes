##python encrypted_backup_extractor.py "/percorso/backup/itunes" "/percorso/directory/output" "password_backup"

import os
import shutil
import sqlite3
import argparse
import datetime
from Crypto.Cipher import AES

def extract_backup_data(backup_path, output_dir, password):
    # Crea la directory di output utilizzando la libreria datetime
    output_dir = os.path.join(output_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(output_dir)

    # Percorso al file del database criptato
    encrypted_db_path = os.path.join(backup_path, "Manifest.db")

    # Percorso al file di output del database decifrato
    decrypted_db_path = os.path.join(output_dir, "Manifest.db")

    # Decifra il database utilizzando la password fornita
    cipher = AES.new(password.encode("utf-8"), AES.MODE_CBC, b"0000000000000000")
    with open(encrypted_db_path, "rb") as encrypted_file:
        with open(decrypted_db_path, "wb") as decrypted_file:
            while True:
                chunk = encrypted_file.read(16)
                if len(chunk) == 0:
                    break
                decrypted_chunk = cipher.decrypt(chunk)
                decrypted_file.write(decrypted_chunk)

    # Estrai le immagini e i video
    media_dir = os.path.join(backup_path, "Media")
    if os.path.exists(media_dir):
        shutil.copytree(media_dir, os.path.join(output_dir, "Media"))

    # Estrai il database di WhatsApp
    whatsapp_db_path = os.path.join(backup_path, "AppDomainGroup-group.net.whatsapp.WhatsApp.shared", "ChatStorage.sqlite")
    if os.path.exists(whatsapp_db_path):
        shutil.copy2(whatsapp_db_path, output_dir)

    # Estrai il database degli SMS
    sms_db_path = os.path.join(backup_path, "3d0d7e5fb2ce288813306e4d4636395e047a3d28")
    if os.path.exists(sms_db_path):
        shutil.copy2(sms_db_path, output_dir)

    # Estrai il registro chiamate
    call_history_db_path = os.path.join(backup_path, "call_history.db")
    if os.path.exists(call_history_db_path):
        shutil.copy2(call_history_db_path, output_dir)

    # Estrai il file della rubrica contatti
    address_book_path = os.path.join(backup_path, "31bb7ba8914766d4ba40d6dfb6113c8b614be442")
    if os.path.exists(address_book_path):
        shutil.copy2(address_book_path, output_dir)

    print("Estrazione completata. I dati sono stati salvati nella directory: {}".format(output_dir))

if __name__ == "__main__":
    # Utilizza la libreria argparse per l'input e l'output
    parser = argparse.ArgumentParser(description='Estrae i dati da un backup iTunes criptato.')
    parser.add_argument('backup_path', type=str, help='Il percorso del backup iTunes')
    parser.add_argument('output_dir', type=str, help='La directory di output')
    parser.add_argument('password', type=str, help='La password per decifrare il backup')
    args = parser.parse_args()

    extract_backup_data(args.backup_path, args.output_dir, args.password)
