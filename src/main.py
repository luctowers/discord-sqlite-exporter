import argparse, sqlite3, discord, itertools, util, urllib.error

SCHEMA_VERSION = 1

parser = argparse.ArgumentParser(description='Export discord chat logs to a Sqlite database.')
parser.add_argument('-t', '--token', help='Discord access token', required=True)
parser.add_argument('-b', '--bot', help='Enable if using a bot token', action='store_true')
parser.add_argument('-c', '--channels', nargs='+', help='Discord channel id(s)')
parser.add_argument('-d', '--database', help='Sqlite database path', required=True)
parser.add_argument('-l', '--limit', type=int, help='Maximum number of messages to consume from channels')

def init_schema(db_cursor):
    with open('./schema/setup.sql', 'r') as sql_file:
        db_cursor.executescript(sql_file.read())

def main(args):
    
    # connect to database
    db = sqlite3.connect(args.database)
    db_cursor = db.cursor()
    db_cursor.execute('PRAGMA foreign_keys = ON')

    # setup database schema
    try:
        db_cursor.execute('SELECT version FROM meta ORDER BY id DESC LIMIT 1')
    except sqlite3.OperationalError as error:
        if error.args == ('no such table: meta',):
            init_schema(db_cursor)
        else:
            raise error

    updated_guilds = set()
    updated_users = set()
    updated_members = set()

    try: # catching keyboard interrupt

        # iterate over channels
        for channel_id in args.channels:

            channel_data = discord.get_channel(args.token, channel_id)
            guild_id = channel_data['guild_id']
            guild_data = discord.get_guild(args.token, guild_id)

            if not guild_id in updated_guilds:
                updated_guilds.add(guild_id)
                util.ensure_guild(db_cursor, guild_data)

            util.ensure_channel(db_cursor, channel_data)

            last_message_id = list(db_cursor.execute('SELECT id FROM message WHERE channel_id = ? ORDER BY id DESC LIMIT 1', [channel_id]))
            last_message_id = last_message_id[0][0] if len(last_message_id) == 1 else 0

            def ensure_user_and_member(user_id):
                if not user_id in updated_users:
                    updated_users.add(user_id)
                    user_data = discord.get_user(args.token, user_id)
                    util.ensure_user(db_cursor, user_data)
                if not (user_id, guild_id) in updated_members:
                    updated_members.add((user_id, guild_id))
                    try:
                        member_data = discord.get_member(args.token, user_id, guild_id)
                        util.ensure_member(db_cursor, member_data, guild_id)
                    except urllib.error.HTTPError as error:
                        if error.code == 404:
                            pass
                        else:
                            raise error

            date = None

            for message in itertools.islice(discord.get_messages(args.token, channel_id, last_message_id), args.limit):

                if message['timestamp'][:10] != date:
                    date = message['timestamp'][:10]
                    print('%s "%s" (%s) "%s" (%s)' % (
                        date,
                        guild_data['name'],
                        guild_data['id'],
                        channel_data['name'],
                        channel_data['id'],
                    ))

                if not message['type'] in {discord.MESSAGE_TYPE_DEFAULT, discord.MESSAGE_TYPE_REPLY}:
                    continue

                ensure_user_and_member(message['author']['id'])
                db_cursor.execute("INSERT INTO message(id,timestamp,edited_timestamp,content,pinned,author_id,reply_to_id,channel_id) VALUES(?,?,?,?,?,?,?,?)", (
                    message['id'],
                    message['timestamp'],
                    message['edited_timestamp'],
                    message['content'] or None,
                    message['pinned'],
                    message['author']['id'],
                    message['referenced_message']['id'] if message['type'] == discord.MESSAGE_TYPE_REPLY and message['referenced_message'] else None,
                    message['channel_id']
                ))
    
    except KeyboardInterrupt:
        pass

    db.commit()
    db.close()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
