"""

Created on 01/03/2019 by Lorenzo Coacci

IGData : defines the class
IGData(IGCocceBot bot) with the basic commands
for collecting data on Instagram.

"""

# * * * * LIBRARIES * * * *
# to manage dfs
import pandas as pd
# to manage datetime
import datetime
# to manage unique
import numpy as np
# to manage URL
import urllib.request
# to manage os
import os
# to manage IGNavigation
from .navigation import IGNavigation
# to manage tools
from .tools import save_to_csv, save_to_xls, parse_2_int
# to manage obj detection
from .yolo import *
# to manage images
from PIL import Image
# to manage time
import time
# to manage text colors
from termcolor import colored

# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"
warning_col = "yellow"


# * * * * CLASS * * * *
class IGData():
    """
    IGData : the Instagram data functions for IGCocceBot

    A class that implements the IGCocceBot to collect data on Instagram easily

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

    Methods
    -------
    get_info_profile(username=None) : dict {}
    get_info_post(pixels=False, obj_detection=False) : dict {}
    get_name(username=None, class_element='rhpdm') : string
    get_bio(username=None,
            x_path_element="//div[@class='-vDIg']/span") : string
    get_link(username=None, class_element='yLUwa') : string
    get_common_followers() : int
    get_username(where="profile") : string
    get_image(img_link, filename="img",
                  folder_saving_path="./", show_debug=True) : int
    get_images(img_links, filename="img",
               folder_saving_path="./", show_debug=True) : list [int]
    get_image_link() : string
    get_pixels_RGB(image_path) : list of tuples
    get_visible_comments() : a list [string]
    get_images_links(username=None, limit=None, time_step=0.3) : string list []
    get_number_media_per_post() : int
    get_time_posted_UTC() : string
    get_time_posted_difference() : float
    get_tags_in_pic(unique=True) : tuple ()
    get_hashtags(unique=True): tuple ()
    get_tags_in_comments() : tuple ()
    get_screenshot_obj_detection(yolo_settings=None) : list []
    get_image_obj_detection(image_path, yolo_settings=None) : list []
    get_number_of_people(confidence_cutoff=0.9) : int
    get_number_of_likes(to_int=True) : int (or string)
    get_post_URL_code() : string
    get_post_caption() : string
    get_time_difference_between_posts(i, j) : float
    get_hashtags_exposure(hashtags_list, method="sum") : float
    my_followers_list() : string list []
    my_following_list() : string list []
    my_followers_following_DFs() : string DataFrame (pandas)
    get_usernames_from_list(limit, mode="tab", df_col_name="",
                            save_step=1000, save_string="file",
                            save_secure=True, save_path="./",
                            time_step=0, step=4, print_mode=True) : string list []
    get_followers_list(username=None, mode="tab",
                       df_col_name="Followers",
                       limit_followers=None,
                       save_step=1000, save_secure=True, save_path="./",
                       time_step=0, step=4) : string list []
    get_following_list(username=None, mode="tab",
                       df_col_name="Following",
                       limit_following=None,
                       save_step=1000, save_secure=True, save_path="./",
                       time_step=0, step=4) : string list []

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

    def get_info_profile(self, username=None):
        """
        RETURN : a dict {} with info profile or None

        Parameters
        ----------
        username (optional): string
            The username to go to

        Returns
        -------
        info_profile : dict {}
            {'posts': x, 'followers': x, 'following': x,
             'commfollowers': x, 'username': x, 'bio': x,
             'name': x, 'link': x}
            None = username was invalid or some other error

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
            # find info profile element
            try:
                info_profile_element = self.ig_bot.driver.find_elements_by_class_name('g47SY ')
            except:
                try:
                    info_profile_element = self.ig_bot.driver.find_element_by_xpath("//span[@class=' _81NM2']/span")
                except:
                    print(colored("Error: cannot find info profile WebElement!",
                          error_col))
                    return None

            info_profile = {}

            # num posts
            try:
                num_posts = info_profile_element[0].text
            except:
                print(colored("Cannot find element 0 or text attribute",
                      error_col))
            # to int
            info_profile["posts"] = parse_2_int(num_posts)

            # num followers
            try:
                num_followers = info_profile_element[1].get_attribute("title")
            except:
                print(colored("Cannot find element 1 or get_title attribute",
                      error_col))
            if parse_2_int(num_followers) is None:
                num_followers = info_profile_element[1].text
            # to int
            info_profile["followers"] = parse_2_int(num_followers)

            # num following
            try:
                num_following = info_profile_element[2].text
            except:
                print(colored("Cannot find element 2 or text attribute",
                      error_col))
            # to int
            info_profile["following"] = parse_2_int(num_following)

            # num common followers
            info_profile["commfollowers"] = self.get_common_followers()
            # username
            info_profile["username"] = self.get_username()
            # name
            info_profile["name"] = self.get_name()
            # bio
            info_profile["bio"] = self.get_bio()
            # link
            info_profile["link"] = self.get_link()

            return(info_profile)

    def get_info_post(self, pixels=False, obj_detection=False):
        """
        RETURN : a dict {} with info post or None

        Parameters
        ----------
        pixels (optional): bool
            Do you wanna download RGB info of any pixel?
        obj_detection (optional): bool
            Do you wanna perform obj detection?

        Returns
        -------
        info_post : dict {}
            {'time_UTC': x, 'time_diff': x, 'num_of_media': x,
             'likes': x, 'post_code': x,
             'tag_in_pic' (the first one): x (tuple),
             'obj_detection' (of first image): x (tuple),
             'hashtags' : x (tuple),
             'visible_comments': (list)
             'post_caption': x, 'img_link': x, 'pixels': list(tuples)}
            None = post was invalid or some other error

        Notes
        -----
        TO DO : finish tag in comments and add here

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        if self.ig_navigation.am_i_on_a_post():
            info_post = {}
            # UTC time
            info_post["time_UTC"] = self.get_time_posted_UTC()
            # time difference
            info_post["time_diff"] = self.get_time_posted_difference()
            # number of media
            info_post["num_of_media"] = self.get_number_media_per_post()
            # likes
            info_post["likes"] = self.get_number_of_likes()
            # post code
            info_post["post_code"] = self.get_post_URL_code()
            # tags in first pic
            info_post["tags_in_pic"] = self.get_tags_in_pic()
            # post caption
            info_post["post_caption"] = self.get_post_caption()
            # hashtags
            info_post["hashtags"] = self.get_hashtags()
            # visible comments
            info_post["visible_comments"] = self.get_visible_comments()
            # is video
            info_post["is_video"] = 1 if self.ig_navigation.is_video() else 0
            # image link
            info_post["img_link"] = self.get_image_link()
            # get pixels
            if info_post["img_link"] is not None:
                result = self.get_image(info_post["img_link"], show_debug=False)  # download img
                if result == 1:
                    # pixels RGB
                    if pixels:
                        info_post["pixels"] = self.get_pixels_RGB(image_path="./img_1.png")
                    else:
                        info_post["pixels"] = None
                    # obj detection
                    if obj_detection:
                        info_post["obj_detection"] = self.get_obj_detection(image_path="./img_1.png")
                    else:
                        info_post["obj_detection"] = None
                    os.remove("./img_1.png")  # remove image after analysis
                else:
                    info_post["pixels"] = None
                    info_post["obj_detection"] = None
            else:
                info_post["pixels"] = None
                info_post["obj_detection"] = None
            return info_post
        else:
            print(colored("You are not on a post!", error_col))
            return None

    def get_name(self, username=None, class_element='rhpdm'):
        """
        RETURN : the name on the profile

        Parameters
        ----------
        username (optional): string
            The username to go to
        class_element (optional): string
            The class for the name element

        Returns
        -------
        name : string
            The name shown on the profile
            or None

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
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", warning_col))
                return None
            try:
                name_element = self.ig_bot.driver.find_element_by_class_name(class_element)
                name = name_element.text
            except:
                print(colored("Cannot find name on profile!", warning_col))
                name = None
        return name

    def get_bio(self, username=None, x_path_element="//div[@class='-vDIg']/span"):
        """
        RETURN : the bio information

        Parameters
        ----------
        username (optional): string
            The username to go to
        x_path_element (optional): string
            The xpath for the bio element

        Returns
        -------
        bio : string
            The bio shown on the profile
            or None

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
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", warning_col))
                return None
            try:
                bio_element = self.ig_bot.driver.find_element_by_xpath(x_path_element)
                bio = bio_element.text
            except:
                print(colored("Cannot find bio on profile!", warning_col))
                bio = None
        return bio

    def get_link(self, username=None, class_element='yLUwa'):
        """
        RETURN : the link under the bio

        Parameters
        ----------
        username (optional): string
            The username to go to
        class_element (optional): string
            The class for the name element

        Returns
        -------
        link : string
            The link shown on the profile
            or None

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
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", warning_col))
                return None
            try:
                link_element = self.ig_bot.driver.find_element_by_class_name(class_element)
                link = link_element.get_attribute("href")
            except:
                print(colored("Cannot find link on profile!", warning_col))
                link = None
        return link

    def get_common_followers(self):
        """
        RETURN : common followers of the profile

        Parameters
        ----------
        username (optional): string
            The username to go to
        class_element (optional): string
            The class for the name element

        Returns
        -------
        commonfollowers : int
            The common followers of the profile
            or None

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
        # am i on profile?
        if not self.ig_navigation.am_i_on_a_profile():
            print(colored("You are not on a profile, maybe on a post to close!", warning_col))
            return None
        # common followers
        try:
            shown_common = self.ig_bot.driver.find_elements_by_xpath("//span[@class='tc8A9']/span")
            common_follows_1 = len(shown_common)
            time.sleep(0.1)
            if common_follows_1 < 3:
                common_follows_2 = 0
            else:
                common_follows_2 = self.ig_bot.driver.find_element_by_class_name('tc8A9').text
                try:
                    common_follows_2 = common_follows_2.split(" + ")[1]
                    common_follows_2 = common_follows_2.split(" ")[0]
                    common_follows_2 = int(common_follows_2)
                except:
                    print(colored("Cannot convert to int!", warning_col))
                    return None
        except:
            common_follows_1 = 0
            common_follows_2 = 0
        # total common folllowers
        common_follows = common_follows_1 + common_follows_2
        return common_follows

    def get_username(self, where="profile"):
        """
        RETURN : username of the profile

        Parameters
        ----------
        where (optional): string ("profile", "post")
            Where to get the username

        Returns
        -------
        username : string
            The username
            or None

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
        if where == "profile":
            # am i on profile?
            if not self.ig_navigation.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", warning_col))
                return None
            try:
                username_element = self.ig_bot.driver.find_element_by_xpath("//div[@class='nZSzR']/h1")
                username = username_element.text
                return username
            except:
                print(colored("Cannot find username on profile!", warning_col))
                return None
        elif where == "post":
            if not self.ig_navigation.am_i_on_a_post():
                print(colored("You are not on a post!", warning_col))
                return None
            try:
                username = self.ig_bot.driver.find_element_by_xpath("//h2[@class='BrX75']//a").text
                return username
            except:
                print(colored("Cannot find username on post!", warning_col))
                return None

    def get_image(self, img_link, filename="img",
                  folder_saving_path="./", show_debug=True):
        """
        RETURN : status code - download image from a img link

        Parameters
        ----------
        img_link : string
            The image link
        filename (optional): string
            The filename/filepath
        folder_saving_path (optional): string
            The folder saving path

        Returns
        -------
        status code : int
            1 = downloaded!
            0 = some error while downlaoding

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
        # get image
        if img_link is None:
            print(colored("Img link is None", warning_col))
            return 0
        else:
            return self.get_images([img_link], filename=filename,
                                   folder_saving_path=folder_saving_path,
                                   show_debug=show_debug)[0]

    def get_images(self, img_links, filename="img",
                   folder_saving_path="./", show_debug=True):
        """
        RETURN : a status code list [] - download images from a img link

        Parameters
        ----------
        img_links : string list []
            The image links
        filename (optional): string
            The filename/filepath
        folder_saving_path (optional): string
            The folder saving path
        show_debug (optional) : bool
            Show debug info?

        Returns
        -------
        status code list : int [0, 1, 1, 0, ...]
            1 = downloaded!
            0 = some error while downlaoding

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
        # define result
        result = []
        # clean folder saving path
        if folder_saving_path[-1] != '/':
            folder_saving_path += '/'

        if img_links is None:
            print(colored("Image links list is None!", warning_col))
            return [0]

        # grab image
        try:
            for i in range(len(img_links)):
                if show_debug:
                    print(colored("Downloading img... {}/{}".format((i+1), len(img_links)), main_col))
                    print(colored("Saving it in {}{}_{}.png".format(folder_saving_path, filename, (i+1)), main_col))
                if img_links[i] is None:
                    print(colored("Img link {} is None".format((i+1)), warning_col))
                    result.append(0)
                else:
                    try:
                        urllib.request.urlretrieve(img_links[i], "{}{}_{}.png".format(folder_saving_path, filename, (i+1)))
                        if show_debug:
                            print(colored("Download completed!", main_col))
                        result.append(1)
                    except:
                        if show_debug:
                            print(colored("urlib request not worked...", warning_col))
                            result.append(0)
        except:
            print(colored("Cannot download the image/images! Check the link/links!",
                           warning_col))
            return [0]
        return result

    def get_image_link(self):
        """
        RETURN : the image link of the post or None if something happened

        Parameters
        ----------
        None

        Returns
        -------
        image_link : string
            The image link of the pic
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            if self.ig_navigation.is_image():
                # get img link
                try:
                    # img element
                    img_elem = self.ig_bot.driver.find_elements_by_xpath("//div[@class='ZyFrc']/div/div/img")[0]
                    link = img_elem.get_attribute("src")
                except:
                    try:
                        # img element
                        img_elem = self.ig_bot.driver.find_elements_by_xpath("//div[@class='ZyFrc']/div/div/div/img")[0]
                        link = img_elem.get_attribute("src")
                    except:
                        print(colored("Cannot find image element!", warning_col))
                        return None
            else:
                if self.ig_navigation.is_video():
                    print(colored("You are on a video, not an image!", warning_col))
                return None
            return link
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_pixels_RGB(self, image_path=None):
        """
        RETURN : the image pixels (R, G, B) of all image

        Parameters
        ----------
        image_path : string
            The image path

        Returns
        -------
        pixels : tuples (R, G, B) list []
            A list of RGB tuples for each pixel
            or None

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
        if image_path is None:
            # get img link
            img_link = self.get_image_link()
            if img_link is not None:
                status = self.get_image(img_link, show_debug=False)  # download img
                if status == 1:
                    # obj detection
                    image_path = "./img_1.png"
                    try:
                        img = Image.open(image_path)
                        pixels = list(img.getdata())
                    except:
                        return None
                    os.remove("./img_1.png")  # remove image after analysis
                else:
                    return None
                return pixels
        else:
            try:
                img = Image.open(image_path)
                pixels = list(img.getdata())
            except:
                return None
            return pixels

    """ TO DO : work in progress...
    def get_image_captions(self, username=None, limit=None, time_step=0.3):
        RETURN : the caption about the image provided by IG
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # close posts if any
            self.ig_navigation.close_post(time_before=0.1, time_after=0.1)
            # set the limit
            if limit is None:
                limit = self.get_info_profile()["posts"]

            # get first image
            img_captions = []
            # go on
            for i in range(limit):
                time.sleep(time_step)
                self.ig_bot.press_key(self.ig_bot.Key.TAB)
                imgs = self.ig_bot.driver.find_elements_by_tag_name('img')
                for img in imgs:
                    try:
                        caption = img.get_attribute("alt")
                        img_captions.append(caption)
                    except:
                        img_captions.append("")
                print(colored("post {}/{}".format(i+1, limit), main_col))

            unique_imgs_captions = list(np.unique(img_captions))
            print(colored("\nUnique captions check (unique/total) : {}/{}\n".format(len(unique_imgs_captions), limit),
                          main_col))

        return unique_imgs_captions
    """

    """ TO DO : work in progress...
    def get_number_of_comments(self):
        RETURN : num of comments of the post

        Parameters
        ----------
        None

        Returns
        -------
        number_of_comments : int
            The number of commnets
            or None

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        if self.ig_navigation.am_i_on_a_post():
            try:
                comm = self.ig_bot.driver.find_elements_by_class_name('Yi5aA ')
                num_comm = ???
            except:
                num_comm = None
            return num_comm
        else:
            print(colored("You are not on a post!", error_col))
            return None
    """

    """ TO DO : work in progress...
    def get_number_of_stories(self):
        pass
    """

    def get_visible_comments(self):
        """
        RETURN : A list with comments [comment1, comment2, ...]

        Parameters
        ----------
        None

        Returns
        -------
        comments : list []
            A list with comments [comment1, comment2, ...]
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                comments_el = self.ig_bot.driver.find_elements_by_xpath("//div[@class='C4VMK']/span")
                comments = []
                for el in comments_el:
                    comments.append(el.text)
                comments = comments[1:]
            except:
                comments = []
            return comments
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_images_links(self, username=None, limit=None, time_step=0.3):
        """
        RETURN : All links of the images in the post matrix in a list []

        Parameters
        ----------
        username (optional): string
            The username to go to
        limit (optional): int
            The limit for the matrix
        time_tab (optional): float
            The time between selection of posts

        Returns
        -------
        images_links : string list []
            The list containing all images links
            or None

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
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return None
        else:
            # close posts if any
            self.ig_navigation.close_post(time_before=0.1, time_after=0.1)
            # set the limit
            if limit is None:
                limit = self.get_info_profile()["posts"]

            # select firt post to begin
            self.ig_navigation.select_post_i(0)

            # get first image
            img_links = []
            # go on
            for i in range(limit):
                time.sleep(time_step)
                self.ig_bot.press_key(self.ig_bot.Key.TAB)
                imgs = self.ig_bot.driver.find_elements_by_tag_name('img')
                try:
                    links = [img.get_attribute("src") for img in imgs]
                except:
                    links = []
                print(colored("post {}/{}".format(i+1, limit), main_col))
                for link in links:
                    img_links.append(link)

            unique_imgs_list = list(np.unique(img_links))
            print(colored("\nUnique usernames check (unique/total) : {}/{}\n".format(len(unique_imgs_list), limit),
                          main_col))

        return unique_imgs_list

    def get_number_media_per_post(self):
        """
        RETURN : number of pics/media on a multiple post

        Parameters
        ----------
        None

        Returns
        -------
        number_of_pics : int
            The number of media (images/videos)
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                pics = self.ig_bot.driver.find_elements_by_class_name('Yi5aA ')
                num_pics = 1 + len(pics)
            except:
                num_pics = None
            return num_pics
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_time_posted_UTC(self):
        """
        RETURN : datetime when the post was posted in UTC time

        Parameters
        ----------
        None

        Returns
        -------
        time_posted_UTC : string
            The datetime when the post was posted UTC time
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                date_post = self.ig_bot.driver.find_element_by_xpath("//a[@class='c-Yi7']/time").get_attribute("datetime")
                date_post = date_post.split('.')[0]
            except:
                date_post = None
            return(date_post)
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_time_posted_difference(self):
        """
        RETURN : time difference between when the post
        was posted in and now in seconds

        Parameters
        ----------
        None

        Returns
        -------
        time_posted_difference : string
            Time difference between when the post
            was posted in and now in seconds
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                date_post = self.ig_bot.driver.find_element_by_xpath("//a[@class='c-Yi7']/time").get_attribute("datetime")
                date_post = date_post.split('.')[0]
                time_DF = (datetime.datetime.utcnow() -
                        datetime.datetime.strptime(date_post, "%Y-%m-%dT%H:%M:%S")).total_seconds()
            except:
                time_DF = 'NA'
            return time_DF
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_tags_in_pic(self, unique=True):
        """
        RETURN : A tuple (number of tags in pic, a list of tags)

        Parameters
        ----------
        unique (optional): bool
            Apply a unique filter to tags?

        Returns
        -------
        tags_in_pics : tuple
            A tuple (number of tags in pic, a list of tags)
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                tags = self.ig_bot.driver.find_elements_by_xpath("//span[@class='eg3Fv']")
                # click the pic to see tags
                self.move_and_click_element(tags[0])
                time.sleep(0.5)
                tags = [tag.text for tag in tags]
            except:
                tags = []

            if unique:
                tags = list(np.unique(tags))

            return (len(tags), tags)
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_hashtags(self, unique=True):
        """
        RETURN : A tuple (number of hashtags, a list of hashtags)

        Parameters
        ----------
        unique (optional): bool
            Apply a unique filter to hashtags?

        Returns
        -------
        hashtags : tuple
            A tuple (number of hashtags, a list of hashtags)
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                hashtags = self.ig_bot.driver.find_elements_by_xpath("//div[@class='C4VMK']/span/a")
            except:
                hashtags = []
            hashtag_names = []
            for i in range(len(hashtags)):
                if (hashtags[i].get_attribute("href").split('/'))[3] == 'explore':
                    hashtag_names.append((hashtags[i].get_attribute("href").split('/'))[5])

            # unique hashtags
            if unique:
                hashtag_names = list(np.unique(hashtag_names))

            return (len(hashtag_names), hashtag_names)
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_screenshot_obj_detection(self, yolo_settings=None):
        """
        RETURN : the result of the object detection on a screenshot (only NON headless mode)

        Parameters
        ----------
        yolo_settings (optional): list [weights, data], len = 2
            The settings of YOLO

        Returns
        -------
        obj_detection : list []
            The result of the object detection on a screenshot
            or None

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
        if self.ig_navigation.am_i_on_a_post():
            # screenshot
            self.ig_bot.driver.save_screenshot("screenshot.png")
            # load YOLO
            if yolo_settings is None:
                yolo_settings = load_YOLO()
            # obj detection!
            result = detect_obj_YOLO(b"screenshot.png", yolo_settings[0],
                                     yolo_settings[1])
            # remove img
            os.remove("./screenshot.png")

            return result
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_obj_detection(self, image_path=None, yolo_settings=None):
        """
        RETURN : the result of the object detection on this post image

        Parameters
        ----------
        yolo_settings (optional): list [weights, data], len = 2
            The settings of YOLO

        Returns
        -------
        obj_detection : list []
            The result of the object detection on a screenshot
            or None

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
        if image_path is None:
            # get img link
            img_link = self.get_image_link()
            if img_link is not None:
                status = self.get_image(img_link, show_debug=False)  # download img
                if status == 1:
                    # obj detection
                    image_path = "./img_1.png"
                    # load YOLO
                    if yolo_settings is None:
                        yolo_settings = load_YOLO()
                    # obj detection!
                    result = detect_obj_YOLO(image_path.encode(), yolo_settings[0],
                                             yolo_settings[1])
                    os.remove("./img_1.png")  # remove image after analysis
                else:
                    return None
                return result
            else:
                return None
        else:
            # load YOLO
            if yolo_settings is None:
                yolo_settings = load_YOLO()
            # obj detection!
            result = detect_obj_YOLO(image_path.encode(), yolo_settings[0],
                                     yolo_settings[1])

            return result

    def get_number_of_people(self, confidence_cutoff=0.9):
        """
        RETURN : the result of the object detection on an image

        Parameters
        ----------
        yolo_settings (optional): list [weights, data], len = 2
            The settings of YOLO
        confidence_cutoff (optional): float, from 0 to 1
            The confidence cutoff to classify someone as a person

        Returns
        -------
        num_of_people : int
            The number of people in the picture
            or None

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
        # YOLO
        if self.ig_navigation.am_i_on_a_post():
            obj = self.get_obj_detection()
            count_people = 0
            if len(obj) != 0:
                labels = obj[1]
                confidence = []
                for i in range(len(labels)):
                    confidence.append(((obj[0])[i])[1])

                for i in range(len(labels)):
                    if confidence[i] >= confidence_cutoff:
                        if labels[i] == b"person":
                            count_people += 1

            return count_people
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_number_of_likes(self, to_int=True):
        """
        RETURN : the number of likes on a post - pictures only

        Parameters
        ----------
        to_int (optional): bool
            Parse to int?

        Returns
        -------
        num_of_likes : int (or string)
            The number of likes on a post

        Notes
        -----
        Warning: it loses 1 like if there is a known liker in the post!
        TO DO : Fix the 1 like problem (or not? it loses in speed)

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        try:
            # if on post page URL
            likes = self.ig_bot.driver.find_element_by_xpath("//a[@class='zV_Nj']/span").text
        except:
            # if on profile/explore/etc..
            try:
                likes = self.ig_bot.driver.find_element_by_xpath("//div[@class='Nm9Fw']/button/span").text
            except:
                print(colored("Cannot grab likes", warning_col))
                return None

        if to_int:
            # parse likes
            likes = parse_2_int(likes)

        return likes

    def get_post_URL_code(self):
        """
        RETURN : get the post URL Code

        Parameters
        ----------
        None

        Returns
        -------
        post_URL_code : string
            The post URL code

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                URL_code = self.ig_bot.driver.current_url.split('/')[4]
            except:
                URL_code = None
                print(colored("Cannot find URL code!", warning_col))
            return URL_code
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_post_caption(self):
        """
        RETURN : get the post caption

        Parameters
        ----------
        None

        Returns
        -------
        post_caption : string
            The post caption

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
        if self.ig_navigation.am_i_on_a_post():
            try:
                post_caption_el = self.ig_bot.driver.find_element_by_xpath("//div[@class='C4VMK']/span")
                post_caption = post_caption_el.text
            except:
                post_caption = None
                print(colored("Cannot find post caption!", warning_col))
            return post_caption
        else:
            print(colored("You are not on a post!", warning_col))
            return None

    def get_time_difference_between_posts(self, i, j):
        """
        RETURN : time difference in sec between 2 posts

        Parameters
        ----------
        i : int
            The index i of the post matrix
        j : int
            The index j of the post matrix

        Returns
        -------
        time_difference_between_posts : string
            The time difference in sec between 2 posts (i and j)

        Raises
        ------
        ValueError
            if index i or j < 0

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
        if i < 0 or j < 0:
            print(colored("Index must be greater or equal to 0!", error_col))
            raise ValueError
        # am i on profile?
        if not self.ig_navigation.am_i_on_a_profile():
            print(colored("You are not on a profile, maybe on a post to close!", warning_col))
            return None
        # Delta Time
        if i == j:
            print(colored("Error : i should be different from j!", warning_col))
            return None
        else:
            self.ig_navigation.open_post_i(i)
            time.sleep(2)
            time_post_i = self.get_time_posted_difference()
            time.sleep(2)
            self.ig_navigation.close_post()
            self.ig_navigation.open_post_i(j)
            time.sleep(2)
            time_post_j = self.get_time_posted_difference()
            time.sleep(1)
            try:
                diff = time_post_j - time_post_i
                return np.abs(diff)
            except:
                print(colored("Some error happened during time difference btw posts!", error_col))
                return None

    def get_hashtags_exposure(self, hashtags_list, method="sum"):
        """
        RETURN : a measure of hashtag exposure
                (sum, avg or etc of n posts under all list of hashtags)

        Parameters
        ----------
        hashtags_list : list []
            An hashtag list to analyze
        method (optional): string  ("sum", "avg")
            The method to compute the exposure feature

        Returns
        -------
        hashtag_exposure : int (or float)
            The hashtag exposure of an hashtag list
            or None

        Notes
        -----
        TO DO : FIX for other languages'exposure (chinese, russian, etc hashtags)!
        TO DO : some bug! maybe too fast, add explicit wait
        TO DO : add other methods

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        # exposure
        if len(hashtags_list) == 0:
            print(colored("Hashtag list is empty, cannot compute exposure!", warning_col))
            return None
        exposure = 0
        for hashtag in hashtags_list:
            valid = self.ig_bot.go_to_URL('https://www.instagram.com/explore/tags/{}/'.format(hashtag))
            if valid == 1:
                time.sleep(1)
                try:
                    popularity_of_hashtag = self.ig_bot.driver.find_element_by_class_name('g47SY ').text
                except:
                    popularity_of_hashtag = 0
                print(colored("Popularity of {}: {}".format(hashtag, popularity_of_hashtag), main_col))
                exposure += parse_2_int(popularity_of_hashtag)

        if method == "avg":
            exposure = exposure/len(hashtags_list)
        elif method == "sum":
            pass

        return exposure

    def my_followers_list(self):
        """
        RETURN : a list - all my followers'usernames
        works : ONLY IN NON HEADLESS MODE (to fix)

        Parameters
        ----------
        None

        Returns
        -------
        my_followers : string list []
            My followers list (all usernames)

        Notes
        -----
        TO DO : fix headless mode !!

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        valid = self.ig_bot.go_to_URL('https://www.instagram.com/accounts/access_tool/accounts_following_you')
        if valid == 1:
            while True:
                time.sleep(1)
                try:
                    followers_names = self.ig_bot.driver.find_elements_by_class_name('-utLf')
                    time.sleep(0.1)
                    more_followers_button = self.ig_bot.driver.find_element_by_xpath("//main[@class='fIcML']//button")
                    more_followers_button.click()
                except:
                    break
            followers_names = self.ig_bot.driver.find_elements_by_class_name('-utLf')
            followers = []
            for i in range(len(followers_names)):
                followers.append(followers_names[i].text)
            return followers

    def my_following_list(self):
        """
        RETURN : a list - all my following'usernames
        works : ONLY IN NON HEADLESS MODE (to fix)

        Parameters
        ----------
        None

        Returns
        -------
        my_following : string list []
            My following list (all usernames)

        Notes
        -----
        TO DO : fix headless mode !!

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        valid = self.ig_bot.go_to_URL('https://www.instagram.com/accounts/access_tool/accounts_you_follow')
        if valid == 1:
            time.sleep(2)
            while True:
                time.sleep(1)
                try:
                    following_names = self.ig_bot.driver.find_elements_by_class_name('-utLf')
                    time.sleep(0.1)
                    more_following_button = self.ig_bot.driver.find_element_by_xpath("//main[@class='fIcML']//button")
                    more_following_button.click()
                except:
                    break
            following_names = self.ig_bot.driver.find_elements_by_class_name('-utLf')
            following = []
            for i in range(len(following_names)):
                following.append(following_names[i].text)
            return following

    def my_followers_following_DFs(self):
        """
        RETURN : my Follower List and my Following List in 2 dfs

        Parameters
        ----------
        None

        Returns
        -------
        my_following_followers_DFs : DataFrame (pandas) list [df1, df2]
            Two DataFrames with
                df1 = Followers list,
                df2 = Following list

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
        # print status
        print(colored("Collectiong my Followers & Following Lists...", main_col))
        # get followers and following
        datetime_check = datetime.datetime.now()
        followers = self.my_followers_list()
        following = self.my_following_list()
        # save info in 2 dfs
        myFollowersDF = pd.DataFrame({"Time": len(followers)*[datetime_check],
                                      "Followers": followers})
        myFollowingDF = pd.DataFrame({"Time": len(following)*[datetime_check],
                                      "Following": following})
        print(colored("Done !", main_col))
        return [myFollowersDF, myFollowingDF]

    """ *** BETA *** """

    def get_usernames_from_list(self, limit, mode="tab", df_col_name="",
                                save_step=1000, save_string="file",
                                save_secure=True, save_path="./",
                                time_step=0, step=4, print_mode=True,
                                which_list="followers"):
        """
        RETURN : a list of usernames collected from a popup scrollable list
        works : ONLY IN NON HEADLESS MODE (fix)

        Parameters
        ----------
        limit : int
            The limit of unique usernames to collect
        mode (optional) : string ("slide", "tab")
            Method used to scroll down the list
        df_col_name (optional) : string
            DataFrame column name
        save_step (optional) : int
            Save the df in an xls file every save_step
        save_string (optional) : string
            The filename for the save_step process
        save_secure (optional) : bool
            Wanna allow the save secure process?
        save_path (optional) : string
            The save path for the save secure process
        time_step (optional) : float
            Time step between each Key press
        step (optional) : int
            How many times to press the Key per cycle
            (4 for a tab mode, others suggested for slide)
        print_mode (optional) : bool
            Print every 100 usernames grabbed?

        Returns
        -------
        unique_usernames_list : string list []
            The unique username list collected

        Notes
        -----
        TO DO : fix in headless mode

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        if mode == "slide":
            try:
                users_list = []
                unique_users_list = []
                # begin!
                i = 0
                # be sure i am on the popup list!
                # go on list with TAB
                self.ig_bot.press_key_N_times(self.ig_bot.Key.TAB, 4, time_step=time_step)
                # go on list with click
                self.ig_bot.move_and_click_element(self.ig_bot.driver.find_elements_by_class_name('wFPL8 ')[0])
                time.sleep(0.5)
                # a range - not precise it stops before!!!
                while len(unique_users_list) < limit - 10:
                    # to save every save_step times
                    if save_secure:
                        if ((i+1) % save_step) == 0:
                            save_to_xls(save_path + save_string,
                                        pd.DataFrame({df_col_name: users_list}))

                    # ok proceed! next users
                    self.ig_bot.press_key_N_times(self.ig_bot.Key.SPACE, step, time_step=time_step)

                    # grab usernames
                    username_elements = self.ig_bot.driver.find_elements_by_xpath("//div[@class='d7ByH']/a")
                    users = [u.text for u in username_elements]

                    # append to users_list
                    users_list.extend(users)

                    # next user
                    i += 1

                    unique_users_list = list(np.unique(users_list))
                    print(colored("Unique list : {}/{}".format(len(unique_users_list), limit), main_col))

                # unique filter:
                unique_users_list = unique_users_list[:limit]
                print(colored("\nUnique usernames check (unique/total) : {}/{}\n".format(len(unique_users_list), limit), main_col))

                return unique_users_list
            except:
                print(colored("You are not on a scrollable list!", error_col))
        elif mode == "tab":
            try:
                users_list = []
                # begin!
                i = 0
                while i < limit:
                    # to measure time performance
                    time_init = time.time()
                    # to save every save_step times
                    if save_secure:
                        if ((i+1) % save_step) == 0:
                            save_to_xls(save_path + save_string,
                                        pd.DataFrame({df_col_name: users_list}))

                    # is the rest of the list loaded?
                    if limit - i > 20:        # NOT when the list is finished!
                        wait = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.CLASS_NAME,
                                                                         "oMwYe", time_out=100)
                        if wait == 0:
                            save_to_xls(save_path + "TIMEOUT_ERROR_" + save_string,
                                        pd.DataFrame({df_col_name: users_list}))
                            self.ig_bot.refresh_page()
                            if which_list == "followers":
                                self.ig_navigation.open_followers_list()
                            elif which_list == "following":
                                self.ig_navigation.open_following_list()

                    # ok proceed! next user
                    self.ig_bot.press_key_N_times(self.ig_bot.Key.TAB, step, time_step=time_step)

                    # grab username
                    username_element = self.ig_bot.driver.switch_to.active_element
                    user = username_element.get_attribute("title")

                    # autotune TAB - to manage a bug that sometimes occures
                    while user is None or user == "":
                        self.ig_bot.press_key(self.ig_bot.Key.TAB)
                        time.sleep(time_step)
                        username_element = self.ig_bot.driver.switch_to.active_element
                        user = username_element.get_attribute("title")

                    # check if restarted from beginning!
                    if user in users_list:
                        print(colored("List restarted from the beginning!",
                                      error_col))
                        if (limit - i) <= 20:
                            break
                        if limit >= 10000:
                            if i > 10000:
                                break
                        # this user doesn't count!
                        i -= 1

                    # append to users_list
                    users_list.append(user)
                    if print_mode:
                        if ((i+1) % 100) == 0:
                            print(colored("username {}/{}\tdelta_t = {}\t{}".format(i+1,
                                          limit, round(time.time()-time_init, 2), user),
                                          main_col))
                    # next user
                    i += 1

                unique_users_list = list(np.unique(users_list))
                print(colored("\nUnique usernames check (unique/total) : {}/{}\n".format(len(unique_users_list), limit), main_col))

                return unique_users_list
            except:
                print(colored("You are not on a scrollable list!", error_col))

    def get_followers_list(self, username=None, mode="tab", df_col_name="Followers",
                           limit_followers=None,
                           save_step=1000, save_secure=True, save_path="./",
                           time_step=0, step=4, print_mode=True):
        """
        RETURN : all or part (set limit) of the followers list of an user

        Parameters
        ----------
        username (optional): string
            The username to go to
        mode (optional) : string ("slide", "tab")
            Method used to scroll down the list
        df_col_name (optional) : string
            DataFrame column name
        limit_followers (optional): int
            The limit of unique usernames to collect
        save_step (optional) : int
            Save the df in an xls file every save_step
        save_string (optional) : string
            The filename for the save_step process
        save_secure (optional) : bool
            Wanna allow the save secure process?
        save_path (optional) : string
            The save path for the save secure process
        time_step (optional) : float
            Time step between each Key press
        step (optional) : int
            How many times to press the Key per cycle
            (4 for a tab mode, others suggested for slide)


        Returns
        -------
        unique_followers_list : string list []
            The unique followers list collected

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
        # valid username?
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return
        else:
            if limit_followers is not None:
                limit = limit_followers
            else:
                limit = self.get_info_profile()["followers"] - 1
            # open followers list
            self.ig_navigation.open_followers_list()
            time.sleep(4)
            # grab followers list
            list_followers = self.get_usernames_from_list(limit,
                                                          save_step=save_step, mode=mode, df_col_name=df_col_name,
                                                          save_string="followersList_{}".format(username),
                                                          save_secure=save_secure, save_path=save_path,
                                                          time_step=time_step, step=step, print_mode=print_mode)

            return list_followers

    def get_following_list(self, username=None, mode="tab", df_col_name="Following",
                           limit_following=None,
                           save_step=1000, save_secure=True, save_path="./",
                           time_step=0, step=4, print_mode=True):
        """
        RETURN : all or part (set limit) of the following list of an user

        Parameters
        ----------
        username (optional): string
            The username to go to
        mode (optional) : string ("slide", "tab")
            Method used to scroll down the list
        df_col_name (optional) : string
            DataFrame column name
        limit_following (optional): int
            The limit of unique usernames to collect
        save_step (optional) : int
            Save the df in an xls file every save_step
        save_string (optional) : string
            The filename for the save_step process
        save_secure (optional) : bool
            Wanna allow the save secure process?
        save_path (optional) : string
            The save path for the save secure process
        time_step (optional) : float
            Time step between each Key press
        step (optional) : int
            How many times to press the Key per cycle
            (4 for a tab mode, others suggested for slide)


        Returns
        -------
        unique_following_list : string list []
            The unique following list collected

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
        # valid username?
        valid = 1
        if username is not None:
            valid = self.ig_navigation.go_to_username(username=username)

        if valid != 1:
            return
        else:
            if limit_following is not None:
                limit = limit_following
            else:
                limit = self.get_info_profile()["following"] - 1
            # open followers list
            self.ig_navigation.open_following_list()
            time.sleep(4)
            # grab following list
            list_following = self.get_usernames_from_list(limit,
                                                          save_step=save_step, mode=mode,
                                                          df_col_name=df_col_name,
                                                          save_string="followingList_{}".format(username),
                                                          save_secure=save_secure, save_path=save_path,
                                                          time_step=time_step, step=step, print_mode=print_mode,
                                                          which_list="following")

            return list_following  