def ensure_guild(db_cursor, guild_data):
    guild_exists = list(db_cursor.execute('SELECT 1 FROM guild WHERE id = ?', [guild_data['id']]))
    guild_exists = len(guild_exists) == 1
    guild_row = (
        guild_data['name'],
        guild_data['id']
    )
    if not guild_exists:
        db_cursor.execute("INSERT INTO guild(name,id) VALUES(?,?)", guild_row)
    else:
        db_cursor.execute("UPDATE guild SET name = ? WHERE id = ?", guild_row)

def ensure_channel(db_cursor, channel_data):
    channel_exists = list(db_cursor.execute('SELECT 1 FROM channel WHERE id = ?', [channel_data['id']]))
    channel_exists = len(channel_exists) == 1
    channel_row = (
        channel_data['name'],
        channel_data['guild_id'],
        channel_data['id']
    )
    if not channel_exists:
        db_cursor.execute("INSERT INTO channel(name,guild_id,id) VALUES(?,?,?)", channel_row)
    else:
        db_cursor.execute("UPDATE channel SET name = ?, guild_id = ? WHERE id = ?", channel_row)

def ensure_user(db_cursor, user_data):
    user_exists = list(db_cursor.execute('SELECT 1 FROM user WHERE id = ?', [user_data['id']]))
    user_exists = len(user_exists) == 1
    user_row = (
        user_data['username'],
        user_data['discriminator'],
        user_data['avatar'],
        user_data.get('bot', False),
        user_data['id']
    )
    if not user_exists:
        db_cursor.execute("INSERT INTO user(username,discriminator,avatar,bot,id) VALUES(?,?,?,?,?)", user_row)
    else:
        db_cursor.execute("UPDATE user SET username = ?, discriminator = ?, avatar = ?, bot = ? WHERE id = ?", user_row)


def ensure_member(db_cursor, member_data, guild_id):
    member_exists = list(db_cursor.execute('SELECT 1 FROM member WHERE user_id = ? AND guild_id = ?', [member_data['user']['id'], guild_id]))
    member_exists = len(member_exists) == 1
    member_row = (
        member_data['nick'] or member_data['user']['username'],
        member_data['user']['id'],
        guild_id
    )
    if not member_exists:
        db_cursor.execute("INSERT INTO member(nick,user_id,guild_id) VALUES(?,?,?)", member_row)
    else:
        db_cursor.execute("UPDATE member SET nick = ? WHERE user_id = ? AND guild_id = ?", member_row)
