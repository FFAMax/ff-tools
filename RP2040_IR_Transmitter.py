import time
import board
import digitalio
import pulseio
import adafruit_irremote

# 1. Словарь ваших отсниффанных команд (Протокол NEC)
ir_commands = {
    "ON":     [0x00, 0xFF, 0xA2, 0x5D],
    "OFF":    [0x00, 0xFF, 0xE2, 0x1D],
    "MODE_1": [0x00, 0xFF, 0xE0, 0x1F],
    "MODE_2": [0x00, 0xFF, 0xA8, 0x57],
    "MODE_3": [0x00, 0xFF, 0x90, 0x6F],
}

# 2. Подаем постоянное питание +3.3В на GPIO16
ir_power = digitalio.DigitalInOut(board.GP16)
ir_power.direction = digitalio.Direction.OUTPUT
ir_power.value = True  

# Даем питанию стабилизироваться перед отправкой
time.sleep(0.1)

# 3. Инициализируем PulseOut напрямую на пине GP17 с частотой 38 кГц
ir_pulseout = pulseio.PulseOut(board.GP17, frequency=38000)

# 4. Инициализируем стандартный энкодер NEC (тайминги в микросекундах)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500],   # Стартовый импульс NEC (9мс High, 4.5мс Low)
    one=[560, 1690],       # Логическая «1» (пачка 560мкс + пауза 1690мкс)
    zero=[560, 560],       # Логический «0» (пачка 560мкс + пауза 560мкс)
    trail=560              # Финальный закрывающий импульс
)

print("Эмулятор ИК-передатчика запущен успешно!")
print("Питание: GP16 (+3.3V) | Сигнал: GP17 (38kHz модуляция через PulseOut)")

# Демонстрационный цикл проверки команд
while True:
    print("Отправка: ON")
    encoder.transmit(ir_pulseout, ir_commands["ON"])
    time.sleep(4)
    
    print("Отправка: MODE_1")
    encoder.transmit(ir_pulseout, ir_commands["MODE_1"])
    time.sleep(4)
    
    print("Отправка: MODE_2")
    encoder.transmit(ir_pulseout, ir_commands["MODE_2"])
    time.sleep(4)
    
    print("Отправка: MODE_3")
    encoder.transmit(ir_pulseout, ir_commands["MODE_3"])
    time.sleep(4)
    
    print("Отправка: OFF")
    encoder.transmit(ir_pulseout, ir_commands["OFF"])
    time.sleep(6)
