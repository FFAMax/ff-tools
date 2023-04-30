# draft

import os
import threading
import psutil
from itertools import chain

num_cores = os.cpu_count()
memory_usage_exceeded = False
max_memory_usage = 5  # %
memory_check_interval = 0.1  # 200 ms
file_b_path = 'b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt'


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

def remove_lines_a_from_lines_b_chunk(lines_a, lines_b_chunk):
    return lines_b_chunk - lines_a

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

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

def find_matches(lines_a, lines_b_chunk, matches):
    matches.update(lines_a.intersection(lines_b_chunk))

if not can_fit_in_memory(file_b_path, max_memory_usage):
    raise MemoryError("File b cannot fit in memory.")


def process_file_a(filename, lines_b_chunks):
    with open(f'a/{filename}', 'r', errors='surrogateescape') as file_a:
        for lines_a in load_lines_in_chunks(file_a):
            threads = []
            for chunk in lines_b_chunks:
                t = threading.Thread(target=find_matches, args=(lines_a, chunk, matches_to_remove))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()
with open(file_b_path, 'r', errors='surrogateescape') as file_b:
    lines_b = set(line.strip() for line in file_b)

lines_b_chunks = split_list(list(lines_b), num_cores)
lines_b_chunks = [set(chunk) for chunk in lines_b_chunks]


matches_to_remove = set()


for filename in filenames:
    print(f'Processing {filename}')
    process_file_a(filename, lines_b_chunks)

lines_b_result = set(chain.from_iterable(lines_b_chunks)) - matches_to_remove

with open('file_c.txt', 'w', errors='surrogateescape') as file_c:
    for line_b in lines_b_result:
        file_c.write(line_b + '\n')

'''
real    5m36.867s
user    4m54.319s
sys     0m42.566s
ffamax@ffamax-MS-7A12:~/3wifi$ wc -l file_c.txt b/*txt && ls -alh file_c.txt b/*txt
  7788496 file_c.txt
 10354402 b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt
 18142898 total
-rw------- 1 ffamax ffamax 115M Apr 30 00:12 b/3wifi-dic-2022-12-05.7z.3WiFi_WiFiKey.txt
-rw-rw-r-- 1 ffamax ffamax  92M Apr 30 10:43 file_c.txt
'''
