from cryptography.fernet import Fernet
key="EzeAxENSleAqYXrXwHaqqaZf23ZJgqm2gKR_J3IkMGw="
system_information_e="e_system.txt"
clipboard_information_e="e_clipboard.txt"
keys_information_e="e_keys_logged.txt"

encrypted_files=[system_information_e,clipboard_information_e,keys_information_e]
c=0
for decrypting_file in encrypted_files:
    with open(encrypted_files[c], 'rb') as f:
        data = f.read()
    # To encrypt the keys
    fernet = Fernet(key)
    dencrypted = fernet.dencrypt(data)

    with open(encrypted_files[c], 'wb') as f:
        f.write(dencrypted)

    c += 1