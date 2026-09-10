import os
import telebot
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  welcome_text = (
      "أهلاً بك! أنا بوت متصل بالذكاء الاصطناعي، يمكنك كتابة أي سؤال وسأجيبك"
      " فوراً."
  )
  bot.reply_to(message, welcome_text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    bot.send_chat_action(message.chat.id, "typing")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=message.text,
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    print(f"حدث خطأ: {e}")
    bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة طلبك.")


if __name__ == "__main__":
  print("...البوت يعمل الآن")
  bot.infinity_polling()
