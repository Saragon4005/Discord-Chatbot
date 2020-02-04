import Main

try:
    Main.bot.run(Main.TOKEN)

except Exception:
    Main.save()
    raise
