import asyncio
import time
from playwright.async_api import async_playwright, TimeoutError
from telegram import Bot

TELEGRAM_BOT_TOKEN = "7601201978:AAFgaPst4KLZaQonFVt1j2KhHDzjnXyVOkA"
TELEGRAM_CHAT_ID = "561035841"

async def take_screenshot(url, filename):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle")
            time.sleep(10) # Espera explícita de 10 segundos para carregar o conteúdo dinâmico
            
            # Para revert.finance, vamos tentar esperar por um elemento que indique o carregamento da conta
            await page.wait_for_selector("div.MuiBox-root.css-1r0q04m", timeout=30000) # Exemplo de seletor, pode precisar de ajuste

            await page.screenshot(path=filename, full_page=True)
            print(f"Screenshot de {url} capturado com sucesso.")
        except TimeoutError:
            print(f"Erro de Timeout ao carregar a página {url}. Tentando capturar mesmo assim.")
            await page.screenshot(path=filename, full_page=True)
        except Exception as e:
            print(f"Erro ao capturar screenshot de {url}: {e}")
        finally:
            await browser.close()

async def send_telegram_photo(photo_path, caption=None):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        with open(photo_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo_file, caption=caption)
        print(f"Foto {photo_path} enviada para o Telegram com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar foto {photo_path} para o Telegram: {e}")

async def main():
    urls = [
        ("https://revert.finance/#/account/0x1c372443e4fC444F812c9e05C522b8E7521C4C00", "revert_finance.png")
    ]

    for url, filename in urls:
        await take_screenshot(url, filename)
        await send_telegram_photo(filename, caption=f"Screenshot de {url}")
    print("Processo de captura e envio de screenshots concluído.")

if __name__ == "__main__":
    asyncio.run(main())
