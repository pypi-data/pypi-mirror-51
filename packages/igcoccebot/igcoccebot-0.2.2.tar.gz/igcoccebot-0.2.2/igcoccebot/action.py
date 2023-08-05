"""

Created on 01/03/2019 by Lorenzo Coacci

Copyright 2019 Lorenzo Coacci

IGAction : defines the class
IGAction(IGCocceBot bot) with the basic commands
for interacting on Instagram

"""

# * * * * LIBRARIES * * * *
# to manage IGData and IGNavigation
from .navigation import IGNavigation
from .data import IGData
import numpy as np
import time
# to manage text colors
from termcolor import colored

# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"


# * * * * CLASS * * * *
class IGAction():
    """
    IGAction : the Instagram action functions for IGCocceBot

    A class that implements the IGCocceBot to interact on Instagram easily

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

    Methods
    -------
    press_like() : int
    press_unlike() : int
    follow(username=None, string_to_check="Following",
               where="profile") : int
    unfollow(username=None, string_to_check="Following",
                 where="profile") : int
    follow_IF(min_max_posts, min_max_followers,
              min_max_following, min_max_common,
              username=None) : int
    unfollow_IF(min_max_posts, min_max_followers,
                min_max_following, min_max_common,
                username=None) : int
    look_stories_feed(time_step=2, limit=inf)
    look_stories(username=None, time_step=2)
    like_post_i(i, username=None) : int
    like_post_i_IF(i, min_max_posts, min_max_followers,
                   min_max_following, min_max_common,
                   username=None) : int
    like_N_posts(I, username=None) : int
    like_N_posts_IF(I, min_max_posts, min_max_followers,
                    min_max_following, min_max_common,
                    username=None) : int

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
        self.ig_data = IGData(bot)
        self.ig_navigation = IGNavigation(bot)

    """ * * * BETA * * * """

    def press_like(self):
        """
        RETURN : status code, press like button

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = liked,
           -1 = already liked,
            0 = some problem happened

        Notes
        -----
        TO DO : bug, element disappears after first like/unlike

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        if self.ig_navigation.am_i_on_a_post():
            try:
                if self.ig_bot.driver.find_element_by_xpath("//span[@class='fr66n']//button/span").get_attribute("aria-label") == "Like":
                    # like !
                    try:
                        self.ig_bot.driver.find_element_by_xpath("//span[@class='fr66n']//button").click()
                        return 1
                    except:
                        return 0
                else:
                    print(colored("Already liked!... no need to like",
                                  main_col))
                    return -1
            except:
                print(colored("Cannot find like button!", error_col))
                return 0
        else:
            print(colored("You are not on a post!", error_col))
            return 0

    def press_unlike(self):
        """
        RETURN : status code, press unlike button

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = unliked,
           -1 = already unliked,
            0 = some problem happened

        Notes
        -----
        TO DO : bug, element disappears after first like/unlike

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        if self.ig_navigation.am_i_on_a_post():
            try:
                if self.ig_bot.driver.find_element_by_xpath("//span[@class='fr66n']//button/span").get_attribute("aria-label") == "Unlike":
                    # unlike !
                    try:
                        self.ig_bot.driver.find_element_by_xpath("//span[@class='fr66n']//button").click()
                        return 1
                    except:
                        return 0
                else:
                    print(colored("Already unliked!... no need to unlike",
                                main_col))
                    return -1
            except:
                print(colored("Cannot find like button!", error_col))
                return 0
        else:
            print(colored("You are not on a post!", error_col))
            return 0

    def follow(self, username=None, string_to_check="Following",
               where="profile"):
        """
        RETURN : status code, follow

        Parameters
        ----------
        username (optional): string
            The username to go to
        string_to_check (optional): string
            String to check
        where (optional): string
            "profile" or "post"

        Returns
        -------
        status code : int
            1 = followed,
           -1 = already followed,
            0 = some problem happened

        Notes
        -----
        TO DO : bug follow element disapper after action! relocate it
        TO DO : bug for private profiles

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return 0
        else:
            try:
                if where == "profile":
                    # am i on profile?
                    if not self.ig_navigation.am_i_on_a_profile():
                        print(colored("You are not on a profile, maybe on a post to close!", error_col))
                        return 0
                    follow_button = self.ig_bot.driver.find_element_by_css_selector('button')
                elif where == "post":
                    if self.ig_navigation.am_i_on_a_post():
                        follow_button = self.ig_bot.driver.find_element_by_xpath("//div[@class='bY2yH']//button")
                    else:
                        print(colored("You are not on a post!", error_col))
                        return 0

                am_i_following = self.ig_navigation.am_i_following(where=where)
                if not am_i_following:
                    try:
                        follow_button.click()
                        return 1
                    except:
                        print(colored("Can't click follow button!", error_col))
                        return 0
                else:
                    print(colored("You are already following this user...",
                                  "no need to follow",
                                  error_col))
                    return -1
            except:
                print(colored("Can't find follow button!", error_col))
                return 0

    def unfollow(self, username=None, string_to_check="Following",
                 where="profile"):
        """
        RETURN : status code, unfollow

        Parameters
        ----------
        username (optional): string
            The username to go to
        string_to_check (optional): string
            String to check
        where (optional): string
            "profile" or "post"

        Returns
        -------
        status code : int
            1 = unfollowed,
           -1 = already unfollowed,
            0 = some problem happened

        Notes
        -----
        TO DO : bug unfollow element disapper after action! relocate it
        TO DO : bug for private profiles

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return 0
        else:
            try:
                if where == "profile":
                    # am i on profile?
                    if not self.ig_navigation.am_i_on_a_profile():
                        print(colored("You are not on a profile, maybe on a post to close!", error_col))
                        return 0
                    follow_button = self.ig_bot.driver.find_element_by_css_selector('button')
                elif where == "post":
                    if self.ig_navigation.am_i_on_a_post():
                        follow_button = self.ig_bot.driver.find_element_by_xpath("//div[@class='bY2yH']//button")
                    else:
                        print(colored("You are not on a post!", error_col))
                        return 0

                am_i_following = self.ig_navigation.am_i_following(where=where)
                if am_i_following:
                    # unfollow!
                    follow_button.click()
                    # wait alert popup
                    time.sleep(3)
                    try:
                        # maybe there is a PopUp Window with confirmation!
                        confirm_button = self.ig_bot.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
                        try:
                            confirm_button.click()
                            return 1
                        except:
                            return 0
                    except:
                        return 1
                else:
                    print(colored("Not following this user...",
                                  "no need to unfollow",
                                  error_col))
                    return -1
            except:
                print(colored("Can't find/click button follow!", error_col))
                return 0

    def follow_IF(self,
                  min_max_posts, min_max_followers,
                  min_max_following, min_max_common,
                  username=None):
        """
        RETURN : status code, follow IF

        Parameters
        ----------
        min_max_posts : int list [min, max], len = 2
            Min posts and max posts
        min_max_followers : int list [min, max], len = 2
            Min followers and max followers
        min_max_following : int list [min, max], len = 2
            Min following and max following
        min_max_common : int list [min, max], len = 2
            Min common followers max common followers
        username (optional): string
            The username to go to

        Returns
        -------
        status code : int
            1 = followed,
           -1 = already followed,
            0 = some problem happened

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
        # grab info to set check IF condition
        info_profile = self.ig_data.get_info_profile(username=username)
        # some problem occured
        if info_profile is None:
            return 0
        time.sleep(5)
        if (info_profile["posts"] >= min_max_posts[0] and info_profile["posts"] <= min_max_posts[1]) and (info_profile["followers"] >= min_max_followers[0] and info_profile["followers"] <= min_max_followers[1]) and (info_profile["following"] >= min_max_following[0] and info_profile["following"] <= min_max_following[1]) and (info_profile["commfollowers"] >= min_max_commonn[0] and info_profile["commfollowers"] <= min_max_common[1]):
            print(colored("Conditions met...", main_col))
            time.sleep(1)
            result = self.follow(username=None, where="profile")
            return result
        else:
            print(colored("Follow skipped, conditions not met!",
                          main_col))
            return 0

    def unfollow_IF(self,
                    min_max_posts, min_max_followers,
                    min_max_following, min_max_common,
                    username=None):
        """
        RETURN : status code, unfollow IF

        Parameters
        ----------
        min_max_posts : int list [min, max], len = 2
            Min posts and max posts
        min_max_followers : int list [min, max], len = 2
            Min followers and max followers
        min_max_following : int list [min, max], len = 2
            Min following and max following
        min_max_common : int list [min, max], len = 2
            Min common followers max common followers
        username (optional): string
            The username to go to

        Returns
        -------
        status code : int
            1 = unfollowed,
           -1 = already unfollowed,
            0 = some problem happened

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
        # grab info to set check IF condition
        info_profile = self.ig_data.get_info_profile(username=username)
        # some problem occured
        if info_profile is None:
            return 0
        time.sleep(5)
        if (info_profile["posts"] >= min_max_posts[0] and info_profile["posts"] <= min_max_posts[1]) and (info_profile["followers"] >= min_max_followers[0] and info_profile["followers"] <= min_max_followers[1]) and (info_profile["following"] >= min_max_following[0] and info_profile["following"] <= min_max_following[1]) and (info_profile["commfollowers"] >= min_max_commonn[0] and info_profile["commfollowers"] <= min_max_common[1]):
            print(colored("Conditions met...", main_col))
            time.sleep(1)
            result = self.press_unfollow(username=username, where="profile")
            return result
        else:
            print(colored("UnFollow skipped, conditions not met!",
                          main_col))
            return 0

    def look_stories_feed(self, time_step=2, limit=np.inf):
        """
        RETURN : number of stories watched

        Parameters
        ----------
        time_step (optional): float
            The time between 2 stories
        limit (optional): int
            Number of stories to look

        Returns
        -------
        stories_looked : int
            The number of stories of the feed looked

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
        count = 0
        valid = self.ig_bot.go_to_URL('https://www.instagram.com/')
        if valid != 1:
            return 0
        else:
            time.sleep(5)
            # remove the alert popup message if exists
            try:
                button_cancel_popup = self.ig_bot.driver.find_elements_by_xpath("//div[@class='mt3GC']/button")[1]
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(button_cancel_popup)
            except:
                pass
            time.sleep(1)
            try:
                stories = self.ig_bot.driver.find_elements_by_class_name('rdlLb')
            except:
                try:
                    stories = self.ig_bot.driver.find_elements_by_class_name('RR-M- ')
                except:
                    print(colored("Cannot find stories!", error_col))
                    return 0
            time.sleep(2)
            # open first story
            try:
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(stories[0])
                count += 1
                ig_logo_found = False
                while count < limit and not ig_logo_found:
                    time.sleep(time_step)
                    self.ig_bot.press_key(self.ig_bot.Key.ARROW_RIGHT)
                    count += 1
                    try:
                        # try to find ig logo
                        self.ig_bot.driver.find_element_by_class_name('cq2ai')
                        ig_logo_found = True
                    except:
                        pass
                return count
            except:
                print(colored("Error cannot click first story", error_col))
                return 0

    def look_stories(self, username=None, time_step=2,
                     limit=np.inf):
        """
        RETURN : number of stories watched

        Parameters
        ----------
        username (optional): string
            The username to go to
        time_step (optional): float
            The time between 2 stories
        limit (optional): int
            Number of stories to look

        Returns
        -------
        stories_looked : int
            The number of stories looked

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
        # TO DO : add time to skip story
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return 0
        else:
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", error_col))
                return 0
            # is it private?
            if self.ig_navigation.is_private():
                print(colored("Cannot open/select any post, this profile is Private!", error_col))
                return 0
            try:
                # define count num of stories
                count = 0
                # find stories button
                stories = self.ig_bot.driver.find_element_by_class_name('_6q-tv')
                time.sleep(1)
                self.ig_bot.move_and_click_element(stories)
                # wait stories
                wait = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.CLASS_NAME, "Szr5J")
                if wait == 0:
                    return 0
                # first story!
                count += 1
                # skip story every n sec
                while count < limit and not self.ig_navigation.am_i_on_a_profile():
                    time.sleep(time_step)
                    self.ig_bot.press_key(self.ig_bot.Key.ARROW_RIGHT)
                    count += 1
                return count
            except:
                print(colored("Cannot find or click story button",
                              error_col))
                return 0

    def like_post_i(self, i, username=None):
        """
        RETURN : status code - like post index i (from 0) in the post matrix

        Parameters
        ----------
        i : int, >0
            The index of the post matrix
        username (optional): string
            The username to go to

        Returns
        -------
        status code : int
            1 = liked,
            0 = some problem happened,
           -1 = already liked,
           -2 = provate profile,
         None = some problems with URL

        Raises
        ------
        ValueError
            if index i < 0

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
        # check index
        if i < 0:
            print(colored("Index must be greater or equal to 0!", error_col))
            raise ValueError

        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # open post i
            is_open = self.ig_navigation.open_post_i(i)
            if is_open == -2:
                return -2
            elif is_open == 1:
                result = self.press_like()
            else:
                return 0

            return result

    def like_post_i_IF(self, i,
                       min_max_posts, min_max_followers,
                       min_max_following, min_max_common,
                       username=None):
        """
        RETURN : status code - like post index i IF (from 0) in the post matrix

        Parameters
        ----------
        i : int, >0
            The index of the post matrix
        min_max_posts : int list [min, max], len = 2
            Min posts and max posts
        min_max_followers : int list [min, max], len = 2
            Min followers and max followers
        min_max_following : int list [min, max], len = 2
            Min following and max following
        min_max_common : int list [min, max], len = 2
            Min common followers max common followers
        username (optional): string
            The username to go to

        Returns
        -------
        status code : int
            1 = liked,
            0 = some problem happened,
           -1 = already liked,
           -2 = provate profile,
         None = some probelms with URL

        Raises
        ------
        ValueError
            if index i < 0

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
        # check index
        if i < 0:
            print(colored("Index must be greater or equal to 0!", error_col))
            raise ValueError

        # grab info to set check IF condition
        info_profile = self.ig_data.get_info_profile(username=username)
        # some error occured
        if info_profile is None:
            return None
        # private profile
        if self.ig_navigation.is_private():
            print(colored("Private profile...", main_col))
            return -2
        time.sleep(5)
        if (info_profile["posts"] >= min_max_posts[0] and info_profile["posts"] <= min_max_posts[1]) and (info_profile["followers"] >= min_max_followers[0] and info_profile["followers"] <= min_max_followers[1]) and (info_profile["following"] >= min_max_following[0] and info_profile["following"] <= min_max_following[1]) and (info_profile["commfollowers"] >= min_max_common[0] and info_profile["commfollowers"] <= min_max_common[1]):
            print(colored("Conditions met...", main_col))
            time.sleep(1)
            is_open = self.ig_navigation.open_post_i(i)
            if is_open == -2:
                return -2
            elif is_open == 1:
                result = self.press_like()
            else:
                return 0

            return result
        else:
            print(colored("like skipped, conditions not met!", main_col))
            return 0

    def like_N_posts(self, I, username=None):
        """
        RETURN : the like actions performed like N post, (N >= 2)

        Parameters
        ----------
        I : int list [], >0
            The list of indexes i
        username (optional): string
            The username to go to

        Returns
        -------
        like_performed : int
            The number of likes performed
            None if some problems with URL

        Raises
        ------
        ValueError
            if index i in I < 0

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
        count = 0
        for i in I:
            # check index
            if i < 0:
                print(colored("Index must be greater or equal to 0!", error_col))
                raise ValueError
            # like post i
            like = self.like_post_i(i, username=username)
            if like is None:
                return None
            # if private profile
            if like == -2:
                break
            # if liked
            elif like == 1:
                count += 1
            # close post
            self.ig_navigation.close_post(time_before=5, time_after=5)

        return count

    def like_N_posts_IF(self, I,
                        min_max_posts, min_max_followers,
                        min_max_following, min_max_common,
                        username=None):
        """
        RETURN : the like IF actions performed like N post, (N >= 2)

        Parameters
        ----------
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
        username (optional): string
            The username to go to

        Returns
        -------
        like_performed : int
            The number of likes performed
            None if something happened

        Raises
        ------
        ValueError
            if index i in I < 0

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
        count = 0
        info_profile = self.ig_data.get_info_profile(username=username)
        # some error occured
        if info_profile is None:
            return None
        if (info_profile["posts"] >= min_max_posts[0] and info_profile["posts"] <= min_max_posts[1]) and (info_profile["followers"] >= min_max_followers[0] and info_profile["followers"] <= min_max_followers[1]) and (info_profile["following"] >= min_max_following[0] and info_profile["following"] <= min_max_following[1]) and (info_profile["commfollowers"] >= min_max_common[0] and info_profile["commfollowers"] <= min_max_common[1]):
            print(colored("Conditions met...", main_col))
            for i in I:
                # check index
                if i < 0:
                    print(colored("Index must be greater or equal to 0!", error_col))
                    raise ValueError
                # like post i
                like = self.like_post_i(i)
                # if private profile
                if like == -2:
                    break
                # if liked
                if like == 1:
                    count += 1
                # close post
                self.ig_navigation.close_post(time_before=5, time_after=5)

            return count
        else:
            print(colored("Like skipped, conditions not met!", main_col))
            return 0

    """
    def comment(self):
        pass
        # TO DO
    """