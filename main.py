# -*- coding: utf8 -*-
import argparse
import os
import re

from dotenv import load_dotenv
from instabot import Bot
from random import choice


def is_user_exist(nicknames):
    return any(bot.get_user_id_from_username(nickname) for nickname in nicknames)


def get_commented_users(post_link):
    users = []
    all_comments = bot.get_media_comments_all(bot.get_media_id_from_link(post_link))
    for comment in all_comments:
        nicknames = re.findall('(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)',
                               comment['text'])
        if is_user_exist(nicknames):
            users.append((str(comment['user']['pk']), comment['user']['username']))
    return set(users)


def get_performed_users(insta_account_name, post_link):
    performed_users = []

    liked_users = bot.get_media_likers(bot.get_media_id_from_link(post_link))
    following_users = bot.get_user_following(insta_account_name)
    commented_users = get_commented_users(post_link)
    for id_user, nickname in commented_users:
        if id_user in liked_users and id_user in following_users:
            performed_users.append(nickname)

    return performed_users


def get_winner(insta_account_name, post_link):
    performed_users = get_performed_users(insta_account_name, post_link)
    print(choice(performed_users))


def main():
    insta_account_name = os.getenv('INSTA_GROUP_NAME')

    parser = argparse.ArgumentParser(description='Enter your post link')
    parser.add_argument('post_link', help='Enter post url')
    args = parser.parse_args()
    post_link = args.post_link

    get_winner(insta_account_name, post_link)


if __name__ == '__main__':
    load_dotenv()
    insta_login = os.getenv('INSTA_LOGIN')
    insta_pass = os.getenv('INSTA_PASS')
    bot = Bot()
    bot.login(username=insta_login, password=insta_pass)
    main()
