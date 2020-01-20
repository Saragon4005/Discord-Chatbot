import Main


class message():  # Simulates a message as seen by the on_message fuction
    type = 0
    tts = False
    timestamp = '2020-01-09T01:20:10.887000+00:00'
    pinned = False
    nonce = 664639515201110016
    mentions = []
    mention_roles = []
    mention_everyone = False

    class member():
        roles = [660986670883274803]
        premium_since = None
        nick = None
        mute = False
        joined_at = "2019-12-29T22:57:55.267000+00:00"
        hoisted_role = 660986670883274803
        deaf = False
    id = 664639523833249802
    flags = 0
    embeds = []
    edited_timestamp = None
    content = "messeage"
    channel_id = 660979844179427371

    class author():
        username = "[HU/EN] Saragon"
        id = 212686680052727814
        discriminator = 2988
        avatar = "2175ab2713aa37ee3dfcb4fac5a5586f"
    attachments = []
    guild_id = 660979844179427368


# A function which makes creating test messages with custom content easy
def custom_message(custom):
    message.content = custom
    return message


'''
{"type": 0, "tts": False,
 "timestamp": "2020-01-09T01:20:10.887000+00:00",
 "pinned": False, "nonce": "664639515201110016", "mentions": [],
 "mention_roles": [], "mention_everyone": False, "member":
 {"roles": ["660986670883274803"], "premium_since": None,
  "nick": None, "mute": False,
  "joined_at": "2019-12-29T22:57:55.267000+00:00",
  "hoisted_role": "660986670883274803", "deaf": False},
 "id": "664639523833249802", "flags": 0, "embeds": [],
 "edited_timestamp": None, "content": message,
 "channel_id": "660979844179427371",
 "author": {"username": "[HU/EN] Saragon",
        "id": "212686680052727814", "discriminator": "2988"
        "avatar": "2175ab2713aa37ee3dfcb4fac5a5586f"},
"attachments": [], "guild_id": "660979844179427368"}
'''


async def test_moirail():
    Main.Moirail = {}
    await Main.on_message(custom_message("<>"))
    assert Main.Moirail == {'[HU/EN] Saragon': 1}
