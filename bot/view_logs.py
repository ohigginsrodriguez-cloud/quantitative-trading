import os
import subprocess

log_file = '/home/pulpo/Documents/quantitative-trading/bot/bot.log'

if os.path.exists(log_file):
    # Ver últimas 50 líneas
    os.system(f'tail -50 {log_file}')
else:
    print("Log no existe aún. Ejecuta el bot primero.")