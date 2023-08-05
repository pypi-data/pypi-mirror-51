"""

Created on 01/03/2019 by Lorenzo Coacci

Copyright 2019 Lorenzo Coacci

IGAlgo : defines the class
IGAlgo(IGCocceBot bot) with the complex
algorithms to automate some task on Instagram.

"""

# to manage IGData and IGAction
from .action import IGAction
from .data import IGData
from .navigation import IGNavigation
import numpy as np
# to manag dfs
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
# to manage text colors
from termcolor import colored
# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"


class IGAlgo():
    """
    IGAlgo : the Instagram complex functions for IGCocceBot (algorithms)

    A class that implements the IGCocceBot to execute complex algorithms
    on Instagram

    Parameters
    ----------
    bot : IGCocceBot
        The initialized IGCocceBot

    Attributes
    ----------
    ig_bot : IGCocceBot (bot)
        An IGCocceBot
    ig_navigation : IGNavigation (bot)
        An IGNavigation object
    ig_data : IGData (bot)
        An IGData object
    ig_action : IGAction (bot)
        An IGAction object

    Methods
    -------
    analyze_posts(username=None, limit=None,
                  obj_detection=False)
    analyze_usernames(usernames_list, limit=None,
                      obj_detection=False,
                      analyze_posts=True,
                      how_many_posts=3) : DataFrame (pandas)
    like_competitor_followers_IF(my_username_to_print,
                                 competitor_user_to_print,
                                 list_followers, I,
                                 min_max_posts, min_max_followers,
                                 min_max_following, min_max_common,
                                 total_likes=inf, begin_from_follower_i=0,
                                 time_step=10) : tuple ()
    likes_vs_time_single_post(postURL, iterations, time_step,
                              time_shift=True, security_save_bool=False,
                              save_step=100) : DataFrame (pandas)
    likes_vs_time_multiple_posts(username, I, iterations, time_step,
                                 time_shift=True, security_save_bool=False,
                                 save_step=100) : DataFrame (pandas)

    Notes
    -----
    TO DO : add notes

    See Also
    --------
    TO DO : add something

    Examples
    --------
    TO DO : add something
    """
    def __init__(self, bot):
        self.ig_bot = bot
        self.ig_navigation = IGNavigation(bot)
        self.ig_data = IGData(bot)
        self.ig_action = IGAction(bot)

    """ * * * BETA * * * """

    def analyze_posts(self, username=None, limit=None,
                      obj_detection=False):
        """
        RETURN : a dataset of posts of an user

        Parameters
        ----------
        username (optional): string
            The username to go to
        limit (optional): int
            The number of posts to analyze (None is all)
        obj_detection (optional): bool
            Enable obj detection for posts?

        Returns
        -------
        info_post : DataFrame (pandas)
            The dataset with posts info or None

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        df = pd.DataFrame(columns=["post_code", "time_UTC", "time_diff",
                                   "num_of_media", "likes",
                                   "tags_in_pic", "post_caption",
                                   "hashtags", "obj_detection", "img_link", "avg_RGB"])
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", error_col))
                return None
            # is it private?
            if self.ig_navigation.is_private():
                print(colored("Cannot open followers list, this profile is Private!", error_col))
                return None
            # num of posts
            if limit is None:
                limit = self.ig_data.get_info_profile()["posts"]
            # posts
            self.ig_navigation.open_post_i(0)
            for i in range(limit):
                print(colored("- - - - - - - - - - - - - - - - - - - - -", main_col))
                print(colored("Post n : {}/{}".format(i + 1, limit), main_col))
                info_posts = self.ig_data.get_info_post(obj_detection=obj_detection)
                # append
                try:
                    df = df.append({"post_code": info_posts["post_code"],
                                    "time_UTC": info_posts["time_UTC"],
                                    "time_diff": info_posts["time_diff"],
                                    "num_of_media": info_posts["num_of_media"],
                                    "likes": info_posts["likes"],
                                    "tags_in_pic": info_posts["tags_in_pic"],
                                    "post_caption": info_posts["post_caption"],
                                    "hashtags": info_posts["hashtags"],
                                    "obj_detection": info_posts["obj_detection"],
                                    "img_link": info_posts["img_link"],
                                    "avg_RGB": info_posts["avg_RGB"]}, ignore_index=True)
                except:
                    print(colored("Erroro while appending to df!", error_col))
                self.ig_navigation.next_post()

            return df

    def analyze_usernames(self, usernames_list, limit=None,
                          obj_detection=False, analyze_posts=True,
                          how_many_posts=3):
        """
        RETURN : a dataset with all the info
        about the usernames in the list

        Parameters
        ----------
        usernames_list : string list []
            The username list to analyze
        limit (optional): int
            The limit for the usernames_list
        obj_detection (optional): bool
            Enable obj detection for posts?
        analyze_posts (optional): bool
            Add info about posts?
        how_many_posts (optional): int, >0, < num_posts
            Info about how many posts?

        Returns
        -------
        df : DataFrame (pandas)

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        df = pd.DataFrame(columns=["username", "name", "posts", "followers",
                                   "following", "commfollowers", "is_private",
                                   "am_i_following", "am_i_followed", "bio",
                                   "link", "post_info"])
        # limit
        if limit is not None:
            usernames_list = usernames_list[:limit]
        # go to next username
        j = 0
        for user in usernames_list:
            print(colored("- - - - - - - - - - - - - - - - - - - - -", main_col))
            print(colored("Username n : {}/{}".format(j + 1, len(usernames_list)), main_col))
            # valid username?
            valid = 1
            if user is not None:
                valid = self.ig_navigation.go_to_username(username=user)

            if valid != 1:
                print(colored("User is None, next...", error_col))
            else:
                # am i on profile?
                if not self.ig_navigation.am_i_on_a_profile():
                    print(colored("You are not on a profile, next...", error_col))
                else:
                    # info profile
                    info_profile = self.ig_data.get_info_profile()
                    # am_i_following
                    if self.ig_navigation.am_i_following() is None:
                        am_i_following = None
                    else:
                        am_i_following = 1 if self.ig_navigation.am_i_following() else 0
                    # am_i_followed
                    if self.ig_navigation.am_i_followed() is None:
                        am_i_followed = None
                    else:
                        am_i_followed = 1 if self.ig_navigation.am_i_followed() else 0

                    # is it private?
                    if self.ig_navigation.is_private():
                        private = 1
                    else:
                        private = 0
                    print(info_profile)
                    if analyze_posts:
                        if private == 1:
                            info_posts = how_many_posts*["NA"]
                        else:
                            # post info
                            info_posts = []
                            # max posts!
                            if how_many_posts > info_profile["posts"]:
                                how_many_posts = info_profile["posts"]
                            for i in range(how_many_posts):
                                self.ig_navigation.open_post_i(i)
                                info_posts.append(self.ig_data.get_info_post(obj_detection=obj_detection))
                                self.ig_navigation.close_post()

                        df = df.append({'username': info_profile["username"],
                                        'name': info_profile["name"],
                                        'posts': info_profile["posts"],
                                        'followers': info_profile["followers"],
                                        'following': info_profile["following"],
                                        'commfollowers': info_profile["commfollowers"],
                                        'bio': info_profile["bio"],
                                        'link': info_profile["link"],
                                        'is_private': private,
                                        'am_i_following': am_i_following,
                                        'am_i_followed': am_i_followed,
                                        'post_info': info_posts}, ignore_index=True)
                    else:
                        df = df.append({'username': info_profile["username"],
                                        'name': info_profile["name"],
                                        'posts': info_profile["posts"],
                                        'followers': info_profile["followers"],
                                        'following': info_profile["following"],
                                        'commfollowers': info_profile["commfollowers"],
                                        'bio': info_profile["bio"],
                                        'link': info_profile["link"],
                                        'is_private': private,
                                        'am_i_following': am_i_following,
                                        'am_i_followed': am_i_followed,
                                        'post_info': "NA"}, ignore_index=True)

            print(colored("- - - - - - - - - - - - - - - - - - - - -\n", main_col))
            j += 1

        return df

    def like_competitor_followers_IF(self, my_username_to_print,
                                     competitor_user_to_print,
                                     list_followers, I,
                                     min_max_posts, min_max_followers,
                                     min_max_following, min_max_common,
                                     total_likes=np.inf, begin_from_follower_i=0,
                                     time_step=10):
        """
        RETURN : like the competitor's followers IF
        a tuple (efficency, effectivness, missed_likes_rate)

        Parameters
        ----------
        my_username_to_print : string
            My username
        competitor_user_to_print : string
            The competitor's username
        list_followers : string list []
            The followers list to like
        I : int list [], >0
            The list of indexes i
        min_max_posts : int list [min, max], len = 2
            Min posts and max posts
        min_max_followers : int list [min, max], len = 2
            Min followers and max followers
        min_max_following : int list [min, max], len = 2
            Min following and max following
        min_max_common : int list [min, max], len = 2
            Min common followers max common followers
        total_likes (optional): int
            The limit for the number of likes to give
        begin_from_follower_i (optional): int
            Begin from follower i in the list_followers
        time_step (optional):
            Time step between 2 profile like actions

        Returns
        -------
        metrics : tuple ()
            A tuple (efficency, effectivness, missed_likes_rate)
            or (-1, i) = some error eith URL loading, i followers to rebegin

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        missed_likes = 0                     # the frequency of failed likes ()
        supposed_likes_per_user = len(I)     # supposed number of likes per user
        time.sleep(1)
        # my followers before
        valid = self.ig_navigation.go_to_username(username=my_username_to_print)
        if valid != 1:
            print(colored("Your username might be incorrect", error_col))
            return (-1, begin_from_follower_i)
        else:
            try:
                n_followers_before = self.ig_data.get_info_profile()["followers"]
            except:
                pass
        likes_count = 0
        follower_i = begin_from_follower_i
        while likes_count < total_likes and follower_i < len(list_followers):
            print(colored("- - - - - - - - - - - - - - - - - - - - -", main_col))
            print(colored("List : {}".format(competitor_user_to_print), main_col))
            print(colored("Follower n : {}/{}".format(follower_i + 1, len(list_followers)), main_col))
            print(colored("Customer : {}\n".format(my_username_to_print), main_col))
            # try
            try:
                liked = self.ig_action.like_N_posts_IF(I,
                                                       min_max_posts,
                                                       min_max_followers,
                                                       min_max_following,
                                                       min_max_common,
                                                       username=list_followers[follower_i])
            except:
                follower_i += 1
                continue

            if liked is None:
                return (-1, follower_i + 1)
            # update missed_likes
            if liked > 0:
                missed_likes += supposed_likes_per_user - liked
            time.sleep(1)

            follower_i += 1
            likes_count = likes_count + liked
            print(colored("Likes count : {}/{}".format(likes_count, total_likes), main_col))

            # METRICS
            try:
                efficency = 100*(((likes_count + missed_likes)/supposed_likes_per_user)/(follower_i - begin_from_follower_i))
                print(colored("Efficency : {0:.2f}%".format(efficency), main_col))
            except:
                efficency = "NA"
                print(colored("Efficency : NA", main_col))
            try:
                missed_like_rate = 100*((missed_likes)/((likes_count + missed_likes)))
                print(colored("Missed Likes : {0:.2f}%".format(missed_like_rate), main_col))
            except:
                missed_like_rate = "NA"
                print(colored("Missed Likes : NA", main_col))
            print(colored("- - - - - - - - - - - - - - - - - - - - -\n", main_col))
            #except:
            #    follower_i += 1
            #    print(colored("Some error, skip user...", error_col))

            # sleep step btw users
            time.sleep(time_step)

        # my followers after
        valid = self.ig_navigation.go_to_username(username=my_username_to_print)
        if valid != 1:
            print(colored("Your username might be incorrect", error_col))
            return (-1, follower_i + 1)
        else:
            n_followers_after = self.ig_data.get_info_profile()["followers"]
        # return effectivness and efficacy and missed likes
        effectivness = n_followers_after - n_followers_before
        return (efficency, effectivness, missed_like_rate)

    def likes_vs_time_single_post(self, postURL, iterations, time_step,
                                  time_shift=True, security_save_bool=False,
                                  save_step=100):
        """
        RETURN : a DataFrame (pandas) with likes and time of
        a single chosen post

        Parameters
        ----------
        postURL : string
            The post URL code
        iterations : int
            The number of records you wanna collect
        time_step : float
            The sample frequency, how many sec between 2 measures
        time_shift (optional): bool
            Want that t0 (initial time) = 0?
        security_save_bool (optional): bool
            Do you wanna save an xls every save_step steps?
        save_step (optional): int
            Save an xls every save_step

        Returns
        -------
        df : DataFrame (pandas)
            A DataFrame with likes and time of a single chosen post

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        df = pd.DataFrame(columns=["Post", "Time", "Likes", "Err_Time",
                                   "Err_Likes"])
        r = self.ig_bot.go_to_URL(postURL)
        if r == 1:
            time.sleep(3)
            postURLCode = self.ig_data.get_post_URL_code()
            # begin algo
            j = 1
            while j <= iterations:
                tIniz = time.time()
                self.ig_bot.refresh_page()
                tFin = time.time()
                # grab likes
                timeData = (tFin + tIniz)/2
                errTimeData = (tFin - tIniz)/2
                if j == 1:
                    initialTime = timeData
                # shift time line
                if time_shift:
                    timeData = timeData - initialTime
                likes = self.ig_data.get_number_of_likes()
                print("- - - - - - - - - - - - - - - - - - - - - -")
                print("Progress: " + str(j) + "/" + str(iterations))
                print("Post: " + str(postURLCode) + "\nTime: " +
                      str(timeData) + "\nLikes: " + str(likes))
                df = df.append({'Post': postURLCode,
                                'Likes': likes,
                                'Time': timeData,
                                'Err_Time': errTimeData,
                                'Err_Likes': 1}, ignore_index=True)
                if security_save_bool:
                    if j % save_step == 0:
                        save_to_xls(str(postURLCode) + "_LikesVSTime_" +
                                    str(j), df)
                j += 1
                time.sleep(time_step)

            return df

    def likes_vs_time_multiple_posts(self, username, I, iterations, time_step,
                                     time_shift=True, security_save_bool=False,
                                     save_step=100):
        """
        RETURN : a DataFrame (pandas) with likes and time of
        multiple posts

        Parameters
        ----------
        username : string
            The username to go to
        I : int list [], >0
            The list of indexes i
        iterations : int
            The number of records you wanna collect
        time_step : float
            The sample frequency, how many sec between 2 measures
        time_shift (optional): bool
            Want that t0 (initial time) = 0?
        security_save_bool (optional): bool
            Do you wanna save an xls every save_step steps?
        save_step (optional): int
            Save an xls every save_step

        Returns
        -------
        df : DataFrame (pandas)
            A DataFrame with likes and time of a multiple posts

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        df = pd.DataFrame(columns=["Post", "Time", "Likes", "Err_Time",
                                   "Err_Likes", "Comments", "Followers"])
        time.sleep(3)
        # begin algo
        j = 1
        while j <= iterations:
            tIniz = time.time()
            # valid username?
            valid = 1
            if username is not None:
                valid = self.ig_navigation.go_to_username(username=username)

            if valid != 1:
                return 0
            else:
                tFin = time.time()
                # get followers
                followers = self.ig_data.get_info_profile()["followers"]
                # grab likes
                timeData = (tFin + tIniz)/2
                errTimeData = (tFin - tIniz)/2
                if j == 1:
                    initialTime = timeData
                # shift time line
                if time_shift:
                    timeData = timeData - initialTime

                print("- - - - - - - - - - - - - - - - - - - - - -")
                print("Progress: " + str(j) + "/" + str(iterations))
                # code and likes of post i
                for i in I:
                    # select and grab comments
                    self.ig_navigation.select_post_i(i)
                    actual_element = self.ig_bot.driver.switch_to.active_element
                    # get comments
                    self.ig_bot.move_to_element(actual_element)
                    # get comments
                    comments = self.ig_bot.driver.find_elements_by_xpath("//li[@class='-V_eO']/span")[1].text
                    self.ig_navigation.open_post_i(i)
                    time.sleep(3)
                    postURLCode = self.ig_data.get_post_URL_code()
                    likes = self.ig_data.get_number_of_likes()
                    print("Post: " + str(postURLCode) + "\nTime: " +
                          str(timeData) + "\nLikes: " + str(likes))
                    df = df.append({'Post': postURLCode,
                                    'Likes': likes,
                                    'Time': timeData,
                                    'Comments': comments,
                                    'Err_Time': errTimeData,
                                    'Err_Likes': 1,
                                    'Followers': followers}, ignore_index=True)
                    self.ig_bot.press_key(self.ig_bot.Key.ESCAPE)
                    time.sleep(1)

                if security_save_bool:
                    if j % save_step == 0:
                        save_to_xls("Multiple_LikesVSTime_" + str(j), df)
            j += 1
            time.sleep(time_step)

        return df