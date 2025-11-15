def read_file(filename):
    result = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('=', 1)
                if len(parts) == 2:
                    hash_val, text = parts
                    result[hash_val] = text
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    return result

def main():
    old_data = read_file('old.txt')
    new_data = read_file('new.txt')
    trans_data = read_file('trans.txt')
    
    hash_changes = []
    text_changes = []
    new_entries = []
    
    with open('new_trans.txt', 'w', encoding='utf-8') as fixed_file:
        for hash_val, new_text in new_data.items():
            if hash_val in trans_data:
                trans_text = trans_data[hash_val]
                if trans_text != new_text:
                    fixed_file.write(f"{hash_val}={trans_text}\n")
                    if hash_val in old_data:
                        old_text = old_data[hash_val]
                        if old_text != trans_text:
                            text_changes.append((hash_val, old_text, trans_text))
                else:
                    fixed_file.write(f"{hash_val}={new_text}\n")
            else:
                fixed_file.write(f"ЖЖЖ{hash_val}={new_text}\n")
                new_entries.append((hash_val, new_text))
    
    for hash_val, text in new_data.items():
        if hash_val in old_data and old_data[hash_val] != text:
            for old_hash, old_text in old_data.items():
                if old_text == text and old_hash != hash_val:
                    hash_changes.append((old_hash, hash_val, text))
                    break
    
    hash_changes.sort()
    text_changes.sort()
    new_entries.sort()
    
    with open('logs.txt', 'w', encoding='utf-8') as log_file:
        for old_hash, new_hash, text in hash_changes:
            log_file.write(f"[ХЭШ] {old_hash}->{new_hash} {text}\n")
        
        for hash_val, old_text, new_text in text_changes:
            log_file.write(f"[ТЕКСТ] {old_text}->{new_text} [{hash_val}]\n")
        
        for hash_val, text in new_entries:
            log_file.write(f"[НОВОЕ] {text} [{hash_val}]\n")

if __name__ == "__main__":
    main()