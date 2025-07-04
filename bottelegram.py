import os
import yt_dlp
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7601201978:AAFgaPst4KLZaQonFVt1j2KhHDzjnXyVOkA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Envie um link de vídeo do YouTube, TikTok, Instagram ou Facebook, e eu farei o download para você."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()

    if any(domain in message for domain in [
        "youtube.com", "youtu.be", "tiktok.com", "instagram.com", "facebook.com"
    ]):
        await update.message.reply_text("🔽 Link de vídeo detectado. Baixando, aguarde...")

        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'noplaylist': True,
            'retries': 3,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as f:
                await update.message.reply_video(video=f)

            os.remove(filename)

        except Exception as e:
            print("Erro:", e)
            await update.message.reply_text(
                f"❌ Erro ao baixar o vídeo:\n`{e}`",
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text("❌ Envie um link válido de vídeo.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot rodando... Pressione Ctrl+C para parar.")
    await app.run_polling()

if __name__ == "__main__":
    # Apply nest_asyncio to allow running asyncio within an existing event loop
    nest_asyncio.apply()
    # Get the current event loop and run the main coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
