# draft

import psutil
import threading
import time
import os

memory_usage_exceeded = False
max_memory_usage = 80  # %
memory_check_interval = 0.2  # 200 ms


filenames = [
    "challenge.txt", "hashes_2015.txt", "hashes_2018.txt", "num8_1.txt", "num8_4.txt", "num8_7.txt", "old_gold.txt",
    "ud_pc.txt", "wp_de.txt", "wp_ru.txt", "wpskey2.txt", "wpskey5.txt", "wpskey8.txt", "cow.txt", "hashes_2016.txt",
    "insidepro.txt", "num8_2.txt", "num8_5.txt", "num8_8.txt", "openwall.txt", "used.txt", "wp_es.txt", "wpskey0.txt",
    "wpskey3.txt", "wpskey6.txt", "wpskey9.txt", "cracked.txt", "hashes_2017.txt", "num8_0.txt", "num8_3.txt",
    "num8_6.txt", "num8_9.txt", "os.txt", "wpchit_bg.txt", "wp_fr.txt", "wpskey1.txt", "wpskey4.txt", "wpskey7.txt",
    "wp.txt"
]

def can_fit_in_memory(file_path, max_memory_usage):
    file_size = os.path.getsize(file_path)
    total_memory = psutil.virtual_memory().total
    available_memory = total_memory * (1 - (max_memory_usage / 100))
    return file_size <= available_memory

def memory_monitor(max_memory_usage, check_interval):
    global memory_usage_exceeded
    while True:
        memory_usage = psutil.virtual_memory().percent
        memory_usage_exceeded = memory_usage >= max_memory_usage
        time.sleep(check_interval)

def load_lines_in_chunks(file):
    global memory_usage_exceeded
    lines = set()
    for line in file:
        lines.add(line.strip())
        if memory_usage_exceeded:
            memory_usage_exceeded = False
            yield lines
            lines = set()
    yield lines

file_b_path = 'b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt'
if not can_fit_in_memory(file_b_path, max_memory_usage):
    raise MemoryError("File b cannot fit in memory.")

with open(file_b_path, 'r', errors='surrogateescape') as file_b:
    lines_b = set(line.strip() for line in file_b)

# Start the memory monitoring thread
monitoring_thread = threading.Thread(target=memory_monitor, args=(max_memory_usage, memory_check_interval), daemon=True)
monitoring_thread.start()

for filename in filenames:
    print(f'Processing {filename}')
    with open(f'a/{filename}', 'r', errors='surrogateescape') as file_a:
        for lines_a in load_lines_in_chunks(file_a):
            lines_b = lines_b - lines_a

with open('file_c.txt', 'w', errors='surrogateescape') as file_c:
    for line_b in lines_b:
        file_c.write(line_b + '\n')
'''
real    6m42.203s
user    5m50.235s
sys     0m52.479s
ffamax@ffamax-MS-7A12:~/3wifi$ wc -l file_c.txt b/*txt && ls -alh file_c.txt b/*txt
  7788496 file_c.txt
 10354402 b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt
-rw------- 1 ffamax ffamax 115M Apr 30 00:12 b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt
-rw-rw-r-- 1 ffamax ffamax  92M Apr 30 09:06 file_c.txt
'''
