# -*- coding: utf8 -*-
import argparse
from instabot import Bot
import os
from dotenv import load_dotenv
import re
from random import choice

load_dotenv()

insta_login = os.getenv('INSTA_LOGIN')
insta_pass = os.getenv('INSTA_PASS')
bot = Bot()
bot.login(username=insta_login, password=insta_pass)


def is_user_exist(nicknames):
    for nickname in nicknames:
        if bot.get_user_id_from_username(nickname):
            return True
    return False


def get_all_post_comments(post_link):
    post_id = bot.get_media_id_from_link(post_link)
    all_comments = bot.get_media_comments_all(post_id)

    return all_comments


def get_commented_users(post_link):
    users = []
    all_comments = get_all_post_comments(post_link)
    for comment in all_comments:
        nicknames = re.findall('(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)',
                               comment['text'])
        if is_user_exist(nicknames):
            users.append((str(comment['user']['pk']), comment['user']['username']))
    return set(users)


def get_liked_users(post_link):
    liked_users = bot.get_media_likers(bot.get_media_id_from_link(post_link))
    return liked_users


def get_following_users(insta_account_name):
    following_users = bot.get_user_following(insta_account_name)
    return following_users


def get_performed_users(insta_account_name, post_link):
    performed_users = []

    liked_users = get_liked_users(post_link)
    following_users = get_following_users(insta_account_name)
    commented_users = get_commented_users(post_link)
    for id_user, nickname in commented_users:
        if id_user in liked_users and id_user in following_users:
            performed_users.append(nickname)

    return performed_users


def get_winner(insta_account_name, post_link):
    performed_users = get_performed_users(insta_account_name, post_link)
    print(choice(performed_users))


def main():
    insta_account_name = 'wowbeautybar.ru'
    # post_link = 'https://www.instagram.com/p/BtON034lPhu/'

    parser = argparse.ArgumentParser(description='Enter your post link')
    parser.add_argument('post_link', help='Enter post url')
    args = parser.parse_args()
    post_link = args.post_link

    get_winner(insta_account_name, post_link)


if __name__ == '__main__':
    main()
