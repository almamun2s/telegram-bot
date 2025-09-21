from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os
TOKEN = os.environ.get("TOKEN")

print("TOKEN =", os.environ.get("TOKEN"))  # just for debug

if TOKEN is None:
    TOKEN = "8486194098:AAExFECDINRSzAkFVC8dbdw6dCmD4H4KVhY";

# Store ongoing games
games = {}  # key: user_id, value: {'number': 42, 'attempts': 0}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your simple chatbot 🤖. Type anything!\nYou can also type /game to play 'Guess the Number'!")

# GitHub command
async def show_github_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is my github link: https://github.com/almamun2s")

# Start the game
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    number = random.randint(1, 100)
    games[user_id] = {'number': number, 'attempts': 0}
    await update.message.reply_text("🎯 I have chosen a number between 1 and 100. Try to guess it!")

# Handle text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    user_id = user.id
    
    # Get user name
    if user.first_name or user.last_name:
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    elif user.username:
        name = f"@{user.username}"
    else:
        name = "there"

    # Check if the user is in a game
    if user_id in games:
        if user_message.isdigit():
            guess = int(user_message)
            games[user_id]['attempts'] += 1
            secret = games[user_id]['number']

            if guess < secret:
                await update.message.reply_text("⬆️ Too low! Try again.")
            elif guess > secret:
                await update.message.reply_text("⬇️ Too high! Try again.")
            else:
                attempts = games[user_id]['attempts']
                del games[user_id]
                await update.message.reply_text(f"🎉 Correct, {name}! You guessed it in {attempts} tries!\nType /game to play again.")
        else:
            await update.message.reply_text("Please send a number between 1 and 100.")
        return

    # Normal chatbot responses
    if user_message.lower() in ["hello", "hi"]:
        await update.message.reply_text(f"Hi, {name}! How can I assist you today? 😊")
    elif user_message.lower() == "bye":
        await update.message.reply_text("Goodbye! Have a great day! 👋")
    elif user_message.lower() == "how are you?":
        await update.message.reply_text("I'm just a bot, but thanks for asking! How can I help you? 🤖")
    else:
        await update.message.reply_text("I'm sorry, I didn't understand that. Can you please rephrase? 🤔")

def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("github", show_github_link))
    app.add_handler(CommandHandler("game", start_game))

    # Reply to all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
