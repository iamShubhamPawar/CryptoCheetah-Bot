import requests, config
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
import os

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """
    Handle the /start command and send a welcome message to the user.

    Args:
        update (telegram.Update): The update object containing the message.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object.
    """
  #Welcome message to the user when /start command is used.
  await update.message.reply_text(f"Hi, I'm the @{update.get_bot().username}")
  await update.message.reply_text(
      "*Commands* \n/p coinName \\- prices\n/nft NFTname \\- NFTs prices\n\n[Reach out to developer](https://t.me/Shubham0x0)",
      parse_mode=ParseMode.MARKDOWN_V2)


def numbersAbb(argu):
  """ 
    Abbreviate large numbers.

    Args:
        argu (int): The number to be abbreviated.

    Returns:
        str: The abbreviated number.
    """
  ko = ("{:,}".format(round(argu)))
  l = ko.split(",")
  switcher = {
      1: f"{l[0]}",
      2: f"{l[0]}K",
      3: f"{l[0]}M",
      4: f"{l[0]}B",
      5: f"{l[0]}T",
      6: f"{l[0]}Q",
      7: f"{l[0]}QN"
  }
  return switcher.get(len(l), "Abbreviation Error")


def handle_response(text: str) -> str:
  """
    Handle the user's command and return the response.

    Args:
        text (str): The user's command.

    Returns:
        str: The response message.
    """
  processed = text.lower()


  # Check the latest Crypto Prices for the given coin if /p command is used.
  if processed.startswith("/p"):
    try:
      coin_name = processed.replace("/p", "").strip().split(" ")[0].upper()
      response = requests.get(
          f"https://api.bybit.com/v5/market/tickers?category=inverse&symbol={coin_name}USDT"
      ).json()["result"]["list"][0]
      return f'{response["symbol"]} [Bybit]\n==${response["lastPrice"]}\nH|L: {response["highPrice24h"]}|{response["lowPrice24h"]} \nChange24H: {round(float(response["price24hPcnt"])*100,2)}%\n'
    except:
      return "Invalid Coin Name. Please use /help to get a list of available commands."

  # Check the latest NFT Prices for the given NFT if /nft command is used.
  elif processed.startswith("/nft"):
    try:
      nft_name = processed.replace("/nft", "").strip().split(" ")[0]
      response = requests.get(
          f"https://api-mainnet.magiceden.dev/v2/collections/{nft_name}/stats"
      ).json()
      return (
          f"Name: {response['symbol']}\nFloor: ◎ {int((response['floorPrice']/1000000000))}\nListed: {response['listedCount']}\nAverage24H Price: ◎ {int(response['avgPrice24hr']/1000000000)}\nTotal Volume: ◎ {round(response['volumeAll']/1000000000)}"
      )
    except:
      return "Invalid NFT Name. Please use /help to get a list of available commands."

  return "Invalid Syntax. Please use /help to get a list of available commands."


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """
    Handle incoming messages from the user.

    Args:
        update (telegram.Update): The update object containing the message.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object.

    Returns:
        None
    """
  message_type = update.message.chat.type
  text = update.message.text
  response = handle_response(text)
  await update.message.reply_text(response)


async def errors(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """
    Handle errors that occur during message handling.

    Args:
        update (telegram.Update): The update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object.

    Returns:
        None
    """
  print(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
  print("Starting Bot.....")
  app = Application.builder().token(config.TGKEY).build()
  app.add_handler(CommandHandler("start", start_command))
  app.add_handler(MessageHandler(filters.TEXT, handle_messages))
  app.add_error_handler(errors)
  print("Starting Polling......")
  app.run_polling()
