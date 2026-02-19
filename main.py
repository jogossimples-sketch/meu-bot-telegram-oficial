from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import time

# Pega o token dos segredos do GitHub
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Base de dados de BINs
BIN_DATABASE = {
    "422061": {"scheme": "VISA", "tipo": "DEBIT", "marca": "VISA ELECTRON", "banco": "Caixa Econômica Federal"},
    "406669": {"scheme": "VISA", "tipo": "CREDIT", "marca": "VISA CLASSIC", "banco": "Banco do Brasil"},
    "516215": {"scheme": "MASTERCARD", "tipo": "CREDIT", "marca": "MASTERCARD STANDARD", "banco": "Bradesco"}
}

# Controla o tempo das últimas consultas por usuário
USER_LAST_QUERY = {}
# Intervalo mínimo entre consultas (em segundos) - ajuste conforme precisar
MIN_INTERVAL = 5  # 5 segundos entre cada consulta por usuário
# Limite de consultas por usuário por minuto
MAX_QUERIES_PER_MINUTE = 10

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🤖 BOT CHECK BINS ATIVO!\n'
                              'Use /bin NUMERO_DO_BIN para consultar\n'
                              'Exemplo: /bin 422061\n'
                              '⚠️ Há intervalo de 5s entre consultas para evitar bloqueios!')

def check_bin(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # Verifica se o usuário enviou o BIN
    if not context.args:
        update.message.reply_text('⚠️ Digite o número do BIN após o comando!\nExemplo: /bin 422061')
        return
    
    bin_num = context.args[0]
    current_time = time.time()

    # Verifica o histórico de consultas do usuário
    if user_id in USER_LAST_QUERY:
        last_time, count = USER_LAST_QUERY[user_id]
        
        # Verifica se ultrapassou o limite por minuto
        if count >= MAX_QUERIES_PER_MINUTE:
            # Verifica se já passou 1 minuto para resetar o contador
            if current_time - last_time < 60:
                update.message.reply_text('⏳ Você ultrapassou o limite de 10 consultas por minuto!\nTente novamente em alguns segundos.')
                return
            else:
                # Reseta o contador após 1 minuto
                USER_LAST_QUERY[user_id] = (current_time, 1)
        else:
            # Verifica o intervalo mínimo entre consultas
            if current_time - last_time < MIN_INTERVAL:
                remaining = round(MIN_INTERVAL - (current_time - last_time))
                update.message.reply_text(f'⏳ Aguarde {remaining}s antes de fazer uma nova consulta!\nIsso evita bloqueios.')
                return
            else:
                # Atualiza o tempo e aumenta o contador
                USER_LAST_QUERY[user_id] = (current_time, count + 1)
    else:
        # Primeira consulta do usuário
        USER_LAST_QUERY[user_id] = (current_time, 1)

    # Mensagem de verificação com pequeno delay
    update.message.reply_text(f'🔍 Verificando BIN {bin_num}...')
    time.sleep(1)  # Delay de 1 segundo antes de responder

    # Procura o BIN
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

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bin", check_bin))
    
    updater.start_polling(timeout=10, read_latency=2)  # Ajusta a taxa de requisições ao Telegram
    updater.idle()

if __name__ == '__main__':
    main()
