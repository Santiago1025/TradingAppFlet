#!/usr/bin/env python3
import asyncio
import logging
import math
import os
from metaapi_cloud_sdk import MetaApi
from prettytable import PrettyTable
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackContext


API_KEY = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJlMTAwYTQyNjdjNzM4NjRlMWE3OWMxNDNiZTVmMjdkMyIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX1dLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZTEwMGE0MjY3YzczODY0ZTFhNzljMTQzYmU1ZjI3ZDMiLCJpYXQiOjE3MDEzMjY0MjR9.GrNjT3nuTnS33nx4X8jwQ72Lt5k502fKxXNlXraOcQLcfrFrPCMlOc6BhjBvMhPVGvD7NVpDI2yUMOw8VtGCeUMmUaVHPmWmxX5-E4aBKFiPsRHPqD5ngCsFgYULEzucZmHIEik6FaQDmZ1odEIuQyBnmFWAmFYs4d05IhXLz-Lj1awnIsoTcVHxLVm_41q_b-P5ikT08COjbczwl9_3TN2HC09c8_lcY1iaZQbQ15GoO_SCm1xUDdq_E8mnHOuLBYoWO_cZid3JQCB6eKNKjXDNdGm9lvr7k13m4GkN-r8qQn0ER8LFipMRyRYxobl_atc5DP0jyJWHfVJST1Y2xd_bpc1jIGAhc7s6mUIMtgzUVyoru9BEo0FFVfiCo6di3vQQnfKGhOd3IDAnOxYMICOvdFj8zXI6ZcUq0etEBOPp7zAxRGS1nulYjt96TyXnYZ_w_QyAF7MYpOYngxzYgAV7-VZHEdvcC9JU6oElwCVPLb-sFKmGsdsZieIsuToTS0eNlwzqagVJNZ6ytZQaN9bzGVk7W4tQjHfExc83XB4Aqkw3D69-jrCcyw5upQwOzbUI26OxIjGe6uo_mHmmC84KK0e4YpXcxeeWsCrR8RTx0kIudp9M8LmtHJZS_Zkg-eOn0nXNdHRKRICjO1a4PFtyDQfMggvVBgGWuW6u7rw'

ACCOUNT_ID = '5dc8e4fd-b397-48c2-9250-9b8cba28d193'

# Telegram Credentials
TOKEN = os.environ.get("TOKEN")
TELEGRAM_USER = os.environ.get("TELEGRAM_USER")

# Heroku Credentials
APP_URL = os.environ.get("APP_URL")

# Port number for Telegram bot web hook
PORT = int(os.environ.get('PORT', '8443'))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def equidad(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text("Hora de Mórfosis")
    """api = MetaApi(API_KEY)
    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        initial_state = account.state
        deployed_states = ['DEPLOYING', 'DEPLOYED']

        if initial_state not in deployed_states:
            # Desplegar la cuenta si aún no está desplegada
            logger.info('Deploying account')
            await account.deploy()

            # Esperar hasta que la cuenta se haya desplegado y conectado al broker
            logger.info('Waiting for the account to be deployed and connected to broker...')
            await account.wait_connected()

        # Conectar a la API de MetaApi
        connection = account.get_rpc_connection()
        await connection.connect()

        while True:
            # Esperar hasta que el estado del terminal se haya sincronizado con el estado local
            logger.info('Esperando que SDK se sincronice con el estado del terminal ...')
            await connection.wait_synchronized()

            # Obtener información de la cuenta desde el servidor de MetaTrader
            account_information = await connection.get_account_information()
            update.effective_message.reply_text("Successfully connected to MetaTrader!🤔")
            equidad = account_information['equity']

            update.effective_message.reply_text(f'La equidad es: {equidad}')
            
            # Esperar un minuto antes de realizar la próxima actualización
            await asyncio.sleep(60)
    
    except Exception as error:
        logger.error(f'Error: {error}')
        update.effective_message.reply_text(f"There was an issue with the connection 😕\n\nError Message:\n{error}")"""
    return
        
# Command Handlers
def welcome(update: Update, context: CallbackContext) -> None:
    """Sends welcome message to user.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    welcome_message = "Sea Bienvenido"
    
    # sends messages to user
    update.effective_message.reply_text(welcome_message)

    return

def error(update: Update, context: CallbackContext) -> None:
    """Logs Errors caused by updates.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    logger.warning('Update "%s" caused error "%s"', update, context.error)

    return

def main() -> None:
    """Runs the Telegram bot."""

    updater = Updater(TOKEN, use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # message handler
    dp.add_handler(CommandHandler("start", welcome))
    
    dp.add_handler(CommandHandler("equidad", equidad))

    """conv_handler = ConversationHandler(
        entry_points=[CommandHandler("trade", Trade_Command), CommandHandler("calculate", Calculation_Command)],
        states={
            TRADE: [MessageHandler(Filters.text & ~Filters.command, PlaceTrade)],
            CALCULATE: [MessageHandler(Filters.text & ~Filters.command, CalculateTrade)],
            DECISION: [CommandHandler("yes", PlaceTrade), CommandHandler("no", cancel)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # conversation handler for entering trade or calculating trade information
    dp.add_handler(conv_handler)"""

    # message handler for all messages that are not included in conversation handler
    #dp.add_handler(MessageHandler(Filters.text, PlaceTrade))

    # log all errors
    dp.add_error_handler(error)
    
    # listens for incoming updates from Telegram
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_URL + TOKEN)
    updater.idle()

    return


if __name__ == '__main__':
    main()
