import sys
import os
import xxhash

if len(sys.argv) != 3:
    print("Usage: python hash_app.py <num_buckets> <max_chars_per_file>")
    sys.exit(1)

num_buckets = int(sys.argv[1])
max_chars = int(sys.argv[2])

def compute_bucket_number(data):
    return xxhash.xxh32(data).intdigest() % num_buckets + 1

def check_file_length(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.read())

def find_storage_file(base):
    file_path = base
    overflow_id = 1

    while True:
        current_size = check_file_length(file_path)
        if current_size < max_chars:
            return file_path
        
        next_overflow = f"bucket{base.replace('.txt', '')}_extra{overflow_id}.txt"
        if not os.path.exists(next_overflow):
            return next_overflow

        file_path = next_overflow
        overflow_id += 1

while True:
    try:
        user_input = input("Type your string (or Ctrl+C to quit): ").strip()
        if user_input == "":
            continue

        bucket = compute_bucket_number(user_input)
        bucket_file = f"{bucket}.txt"
        target_file = find_storage_file(bucket_file)

        with open(target_file, 'a', encoding='utf-8') as file:
            file.write(user_input + "\n")

        print(f"✅ Saved: '{user_input}' in file → {target_file}")

    except KeyboardInterrupt:
        print("\n👋 Exiting program. Bye!")
        break
