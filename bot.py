import asyncio
import os
import time
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

# Tu configuración personal
api_id = 23810582
api_hash = "079750c767b2d4154acfff724a1a6b6e"
session_name = "consulta_dnis"
bot_username = "KingDataOFC_bot"  # o puedes usar el ID: 7645844153

# Cargar lista de DNIs desde el archivo
with open("dnis_extraidos.txt", "r") as f:
    dnis = [line.strip() for line in f if line.strip()]

# Crear cliente de Telethon
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()
    print("✅ Sesión iniciada correctamente.")

    for dni in dnis:
        print(f"🔎 Consultando DNI {dni}...")
        await client.send_message(bot_username, f"/dni {dni}")

        # Esperar por las 2 respuestas del bot (normalmente envía texto + imagen)
        fotos_recibidas = 0

        @client.on(events.NewMessage(from_users=7645844153))  # ID del bot
        async def handler(event):
            nonlocal fotos_recibidas
            if isinstance(event.media, MessageMediaPhoto):
                fotos_recibidas += 1
                if fotos_recibidas == 2:  # Solo guardamos la segunda imagen
                    path = f"{dni}.jpg"
                    await event.download_media(file=path)
                    print(f"🖼️ Imagen guardada como {path}")
                    await client.remove_event_handler(handler)

        # Esperar máximo 15 segundos por respuestas
        await asyncio.sleep(15)

        print(f"⏳ Esperando 5 segundos para el siguiente DNI...")
        await asyncio.sleep(5)

    print("✅ Todas las consultas finalizadas.")

# Ejecutar cliente
with client:
    client.loop.run_until_complete(main())
