"""

Created on 01/03/2019 by Lorenzo Coacci

IGCocceBot : defines the class
IGCocceBot() with the basic commands
for browsing the web driver with Selenium.

"""

# * * * * LIBRARIES * * * *
# to manage Web scraping - Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
# to manage time
import time
# to hide passwords
import getpass
# to manage text colors
from termcolor import colored

# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"


# * * * * CLASS * * * *
class IGCocceBot():
    """
    IGCocceBot : an Instagram bot

    A selenium webdriver capable of interacting with the
    Instagram environment.
    It is initialized with some generic browser methods
    usable not only on Instagram but also everywhere.

    Parameters
    ----------
    path_to_driver : string
        Where is the webdriver in your os
    headless (optional): bool
        Headless mode for the browser (BETA)
    no_images (optional): bool
        Do you want NOT to load images?

    Attributes
    ----------
    driver : webdriver (Selenium)
        A webdriver from Selenium
    Key : Keys (Selenium)
        The Keys from Selenium (TAB, SPACE, etc)
    By : By (Selenium)
        The By of Selenium (By.CLASS_NAME, By.ID, etc)
    Action : ActionChains(driver) (Selenium)
        The ActionChains(driver) from Selenium

    Methods
    -------
    go_to_URL(string_URL, show_debug=True) : int
    login(input_username, input_password) : void
    ask_login() : string
    refresh_page() : void
    go_back() : void
    go_forward() : void
    close_tab() : void
    quit_bot() : void
    tabs_opened(self) : strings {dict}
    open_tab(url=''): void
    change_tab(index): void
    scroll_page_down(y) : void
    infinite_scroll_page_down(time_wait) : void
    write_keys(string) : void
    where_am_i() : string
    move_and_click_element(element, time_between_move_and_click=1) : void
    move_and_double_click_element(element,
                                  time_between_move_and_click=1) : void
    move_to_element(element) : void
    move_by_offset(xoffset, yoffset) : void
    one_click() : void
    double_click() : void
    press_key(Key, down_up=False) : void
    press_key_N_times(Key, N, time_step=0.3) : void
    wait_element_to_be_present_by(by_selector,
                                  element_selector, time_out=10,
                                  show_debug=True) : int
    wait_element_to_be_visible_by(by_selector,
                                  element_selector, time_out=10,
                                  show_debug=True) : int

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
    def __init__(self, path_to_driver, headless=False, no_images=False,
                 ig_login_page='https://www.instagram.com/accounts/login/?source=auth_switcher'):
        # welcome
        print(colored("""
            ____         ______                        ____        __
           /  _/___ _   / ____/___  _____________     / __ )____  / /_
           / // __ `/  / /   / __ \/ ___/ ___/ _ \   / __  / __ \/ __/
         _/ // /_/ /  / /___/ /_/ / /__/ /__/  __/  / /_/ / /_/ / /_
        /___/\__, /   \____/\____/\___/\___/\___/  /_____/\____/\__/
            /____/""", main_col))
        print(colored('Begin setup...', main_col))
        # using Chrome + Selenium
        chrome_options = Options()    # options
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--disable-gpu')
        # english language set
        chrome_options.add_experimental_option('prefs',
                                               {'intl.accept_languages':
                                                'en,en_EN'})
        # no images
        if no_images:
            chrome_options.add_experimental_option('prefs',
                                                   {"profile.managed_default_content_settings.images": 2})
        # Open driver
        print(colored('Opening Chrome...', main_col))
        ###############
        # driver
        self.driver = webdriver.Chrome(executable_path=path_to_driver,
                                       options=chrome_options)
        # Keys
        self.Key = Keys()
        # By
        self.By = By()
        # Action
        self.Action = ActionChains(self.driver)
        ###############
        print(colored('End setup...', main_col))
        print(colored('Opening Instagram...', main_col))
        # log in page
        self.go_to_URL(ig_login_page)

    def go_to_URL(self, string_URL, show_debug=True,
                  time_out=10):
        """
        RETURN : status code, go to URL(type_your_URL)

        Parameters
        ----------
        string_URL : string
            The URL to go to
        show_debug (optional): bool
            Show the debug info about status code?

        Returns
        -------
        status code : int
            1 = everything ok
            0 = Invalid URL
           -1 = No internet
           -2 = DNS error no URL
           -3 = Another Error

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
        # go to URL
        self.driver.set_page_load_timeout(time_out)
        try:
            self.driver.get(string_URL)
        except TimeoutException:
            print(colored("Timeout while loading page!", error_col))
            return -1
        except WebDriverException:
            # URL doesn't exist!
            if show_debug:
                print(colored("Invalid URL!", error_col))
            return 0
        except:
            if show_debug:
                print(colored("Another Error occured!", error_col))

        # any other problem?
        try:
            # error code text
            error = self.driver.find_element_by_class_name('error-code').text
            if error == 'ERR_INTERNET_DISCONNECTED':
                if show_debug:
                    print(colored('No Internet Connection!', error_col))
                return -2
            elif error == 'ERR_NAME_NOT_RESOLVED':
                if show_debug:
                    print(colored('Cannot find the URL (DNS error)!',
                          error_col))
                return -3
            if show_debug:
                print(colored("Another Internet Error occured!", error_col))
            return -4
        except:
            # everything is OK ! Hurray!
            if show_debug:
                print(colored("The URL is ok!", main_col))
            return 1

    def login(self, input_username, input_password):
        """
        RETURN : status code, write user + pass to access Instagram

        Parameters
        ----------
        input_username : string
            The Instagram username
        input_password : string
            The Instagram password

        Returns
        -------
        status code : int
            1 login succsessful
            0 login failed

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
        # find username and password field
        try:
            username_field = self.driver.find_element_by_name('username')
            password_field = self.driver.find_element_by_name('password')
        except:
            username_field = self.driver.find_element_by_id("fc9079168d6328")
            password_field = self.driver.find_element_by_id('fc2ad31c4193d')
        # Insert username & password
        try:
            username_field.clear()                        # clear username field
            username_field.send_keys(input_username)      # insert username
            password_field.clear()                        # clear password field
            password_field.send_keys(input_password)      # insert password
            password_field.send_keys(Keys.ENTER)          # press Enter Button
            time.sleep(10)

            # To manage IG suspicious Login procedure
            try:
                # find suspicious alert panel
                self.driver.find_element_by_class_name('O4QwN')
                # fix it and send code
                try:
                    # via text message if present
                    cell_radio_button = self.driver.find_element_by_xpath("//*[@id='react-root']/section/div/div/div[3]/form/div/div[2]/label/div")
                    self.move_and_click_element(cell_radio_button)
                except:
                    pass
                print(colored("IG Suspicious login procedure begins!", main_col))
                time.sleep(2)
                try:
                    # click ok button and send code
                    ok_button = self.driver.find_element_by_xpath("//*[@id='react-root']/section/div/div/div[3]/form/span/button")
                    self.move_and_click_element(ok_button)
                    # ask code
                    code = input(colored("Suspicious Login procedure! Insert IG Code: ", main_col))
                    # write code
                    code_insert_element = self.driver.find_element_by_id('security_code')
                    code_insert_element.send_keys(code)
                    # click ok button and enter IG
                    url = self.where_am_i()
                    ok_button = self.driver.find_element_by_xpath("//*[@id='react-root']/section/div/div/div[2]/form/span/button")
                    self.move_and_click_element(ok_button)
                    time.sleep(6)
                    if url == self.where_am_i():
                        print(colored("Problem with suspicious login! IG changed something or Check your code...closing process", error_col))
                        return 0
                    return 1
                except:
                    # nope
                    return 0
            except:
                # ok
                return 1
        except:
            return 0

    def ask_login(self):
        """
        RETURN : ask & try to login until your user+pass is correct,
        then return username

        Parameters
        ----------
        None

        Returns
        -------
        my_username : string
            The username you used to login

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
        # ask - - - - - - - - - - - - - - - - - - - - - - - -
        print(colored('Instagram Login:', main_col))
        my_username = input(colored('USERNAME:  ', main_col))
        password = getpass.getpass(colored('PASSWORD:  ', main_col))
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        # store URL to check
        previous_URL = self.where_am_i()
        # login
        result = self.login(my_username, password)
        time.sleep(4)
        if result == 0:
            self.quit_bot()
            return None
        # if wrong repeat!
        while previous_URL == self.where_am_i():
            print(colored('Wrong username or password!', error_col))
            # ask - - - - - - - - - - - - - - - - - - - - - - - -
            print(colored('Instagram Login:', main_col))
            my_username = input(colored('USERNAME:  ', main_col))
            password = getpass.getpass(colored('PASSWORD:  ', main_col))
            # - - - - - - - - - - - - - - - - - - - - - - - - - -
            print(colored('Logging in...', main_col))
            # clear inputs user + pass by refreshing
            self.driver.refresh()
            # store URL to check
            previous_URL = self.where_am_i()
            # try again!
            result = self.login(my_username, password)
            time.sleep(4)
            if result == 0:
                self.quit_bot()
                return None

        return my_username

    def refresh_page(self):
        """
        VOID : refresh the web page

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            self.driver.refresh()
        except:
            print(colored("Error! Cannot refresh page", error_col))

    def go_back(self):
        """
        VOID : go back

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            self.driver.back()
        except:
            print(colored("Error! Cannot go back", error_col))

    def go_forward(self):
        """
        VOID : go forward

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            self.driver.forward()
        except:
            print(colored("Error! Cannot go forward", error_col))

    def quit_bot(self):
        """
        VOID : close all driver pages and Bot

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            self.driver.quit()
        except:
            print(colored("Error! Cannot quit bot", error_col))

    def tabs_opened(self):
        """
        RETURN : the opened tabs dict with urls

        Parameters
        ----------
        None

        Returns
        -------
        tabs_dict: {index: string} (dict)
            The dict of tabs opened -> {0: "url1", 1: "url2", ...}

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
        tabs = self.driver.window_handles
        tabs_dict = {}
        for i in range(len(tabs)):
            self.change_tab(i)
            tabs_dict[i] = self.where_am_i()
        return tabs_dict

    def open_tab(self, url=''):
        """
        VOID : open a new tab and return to first tab -> tabs[0]
              (it does NOT go there!,
               to do so use change_tab(index))

        Parameters
        ----------
        url (optional): string
            The url for the new opened tab

        Returns
        -------
        void

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
            self.driver.execute_script("window.open('{}','_blank');".format(url))
            # back to where you opened the tab
            self.change_tab(0)
        except:
            print(colored("Cannot open new tab, some error occured...", error_col))

    def close_tab(self):
        """
        VOID : close current tab and select another one if exists

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            self.driver.close()
            # select the first other tab if exists
            try:
                self.change_tab(0)
            except:
                pass
        except:
            print(colored("Error! Cannot close page", error_col))

    def change_tab(self, index):
        """
        VOID : change tab and go there

        Parameters
        ----------
        index : int
            The tab index to change tab

        Returns
        -------
        void

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
        tabs = self.driver.window_handles
        n = len(tabs)
        if index >= n:
            print(colored("There are only {} tabs opened! Remember start counting from 0...".format(n), error_col))
        else:
            # switch
            self.driver.switch_to.window(tabs[index])

    def scroll_page_down(self, y):
        """
        VOID : scroll down the page to height 'y'

        Parameters
        ----------
        y : float
            The ABSOLUTE height of the page

        Returns
        -------
        void

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
        self.driver.execute_script("window.scrollTo(0, {})".format(y))

    def infinite_scroll_page_down(self, time_wait):
        """
        VOID : infinite scroll (down)

        Parameters
        ----------
        time_wait : float
            How much time to wait between each scroll down

        Returns
        -------
        void

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
        while True:
            self.scroll_page_down(100000)
            time.sleep(time_wait)

    def write_keys(self, string):
        """
        VOID : write keys / send keys

        Parameters
        ----------
        string : string
            The string to write in a form/box/placeholder...

        Returns
        -------
        void

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
            ActionChains(self.driver).send_keys(string).perform()
        except:
            print(colored("Error! Cannot write keys", error_col))

    def where_am_i(self):
        """
        RETURN : string - current URL

        Parameters
        ----------
        None

        Returns
        -------
        where_am_i : string
            The current URL
        """
        return self.driver.current_url

    def move_and_click_element(self, element,
                               time_between_move_and_click=1):
        """
        VOID : move to an object and one click mouse

        Parameters
        ----------
        element : WebElement (Selenium)
            The WebElement to move to and click
        time_between_move_and_click (optional): float
            The time between the move action and the click action

        Returns
        -------
        void

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
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(time_between_move_and_click)
            ActionChains(self.driver).click().perform()
        except:
            print(colored("Error! Cannot move and click", error_col))

    def move_and_double_click_element(self, element,
                                      time_between_move_and_click=1):
        """
        VOID : move to an object and double click mouse

        Parameters
        ----------
        element : WebElement (Selenium)
            The WebElement to move to and click
        time_between_move_and_click (optional): float
            The time between the move action and the click action

        Returns
        -------
        void

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
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(time_between_move_and_click)
            ActionChains(self.driver).double_click().perform()
        except:
            print(colored("Error! Cannot move and double click", error_col))

    def move_to_element(self, element):
        """
        VOID : move to an object

        Parameters
        ----------
        element : WebElement (Selenium)
            The WebElement to move to and click

        Returns
        -------
        void

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
            ActionChains(self.driver).move_to_element(element).perform()
        except:
            print(colored("Error! Cannot move to element", error_col))

    def move_by_offset(self, xoffset, yoffset):
        """
        VOID : move by offset the mouse

        Parameters
        ----------
        xoffset : float
            The xoffset to move mouse position
        yoffset : float
            The yoffset to move mouse position

        Returns
        -------
        void

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
            ActionChains(self.driver).move_by_offset(xoffset, yoffset).perform()
        except:
            print(colored("Error! Cannot move by offset", error_col))

    def one_click(self):
        """
        VOID : one click operation wherever the mouse is

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            ActionChains(self.driver).click().perform()
        except:
            print(colored("Error! Cannot press one click", error_col))

    def double_click(self):
        """
        VOID : double click operation wherever the mouse is

        Parameters
        ----------
        None

        Returns
        -------
        void

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
            ActionChains(self.driver).double_click().perform()
        except:
            print(colored("Error! Cannot press double click", error_col))

    def press_key(self, Key, down_up=False):
        """
        VOID : click KEY - once or twice if down_up is True

        Parameters
        ----------
        Key : Keys (Selenium)
            The Key to press (Key.SPACE, Key.TAB, etc)
        down_up (optional): bool
            Press 2 times? (down and up)

        Returns
        -------
        void

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
            if down_up:
                ActionChains(self.driver).key_down(Key).key_up(Key).perform()
            else:
                ActionChains(self.driver).key_down(Key).perform()
        except:
            print(colored("Error! Cannot press key", error_col))

    def press_key_N_times(self, Key, N, time_step=0.3):
        """
        VOID : click a KEY, N times

        Parameters
        ----------
        Key : Keys (Selenium)
            The Key to press (Key.SPACE, Key.TAB, etc)
        time_step (optional): float
            Time step between each key press

        Returns
        -------
        void

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
            # press a key multiple times
            for _ in range(N):
                self.press_key(Key)
                time.sleep(time_step)
        except:
            print(colored("Error! Cannot press key", error_col))

    def wait_element_to_be_present_by(self, by_selector, element_selector,
                                      time_out=10, show_debug=True):
        """
        RETURN : the status code - 1 found, 0 not found

        Parameters
        ----------
        by_selector : By (Selenium)
            Select element By.(CLASS_NAME ,ID, XPATH, etc)
        element_selector : string
            Class string, id string, xpath string, etc
        time_out (optional): float
            Max time waiting

        Returns
        -------
        status code : int
            1 = found
            0 = not found

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
        # is the element present?
        try:
            wait = WebDriverWait(self.driver, time_out)
            element = wait.until(EC.presence_of_element_located((by_selector,
                                                                 element_selector)))
            return 1
        except:
            if show_debug:
                print(colored("Timeout, cannot find the element!",
                    error_col))
            return 0

    def wait_element_to_be_visible_by(self, by_selector, element_selector,
                                      time_out=10, show_debug=True):
        """
        RETURN : the status code - 1 found, 0 not found

        Parameters
        ----------
        by_selector : By (Selenium)
            Select element By.(CLASS_NAME ,ID, XPATH, etc)
        element_selector : string
            Class string, id string, xpath string, etc
        time_out (optional): float
            Max time waiting

        Returns
        -------
        status code : int
            1 = found
            0 = not found

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
        # is the element present?
        try:
            wait = WebDriverWait(self.driver, time_out)
            element = wait.until(EC.visibility_of_element_located((by_selector,
                                                                  element_selector)))
            return 1
        except:
            if show_debug:
                print(colored("Timeout, cannot find the element!",
                    error_col))
            return 0