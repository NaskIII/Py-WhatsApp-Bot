class InternetExeption(Exception):
    """
    Host machine is not connected to the Internet or the connection Speed is Slow
    """

    pass


class InvalidParameterException(Exception):
    """
    The parameter received is invalid. Choose between 1 to write in the contact search box or 2 to write in the message text box
    """

    pass
