import Main
import discord.ext.test as dpytest
import pytest

"""
TODO https://pypi.org/project/dpytest/ this could possibly be used
Its A bit messy, but works better than whatever I have right now
"""

bot = Main.bot
dpytest.configure(bot)


class User():
    def __init__(
            self, username, discrim, avatar, id_num=-1, flags=0, **kwargs):
        dict = dpytest.factories.make_user_dict(
            username, discrim, avatar, id_num, flags, **kwargs)
        self.id = dict['id']
        self.name = dict['username']
        self.discriminator = dict['discriminator']
        self.avatar = dict['avatar']


testUser = User(
    "Test", 1111, "2175ab2713aa37ee3dfcb4fac5a5586f", id_num=1234)


@pytest.mark.asyncio
async def test_moirail():
    try:
        MoirailV = (Main.db.QueryMoirail(1234))[0]
    except TypeError:
        MoirailV = 0
    await dpytest.message("<>", member=testUser)
    assert (Main.db.QueryMoirail(1234))[0] == MoirailV + 1
