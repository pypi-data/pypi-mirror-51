"""

Created on 01/03/2019 by Lorenzo Coacci

__init__.py (tools) : defines some
useful functions for the package

"""

# * * * * LIBRARIES * * * *
# to manage data - pandas
import pandas as pd
# to manage text colors
from termcolor import colored
# import the smtplib module
import smtplib

# * * * * Global variables * * * *
# program text colors
main_col = "white"
error_col = "red"


def parse_2_int(string):
    """
    RETURN : an int from a string removing commas and points

    Parameters
    ----------
    string : string
        A string number with points '.' or commas ',' to remove

    Returns
    -------
    number : int
        The string parse 2 int
        None if can't

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
    # try to parse to int
    try:
        string = string.replace(',', '')
        string = string.replace('.', '')
        number = int(string)
    except:
        print(colored("Cannot parse to int - returning 'NA'", error_col))
        number = None
    return number


def ask_input_int(msg_string, to_bool=False):
    """
    RETURN : Ask an int to the user and return it as int or bool

    Parameters
    ----------
    msg_string : string
        A string message for the user before the input
    to_bool : bool
        Cast the int to bool?

    Returns
    -------
    input : int (or bool)
        The user input to int (or bool), None if "None" is the input

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
    input_msg = input(msg_string)
    if input_msg == "None":
        return None
    try:
        if to_bool:
            # parse it to int and evaluate bool
            input_bool = (int(input_msg) >= 1)
            return input_bool
        else:
            # parse it to int
            input_int = int(input_msg)
            return input_int
    except:
        # cannot parse it to int
        print(colored("Error! Please enter a valid integer...", error_col))
        ask_input_int(msg_string, to_bool)   # try again!


def save_to_xls(file_name, df, show_debug=True):
    """
    RETURN : status (True/False) - save a DataFrame to an xls file

    Parameters
    ----------
    file_name : string
        The file name/file path without extension
    df : DataFrame (pandas)
        The DataFrame to save as a xls
    show_debug (optional) : bool
        Show debug info?

    Returns
    -------
    status : bool
        True = it worked
        False = some error happened
    """
    try:
        writer = pd.ExcelWriter(file_name + '.xls')
        if show_debug:
            print(colored('Writing data to Excel...', main_col))
        df.to_excel(writer, 'Sheet1', index=None, header=True)
        writer.save()
        return True
    except:
        return False


def save_to_csv(file_name, df):
    """
    VOID : save a DataFrame to csv

    Parameters
    ----------
    file_name : string
        The file name/file path without extension
    df : DataFrame (pandas)
        The DataFrame to save as a csv

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
    print(colored('Writing data to CSV...', main_col))
    df.to_csv(file_name + '.csv', sep='\t', encoding='utf-8')


def send_email(my_email, my_password, send_to, subject, message,
               host='', port=25, timeout=2):
    """
    VOID : send an email with 'host' as default host

    Parameters
    ----------
    my_email: string
        The email of the sender
    my_password : string
        The password of the sender
    send_to : string (list of strings)
        Receivers of the email
    subject : string
        The subject of the email
    message : string
        The message of the email
    host : string
        The smpt host (ex : smpt.gmail.com)
    port : int
        The port for the smpt connection
    timeout : float
        The timeout before aborting the email function

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
    # set server
    try:
        server = smtplib.SMTP_SSL(host, port, timeout=timeout)
        print(colored("SSL protocol server for email working...", main_col))
    except:
        try:
            print(colored("SSL failed! Trying non SSL...", error_col))
            server = smtplib.SMTP(host, port, timeout=timeout)
            print(colored("Server for email working...", main_col))
        except:
            print(colored("Connection to server failed!", error_col))
            return
    # login
    try:
        server.login(my_email, my_password)
        print(colored("Authentication working...", main_col))
    except:
        print(colored("Authentication failed!", error_col))
        server.quit()
        return
    try:
        server.sendmail(
            my_email,
            send_to,
            message)
        print(colored("Successfully sent email", main_col))
    except:
        print(colored("Email failed!", error_col))
        server.quit()

    server.quit()