from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Pega o token dos segredos do GitHub
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Base de dados de BINs (você pode adicionar mais conforme precisar)
BIN_DATABASE = {
    "422061": {
        "scheme": "VISA",
        "tipo": "DEBIT",
        "marca": "VISA ELECTRON",
        "banco": "Caixa Econômica Federal"
    },
    "406669": {
        "scheme": "VISA",
        "tipo": "CREDIT",
        "marca": "VISA CLASSIC",
        "banco": "Banco do Brasil"
    },
    "516215": {
        "scheme": "MASTERCARD",
        "tipo": "CREDIT",
        "marca": "MASTERCARD STANDARD",
        "banco": "Bradesco"
    }
}

# Comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🤖 BOT CHECK BINS ATIVO!\n'
                              'Use /bin NUMERO_DO_BIN para consultar\n'
                              'Exemplo: /bin 422061')

# Comando /bin para consultar
def check_bin(update: Update, context: CallbackContext) -> None:
    # Verifica se o usuário enviou o número do BIN
    if not context.args:
        update.message.reply_text('⚠️ Digite o número do BIN após o comando!\n'
                                  'Exemplo: /bin 422061')
        return
    
    bin_num = context.args[0]
    update.message.reply_text(f'🔍 Verificando BIN {bin_num}...')
    
    # Procura o BIN na base de dados
    if bin_num in BIN_DATABASE:
        dados = BIN_DATABASE[bin_num]
        resposta = (f'\n✅ BIN ENCONTRADO NA LISTA!\n\n'
                    f'📊 BIN: {bin_num}\n'
                    f'💳 Scheme: {dados["scheme"]}\n'
                    f'🗃️ Tipo: {dados["tipo"]}\n'
                    f'🏷️ Marca: {dados["marca"]}\n'
                    f'🏦 Banco: {dados["banco"]}')
    else:
        resposta = f'\n❌ BIN {bin_num} NÃO ENCONTRADO NA LISTA!'
    
    update.message.reply_text(resposta)

# Função principal
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bin", check_bin))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
