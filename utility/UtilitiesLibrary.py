import random,string,time,calendar,os,webbrowser,math,ssl
from decimal import Decimal
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from ast import literal_eval
from Selenium2Library import Selenium2Library
from selenium import webdriver
import requests
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.utils import (is_dict_like, is_string, is_truthy, plural_or_not,
                         seq2str, seq2str2, type_name, unic, Matcher)


def format_money(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = Decimal(value).quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def format_date_time_as_per_definition(string_datetime, with_ms, output_format):
    # Convert a date time string to the required format.
    # Input: a date time string in the format YYYY-MM-DD HH:MM:SS.f (e.g. 2014-12-18 13:45:58.064415) or YYYY-MM-DD HH:MM:SS (e.g. 2014-12-18 13:45:58)
    # Output: Output format is as per user's needs (e.g. "%d %b %Y" or "%d %b %Y %I:%M %p")

    myindex= string_datetime.find('.')
    #logger.console(myindex)
    # if with_ms == 'False':
    #     struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")
    #     #output_s = "%d %b %Y"
    # else:
    #     struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S.%f")
    if myindex == -1:
        struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")
    else:
        struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S.%f")

    return struct_datetime.strftime(output_format)


def title_should_start_with(expected):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    title = seleniumlib.get_title()
    if not title.startswith(expected):
        raise AssertionError("Title '%s' did not start with '%s'"
                             % (title, expected)) 
        

# This method will generate N length random digits whose first number will not be zero always
def generate_a_random_digit(lengthStr):
    length = int (lengthStr)
    final=''
    for x in range(0, length):
        randomNum = int (random.random()*10)
        if randomNum==0 and x==0:
            randomNum=1
        final=str(final)+str(randomNum)         
    return  final   


# This method will generate N length random Letters
def generate_a_random_word(lengthStr):
    length = int (lengthStr)
    final=''
    for x in range(0, length):
        randomNum = random.choice(string.letters)
        final=str(final)+str(randomNum)         
    return  final   


# Return the year, according to the input
def get_year(argStr=0):
    arg= int (argStr)
    currentYear= datetime.now().year
    expYear=currentYear+arg
    return   expYear
# Verify If the element Present in the page


def verify_element_is_visible(id):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    browser = seleniumlib._current_browser()
    elements = seleniumlib._element_finder.find(browser, id, None)
    if len(elements) ==  0:
         return 0
    else:
        return 1


def append_element_ids(list,lengthStrStart,lengthStrEnd):
    finalList=[]
    start=int (lengthStrStart)
    end= int (lengthStrEnd)
    for i in list:
         for j in range(start, end):
             finalList.append(i+str(j))
    return   finalList  


def create_list_of_xpaths(list,str,replace_word):
    finalList=[]
    for i in list:
        finalList.append(str.replace(replace_word,i))
    return   finalList   


def generate_random_data(lenStr,typeStr, valueStr):
    if  valueStr:
        #raise AssertionError("No NO random value   valueStr=  %s"%(valueStr))
        return  valueStr
    len = int (lenStr)
    type = int  (typeStr)
    finalData = ''
    if type == 0:
        print "Alphabets"
        finalData = generate_a_random_word(len)
    elif  type == 1:
        print  "Numerics"
        finalData = generate_a_random_digit(len)
    elif  type == 2:
        print   "Alphanumerics"
    elif  type == 3:   
        print "Special"
    return  finalData


def generate_xpaths_with_attribute(tag,list,atrr):
    finalList=[] 
    for i in list:
        xpath= '//'+tag+'[@'+atrr+'=\"'+i+'\"]'
        finalList.append(xpath)
    return finalList  


def do_special_click(id,attribute,value,posStr,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    seleniumlib.wait_until_element_is_visible(id,waitTime)
    seleniumlib.click_element(id)
    ariaExpanded= seleniumlib.get_element_attribute(id+'@'+attribute)
    pos= int(posStr)
    while  ariaExpanded==value:
       ele =  seleniumlib._element_find(id,True,True,None)
       loc = ele.location
       y = loc.get('y')
       y=y+pos
       seleniumlib.execute_javascript('window.scrollTo(0,'+str (y)+')')
       seleniumlib.wait_until_element_is_visible(id,waitTime)
       #move_focus_to_element_position(id)
       time.sleep(1)
       seleniumlib.click_element(id)
       ariaExpanded= seleniumlib.get_element_attribute(id+'@'+attribute)


def move_focus_to_element_position(id,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    seleniumlib.wait_until_element_is_visible(id,waitTime)
    ele =  seleniumlib._element_find(id,True,True,None)
    loc = ele.location
    y = loc.get('y')
    seleniumlib.execute_javascript('window.scrollTo(0,'+str (y)+')')
    #seleniumlib.execute_javascript('window.scrollBy(0,-100)')


def move_focus_to_element_position_with_offset(id, offset=-50, waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    seleniumlib.wait_until_element_is_visible(id,waitTime)
    ele =  seleniumlib._element_find(id,True,True,None)
    loc = ele.location
    y = loc.get('y')
    seleniumlib.execute_javascript('window.scrollTo(0,'+str(y)+')')
    time.sleep(1)
    seleniumlib.execute_javascript('window.scrollBy(0,'+str(offset)+')')
    time.sleep(1)

def input_text_tweak(id, text, waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    browser = seleniumlib._current_browser()

    seleniumlib.wait_until_element_is_visible(id, waitTime)
    element = seleniumlib._element_find(id, True, True)
    maxLength = element.get_attribute('maxlength')

    repeat = 0
    if maxLength is None or len(text) < maxLength:
        length = len(text) - 1
    else:
        length = maxLength - 1

    browser.execute_script("arguments[0].value = arguments[1];", element, text[:length])
    element.send_keys(text[length:])

    time.sleep(0.3)
    if element.get_attribute('value') != text:
        browser.execute_script("arguments[0].value = arguments[1];", element, text[:length])
        element.send_keys(text[length:])
        repeat = 1
    return repeat


def add_thousand_precision_comma(valueList):
    resultList =[]
    for value in valueList:
        res= "{:,}".format(float(value))
    
        if res.find(".0")!=-1:
            res=res+"0"
            resultList.append(res)  
        else:
            resultList.append(res)  
    return  resultList


def select_date_from_calendar(calendar_id,date,prevDate=None,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    seleniumlib.wait_until_element_is_visible(calendar_id,waitTime);
    seleniumlib.click_element(calendar_id)
   
    if  prevDate is None:
        today = datetime.now()
        toDate = today.date
        monthNumber = today.month
        thisYear = today.year
        monthName = calendar.month_name[monthNumber]
        monthYear = monthName + " " + str(thisYear)
        
    else :
        # This case is for finding out the default month wrt the previous daet selection
        dateArr = prevDate.split(" ")
        relMonth = dateArr[1]
        relyear = dateArr[2]
        monthYear = relMonth + " " + relyear
        date_object = datetime.strptime(monthYear, '%b %Y')
        monthNum = date_object.strftime('%m')
        monthName = calendar.month_name[int(monthNum)]
        monthYear = monthName + " " + relyear
        thisYear = relyear
        toDate = dateArr[0]
        
    
    monthYearXPath = "//th[text()='"+monthYear+"']"
    seleniumlib.wait_until_element_is_visible(monthYearXPath,waitTime);
    seleniumlib.click_element(monthYearXPath)
    yearXPath = "//th[text()='"+str(thisYear)+"']"
    seleniumlib.wait_until_element_is_visible(yearXPath,waitTime);
    seleniumlib.click_element(yearXPath)
    startYearXPath="//span[@class='year old' or @class= 'year old disabled']"
    endYearXPath="//span[@class='year new']"
    
    seleniumlib.wait_until_element_is_visible(startYearXPath,waitTime);
    seleniumlib.wait_until_element_is_visible(endYearXPath,waitTime);

    startYearStr= seleniumlib._element_find(startYearXPath,True,True,None).text
    endYearStr= seleniumlib._element_find(endYearXPath,True,True,None).text
    startYear= int (startYearStr)
    endYear = int (endYearStr)
    

    dateList =  date.split(" ")
    dateToClick= dateList[0]
    monthToClick = dateList[1]
    yearToClick = dateList[2]
    
    
    expDay = dateToClick+" "+monthToClick+" "+ str (yearToClick) 
    actDay = str (toDate)+" "+monthYear
    
    
 
    # Check The requested date is today , if yes click on today option in calendar
    todayXPath = "//th[text()='Today']"
    if  expDay==actDay:
        seleniumlib.click_element(todayXPath)
        return
        
    
    while  ((startYear<= int (yearToClick) <= endYear) != True):
        

        range = find_range_of_years(startYear+1)
        if  yearToClick < startYear :
            # click on previous year
            previousArrowXPath= "//th[text()='"+range+"']/preceding-sibling::th"
            seleniumlib.wait_until_element_is_visible(previousArrowXPath,10);
            seleniumlib.click_element(previousArrowXPath)
        else:
            # click on previous year
            nextArrowXPath= "//th[text()='"+range+"']/following-sibling::th"
            seleniumlib.wait_until_element_is_visible(nextArrowXPath,10);
            seleniumlib.click_element(nextArrowXPath)
        

        seleniumlib.wait_until_element_is_visible(startYearXPath,waitTime);
        seleniumlib.wait_until_element_is_visible(endYearXPath,waitTime);

        startYearStr= seleniumlib._element_find(startYearXPath,True,True,None).text
        endYearStr= seleniumlib._element_find(endYearXPath,True,True,None).text
        startYear= int (startYearStr)
        endYear = int (endYearStr)
    
    requestedyearXpath = "//span[text()='"+str (yearToClick)+"']";
    requestedmonthXpath = "//span[text()='"+monthToClick+"' and @class='month']";
    
    dateToClickInt = int (dateToClick)
    dateToClick = str (dateToClickInt)
    requesteddayXpath = "//td[text()='"+dateToClick+"' and @class='day']";

    seleniumlib.wait_until_element_is_visible(requestedyearXpath,waitTime);
    seleniumlib.click_element(requestedyearXpath);  
    seleniumlib.wait_until_element_is_visible(requestedmonthXpath,waitTime); 
    seleniumlib.click_element(requestedmonthXpath);  
    seleniumlib.wait_until_element_is_visible(requesteddayXpath,waitTime);  
    seleniumlib.click_element(requesteddayXpath);  


def find_range_of_years(year):
    lastDigit = year % 10
    firstyear = year - lastDigit
    lastyear = firstyear + 9
    return  str (firstyear)+"-"+str (lastyear)


def get_elements(id,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    list = seleniumlib._element_find(id,False,True)
    return  list


def get_elements_as_text(id,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    list = seleniumlib._element_find(id,False,True)
    final=[]
    for i in list:
        final.append(i.text)    
    return  final


def get_a_random_value_from_dropdown(id,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    id= "//*[@id='"+id+"']//option"
    list = seleniumlib._element_find(id,False,True)
    length = len (list)
    index= random.randrange(1,length-1)
    counter=0
    seleniumlib._info(length)
    seleniumlib._info(index)
    seleObj=None
    for i in list:
        if counter==index:
            seleObj=i
            break
        else:
            counter=counter+1
        
    
    return  seleObj.get_attribute('value')
    
def get_dropdown_values_as_list(id,waitTime=10):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    id= "//*[@id='"+id+"']//option"
    list = seleniumlib._element_find(id,False,True)
    finalList=[]
    for i in list:
            finalList.append(i.get_attribute('value'))
    return finalList
        
    
def get_true_or_false():
     index= random.randrange(1,3)
     if index==1:
         return "true"
     else:
         return "false"


def upload_file(id,path):
        seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        ele=  seleniumlib._element_find(id,True,False).send_keys(os.path.expanduser(path))


def date_difference_in_months(d1, d2):
    date1= datetime.strptime(d1,'%d %b %Y')
    date2= datetime.strptime(d2,'%d %b %Y')
    diff= (date1.year - date2.year)*12 + date1.month - date2.month
    diffdays= (date1.day - date2.day)
    if diffdays>=0:
        diff= diff +1
    else:
        diff = diff

    print diff
    if diff==0:
        return 1
    else:
        return diff


def open_html_report(path):
    print path
    path="file://"+path+"/report.html"
    print path
    webbrowser.open_new(path)


def convert_to_decimal_and_mutiply(n1,n2):
    n1= Decimal(n1)
    n2= Decimal(n2)
    n3 = n1*n2
    return Decimal(n3)  


def convert_to_fixed_two_decimal_test(n1):
    n2= Decimal(n1)
    n2= "{0:.2f}".format(n2)
    return Decimal(n2)


def convert_to_fixed_two_decimal(n1, power=2):
    n1= pow(10, power) * Decimal(n1)
    n1 = int(n1)
    n1 = Decimal(n1) / pow(10, power)
    n1= "{0:.2f}".format(n1)
    return n1


def get_random_float_with_two_decimal(x,y):
    x= int(x)
    y= int(y)
    z= Decimal('%d.%d' % (random.randint(x,y),random.randint(0,99)))
    return format(z, '.2f')


def convert_sequence_to_string(sequence):
    string= seq2str(sequence)
    return string


def should_contain_one_of_these_substrings(value, *substrings):
    value= seq2str(value)
    substrings= seq2str(substrings)
    if not any(substring in value for substring in substrings):
        raise AssertionError("'%s' does not contain one of: %s" % (value, substrings))
    return True


def is_empty(value):
    if value:
        return False
    else:
        return True


def set_chrome_options():
    chromeOptions = webdriver.ChromeOptions()
    # Prefs to disable password/credentials saving alert (for Appian login)
    prefs = {"credentials_enable_service": False,
             'profile': {'password_manager_enabled': False}}
    chromeOptions.add_experimental_option("prefs", prefs)
    #Start Fullscreen because as of 9 June 2017 start-maximized switch is bugged
    chromeOptions.add_argument("start-fullscreen")
    chromeOptions.add_argument("window-size=1280,1080")
    #Disable all extensions before running
    chromeOptions.add_argument("disable-extensions")
    #Ignore certificate errors (Appian side self-signed)
    chromeOptions.add_argument("ignore-certificate-errors")
    #Disable insecure content error
    chromeOptions.add_argument("allow-running-insecure-content")
    # Add additional switches/arguments below where necessary (reference: http://peter.sh/experiments/chromium-command-line-switches)
    return chromeOptions


def generate_start_and_end_dates(max_years=50, max_days=365):
    '''
    Returns a random Start and End date value as 2 separate strings.
    This can be any Year from 1990 up to +50 years by default.
    Time between Start and End dates is randomised but depends on upper limit set by max_days (default: up to 1 year).
    Formatted as dd Mmm yyyy.
    WARNING: Use generate_future_start_and_end_dates if you want only FUTURE dates instead
    WARNING: Use generate_past_start_and_end_dates if you want only PAST dates instead.
    '''

    y = random.randint(1990, 1990 + max_years)
    m = random.randint(1, 12)
    d = random.randint(m, calendar.monthrange(y, m)[1])

    days = random.randint(1, max_days)

    start_date = date(y, m, d)
    start_date_formatted = start_date.strftime("%d %b %Y")

    end_date = start_date + timedelta(days=days)
    end_date_formatted = end_date.strftime("%d %b %Y")

    return start_date_formatted, end_date_formatted


def generate_future_start_and_end_dates(max_years=10, max_days=365):
    '''
    Returns a random Start and End date value as 2 separate strings.
    These dates are a random FUTURE date which CAN include Today.
    Upper limit of Start date year is set by max_years (default: up to 1 year)
    Time between Start and End dates is randomised but depends on upper limit set by max_days (default: up to 1 year).
    Formatted as dd Mmm yyyy.
    '''

    max_years=int(max_years)
    max_days=int(max_days)

    this_year = date.today().year

    y = this_year + random.randint(0, max_years)

    if y == this_year:
        m = random.randint(date.today().month, 12)
        d = random.randint(date.today().day, calendar.monthrange(y, m)[1])
    elif y != this_year:
        m = random.randint(1, 12)
        d = random.randint(m, calendar.monthrange(y, m)[1])

    days = random.randint(1, max_days)

    start_date = date(y, m, d)
    start_date_formatted = start_date.strftime("%d %b %Y")

    end_date = start_date + timedelta(days=days)
    end_date_formatted = end_date.strftime("%d %b %Y")

    return start_date_formatted, end_date_formatted


def generate_past_start_and_end_dates(max_years=10, max_days=365):
    '''
    Returns a random Start and End date value as 2 separate strings.
    These dates are a random PAST date UP TO Yesterday.
    Lower limit of Start date year is set by max_years (default: up to 1 year)
    Time between Start and End dates is randomised but depends on upper limit set by max_days (default: up to 1 year).
    Formatted as dd Mmm yyyy.
    '''
    this_year = date.today().year

    y = this_year - random.randint(0, max_years)
    if y == this_year:
        m = random.randint(1, date.today().month)
        d = random.randint(calendar.monthrange(y, m)[1], int(date.today().day)-1)
    elif y != this_year:
        m = random.randint(1, 12)
        d = random.randint(m, calendar.monthrange(y, m)[1])

    days = random.randint(1, max_days)

    start_date = date(y, m, d)
    start_date_formatted = start_date.strftime("%d %b %Y")

    end_date = start_date + timedelta(days=days)
    end_date_formatted = end_date.strftime("%d %b %Y")

    return start_date_formatted, end_date_formatted


def send_telegram_message(bot_token, chat_id, message):
    '''
    Send a telegram notification via bot.
    You must specify bot token, chat ID and your message.

    Use your own bot token or the following(for @BGP_QE_bot):
    bot474570244:AAFOfneZ71D6ZntimpRmcB6YgSJqrYGS5Fw

    Then send any message to @BGP_QE_bot
    and get the chat_id from:
    https://api.telegram.org/$BOT_TOKEN_HERE/getupdates
    '''
    params= {'chat_id': chat_id, 'text': message}
    proxies={'http': 'http://10.3.11.62:3128', 'https': 'http://10.3.11.62:3128'}
    url="https://api.telegram.org/"+bot_token+"/"
    response= requests.post(url + 'sendMessage', data=params, proxies=proxies)
    return response


def generate_random_integer_with_exclusion(lower_limit, upper_limit, exclusion):
    start= int(lower_limit)
    end= int(upper_limit)
    exclude= int(exclusion)
    my_range= range(start, end+1)
    my_range.remove(exclude)
    my_num= random.choice(my_range)
    return my_num


def get_todays_date():
    return datetime.now().strftime('%d %b %Y');


def get_random_item_from_array(array):
    '''
    Returns a random item from input 'array'
    '''
    choice = random.choice(array)
    return choice

def get_random_items_from_array(array, numofitems):
    '''
    Returns a random items based on numofitems from input 'array'
    '''
    rand_items = random.sample(array, numofitems)
    return rand_items


def get_random_country():
    country_list = [ 'Austria', 'Brazil', 'Canada', 'Egypt', 'Finland', 'Haiti', 'Iceland', 'Japan', 'Jamaica', 'Kuwait', 'Latvia', 'Maldives', 'New Zealand', 'Nepal', 'Oman', 'Poland', 'Qatar', 'Romania', 'Singapore', 'Thailand', 'Togo', 'United States', 'Vietnam', 'Yemen', 'Zambia' ]
    return get_random_item_from_array(country_list)


def get_random_countries(numItems):
    country_list = [ 'Austria', 'Brazil', 'Canada', 'Egypt', 'Finland', 'Haiti', 'Iceland', 'Japan', 'Jamaica', 'Kuwait', 'Latvia', 'Maldives', 'New Zealand', 'Nepal', 'Oman', 'Poland', 'Qatar', 'Romania', 'Singapore', 'Thailand', 'Togo', 'United States', 'Vietnam', 'Yemen', 'Zambia' ]
    return get_random_items_from_array(country_list, numItems)


def get_random_currency_code_type():
    currency_code = [ 'AUD', 'CAD', 'CNY', 'GBP', 'HKD', 'IDR', 'KPW', 'NZD', 'SGD', 'THB', 'USD' ]
    return get_random_item_from_array(currency_code)


def get_random_foreign_currency_code_type():
    currency_code = [ 'AUD', 'CAD', 'CNY', 'GBP', 'HKD', 'IDR', 'KPW', 'NZD', 'THB', 'USD' ]
    return get_random_item_from_array(currency_code)


def get_random_sector_sub_sector(excluded=''):
    sector_sub_sector_mapping = [
        ['IT', ''],
        ['Media', ''],
        ['Maritime', ''],
        ['Landscape', ''],
        ['Logistics',''],
        ['Retail', ''],
        ['Services', ''],
        ['Others', ''],
        ['Manufacturing & Engineering', 'Precision Engineering'],
        ['Manufacturing & Engineering', 'Cleantech'],
        ['Manufacturing & Engineering', 'Marine & Offshore'],
        ['Manufacturing & Engineering', 'Advanced Manufacturing'],
        ['Manufacturing & Engineering', 'Engineering Services'],
        ['Manufacturing & Engineering', 'Biomedical Sciences'],
        ['Manufacturing & Engineering', 'Other Manufacturing'],
        ['Food & Beverages', 'Food Services'],
        ['Food & Beverages', 'Food Manufacturing'],
        ['Tourism', 'Attractions'],
        ['Tourism', 'Cruise'],
        ['Tourism', 'Hotels'],
        ['Tourism', 'Integrated Resorts'],
        ['Tourism', 'MICE'],
        ['Tourism', 'Travel Agents'],
        ['Building & Construction', 'Builders (Contractors)'],
        ['Building & Construction', 'Non-Builders'],
        ['Agriculture', ''],
        ['Healthcare', ''],
        ['Professional Services', ''],
        ['Cleaning Services', ''],
        ['Wholesale Trade', '']
    ]
    if excluded!='':
        index=0
        for x in sector_sub_sector_mapping:
            if x[0]==excluded:
                del sector_sub_sector_mapping[index]
                break
            if x[1]==excluded:
                del sector_sub_sector_mapping[index]
                break
            index=index+1
    return get_random_item_from_array(sector_sub_sector_mapping)


def get_current_year():
    now = datetime.now()
    currentyear = now.year
    return currentyear


def generate_random_nric(type='Singaporean'):
    # Based on the NRIC formula checksum for last character of NRIC
    nric_local_firstchar_array = [
        'S','T'
    ]
    nric_foreign_firstchar_array = [
        'F','G'
    ]
    nric_local_lastchar_array = [
        'J', 'Z', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A'
    ]
    nric_foreign_lastchar_array = [
        'X', 'W', 'U', 'T', 'R', 'Q', 'P', 'N', 'M', 'L', 'K'
    ]

    nric_factor_array = [
        2, 7, 6, 5, 4, 3, 2
    ]

    offset_value = 0
    if type!='Foreigner':
        nric_first = get_random_item_from_array(nric_local_firstchar_array)
    else:
        nric_first= get_random_item_from_array(nric_foreign_firstchar_array)

    if nric_first=='T' or nric_first=='G':
        offset_value=4

    low = 0
    high = 9
    random_nric = [random.randint(low, high) for k in range(7)]

    mytotal=0
    for x in range(0, 7):
        mytotal = mytotal + (nric_factor_array[x]*random_nric[x])

    mytotal = mytotal + offset_value

    remainder= mytotal % 11
    if type!='Foreigner':
        nric_last = nric_local_lastchar_array[remainder]
    else:
        nric_last= nric_foreign_lastchar_array[remainder]

    nric=nric_first
    nric=nric + ''.join(str(e) for e in random_nric)

    nric=nric + nric_last

    return nric


def select_random_from_list(myarray):
    return get_random_item_from_array(myarray)


def generate_random_exhange_rate(low=0, high=6):
    low = int(low)
    high= int(high)
    myrate = str("{0:.9f}".format(random.uniform(low, high)))
    return myrate


def click_element_using_action_chain(elementid):
    se2lib = BuiltIn().get_library_instance('Selenium2Library')
    driver = se2lib._current_browser()
    elementid = str(elementid)
    print elementid

    myelement = driver.find_element_by_id(elementid)
    webdriver.common.action_chains.ActionChains(driver).move_to_element(myelement).click().perform()


def check_if_element_is_visible(xpath):
    se2lib = BuiltIn().get_library_instance('Selenium2Library')
    driver = se2lib._current_browser()
    xpath = str(xpath)
    element = driver.find_element_by_xpath(xpath)
    if element is None:
        visible= False
        return visible

    if element.is_displayed():
        visible=True
    else:
        visible = False

    return visible


def get_value_of_radio_group(groupname):
    se2lib = BuiltIn().get_library_instance('Selenium2Library')
    driver = se2lib._current_browser()
    xpath= "//input[@name='" + groupname + "']"
    value = None
    radiobuttons = driver.find_elements_by_xpath(xpath)
    for radiobutton in radiobuttons :
        if radiobutton.is_selected() :
            value = radiobutton.get_attribute("value")
            break

    return value


def calculate_claim_expiry_date(string_datetime):

    myindex = string_datetime.find('.')

    if myindex == -1:
        struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")
    else:
        struct_datetime = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S.%f")

    struct_datetime = struct_datetime + relativedelta(months=+3)

    return struct_datetime.strftime("%d %b %Y")




