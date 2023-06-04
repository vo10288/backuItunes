import os
import plistlib
import sqlite3
import shutil

def extract_data_from_backup(backup_path):
    # Verifica se il percorso del backup esiste
    if not os.path.exists(backup_path):
        print("Il percorso del backup non esiste.")
        return
    
    # Percorso dei file SQLite del backup di iTunes
    info_path = os.path.join(backup_path, "Info.plist")
    db_path = os.path.join(backup_path, "3d0d7e5fb2ce288813306e4d4636395e047a3d28")
    
    # Verifica se i file necessari esistono
    if not os.path.exists(info_path) or not os.path.exists(db_path):
        print("Il backup di iTunes non contiene i file necessari.")
        return
    
    # Lettura del file Info.plist
    with open(info_path, "rb") as info_file:
        info_data = plistlib.load(info_file)
        device_name = info_data.get("Device Name", "Unknown Device")
        backup_date = info_data.get("Last Backup Date", "Unknown Date")
    
    # Controllo se il backup è criptato
    is_encrypted = info_data.get("IsEncrypted", False)
    if is_encrypted:
        password = input("Il backup di iTunes è criptato. Inserisci la password: ")
        # Verifica se la password è corretta
        if not verify_backup_password(backup_path, password):
            print("La password inserita non è corretta.")
            return
    
    # Connessione al database SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Estrarre i contatti dal backup
    cursor.execute("SELECT ABPerson.First, ABPerson.Last, ABMultiValue.value FROM ABPerson, ABMultiValue WHERE ABPerson.ROWID = ABMultiValue.record_id AND ABMultiValue.property = 3")
    contacts = cursor.fetchall()
    
    # Stampa dei contatti
    print("Contatti nel backup di", device_name, "effettuato il", backup_date)
    for contact in contacts:
        first_name = contact[0]
        last_name = contact[1]
        phone_number = contact[2]
        print("Nome:", first_name)
        print("Cognome:", last_name)
        print("Numero di telefono:", phone_number)
        print()
    
    # Estrarre le foto dal backup
    photo_dir = os.path.join(backup_path, "Media/DCIM")
    if os.path.exists(photo_dir):
        dest_dir = "./photos"
        os.makedirs(dest_dir, exist_ok=True)
        photo_files = os.listdir(photo_dir)
        for photo_file in photo_files:
            src_path = os.path.join(photo_dir, photo_file)
            dest_path = os.path.join(dest_dir, photo_file)
            shutil.copy(src_path, dest_path)
        print("Le foto sono state estratte correttamente.")
    
    # Estrarre i video dal backup
    video_dir = os.path.join(backup_path, "Media/DCIM")
    if os.path.exists(video_dir):
        dest_dir = "./videos"
        os.makedirs(dest_dir, exist_ok=True)
        video_files = os.listdir(video_dir)
        for video_file in video_files:
            src_path = os.path.join(video_dir, video_file)
            dest_path = os.path.join(dest_dir, video_file)
            shutil.copy(src_path, dest_path)
        print("I video sono stati estratti correttamente.")
    
    # Estrarre le chat di WhatsApp dal backup
    wa_db_path = os.path.join(backup_path, "AppDomainGroup-group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite")
    if os.path.exists(wa_db_path):
        wa_conn = sqlite3.connect(wa_db_path)
        wa_cursor = wa_conn.cursor()
        wa_cursor.execute("SELECT ZCONTACTJID, ZTEXT FROM ZWAMESSAGE")
        whatsapp_messages = wa_cursor.fetchall()
        print("Chat di WhatsApp nel backup di", device_name)
        for message in whatsapp_messages:
            contact_jid = message[0]
            text = message[1]
            print("Contatto JID:", contact_jid)
            print("Messaggio:", text)
            print()
        wa_conn.close()
    
    # Chiusura della connessione al database SQLite
    conn.close()

def verify_backup_password(backup_path, password):
    # Verifica se la password è corretta
    # Implementa qui la logica per verificare la password del backup
    # Puoi utilizzare librerie come 'keyring' o 'cryptography' per decifrare il backup
    # Restituisci True se la password è corretta, False altrimenti
    return True

# Percorso del backup di iTunes
backup_path = "/percorso/backup/itunes"

# Chiamata alla funzione per estrarre i dati dal backup
extract_data_from_backup(backup_path)
