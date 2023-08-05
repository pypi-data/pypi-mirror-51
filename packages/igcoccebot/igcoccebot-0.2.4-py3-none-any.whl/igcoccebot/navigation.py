"""

Created on 01/03/2019 by Lorenzo Coacci

IGNavigation : defines the class
IGNavigation(IGCocceBot bot) with the basic commands
for navigating on Instagram.

"""

# * * * * LIBRARIES * * * *
from termcolor import colored
# to manage time
import time

# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"


# * * * * CLASS * * * *
class IGNavigation():
    """
    IGNavigation : the Instagram navigation functions for IGCocceBot

    A class that implements the IGCocceBot to navigate on Instagram easily

    Parameters
    ----------
    bot : IGCocceBot
        The initialized IGCocceBot

    Attributes
    ----------
    ig_bot : IGCocceBot (bot)
        An IGCocceBot

    Methods
    -------
    go_to_username(username) : int
    go_to_explore() : int
    go_to_feed() : int
    go_to_settings() : int
    is_page_valid() : bool
    is_private(username=None,
               string_to_check="This Account is Private") : bool
    is_video() : bool
    is_image() : bool
    am_i_following(username=None, where="profile",
                   string_to_check="Following") : bool
    am_i_followed(username=None, where="profile",
                  string_to_check="Follow back") : bool
    am_i_on_a_post() : bool
    am_i_on_a_profile() : bool
    select_post_i(i, username=None,
                  time_tab=0.3) : int
    open_post_i(i, username=None,
                time_tab=0.3) : int
    close_post(time_before=0.5, time_after=0.5,
               class_close_button='ckWGn') : int
    next_post(time_before=0.5, time_after=0.5) : int
    previous_post(time_before=0.5, time_after=0.5) : int
    next_image() : int
    previous_image() : int
    search_bar(string_to_write) : int
    open_followers_list(string_to_check="followers") : int
    open_following_list(string_to_check="following") : int

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

    def go_to_username(self, username):
        """
        RETURN : status code - go to username page

        Parameters
        ----------
        username : string
            The username to go to

        Returns
        -------
        status code : int
            1 = everything ok
            0 = username doesn't exist - invalid
           -1 = timeout while loading
           -2 = invalid URL
           -3 = some error

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
        result = self.ig_bot.go_to_URL("https://www.instagram.com/{}/".format(username))
        if result == 1:
            # IG validity of the page, this username exists?
            valid = 1 if self.is_page_valid() else 0
        elif result == -1:
            return -1
        elif result == -2:
            return -2
        else:
            return -3

        return valid

    def go_to_explore(self):
        """
        RETURN : status code - go to explore page

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = everything ok
            0 = some error

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
        result = self.ig_bot.go_to_URL("https://www.instagram.com/explore/")
        if result == 1:
            return 1
        else:
            return 0

    def go_to_feed(self):
        """
        RETURN : status code - go to feed page

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = everything ok
            0 = some error

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
        result = self.ig_bot.go_to_URL("https://www.instagram.com/")
        if result == 1:
            return 1
        else:
            return 0

    def go_to_settings(self):
        """
        RETURN : status code - go to settings page

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = everything ok
            0 = some error

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
        result = self.ig_bot.go_to_URL("https://www.instagram.com/accounts/edit/")
        if result == 1:
            return 1
        else:
            return 0

    def is_page_valid(self):
        """
        RETURN : a bool - is the page valid?

        Parameters
        ----------
        None

        Returns
        -------
        is_page_valid : bool

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
        try:
            header = self.ig_bot.driver.find_element_by_xpath("//h2")
            invalid_text = header.text
            if "Sorry" in invalid_text:
                print(colored("Invalid IG page!", error_col))
                return False
            return True
        except:
            return True

    def is_private(self, username=None,
                   string_to_check="This Account is Private"):
        """
        RETURN : a bool - is the page valid?

        Parameters
        ----------
        username (optional): string
            The username to go to
        string_to_check (optional): string
            String to check to assert privacy

        Returns
        -------
        is_private : bool

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
            valid = self.go_to_username(username=username)

        if valid != 1:
            print(colored("An error occured while loading username!",
                          error_col))
        else:
            # am i on profile?
            if not self.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", error_col))
                return
            try:
                text = self.ig_bot.driver.find_element_by_class_name('rkEop').text
                if text == string_to_check:
                    return True
            except:
                return False

    def is_video(self):
        """
        RETURN : bool - is the post a video?

        Parameters
        ----------
        None

        Returns
        -------
        is_video : bool

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
        on_a_post = self.am_i_on_a_post()
        if on_a_post:
            try:
                video_button = self.ig_bot.driver.find_element_by_class_name('QvAa1 ')
                return True
            except:
                return False
        else:
            print(colored("Cannot check if is a video! You are not on a Post!",
                  error_col))

    def is_image(self):
        """
        RETURN : bool - is the post an image?

        Parameters
        ----------
        None

        Returns
        -------
        is_video : bool

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
        on_a_post = self.am_i_on_a_post()
        if on_a_post:
            is_a_video = self.is_video()
            if is_a_video:
                return False
            return True
        else:
            print(colored("Cannot check if is an image! You are not on a Post!", error_col))

    """ TO DO : work in progress...
    def is_verified(self):
    """

    def am_i_following(self, username=None, where="profile",
                       string_to_check="Following"):
        """
        RETURN : bool - am i following this user?
        works : ONLY IN NON HEADLESS (fix)

        Parameters
        ----------
        username (optional): string
            The username to go to
        where (optional): string
            "profile" or "post"
        string_to_check (optional): string
            String to check

        Returns
        -------
        am_i_following : bool

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
            valid = self.go_to_username(username=username)

        if valid != 1:
            print(colored("An error occured while loading username!",
                          error_col))
        else:
            try:
                if where == "profile":
                    # am i on profile?
                    if not self.am_i_on_a_profile():
                        print(colored("You are not on a profile, maybe on a post to close!", error_col))
                        return
                    follow_button = self.ig_bot.driver.find_element_by_css_selector('button')
                elif where == "post":
                    # am i on post?
                    if not self.am_i_on_a_post():
                        print(colored("You are not on a post!", error_col))
                        return
                    follow_button = self.ig_bot.driver.find_element_by_xpath("//div[@class='bY2yH']//button")

                if (follow_button.text == string_to_check):
                    return True
                else:
                    return False
            except:
                print(colored("Can't find follow button!", error_col))

    def am_i_followed(self, username=None, where="profile",
                      string_to_check="Follow back"):
        """
        RETURN : bool - am i followed by this user?
        works : ONLY IN NON HEADLESS (fix)

        Parameters
        ----------
        username (optional): string
            The username to go to
        where (optional): string
            "profile" or "post"
        string_to_check (optional): string
            String to check

        Returns
        -------
        am_i_followed : bool

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
            valid = self.go_to_username(username=username)

        if valid != 1:
            print(colored("An error occured while loading username!",
                          error_col))
        else:
            try:
                if where == "profile":
                    # am i on profile?
                    if not self.am_i_on_a_profile():
                        print(colored("You are not on a profile, maybe on a post to close!", error_col))
                        return
                    # if I am following cannot determine
                    if self.am_i_following(where="profile"):
                        print(colored("Cannot determine becuase you are following this user!", error_col))
                        return
                    follow_button = self.ig_bot.driver.find_element_by_css_selector('button')
                elif where == "post":
                    # am i on post?
                    if not self.am_i_on_a_post():
                        print(colored("You are not on a post!", error_col))
                        return
                    # if I am following cannot determine
                    if self.am_i_following(where="post"):
                        print(colored("Cannot determine becuase you are following this user!", error_col))
                        return
                    follow_button = self.ig_bot.driver.find_element_by_xpath("//div[@class='bY2yH']//button")

                if (follow_button.text == string_to_check):
                    return True
                else:
                    return False
            except:
                print(colored("Can't find follow button!", error_col))

    def am_i_on_a_post(self):
        """
        RETURN : bool - are you looking a post (is it open)?

        Parameters
        ----------
        None

        Returns
        -------
        am_i_on_a_post : bool

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
        try:
            post_url = self.ig_bot.driver.current_url
            post_pre_code = post_url.split('/')[3]
            if post_pre_code == 'p':
                return True
            return False
        except:
            return False

    def am_i_on_a_profile(self):
        """
        RETURN : bool - are you on a profile?

        Parameters
        ----------
        None

        Returns
        -------
        am_i_on_a_profile : bool

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
        try:
            if self.am_i_on_a_post():
                return False
            username_element = self.ig_bot.driver.find_element_by_xpath("//div[@class='nZSzR']/h1")
            username = username_element.text
            if username == '':
                return False
            try:
                # check it if a list is open
                header_elem = self.ig_bot.driver.find_element_by_xpath("//h1[@class='m82CD']/div")
                return False
            except:
                return True
        except:
            return False

    def select_post_i(self, i, username=None,
                      time_tab=0.3):
        """
        RETURN : status code - select post i (from i=0) in a post matrix

        Parameters
        ----------
        i : int, >0
            The index of the post matrix
        username (optional): string
            The username to go to
        time_tab (optional): float
            The time between selection to go to post i from i=0


        Returns
        -------
        status code : int
            1 = selected,
            0 = some error,
           -1 = not on profile,
           -2 = private profile

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

        # valid username?
        valid = 1
        if username is not None:
            valid = self.go_to_username(username=username)

        if valid != 1:
            return 0
        else:
            # am i on profile?
            if not self.am_i_on_a_profile():
                print(colored("You are not on a profile, maybe on a post to close!", error_col))
                return 0
            # is it private?
            if self.is_private():
                print(colored("Cannot open/select any post, this profile is Private!", error_col))
                return 0
            try:
                x_path_posts = "//div//a[contains(@href, '/p/')]"
                # get the posts grid nx3
                posts = self.ig_bot.driver.find_elements_by_xpath(x_path_posts)
                time.sleep(0.5)
                posts[0].click()
            except:
                try:
                    # another approach if xpath fails! - Security feature
                    class_posts = 'v1Nh3 kIKUG  _bz0w'
                    # first post
                    post_0 = self.ig_bot.driver.find_element_by_class_name(class_posts)[0]
                    time.sleep(0.5)
                    # click first post
                    post_0.click()
                except:
                    print(colored("Cannot find or click/open the " +
                                  "post index: {}".format(i), error_col))
                    return 0
            time.sleep(0.5)
            if i > 0:
                # go to post[i]
                for n in range(i):
                    time.sleep(2)
                    if n == 0:
                        self.ig_bot.press_key(self.ig_bot.Key.ENTER)
                        # self.ig_bot.press_key(self.ig_bot.Key.ARROW_RIGHT)
                    else:
                        self.next_post()
                time.sleep(0.2)
                # post i selected!
                return 1
            else:
                # post 0 selected!
                return 1

    def open_post_i(self, i, username=None,
                    time_tab=0.3):
        """
        RETURN : status code - click & open post i (from i=0) in post matrix

        Parameters
        ----------
        i : int, >0
            The index of the post matrix
        username (optional): string
            The username to go to
        time_tab (optional): float
            The time between selection to go to post i from i=0


        Returns
        -------
        status code : int
            1 = opened,
            0 = some error,
           -1 = not on profile,
           -2 = private profile

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

        # select the post
        result = self.select_post_i(i, username=username, time_tab=time_tab)
        if result == 1:
            # wait post to load
            wait = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.CLASS_NAME, 'fr66n')
            if wait == 0:
                return 0
            wait2 = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.XPATH, "//div[@class='ZyFrc']/div/div/img",
                                                              show_debug=False)
            if wait2 == 0:
                wait3 = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.XPATH, "//div[@class='ZyFrc']/div/div/div/img",
                                                                  show_debug=False)
                if wait3 == 0:
                    if self.is_video():
                        return result
                    else:
                        return 0
            # ok the post is opened
            return result
        else:
            return result

    def close_post(self, time_before=0.5, time_after=0.5,
                   class_close_button='ckWGn'):
        """
        RETURN : status code - close a temporary opened post

        Parameters
        ----------
        time_before (optional): float
            The time to wait before the click
        time_after (optional): float
            The time to wait after the click
        class_close_button (optional): string
            The class of the X close button

        Returns
        -------
        status code : int
            1 = closed
            0 = some error

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
        if self.am_i_on_a_post():
            try:
                time.sleep(time_before)
                self.ig_bot.driver.find_element_by_class_name(class_close_button).click()
                time.sleep(time_after)
                if self.am_i_on_a_post():
                    return 0
                return 1
            except:
                print(colored("Cannot find X butt to close a post", error_col))
                print(colored("Trying instead the ESC Key", main_col))
                time.sleep(time_before)
                self.ig_bot.press_key(self.ig_bot.Key.ESCAPE)
                time.sleep(time_after)
                if self.am_i_on_a_post():
                    return 0
                return 1
        else:
            print(colored("No need to close a post, you are not on it...",
                  error_col))
            return 0

    def next_post(self, time_before=0.5, time_after=0.5):
        """
        RETURN : status code - go to next post

        Parameters
        ----------
        time_before (optional): float
            The time to wait before the click
        time_after (optional): float
            The time to wait after the click


        Returns
        -------
        status code : int
            1 = done
            0 = some error

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
        if self.am_i_on_a_post():
            try:
                arrows = self.ig_bot.driver.find_elements_by_xpath("//div[@class='D1AKJ']/a")
                next_arrow = arrows[1]
                if next_arrow.text == "Next":
                    time.sleep(time_before)
                    next_arrow.click()
                    time.sleep(time_after)
                    return 1
                print(colored("Cannot find next arrow or something strange happened", error_col))
                return 0
            except:
                print(colored("Cannot find arrows to perform next post", error_col))
        else:
            print(colored("You are not on a post, cannot perform prev post method...",
                  error_col))
            return 0

    def previous_post(self, time_before=0.5, time_after=0.5):
        """
        RETURN : status code - go to previous post

        Parameters
        ----------
        time_before (optional): float
            The time to wait before the click
        time_after (optional): float
            The time to wait after the click


        Returns
        -------
        status code : int
            1 = done
            0 = some error

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
        if self.am_i_on_a_post():
            try:
                arrows = self.ig_bot.driver.find_elements_by_xpath("//div[@class='D1AKJ']/a")
                prev_arrow = arrows[0]
                if prev_arrow.text == "Previous":
                    time.sleep(time_before)
                    prev_arrow.click()
                    time.sleep(time_after)
                    return 1
                print(colored("Cannot find next arrow or something strange happened", error_col))
                return 0
            except:
                print(colored("Cannot find arrows to perform next post", error_col))
        else:
            print(colored("You are not on a post, cannot perform prev post method...",
                  error_col))
            return 0


    """ TO DO : work in progress...
    def change_to_tagged(self):
        pass
    """

    """ TO DO : work in progress...
    def change_to_IGTV(self):
        pass
    """

    """ TO DO : work in progress...
    def change_to_posts(self):
        pass
    """

    def next_image(self):
        """
        RETURN : status code - go to next image

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = done
            0 = some error

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
        # go to next image in multiple images
        try:
            self.ig_bot.driver.find_element_by_class_name('  _6CZji').click()
            return 1
        except:
            print(colored("Cannot go to next image, no ohter images on the right...", error_col))
            return 0

    def previous_image(self):
        """
        RETURN : status code - go to previous image

        Parameters
        ----------
        None

        Returns
        -------
        status code : int
            1 = done
            0 = some error

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
        # go to previous image in multiple images
        try:
            self.ig_bot.driver.find_element_by_class_name(' POSa_ ').click()
            return 1
        except:
            print(colored("Cannot go to previous image, no ohter images on the left...", error_col))
            return 0

    """ TO DO : work in progress...
    def search_bar(self, string_to_write):
        RETURN : status code - write a string in the search bar

        Parameters
        ----------
        string_to_write : string
            The string to send to the search bar

        Returns
        -------
        status code : int
            1 = done
            0 = some error

        Notes
        -----
        TO DO : add notes

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        #try:
        # find search bar on the top nav
        search_elem = self.ig_bot.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        # select it
        self.ig_bot.move_and_click_element(search_elem)
        # clear text
        search_elem.clear()
        time.sleep(1)
        # write keys
        self.ig_bot.write_keys(string_to_write)
        return 1
        #except:
        #    print(colored("Some error happened with the search bar elem", error_col))
        #    return 0
    """

    def open_followers_list(self, string_to_check="followers"):
        """
        RETURN : status code - open followers list

        Parameters
        ----------
        string_to_check (optional): string
            String to check

        Returns
        -------
        status code : int
            1 = opened,
            0 = some error,
           -1 = not on profile,
           -2 = private profile

        Notes
        -----
        Warning : little bug to fix, if you are down on the profile,
        it will try to go to the top but still miss the button

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        # am i on profile?
        if not self.am_i_on_a_profile():
            print(colored("You are not on a profile, maybe on a post to close!", error_col))
            return -1
        # is it private?
        if self.is_private():
            print(colored("Cannot open followers list, this profile is Private!", error_col))
            return -2
        # refrsh page to avoid the scroll down page bug
        self.ig_bot.refresh_page()
        try:
            followers_list_button = self.ig_bot.driver.find_elements_by_xpath("//li[@class='Y8-fY ']/a")
            if string_to_check in followers_list_button[0].get_attribute("href"):
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(followers_list_button[0])
            elif string_to_check in followers_list_button[1].get_attribute("href"):
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(followers_list_button[1])
            elif string_to_check in followers_list_button[2].get_attribute("href"):
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(followers_list_button[2])
            else:
                print(colored("Not going to click the followers button list!" +
                              "maybe different language in parameters",
                              error_col))
                return 0

            # check if it has been opened
            try:
                # wait the header
                wait = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.XPATH,
                                                                 "//h1[@class='m82CD']/div")
                if wait == 0:
                    return 0
                # check it
                header_elem = self.ig_bot.driver.find_element_by_xpath("//h1[@class='m82CD']/div")
                header = header_elem.text
                if header.lower() == string_to_check:
                    return 1
                else:
                    print(colored("List Title is not matching with the string_to_check parameter!", error_col))
                    return 0
            except:
                print(colored("Followers List has been clicked but not opened!", error_col))
                return 0
        except:
            print(colored("Cannot find followers list button", error_col))
            return 0

    def open_following_list(self, string_to_check="following"):
        """
        RETURN : status code - open following list

        Parameters
        ----------
        string_to_check (optional): string
            String to check

        Returns
        -------
        status code : int
            1 = opened,
            0 = some error,
           -1 = not on profile,
           -2 = private profile

        Notes
        -----
        Warning : little bug to fix, if you are down on the profile,
        it will try to go to the top but still miss the button

        See Also
        --------
        TO DO : add something

        Examples
        --------
        TO DO : add something
        """
        # am i on profile?
        if not self.am_i_on_a_profile():
            print(colored("You are not on a profile, maybe on a post to close!", error_col))
            return -1
        # is it private?
        if self.is_private():
            print(colored("Cannot open following list, this profile is Private!", error_col))
            return -2
        # refrsh page to avoid the scroll down page bug
        self.ig_bot.refresh_page()
        try:
            following_list_button = self.ig_bot.driver.find_elements_by_xpath("//li[@class='Y8-fY ']/a")
            if "following" in following_list_button[1].get_attribute("href"):
                time.sleep(0.5)
                self.ig_bot.move_and_click_element(following_list_button[1])
                # check if it has been opened
                try:
                    # wait the header
                    wait = self.ig_bot.wait_element_to_be_present_by(self.ig_bot.By.XPATH,
                                                                     "//h1[@class='m82CD']/div")
                    if wait == 0:
                        return 0
                    # check it
                    header_elem = self.ig_bot.driver.find_element_by_xpath("//h1[@class='m82CD']/div")
                    header = header_elem.text
                    if header.lower() == string_to_check:
                        return 1
                    else:
                        print(colored("List Title is not matching with the string_to_check parameter!", error_col))
                        return 0
                except:
                    print(colored("Following List has been clicked but not opened!", error_col))
                    return 0
            else:
                print(colored("Not going to click the following button list!",
                              "maybe different language in parameters",
                              error_col))
                return 0
        except:
            print(colored("Cannot find following list", error_col))
            return 0
