CREATE TABLE meta (
    id BIGINT NOT NULL,
    version INT NOT NULL,
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE guild (
    id BIGINT NOT NULL,
    name VARCHAR(32) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE channel (
    id BIGINT NOT NULL,
    name VARCHAR(32) NOT NULL,
    guild_id BIGINT NOT NULL,
    FOREIGN KEY (guild_id) REFERENCES guild(id),
    PRIMARY KEY (id)
);

CREATE TABLE message (
    id BIGINT NOT NULL,
    timestamp DATETIME NOT NULL,
    edited_timestamp DATETIME,
    content TEXT,
    pinned BOOLEAN NOT NULL,
    author_id BIGINT NOT NULL,
    reply_to_id BIGINT,
    channel_id BIGINT NOT NULL,
    FOREIGN KEY (reply_to_id) REFERENCES message(id),
    FOREIGN KEY (author_id) REFERENCES user(id),
    FOREIGN KEY (channel_id) REFERENCES channel(id),
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id BIGINT NOT NULL,
    username VARCHAR(32) NOT NULL,
    discriminator SMALLINT NOT NULL,
    avatar VARCHAR(255),
    bot BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE member (
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    nick VARCHAR(32) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (guild_id) REFERENCES guild(id),
    PRIMARY KEY (user_id, guild_id)
);

-- CREATE TABLE mention (
--     message_id BIGINT NOT NULL,
--     user_id BIGINT NOT NULL,
--     FOREIGN KEY (message_id) REFERENCES message(id),
--     FOREIGN KEY (user_id) REFERENCES user(id),
--     PRIMARY KEY (message_id, user_id)
-- );

-- CREATE TABLE reaction (
--     message_id BIGINT NOT NULL,
--     emoji_id BIGINT NOT NULL,
--     emoji_name BIGINT NOT NULL,
--     count INT NOT NULL,
--     FOREIGN KEY (message_id) REFERENCES message(id),
--     FOREIGN KEY (emoji_id, emoji_name) REFERENCES emoji(id, name),
--     PRIMARY KEY (message_id, emoji_id, emoji_name)
-- );

-- CREATE TABLE emoji (
--     id BIGINT NOT NULL,
--     name VARCHAR(32) NOT NULL,
--     is_animated BOOLEAN NOT NULL,
--     image_url VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id, name)
-- );

-- CREATE TABLE attachment (
--     id BIGINT NOT NULL,
--     url VARCHAR(255) NOT NULL,
--     name VARCHAR(255) NOT NULL,
--     size INT NOT NULL,
--     message_id BIGINT NOT NULL,
--     FOREIGN KEY (message_id) REFERENCES message(id),
--     PRIMARY KEY (id)
-- );
