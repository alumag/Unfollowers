#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a set of the user's Unfollowers in order to kick their asses later

from InstagramAPI import InstagramAPI

USERNAME = "username"
PASSWORD = "password"


def getTotalFollowings(api, user_id):
    """
    Returns the list of followings of the user.
    """
    api.getUsernameInfo(user_id)
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        following.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')

    return following


def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    """

    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


if __name__ == "__main__":
    # Login
    api = InstagramAPI(USERNAME, PASSWORD)
    api.login()

    user_id = api.username_id

    # List of all followers
    followers = {i['username'] for i in getTotalFollowers(api, user_id)}
    print('Number of followers:', len(followers))

    # List of all followings
    followings = {i['username'] for i in getTotalFollowings(api, user_id)}
    print('Number of followings:', len(followings))

    # Difference
    print('Unfollowers:', followings - followers)
