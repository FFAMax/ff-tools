import time
import board
import digitalio
import pulseio
import adafruit_irremote

# 1. Настраиваем землю (GND) на GPIO19
ir_gnd = digitalio.DigitalInOut(board.GP19)
ir_gnd.direction = digitalio.Direction.OUTPUT
ir_gnd.value = False  # Жестко притягиваем к 0В

# 2. Настраиваем питание (VCC) на GPIO18
ir_power = digitalio.DigitalInOut(board.GP18)
ir_power.direction = digitalio.Direction.OUTPUT
ir_power.value = True  # Подаем +3.3В

# Даем датчику 100 мс на стабилизацию внутренних цепей
time.sleep(0.1)

# 3. Настраиваем вход для ИК-сигнала на GPIO20
# За счет pull-up=True включаем внутреннюю подтяжку RP2040 к 3.3В
pulsein = pulseio.PulseIn(board.GP20, maxlen=120, idle_state=True)

# 4. Инициализируем декодер
decoder = adafruit_irremote.NonblockingGenericDecode(pulsein)

print("Линия питания готова (GP18=+3.3V, GP19=GND).")
print("Сниффер на GP20 запущен. Нажмите кнопку на пульте...")

while True:
    for message in decoder.read():
        if isinstance(message, adafruit_irremote.IRMessage):
            print("Успешно декодировано!")
            print("Байты команды (HEX):", [hex(b) for b in message.code])
            
        elif isinstance(message, adafruit_irremote.NECRepeatIRMessage):
            print("Повтор кнопки (NEC Repeat)")
            
        elif isinstance(message, adafruit_irremote.UnparseableIRMessage):
            print("Сигнал пойман, но протокол не NEC. Причина:", message.reason)
            print("Сырые импульсы для ручного разбора:")
            print(list(message.pulses))
            
        print("-" * 30)
