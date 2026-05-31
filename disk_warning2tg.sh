#!/bin/bash

#0 * * * * THRESHOLD=90 /bin/bash /home/user/test/disk_warning.sh 2>&1 | /usr/bin/logger -t disk_warning
#journalctl -t disk_warning

# Threshold percentage for disk space warning
THRESHOLD="${THRESHOLD:-90}"
BOT_TOKEN="${BOT_TOKEN:-1234:abrakadabra}"
CHAT_ID="${CHAT_ID:--12345}"


# Получаем список всех смонтированных физических разделов
# Исключаем tmpfs, cdrom, loop-устройства и заголовки таблицы
df -x tmpfs -x devtmpfs -x overlay -x squashfs -ll | tail -n +2 | while read -r line; do

    # Извлекаем точку монтирования и процент использования
    MOUNT=$(echo "$line" | awk '{print $6}')
    USED_PERCENT=$(echo "$line" | awk '{print $5}' | sed 's/%//')

    # Проверяем, что получили число
    if [[ "$USED_PERCENT" =~ ^[0-9]+$ ]]; then

        # Если занято больше или равно 90% (свободно меньше 10%)
        if [ "$USED_PERCENT" -ge "$THRESHOLD" ]; then
            FREE_PERCENT=$((100 - USED_PERCENT))
            TEXT="⚠️ ${HOSTNAME} ${MOUNT} ${FREE_PERCENT}%"

            # Отправка в Telegram
            curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
                 -H "Content-Type: application/json" \
                 -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"${TEXT}\"}"

            # Лог в консоль
            echo "Предупреждение отправлено для ${MOUNT}"
        fi
    fi
done

exit 0
