# Estructura de archivos y código completo para descarga

# mini-proyecto/
# ├─ web/
# │   ├─ index.html
# │   ├─ style.css
# │   └─ script.js
# └─ bot/
#     ├─ app.py
#     └─ requirements.txt

# --- web/index.html ---
index_html = """<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Recordatorio Online</title>
    <link rel=\"stylesheet\" href=\"style.css\">
</head>
<body>
<div class=\"container\">
    <h1>Recordatorio Online</h1>
    <form id=\"reminderForm\">
        <label for=\"chat_id\">Tu Chat ID de Telegram:</label>
        <input type=\"text\" id=\"chat_id\" required>

        <label for=\"text\">Texto del recordatorio:</label>
        <input type=\"text\" id=\"text\" required>

        <label for=\"datetime\">Fecha y hora:</label>
        <input type=\"datetime-local\" id=\"datetime\" required>

        <button type=\"submit\">Enviar</button>
    </form>
    <p id=\"status\"></p>
</div>
<script src=\"script.js\"></script>
</body>
</html>"""

# --- web/style.css ---
style_css = """body {
    font-family: Arial, sans-serif;
    background: #1e1e2f;
    color: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}
.container {
    background: #2c2c3c;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    width: 90%;
    max-width: 400px;
}
h1 { text-align: center; margin-bottom: 20px; }
form label { display: block; margin-top: 10px; }
form input { width: 100%; padding: 8px; margin-top: 5px; border-radius: 6px; border: none; }
button {
    margin-top: 15px; padding: 10px; width: 100%; border: none;
    border-radius: 6px; background: #4caf50; color: white; font-weight: bold; cursor: pointer;
}
button:hover { background: #45a049; }
#status { margin-top: 15px; text-align: center; }"""

# --- web/script.js ---
script_js = """document.getElementById('reminderForm').addEventListener('submit', async function(e){
    e.preventDefault();

    const chat_id = document.getElementById('chat_id').value;
    const text = document.getElementById('text').value;
    const datetime = document.getElementById('datetime').value;

    if(!chat_id || !text || !datetime){
        alert('Completa todos los campos');
        return;
    }

    try {
        const response = await fetch('https://TU_BACKEND_URL/reminder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id, text, datetime })
        });
        const result = await response.json();
        document.getElementById('status').innerText = result.message;
    } catch (error) {
        console.error(error);
        document.getElementById('status').innerText = 'Error al enviar recordatorio ❌';
    }

    document.getElementById('text').value = '';
    document.getElementById('datetime').value = '';
});"""

# --- bot/app.py ---
app_py = """from flask import Flask, request, jsonify
from telegram import Bot
import threading
import time
from datetime import datetime
import os

TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)
app = Flask(__name__)

reminders = {}  # {chat_id: [ {text, datetime} ]}

def reminder_checker():
    while True:
        now = datetime.now()
        for chat_id in list(reminders.keys()):
            to_send = []
            for r in reminders[chat_id]:
                r_time = datetime.fromisoformat(r['datetime'])
                if r_time <= now:
                    bot.send_message(chat_id=chat_id, text=f'⏰ Recordatorio: {r["text"]}')
                    to_send.append(r)
            for r in to_send:
                reminders[chat_id].remove(r)
            if not reminders[chat_id]:
                del reminders[chat_id]
        time.sleep(30)

@app.route('/reminder', methods=['POST'])
def add_reminder():
    data = request.get_json()
    chat_id = data.get('chat_id')
    text = data.get('text')
    datetime_str = data.get('datetime')

    if not chat_id or not text or not datetime_str:
        return jsonify({'message': 'Datos incompletos'}), 400

    if chat_id not in reminders:
        reminders[chat_id] = []
    reminders[chat_id].append({'text': text, 'datetime': datetime_str})
    return jsonify({'message': 'Recordatorio enviado al bot ✅'}), 200

if __name__ == '__main__':
    thread = threading.Thread(target=reminder_checker, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)"""

# --- bot/requirements.txt ---
requirements_txt = """Flask
python-telegram-bot==20.3"""

# Guardar archivos en /mnt/data para descargar
import os
os.makedirs('/mnt/data/mini-proyecto/web', exist_ok=True)
os.makedirs('/mnt/data/mini-proyecto/bot', exist_ok=True)

with open('/mnt/data/mini-proyecto/web/index.html', 'w') as f:
    f.write(index_html)
with open('/mnt/data/mini-proyecto/web/style.css', 'w') as f:
    f.write(style_css)
with open('/mnt/data/mini-proyecto/web/script.js', 'w') as f:
    f.write(script_js)
with open('/mnt/data/mini-proyecto/bot/app.py', 'w') as f:
    f.write(app_py)
with open('/mnt/data/mini-proyecto/bot/requirements.txt', 'w') as f:
    f.write(requirements_txt)

'/mnt/data/mini-proyecto'
