from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Pega o token dos segredos do GitHub (não está no código!)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Comando /start
def start(update: Update, context: CallbackContext) -> None:
    usuario = update.effective_user.first_name
    update.message.reply_text(f'Olá {usuario}! 🤖 Sou o seu bot!\n'
                              'Comandos: /start, /ajuda, /info')

# Comando /ajuda
def ajuda(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Envie qualquer mensagem que eu a repito!\nUse /info para saber mais.')

# Comando /info
def info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot criado no GitHub com segurança! ✅')

# Repete mensagens
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Você disse: {update.message.text}')

# Função principal
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ajuda", ajuda))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
