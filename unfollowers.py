#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a set of the user's Unfollowers in order to kick their asses later
import pickle
import os

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


def getFollowersDiff(followers):
    """
    Return the diff between current followers and past followers
    """
    if os.path.exists('followers.json'):
        with open('followers.json') as f:
            followers_diff = pickle.load(f)
            return followers_diff - followers


def getFollowinsgDiff(followings):
    """
        Return the diff between current followings and past followings
        """
    if os.path.exists('followings.json'):
        with open('followings.json') as f:
            followings_diff = pickle.load(f)
            return followings_diff - followings


def main():
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
    print('Poepole that not following me back:', followings - followers)

    print('Followers diff from last state:', getFollowersDiff(followers))
    print('Followings diff from last state:', getFollowinsgDiff(followings))

    save = raw_input('Save current state?: (y/n)')

    if 'y' == str(save).lower() or 'yes' == str(save).lower():
        with open('followers.json', 'w') as f:
            pickle.dump(followers, f)

        with open('followings.json', 'w') as f:
            pickle.dump(followings, f)


if "__main__" == __name__:
    main()
