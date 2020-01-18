import Main

try:
    Main.client.run(Main.TOKEN)
    Main.bot.run(Main.TOKEN)

except Exception:
    Main.save()
    raise
