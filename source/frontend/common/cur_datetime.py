from datetime import datetime


def cur_datetime():
    """
    return string of current date time
    this function is general so need to be in different file
    :return: string of current date time
    """
    cur_date = datetime.now().strftime("%d/%m/%y")
    cur_time = datetime.now().strftime("%H:%M:%S")
    ret = (str(cur_date) + "-" + str(cur_time))
    print(ret)
    return ret