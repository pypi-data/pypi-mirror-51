'''
Inventory Viewer/Controller
Version 1.0
Author: Jonathan Hoyle
Created: 7/20/17
Description: Creates a GUI for visualization and modification of store item information stored locally on this device
'''

### Imports ###
# noinspection PyUnresolvedReferences
import os, re, time, shelve, webbrowser, json, urllib.request, urllib.parse, urllib.error, subprocess, threading, glob,\
    ftfy
from collections import namedtuple
import interface
# noinspection PyPackageRequirements
from splinter import Browser
# noinspection PyPackageRequirements
from win32api import GetSystemMetrics
# noinspection PyPackageRequirements
from PIL import Image
# noinspection PyPackageRequirements
from appJar import gui
# noinspection PyPackageRequirements
from addict import Dict
from DataConversion import Conversion
# noinspection PyPackageRequirements
from selenium.webdriver.chrome.options import Options
# noinspection PyUnresolvedReferences
# noinspection PyPackageRequirements
from selenium.webdriver.common.by import By
# noinspection PyPackageRequirements
# noinspection PyUnresolvedReferences
from selenium.webdriver.support import expected_conditions as EC
# noinspection PyPackageRequirements
# noinspection PyUnresolvedReferences
from selenium.webdriver.support.ui import WebDriverWait
from information import Info
from shortcuts import *
from datetime import date
import SplinterShortcuts as SpS
import SystemShortcuts as SyS
import pyautogui as pa
import GuiManual, UpdateGui

### Global Variables ###

# region Globals
''' JSON And XML Data Variables '''
# Conversion variable
c = Conversion()
# Json Data
jd = c.convert('items.json')
jda = Dict(jd)
# Named tuple for individual items
Item = namedtuple('Item', list(jd[list(jd.keys())[0]].keys()))
jdn = {}
for k in jd.keys():
    # noinspection PyUnresolvedReferences
    jdn[k] = Item._make([jd[k][k1] for k1 in jd[k]])
# Dict for old json data
jdo = {}
# Current indentation for xml string
current_tabs = 0
# String to store the xml
xml_string = ''
# Number to word conversion
ntw = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']

''' App Variable '''
# App for the GUI
'''
app = gui()
'''
app = None
# '''

''' Start Progress Variables '''
start_progress = 0.0
stopped = False

''' Orders Variable '''
orders = []

''' Old Item Information Variable '''
old_items = {}

''' Items to Upload Variable '''
upload_these = []

''' Changes Allowed Variable '''
changes_allowed = {}

''' New Items to Add Variable '''
new_item_selection = []
old_item_selection = []

''' Current Store Item Names Variable '''
item_names = []
old_item_names = []

''' Items with Required Updates Variable '''
items_to_be_updated = []
updates_needed = None

''' Items with Cancelled Updates Variable '''
cancelled_updates = {}

''' Time that the online items database was last updated '''
last_updated = 0

''' Variable to indicate the item being edited '''
editing_item = ''

''' All Current Items Online Names Variable '''
all_items_uploaded = []

''' Origin Stores Variable '''
origins = []

''' Browser Variable '''
# Create the browser to be created, closed, and otherwise in the program
browser = None
s_browser = None

''' Update Info Splinter and Browser Variables '''
# u_b = u.browser
u_b = interface.browser.driver
# usb = u.s_browser
usb = interface.browser

''' XPath Selector Variables '''
# Order Page Button
order_page_button = '//div[@class="title" and contains(text(), "Order")]'
# Item information (use with xpath(this).text)
item_info_text = '//table[contains(@class, "order-rows")]/tbody'
# Address/Orderer Information (same as above)
order_info_text = '//table[contains(@class, "order-summary")]/tbody'
# Path for Chrome
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# Path for Firefox
firefox_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'

''' Variable for Order Update Thread '''
timer_thread = None

''' Initial and Actual Stock Values '''
initial_stock_values = None
actual_stocks = {}

''' App and Update Threads '''
app_thread = None
loading_thread = None

''' Transfer Var for Drag/Drop '''
transfer = None

''' Var for Entering Brand Information for Email '''
brand_emails = {}

''' Location of scrapers in the system '''
scraper_location = 'C://Users//Shipping//Documents//LiClipse Workspace//ScrapyDerp//LSL_Scrapers//scrapers//scrapers'

''' Brands being managed '''
managed_brands = []

''' Grab the names of all files in the current scraper folder '''
scraper_names = glob.glob(scraper_location + '//spiders//*.py')
# Create a list for the brand names
brand_names = []
# Loop through the spiders
for s in scraper_names:
    # Open each spider
    with open(s) as temp_file:
        # Find the store line and store that line in the names list
        try:
            brand_names.append(temp_file.readlines()[3].strip().split(': ')[1])
        # If that line doesn't exist, don't worry about it
        except:
            pass

''' List of names of the check boxes for Manage Brands window '''
brand_checks = []

''' Email information variables '''
current_email_row = 0
cer = current_email_row
email_information = dict()

'''Application Information'''
version = '1.0'

# endregion

""" Browser Control Methods """


# region Browser Control

##- Browser Initialization/Creation and Termination -##
# Creates/starts the browser and navigates to the needed page
def start_browser():
    # Get the browser
    global browser, s_browser
    opts = Options()
    opts.add_argument("--window-size=1920,1080")
    s_browser = Browser('chrome', options=opts)
    bad_count = 0
    coords = None
    while coords is None and bad_count < 50:
        try:
            # If it has been found
            if len(list(pa.locateAllOnScreen('imgs/ChromeOpenedLike.png'))) > 0 or len(
                    list(pa.locateAllOnScreen('imgs/ChromeOpenedTitle.png'))) > 0:
                # Set the coordinates and break the loop
                coords = list(pa.locateAllOnScreen('imgs/ChromeOpenedLike.png'))[0] \
                    if len(list(pa.locateAllOnScreen('imgs/ChromeOpenedLike.png'))) > 0 else \
                    list(pa.locateAllOnScreen('imgs/ChromeOpenedTitle.png'))[0]
                bad_counter = 50
                break
            # Otherwise
            else:
                # Python used Rest!
                SyS.slp(0.2)
                # Increment the counter
                bad_count += 1
        except:
            # Python used Rest!
            SyS.slp(0.2)
            # Increment the counter
            bad_count += 1
    # Python used Teleport!
    old_mouse = pa.position()
    # Python used Pound!
    pa.click(coords[0], coords[1])
    # Python used Minimize!
    pa.keyDown('win')
    pa.keyDown('h')
    pa.keyUp('h')
    pa.keyUp('win')
    # Python used Teleport!
    pa.moveTo(old_mouse[0], old_mouse[1])
    # Python used Rest!
    SyS.slp3()
    # s_browser = Browser('chrome', options=opts)
    # Set the global browser to a new PhantomJS browser
    browser = s_browser.driver
    set_browser(browser)
    # Maximize the browser to ensure its validity
    # browser.maximize_window()
    # Go to the main page
    s_browser.visit(Info.HOME_PAGE)
    # Log in to the website
    login()
    # Rest another second just to be safe
    # Python used Rest!
    slp(1)
    # Python used Future Sight!
    try:
        # Navigate to the orders page
        xpath(order_page_button).click()
    # It wasn't very effective...
    except:
        pass
    # Python used Rest!
    slp(3)


# Stops the browser
def stop_browser():
    # Get the browser
    global browser
    # Close the browser only if necessary
    if browser is not None:
        browser.quit()
        # Reset the variable entirely
        browser = None


##- Browser Navigation Utilities -##
# Logs in to the website
def login():
    # Get the browser
    global browser, s_browser
    try:
        # Send the email for the login to the email field
        s_browser.fill('email', Info.LOGIN)
        # Python used Rest!
        slp()
        # Send the password for the login to the password field
        s_browser.fill('password', Info.PWD)
        # Send the Enter key to the password field to submit
        s_browser.find_by_text('Log In').click()
        # Python used Rest!
        slp()
    except:
        # Python used Rest!
        slp(5)
        # Reload the page
        s_browser.reload()
        # Try to login again
        login()


# Finds and selects the item with the given name
def select_name(given_name):
    SpS.select_item(SpS.item_name(given_name))
    # SpS.select_item(SpS.item_name(given_name))

# Unhides the specified item from the store
def unhide_items(item_names, value='Visible'):
    # Grab the globals needed
    global ntw, app, u, u_b, usb, jd
    # usb = u.s_browser
    usb = interface.browser
    # print item_names
    # print visibility_option[0]
    # checking = u.urls
    # Uncomment/comment the below two lines when multiple pages are implemented
    #checking = [Info.STORE_PAGE]
    checking = Info.STORE_PAGE
    # checking = interface.urls
    # Variable for the current page visited
    current_page = 0
    # Go through each page with item_names still has contents
    #while len(item_names) > 0 and current_page < len(checking):
    while len(item_names) > 0:
        # If there are no more items, break the loop
        if len(item_names) <= 0:
            break
        # Don't navigate to the page again if the browser is already there
        #if usb.url != checking[current_page]:
        #    usb.visit(checking[current_page])
        # For each item name (reversed to allow deletion)
        for i in reversed(item_names):
            # Try to find and click the proper visibility setting
            try:
                # Python used Pound!
                try:
                    # Tries using the given name with it's origin before, as displayed in-store
                    select_name(jdn[i].origin + ' ' + i)
                except:
                    # If that fails, it just uses the name given
                    select_name(i)
                element_looking_for = usb.find_by_css('div.clear.field-workflow-wrapper')
                # Python used Rest!
                slp(1)
                while not usb.is_element_present_by_css('div.clear.field-workflow-wrapper'):
                    slp()
                # Python used Pound!
                usb.find_by_css('div.clear.field-workflow-wrapper').click()
                # Python used Rest!
                slp()
                # Python used Pound!
                try:
                    try:
                        usb.find_by_xpath('//*[contains(text(), "' + value + '")]')[0].click()
                    except:
                        usb.find_by_xpath('//*[contains(text(), "Visible")]')[0].click()
                except:
                    try:
                        usb.find_by_css('div.field-workflow-flyout-option-wrapper')[2 if value =='Hidden' else 0].click()
                    # It wasn't very effective...
                    except:
                        usb.find_by_css('div.field-workflow-flyout-option-wrapper')[0].click()
                # Python used Rest!
                slp(1)
                # Python used Pound!
                usb.find_by_css('input.saveAndClose').click()
                # Python used Rest!
                slp(1)
                # Remove the item name now that it's been completed
                item_names.remove(i)
            # It wasn't very effective...
            except:
                # Do nothing
                print('Failed')
                pass
        # Indicate to go to the next page in the list
        current_page += 1
    # updates_needed = u.compareBefore()
    updates_needed = interface.compare_before()


# endregion

""" Utility Methods """


# region Utilities

## Start Tag Creation ##
# Returns the start tag of the given item/category
def start_tag(tag, just_text=False):
    # Grab the current amount of tabs and increment it
    global current_tabs
    current_tabs += 1
    ntag = tag
    # Format number(s) out of the string
    if len(re.findall('[0-9]', ntag)) > 0:
        for n in ntw:
            try:
                ntag = re.sub(str(ntw.index(n)), n, ntag)
            except:
                pass
    ntag = ftfy.fix_text(ntag)
    # Handling a few other cases for errors here
    try:
        ntag = re.sub('"', '_inch_', ntag)
    except:
        pass
    try:
        ntag = re.sub('&', '_and_', ntag)
    except:
        pass
    try:
        ntag = re.sub(',', '_comma_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\.', '_point_', ntag)
    except:
        pass
    try:
        ntag = re.sub("'", '_sq_', ntag)
    except:
        pass
    try:
        ntag = re.sub("#", '_hash_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\(', '_sp_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\)', '_ep_', ntag)
    except:
        pass
    try:
        ntag = re.sub('/', '_sl_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\$', '_ds_', ntag)
    except:
        pass
    try:
        ntag = re.sub(' ', '_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\u00ae', '_r_', ntag)
    except:
        pass
    # If the call was just to format text
    if just_text:
        # Check and ensure dashes aren't in the current info
        if '-' in ntag:
            ntag = ntag.replace('-', '_')
        # Return properly formatted text
        return ntag if ntag[0] != '_' else ntag[1:]
    # Return the string
    return '<{0}>'.format(ntag)


## End Tag Creation ##
# Returns the end tag of the given item/category
def end_tag(tag, just_text=False):
    # Grab the current amount of tabs and decrement it
    global current_tabs
    current_tabs -= 1
    ntag = tag
    # Format number(s) out of the string
    if len(re.findall('[0-9]', ntag)) > 0:
        for n in ntw:
            try:
                ntag = re.sub(str(ntw.index(n)), n, ntag)
            except:
                pass
    ntag = ftfy.fix_text(ntag)
    # Handling a few other cases for errors here
    try:
        ntag = re.sub('"', '_inch_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\xa0', ' ', ntag)
    except:
        pass
    try:
        ntag = re.sub('&', '_and_', ntag)
    except:
        pass
    try:
        ntag = re.sub(',', '_comma_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\.', '_point_', ntag)
    except:
        pass
    try:
        ntag = re.sub("'", '_sq_', ntag)
    except:
        pass
    try:
        ntag = re.sub("#", '_hash_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\(', '_sp_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\)', '_ep_', ntag)
    except:
        pass
    try:
        ntag = re.sub('/', '_sl_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\$', '_ds_', ntag)
    except:
        pass
    try:
        ntag = re.sub(' ', '_', ntag)
    except:
        pass
    try:
        ntag = re.sub('\u00ae', '_r_', ntag)
    except:
        pass
    # If the call was just to format text
    if just_text:
        # Check and ensure dashes aren't in the current info
        if '-' in ntag:
            ntag = ntag.replace('-', '_')
        # Return properly formatted text
        return ntag if ntag[0] != '_' else ntag[1:]
    # Return the string
    return '</{0}>'.format(ntag)


##- Tabifying Function -##
def tabify():
    # Grab the current amount of tabs
    global current_tabs
    # Create the output string
    out = ''
    # Technically unnecessary, but better safe than sorry
    if current_tabs > 0:
        # Add as many tabs as necessary
        for i in range(0, current_tabs):
            out += '\t'
    # Return the tabs in str form
    return out


##- String Append Function -##
def x(a):
    # Grab the global xml string
    global xml_string
    # Append the string as necessary
    try:
        xml_string += str(a)
    except:
        xml_string += a


##- Normalized the string to what it was before formatting -##
def normalize(s):
    # Grab the global variable we need
    global ntw
    # Save to a local var
    ns = s
    # For each word in the array
    for n in ntw:
        # If that word is in the string
        if n in ns:
            # Replace it with the number
            ns = re.sub(n, str(ntw.index(n)), ns)
    # Replace the inch symbol
    try:
        ns = re.sub('_inch_', '"', ns)
    except:
        pass
    # Replace the and symbol
    try:
        ns = re.sub('_and_', '&', ns)
    except:
        pass
    # Replace the comma symbol
    try:
        ns = re.sub('_comma_', ',', ns)
    except:
        pass
    try:
        ns = re.sub('_point_', '.', ns)
    except:
        pass
    # Replace the single quotation symbol
    try:
        ns = re.sub('_sq_', "'", ns)
    except:
        pass
    try:
        ns = re.sub("_hash_", '#', ns)
    except:
        pass
    # Replace the starting parentheses symbol
    try:
        ns = re.sub('_sp_', '\(', ns)
    except:
        pass
    # Replace the end parentheses symbol
    try:
        ns = re.sub('_ep_', '\)', ns)
    except:
        pass
    # Replace the forward slash symbol
    try:
        ns = re.sub('_sl_', '/', ns)
    except:
        pass
    # Replace the dollar symbol
    try:
        ns = re.sub('_ds_', '\$', ns)
    except:
        pass
    try:
        ns = re.sub('_r_', '\u00ae', ns)
    except:
        pass
    # Replace the space symbol
    try:
        ns = re.sub('_', ' ', ns)
    except:
        pass
    # Return the formatted string
    return ns


##- JSON to XML Formatting -##
def format_json():
    ## Initialization ##
    # Grab the globals we need
    global jd, jda, jdn, xml_string
    # Create the string that will hold the xml data
    x(start_tag('Items'))
    # Store origin variable
    new_dict = {}
    nda = Dict()
    # Find the length for percentage of completion
    o_l = len(jd)
    ## Sorting ##
    # Find the origins of all of the items
    for i in jd:
        # Using addict as comparison, only step needed for this loop
        try:
            nda[jda[i].origin][i] = jda[i]
        except:
            pass
        # If the origin company is not already included
        if jd[i]['origin'] not in new_dict:
            # Initalize that origin company
            new_dict[jd[i]['origin']] = {}
        # Append the item to the respective origin company's list
        new_dict[jd[i]['origin']][i] = jd[i]
    ## XML String Creation ##
    try:
        list(new_dict.keys()).sort()
    except:
        pass
    # Now use the new dict to make a properly formatted xml tree
    # For each origin store
    for key in list(new_dict.keys()):
        # Start the origin store's tag
        x(start_tag(key))
        # print ''
        # print key
        # Go through it's products
        for item in sorted(new_dict[key]):
            # Append the item as the first tag
            x(start_tag(item))
            # Append the end tag for this item
            x(end_tag(item))
        # End for
        # Add the origin store's end tag
        x(end_tag(key))
    # End for
    # Then close the xml document
    x(end_tag('Items'))
    xml_string = re.sub('\(', '', xml_string)
    xml_string = re.sub('\)', '', xml_string)
    return xml_string


# Get the data required for the GUI
def obtain_data():
    global old_items, item_names, updates_needed
    # Grab the updates needed info
    # updates_needed = u.compareBefore()
    updates_needed = interface.compare_before()
    # origins = u.origins
    origins = interface.origins
    # Create a variable for the grabbed JSON data from the website
    items_displayed = None
    # Obtain the JSON data from the website
    while items_displayed is None:
        try:
            # items_displayed = json.loads(urllib.urlopen(u.get_json_url('')).read())['items']
            items_displayed = json.loads(urllib.request.urlopen(SyS.get_json_url('')).read())['items']
        except:
            pass
    '''
    current = 0
    while items_displayed is None and current < 20:
        try:
            #items_displayed = json.loads(urllib.urlopen(u.get_json_url('')).read())['items']
            items_displayed = json.loads(urllib.urlopen(SyS.get_json_url('')).read())['items']
        except:
            current += 1'''
    # Find the names and information for each item found
    item_names = []
    old_items = {}
    for i in sorted(items_displayed, key=lambda c: c['title']):
        # Name
        # temp_name = u.generalize(i['title'])
        temp_name = interface.generalize(i['title'])
        item_names.append(ftfy.fix_text(temp_name))
        # Description
        temp_desc = i['excerpt']
        temp_desc = re.sub('<p>', '', temp_desc)
        temp_desc = re.sub('</p>', '', temp_desc)
        # Details
        temp_body = i['body']
        # Get everything needed
        temp_dets = re.findall(r'<li>(?P<inner_desc>.*?)</li>', temp_body)
        # If nothing was found, try a different search
        if len(temp_dets) == 0:
            temp_dets = re.findall(r'<p>-\s(?P<inner_desc>.*?)</p>', temp_body)
        try:
            temp_tags = i['tags']
        except:
            temp_tags = []
        # Colors, SKUs, and Price
        temp_colors = []
        temp_skus = []
        temp_price = ''
        first = True
        # Go through each variant
        for v in i['variants']:
            # Colors
            # If the color isn't included already
            ### Note that originally 'optionValues' was u'optionValues', putting this here in case something goes wrong later ###
            try:
                if v['optionValues'][0]['value'] not in temp_colors:
                    # Add the color to the temp
                    temp_colors.append(v['optionValues'][0]['value'])
                    # Add the SKU to the temp
                    temp_skus.append(v['sku'])
            except:
                temp_skus.append(v['sku'])
            # Price
            # Only run for the first time around
            if first:
                # Append the price
                temp_price = float(float(v['price']) / 100.0)  # Confirmed
                # Indicate not to run this any more
                first = False
        # Images
        temp_images = []
        for img in i['items']:
            # Take just the file name
            temp_images.append(img['assetUrl'].split('/')[-1])
        old_items[temp_name] = {'description': temp_desc, 'details': temp_dets, 'tags': temp_tags,
                                'colors': temp_colors,
                                'skus': temp_skus, 'price': temp_price, 'images': temp_images}
    # Format the obtained data into an xml that the tree can display
    xml_string = '<Items>'
    for n in item_names:
        xml_string += start_tag(n) + end_tag(n)
    xml_string += '</Items>'
    return xml_string


# Returns True or False depending on whether the giving tracking number is valid or not
def is_valid(sn):
    # Carrier information
    carriers = {'UPS': [11], 'FedEx': [12, 15], 'USPS': [20, 30]}
    # Create the boolean
    valid = False
    # Find the length of the shipping number
    length = len(sn)
    # Check each carrier and see if the information matches
    for c in carriers:
        if length in carriers[c]:
            valid = True
            break
    return valid


# Remove HTML tags from given text
def remove_html(s):
    fs = re.sub(r'<[^>]*>', '', s)
    return fs

# Displays about infobox
def aboutMe(button):
    global app
    app.infoBox("About SqUp",
                "---\n" +
                "Jonathan Hoyle, 2017-2019\n" +
                "---\n\t" +
                "Version: " + version + "\n" +
                "Python: 3.7.3\n" +
                "appJar: 0.94.0\n" +
                "splinter: 0.10.0\n" +
                "selenium: 3.141.0\n" +
                "Pillow: 6.0.0\n" +
                "addict: 2.2.1\n" +
                "PyAutoGUI: 0.9.44\n" +
                "ahk: 0.6.1\n" +
                "---\n" +
                "Filename: InventoryGui.pyw\n" +
                "---")

# endregion

""" Order Information Acquiring Methods """


# region Order Info Acquisition

# Updates the contents of the window when a new order is selected
def change_contents(event):
    # Grab all of the globals that we need
    global orders, app
    # Create an empty variable to hold the information found
    item = None
    # Save the current selection
    co = app.getOptionBox('orders')
    # For every order we have
    for o in orders:
        # If the order number is found
        if o['order_number'] == co:
            # Save the information, and break
            item = o
            break
    # As long as something was found
    if item is not None:
        # Create a temporary variable to hold the items found
        items_temp = []
        # Old shipping number
        old_shipping = app.getEntry('shipping_num')
        # Get the shipping number
        app.setEntry('shipping_num', item['shipping_info'])
        # Check if the content is valid
        valid = is_valid(app.getEntry('shipping_num'))
        # Change the text of the save button depending on content of the shipping information
        if not valid:
            # Change the text on the button to show that the item has been saved
            app.setButton('Save and Continue', "Please Enter a Valid Shipping Number")
        elif item['shipping_info'].strip() != '':
            app.setButton('Save and Continue', "Saved!")
        else:
            app.setButton('Save and Continue', "Save and Continue")
        # Change the text of the Complete Order button based on the relevant information
        if item['completed']:
            app.setButton('Complete Order', "Completed!")
        # If it's not, reset the window
        else:
            app.setButton('Complete Order', "Complete Order")
        # If this item was saved and the the original and new aren't the same, reset the variable
        if event == 'saved' and old_shipping != app.getEntry('shipping_num'):
            app.setButton('Complete Order', "Complete Order")
        # Get the name of the client
        app.setLabel('customer', item['client']['billing'][0])
        # Get the address this order is being shipped to
        addstring = item['client']['address'][0]
        # Construct a string based on that address
        for i in item['client']['address'][1:]:
            addstring = addstring + '\n' + i
        # Set the address to the string constructed
        app.setLabel('shipping_addr', addstring)
        # Set the item field to the necessary information
        items_temp = format_items(item['items'])
        # Create the string for the items
        items_str = ''
        for i in items_temp:
            items_str += i + '\n'
        # Update the text
        app.setLabel('order_items', items_str)
        # Finally, enable the Complete Order button if the item has a shipping number
        if app.getEntry('shipping_num').strip() != '' and valid:
            app.enableButton('Complete Order')
        else:
            app.disableButton('Complete Order')
            # End Change Contents


# Marks the current item for completion
def complete_item(button):
    # From StoreGui.py:
    global orders, app
    # Get the current order number
    # co = current_order.get()
    # Create a variable for the item
    item = None
    # Go through each order
    for o in orders:
        # Once the correct order is found
        if o['order_number'] == app.getOptionBox('orders'):
            # Set the item variable
            item = o
            break
    # If the item was found
    if item is not None:
        # Mark it as completed
        item['completed'] = True
    # Save the orders
    main_file = shelve.open('orders_db')
    main_file['orders'] = orders
    main_file.close()
    # Update the contents of the window()
    change_contents(None)


# Method for officially completing an item
def complete_items(button):
    # Grab the global needed
    global orders
    # Create arrays for the completed order numbers and shipping information
    completed_numbers = []
    completed_shipping = []
    # For each order
    for o in orders:
        # If it's been marked as completed
        if o['completed']:
            # Append this orders information
            completed_numbers.append(o['order_number'])
            completed_shipping.append(o['shipping_info'])
    # If there are in fact completed orders
    if len(completed_numbers) != 0:
        # Clear the current content of the window
        reset_contents()
        # Send this information off to the proper method
        complete_orders(completed_numbers, completed_shipping)
    # Finally, to perform the last update, refresh the orders
    refresh_orders(None)


# Takes an array of orders to complete on the website and does so
def complete_orders(order_ids, tracking_ids):
    # Get the browser
    global browser, app
    # Change the window title
    app.setTitle('Please wait while your completed items are being processed')
    # Start the browser
    start_browser()
    # Create an array for the newly fulfilled orders
    fulfilled_orders = []
    # Find the orders we need to complete based on the order ids given
    for o in order_ids:
        fulfilled_orders.append(xpath(
            '//div[contains(@class, "cell") and contains(@class, "order-number") and contains(text(), "' + o + '")]/..'))
    # Now, go through and fulfill each order
    for f in fulfilled_orders:
        # Python used Pound!
        f.click()
        # Python used Rest!
        slp(1)
        # Find the button to fulfill the order
        fulfill_button = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="button" and @value="Mark Fulfilled"]')))
        # Python used Pound!
        fulfill_button.click()
        # Python used Rest!
        slp()
        # Find the input for the tracking number
        tracking_input = name('trackingNumber')
        # Send the tracking ID to the input
        tracking_input.send_keys(tracking_ids[fulfilled_orders.index(f)])
        # Wait on the web page to recognize the carrier of the package
        # Python used Rest!
        slp(3)
        # Find and press the confirm button
        confirm = xpath('//input[@value="Confirm"]')
        # Python used Pound!
        confirm.click()
        # Python used Rest!
        slp(1)
    # Now that everything should be done, stop the browser
    stop_browser()
    # Reset the title of the window
    app.setTitle('Store Orders For Completion')


# Returns a string with the items supplied
def format_items(item_dict):
    # Create the string to save everything to
    final_string = []
    # For each item in the list
    for i in item_dict:
        # Create a smaller string to construct this item
        current_string = 'Item:\t'
        # Add the name
        current_string = current_string + i + '\n'
        # Add the color
        current_string = current_string + 'Color:\t' + item_dict[i]['color'] + '\n'
        # Add the quantity
        current_string = current_string + 'Quantity:\t' + item_dict[i]['quantity'] + '\n'
        # Add the size
        current_string = current_string + 'Size:\t' + item_dict[i]['size'] + '\n'
        # Add the price
        current_string = current_string + 'Price:\t' + item_dict[i]['price'] + '\n'
        # Add the total cost
        current_string = current_string + 'Total:\t' + item_dict[i]['total'] + '\n\n'
        # Add the current string to the overall one
        final_string.append(current_string)
    # Finally, return the constructed string
    return final_string


# Gets the information for the orders in the interface
def get_order_info():
    # Get the browser sqs-order-list-content
    global s_browser, browser, orders
    # Get the current url
    c_url = interface.browser.url
    # Use the interface's browser to do the heavy lifting
    interface.browser.visit(Info.ORDER_PAGE)
    s_browser = interface.browser
    set_browser(s_browser)
    # Make sure the browser is running, and if not run it
    #if browser is None:
    #    start_browser()
    #while s_browser.url != Info.ORDER_PAGE:
    #    s_browser.reload()
    #    s_browser.visit(Info.ORDER_PAGE)
    # Do nothing until the wrapper is detected
    while not s_browser.is_element_present_by_xpath('//div[contains(@class, "sqs-order-content")]'):
        print('Repeating')
    # Once it's detected, find the orders
    all_orders = s_browser.find_by_xpath(
        '//div[contains(@class,"sqs-model-list-content") and contains(@class, "sqs-order-list-content")]//div[contains(@class, "order-summary")]')
    # Create a variable for the basic text of each order
    all_order_texts = []
    # Get the basic text from each order
    for a in all_orders:
        # Split the text from the parent element by line breaks
        all_order_texts.append(a.text.split('\n'))
    # Create a variable for the pending orders
    orders_pending = []
    orders_removed = []
    # Figure out which orders are pending
    for a in reversed(all_order_texts):
        # If it is, add its number to the list
        if 'Pending' in [x.title() for x in a]:
            orders_pending.append(a)
        # Otherwise, remove it from the original array of elements
        else:
            all_orders.remove(all_orders[all_order_texts.index(a)])
            orders_removed.append(all_order_texts.index(a))
    # Now remove the remaining orders from the current texts
    for o in orders_removed:
        all_order_texts.remove(all_order_texts[o])
    # Python used Rest!
    slp()
    # Now go through the remaining orders
    for a in all_orders:
        # Create a dict to put all of this in
        this_order_information = {}
        # Python used Pound!
        a.click()
        # Python used Rest!
        slp()
        # Loop here until the stuff we need is visible
        while not s_browser.is_element_present_by_xpath(item_info_text):
            print('Repeating sub')
        # Grab the two pieces of information that we need
        # Get the item information element
        # Item information, parsed and stripped
        order_item_text = [x.strip() for x in s_browser.find_by_xpath(item_info_text).text.split('\n')]
        # Shorter name and removal of titles for ease of use
        oit = order_item_text[4:]
        # Find the index where the price information starts
        price_index = oit.index('Item Subtotal')
        # Create an array for price information
        price_info = []
        # Add every item after that index to the new array
        for i in range(price_index, len(oit)):
            price_info.append(oit[i])
        # Now remove all of the information added to the price array from the original array
        for p in reversed(price_info):
            oit.remove(p)
        # Create an array to represent the items ordered
        ordered_items = []
        # Create a variable to indicate which entry of the items we are on
        curr = 0
        # And an array to hold each item's information in during assembly
        temp = []
        # Split the remaining entries into individual items
        while curr < len(oit):
            # Determine if there is a dollar sign in the string
            if '$' not in oit[curr]:
                # If not, just append the current string to the temporary array
                temp.append(oit[curr])
                # Increment the current value by 1
                curr += 1
            # If a dollar sign is found
            else:
                # Put the current line and the next line in the temporary array
                temp.append(oit[curr])
                temp.append(oit[curr + 1])
                # Increment by 2
                curr += 2
                # Append the temporary array to the total items
                ordered_items.append(temp)
                # Reset the temporary array
                temp = []
        # Create an array for the ordered item attributes
        item_names = []
        item_colors = []
        item_sizes = []
        item_number = []
        item_prices = []
        item_totals = []
        item_adds = []
        # For each ordered item
        for o in ordered_items:
            # Append this item's name to the ordered names
            item_names.append(o[0])
            # Split the item's color and size info
            parts = o[2].split('/')
            # Save Color and Size as their own variables
            ct = parts[0].strip()
            try:
                st = parts[1].strip()
            except:
                st = ''
            # Check to make sure that the next field is the quantity
            try:
                temp_int = int(o[3])
            # If it isn't, handle the size appropriately
            except:
                if 'Length' in o[3]:
                    st = st + ' x ' + str(o[4]) + 'L'
                else:
                    st = st + ', ' + o[3] + ':' + o[4]
            # Append this item's color and size
            item_colors.append(ct)
            item_sizes.append(st)
            # Remaining items are located from the bottom to help eliminate possible parsing errors
            # Append the quantity of this item in the order
            item_number.append(o[len(o) - 3])
            # Append the price of this item
            item_prices.append(o[len(o) - 2])
            # Append the total cost of these items
            item_totals.append(o[len(o) - 1])
        # Create a dict for the final items
        final_items = {}
        # Put all of the information into the final dict
        for i in range(0, len(item_names)):
            final_items.setdefault(item_names[i],
                                   {'color': item_colors[i], 'size': item_sizes[i], 'quantity': item_number[i],
                                    'price': item_prices[i], 'total': item_totals[i]})
        # Order/Shipping information
        address_info_text = xpath(order_info_text).text.split('\n')
        # Shorter name for ease of use
        ait = address_info_text
        # Get Shipping Information first
        # Method of shipment
        method_txt = ait[-1]
        # Find out how long this thing is, and work accordingly
        # If the Billing and Shipping address are the same
        if ait[1] == 'SHIPPING TO:':
            # Home Address
            shipping_txt = ait[2:6]
            # Billing Address
            billing_txt = shipping_txt
            # Email Address
            email_txt = ait[7]
            # Phone Number (properly formatted for readability)
            # Format: Area Code + '-' + First 3 Numbers + '-' + Last 4 Numbers
            phone_txt = ait[8][:3] + '-' + ait[8][3:6] + '-' + ait[8][6:]
        # Otherwise
        else:
            # Billing Address
            billing_txt = ait[1:5]
            # Shipping Address
            shipping_txt = ait[6:10]
            # Email Address
            email_txt = ait[11]
            # Phone Number
            phone_txt = ait[12][:3] + '-' + ait[12][3:6] + '-' + ait[12][6:]
        # Save all of this information in a dict
        client_info = {'billing': billing_txt, 'address': shipping_txt, 'email': email_txt, 'phone': phone_txt}
        # Now make sure set all of this items information is saved
        this_order_information = {'order_number': all_order_texts[all_orders.index(a)][0], 'items': final_items,
                                  'client': client_info, 'shipping_info': '', 'completed': False}
        # And add the information to the overall array
        orders.append(this_order_information)
        # Python used Pound!
        css('a.cancel').click()
        # Python used Rest!
        slp()
    # End for loop
    # Now that order parsing is complete, close the browser
    #stop_browser()
    interface.browser.visit(c_url)
    # Save the orders to the current file
    main_file = shelve.open('orders_db')
    try:
        old_orders = main_file['orders']
        for o in orders:
            for l in old_orders:
                if (o['order_number'] == l['order_number']) and l['shipping_info'].strip() != '':
                    o['shipping_info'] = l['shipping_info']
                    break
    except:
        main_file['orders'] = orders
    main_file.close()


# Obtains backup data
def load_backup_orders():
    # Get the global we need
    global orders
    # Open the main file to save this one too
    main_file = shelve.open('orders_db')
    # Save the current info
    main_file['orders'] = orders
    # Close the main file
    main_file.close()
    # Open the backup file
    b_f = shelve.open('save_data.jon')
    # Load in the backu orders
    orders = b_f['orders']
    # Close the backup file
    b_f.close()


# Obtains order information from a saved file
def load_order_info(*filename):
    # Get the global we need
    global orders
    # If the orders aren't blank
    if orders is not None:
        # Open the backup file first
        b_f = shelve.open('save_data.jon')
        # Save the current orders to the backup file
        b_f['orders'] = orders
        # Close the backup file
        b_f.close()
    # Try to open it with a given filename
    try:
        # Open the file with the information in it
        load_file = shelve.open(filename)
        # Load the information
        orders = load_file['orders']
        # Close the opened file
        load_file.close()
    # If that doesn't work, go with the default database
    except:
        # Open the file with the information in it
        load_file = shelve.open('orders_db')
        # Load the information
        orders = load_file['orders']
        # Close the opened file
        load_file.close()
    # End lad-order_info


# Refreshes the orders listed
def refresh_orders(button):
    global orders, app
    # Save the current orders, just in case something goes wrong
    # Open a backup file
    backup = shelve.open('save_data.jon')
    backup['orders'] = orders
    lastorders = orders
    backup.close()
    # Reset the orders variable
    orders = []
    # Change the title of the window to reflect the status of the update
    app.setTitle('Please wait while orders are being refreshed')
    # Disable the order selection until it's done
    app.disableOptionBox('orders')
    # Call the get information method
    get_order_info()
    # Get all of the order numbers from this new data
    new_numbers = [on['order_number'] for on in orders]
    # Make sure that if a shipping number has been saved, it's added to the entry
    for l in lastorders:
        for o in orders:
            # If the order numbers are the same and the original is not empty and the new one is
            if (l['order_number'] == o['order_number']) and l['shipping_info'] != '' and o['shipping_info'] == '':
                o['shipping_info'] = l['shipping_info']
    # Reset the title of the window
    app.setTitle('Store Orders For Completion')
    # Refresh the list's content
    try:
        app.changeOptionBox('orders', [o['order_number'] for o in orders])
    except:
        pass
    # Re-enable the list
    app.enableOptionBox('orders')


# Resets the contents of every element so that
def reset_contents():
    # Grab all of the globals that we need
    global app
    # Get the shipping number
    app.setEntry('shipping_num', '')
    # Get the name of the client
    app.setLabel('customer', '')
    # Set the address to the string constructed
    app.setLabel('shipping_addr', '')
    # Update the text
    app.setLabel('order_items', '')
    # Disable the item complete button
    app.disableButton('Submit All Completed')


# Saves the information currently in the shipping information entry
# to this item's shipping number
def save_item(button):
    # From StoreGui.py:
    # Get the globals
    global orders, app
    # Get the shipping information
    sn = app.getEntry('shipping_num')
    # Check to make sure the shipping number is valid
    valid = is_valid(sn)
    # If a valid shipping number has been entered
    if valid:
        # Create a variable for the item
        item = None
        # For each order
        for o in orders:
            # Check to see if it's the current one
            if o['order_number'] == app.getOptionBox('orders'):
                # If it is, set the current order and break
                item = o
                break
        # As long as it was found, which it always should have been
        if item is not None:
            # Set the item's shipping information to the currently entered entry
            item['shipping_info'] = sn
        # Open the file holding the information of the orders
        save_file = shelve.open('orders_db')
        # Save the changes made to the order
        save_file['orders'] = orders
        # Close the file
        save_file.close()
    # Update the contents of the window with the new information
    change_contents('saved')


# Regularly updates the orders
def order_updates():
    global timer_thread
    timer_thread = threading.Timer(1800.0, order_updates)
    timer_thread.start()
    refresh_orders(None)


# endregion

''' Menu Item Functions '''


# region Menu Items

# Opens the Fedex home page in Chrome
def open_fedex(button):
    # Get the path for Chrome
    global chrome_path
    # Navigate to the page
    webbrowser.get(chrome_path).open('https://www.fedex.com/us/index.html')


def open_fedex_firefox(button):
    # Get the path for Chrome
    global firefox_path
    # Navigate to the page
    webbrowser.get(firefox_path).open('https://www.fedex.com/us/index.html')


# Opens the home page in a window of Chrome
def open_home(button):
    # Get the path for Chrome
    global chrome_path
    # Get the page in Chrome
    subprocess.call(chrome_path[:-2] + 'https://brent-cline-7fyn.squarespace.com/config/orders')


# Opens the folder that images are stored in
def open_image_folder(button):
    subprocess.call(r'explorer /select,C:\imgJson\full')


# Opens the folder that the JSON for the items is stored in
def open_item_folder(button):
    subprocess.call(
        r'explorer /select,"C:\Users\Shipping\Documents\Integration Dev\SquarespaceUploader\SquarespaceUploader"')


# Allows user to write feedback for future features/releases
def leave_feedback(button):
    app.showSubWindow('leave_feedback')


# Closes the feedback window
def exit_feedback(button):
    app.hideSubWindow('leave_feedback')


# Saves the entered feedback and closes the window
def send_feedback(button):
    # Get the text input
    feedback_text = app.getTextArea('feedback_input')
    # Save the current contents of the file
    lines = []
    with open('feedback.txt') as ff:
        lines = ff.readlines()
    # Create the final list
    final_lines = []
    # Ensure that the input is formatted properly
    if len(feedback_text.split('\n')) > 1:
        final_lines = feedback_text.split('\n')
    else:
        final_lines.append(feedback_text)
    # Append the new lines to the old ones
    lines.extend(final_lines)
    fl = []
    for l in lines:
        if l.strip() not in ['', '\n']:
            fl.append(l)
    lines = fl
    # Save the new lines to the file
    with open('feedback.txt', 'w') as ff:
        ff.write('\n'.join([l.strip() for l in lines]) + '\n')
    # Reset the text input and close the window
    app.setTextArea('feedback_input', '')
    app.hideSubWindow('leave_feedback')


# endregion

""" Program Methods """

''' Content Updating '''


# region Content Update

## Inventory Page Methods ##
# Displays item information on item double-click
def display_info(tree, *args):
    # Grab the globals needed
    global app, jd, jdn, changes_allowed
    # Grab the currently selected item
    item = app.getTreeSelected('nav')
    # Initialize the current item and its name
    ci = None
    item_name = ''
    # Try to get the item based purely on the selected element
    try:
        item_name = normalize(item)
        ci = jdn[item_name]
    # If that fails
    except:
        # Search through all of the items
        for j in jdn:
            # And find the one that contains the text of this item
            if type(item) is tuple:
                item = item[0]
            if normalize(item) in j:
                item = j
                item_name = j
                break
        # And set the current item appropriately if one is found
        if item != app.getTreeSelected('nav'):
            try:
                ci = jdn[item]
                item_name = item
            except:
                ci = jdn[list(jdn.keys())[0]]
                item_name = list(jdn.keys())[0]
        # If one isn't found, set the data to be the default item's data
        else:
            ci = jdn[list(jdn.keys())[0]]
            item_name = list(jdn.keys())[0]
    # Set the contents appropriately
    # Name
    last_item = app.getLabel('name')
    
    # Sub functions to get the checkmarks updated
    # Handling labels
    def update_checks(i, check_text):
        changes_allowed[normalize(last_item)][i] = (not app.getCheckBox(check_text))
        app.setCheckBox(check_text, ticked=(not changes_allowed[normalize(item)][i]))
        app.setLabel(i, ci[i])
    
    # Handling Messages
    def update_checks_message(i, check_text):
        changes_allowed[normalize(last_item)][i] = (not app.getCheckBox(check_text))
        app.setCheckBox(check_text, ticked=(not changes_allowed[normalize(item)][i]))
        app.setMessage(i, ci[i])
    
    # Handling ListBoxes
    def update_checks_list(i, check_text):
        changes_allowed[normalize(last_item)][i] = (not app.getCheckBox(check_text))
        app.setCheckBox(check_text, ticked=(not changes_allowed[normalize(item)][i]))
        app.updateListBox(i, ci[i])
    
    # Continuing method here
    if last_item != '':
        update_checks('url', 'URL:')
        update_checks('origin', 'Store of origin:')
        update_checks('sku', 'SKU:')
        update_checks('price', 'Price:')
        update_checks_message('description', 'Description:')
        update_checks_list('details', 'Details:')
        update_checks_list('image_paths', 'Image Paths:')
    app.setLabel('name', item_name)
    # Image
    im = Image.open('C:/imgJson/' + ci.image_paths[0])
    im.save('imgs/item.gif', 'GIF')
    app.reloadImage('item_image', 'imgs/item.gif')
    app.zoomImage('item_image', -3)
    # Url
    app.setLabel('url', ci.url)
    # Origin
    app.setLabel('origin', ci.origin)
    # SKU
    app.setLabel('sku', ci.sku)
    # Price
    app.setLabel('price', ci.price)
    # Description
    app.setMessage('description', ci.description)
    # Details
    app.updateListBox('details', ci.details)
    # Image Paths
    app.updateListBox('image_paths', ci.image_paths)


## Updates Page Methods ##
# Stops the Add Item Sub-Window and resets the new item selection
def cancel_sub(button):
    # Grab the global app and new items
    global app, new_item_selection
    # Reset the new items array
    # new_item_selection = []
    # Hide the window
    app.hideSubWindow('Add Items')


# Stops the Add Item Sub-Window and applies the selected items to the Compare/Update/Upload database
def confirm_sub(button):
    # Grab the global app and new items to be added to the update
    global app, old_items, new_item_selection, all_items_uploaded_old, ntw, items_to_be_updated
    # Attempt to "un-format" the item name, just as a precaution
    for i in range(0, len(new_item_selection)):
        new_item_selection[i] = normalize(new_item_selection[i])
    print(new_item_selection)
    # Create an array of items to upload and unhide
    upload_these = []
    unhide_these = []
    # For each item
    for n in new_item_selection:
        items_to_be_updated.append(n)
        # If it's not already online
        if n not in all_items_uploaded_old:
            # Put a blank slot where it will be
            old_items[n] = {'description': '', 'details': [], 'tags': [], 'colors': [],
                            'skus': [], 'price': '', 'images': []}
            upload_these.append(n)
        # Otherwise
        else:
            unhide_these.append(n)
    unhide_items(unhide_these)
    # Hide the window
    app.hideSubWindow('Add Items')


# Launches the Add Item Sub-Window
def launch_sub(button):
    # Grab the global app
    global app
    # Show the Window
    app.showSubWindow('Add Items')


# Modifies list of new items to add based on action in item tree
def modify_new_items(tree):
    # Grab the globals
    global app, new_item_selection
    # Get the currently selected name
    new_name = app.getTreeSelected(tree)
    # If it hasn't been added, add it to the list
    if new_name not in new_item_selection:
        new_item_selection.append(new_name)
    # If it has, remove it
    else:
        new_item_selection.remove(new_name)
    # Update the list of items selected
    app.updateListBox('added_items', new_item_selection)


# Updates the contents in the comparison fields of the Update Item tab
def update_contents(tree, test):
    # Grab the globals needed
    global app, jd, jdn, old_items, cancelled_updates
    # Grab the selected element
    selected = app.getTreeSelected(tree)
    # Normalize it
    selected = normalize(selected)
    # If the returned thing is a tuple, make it a string
    if type(selected) is tuple:
        selected = selected[0]
    # Try one more convert, just in case
    selected = normalize(selected)
    # UpdateItem Contents
    # Name
    app.setLabel('old_item_name', 'Name: ' + selected)
    app.setLabel('new_item_name', 'Name: ' + selected)
    # Description
    try:
        app.setMessage('old_item_desc', old_items[selected]['description'].replace('&nbsp;', '').strip())
    except:
        try:
            app.setMessage('old_item_desc', old_items[selected]['description'].strip())
        except:
            app.setMessage('old_item_desc', '')
    try:
        app.setMessage('new_item_desc', remove_html(jdn[selected].description.replace('&nbsp;', '')).strip())
    except:
        try:
            app.setMessage('new_item_desc', jdn[selected].description.strip())
        except:
            app.setMessage('new_item_desc', '')
    # Details
    try:
        app.updateListBox('old_item_details', old_items[selected]['details'])
    except:
        app.updateListBox('old_item_details', [])
    try:
        app.updateListBox('new_item_details', jdn[selected].details)
    except:
        app.updateListBox('new_item_details', [])
    # Colors
    try:
        app.updateListBox('old_item_colors', old_items[selected]['colors'])
    except:
        app.updateListBox('old_item_colors', [])
    try:
        app.updateListBox('new_item_colors', jdn[selected].colors)
    except:
        app.updateListBox('new_item_colors', [])
    # Button Options
    try:
        if not cancelled_updates[normalize(selected)]:
            app.setButton('Disable Update', 'Disable Update')
        else:
            app.setButton('Disable Update', 'Enable Update')
    except:
        cancelled_updates[normalize(selected)] = False
        app.setButton('Disable Update', 'Disable Update')


# Updates the content of the first window that appears
def update_meter():
    global app, start_progress, stopped
    app.setStatusbar('Startup is ' + str(start_progress) + '\% Complete')
    if start_progress > 99.8 and not stopped:
        app.hideSubWindow('Start Application')
        stopped = True


# endregion

''' Update Management Methods '''


# region Update Management

# Diables updates for an item (symbolically, full function TBI)
def disable_update(button):
    # Grab the globals needed
    global app, items_to_be_updated, cancelled_updates
    # Grab the normalized version of the currently selectedd item
    selected = normalize(app.getTreeSelected('update_tree'))
    # If the update hasn't been cancelled, do so and change the button's text
    if not cancelled_updates[selected]:
        items_to_be_updated.remove(selected)
        app.setButton('Disable Update', 'Enable Update')
    # If it has, un-cancel it
    else:
        items_to_be_updated.append(selected)
        app.setButton('Disable Update', 'Disable Update')
    cancelled_updates[selected] = not cancelled_updates[selected]


# Hides and unhides the proper items on the online store
def hide_unhide(button):
    # Change this back once multiple pages are implemented
    # Grab the globals
    global new_item_selection, old_item_selection, upload_these, app
    # Show the sub window to prevent interaction
    app.showSubWindow('apply_wait_indicator')
    # Change the sub-window's wait message
    app.setLabel('apply_loading_message', SyS.get_loading_message())
    # Create the array to unhide and upload
    current_page_items = SpS.get_item_names()
    unhide_these = []
    upload_these = []
    # For each item in the new items selected
    for n in new_item_selection:
        # If it's not already unhidden
        # if n in all_items_uploaded:
        if n in current_page_items:
            # Indicate to unhide it
            unhide_these.append(n)
        else:
            upload_these.append(n)
            # print upload_these
    # Unhide the indicated items
    unhide_items(unhide_these)
    # Hide the old items
    unhide_items(old_item_selection, 'Hidden')
    # Hide the sub-window
    app.hideSubWindow('apply_wait_indicator')


# Indicates an item to move from offline to online
def off_to_on(button):
    # Grab the globals needed
    global app, new_item_selection, old_item_selection, origins
    for o in origins:
        # Create a string for the prefix of the items selected
        off_pref = ''
        on_pref = ''
        # If it's in the upload page
        if 'upload' in button:
            off_pref = 'upload_offline_items_'
            on_pref = 'upload_online_items_'
        # Otherwise
        else:
            off_pref = 'offline_items_'
            on_pref = 'online_items_'
        # Grab the selected items from the offline list
        selected = app.getListBox(off_pref + o.lower().replace(' ', '_'))
        # print 'offline_items_' + o.lower().replace(' ', '_')
        # Grab the total online and offline lists
        offline = app.getAllListItems(off_pref + o.lower().replace(' ', '_'))
        online = app.getAllListItems(on_pref + o.lower().replace(' ', '_'))
        if selected is not None:
            # For every selected element
            for s in selected:
                # Remove it from the offline list
                offline.remove(s)
                # Append it to the online list
                online.append(s)
                # Work with the global lists as necessary
                if s in old_item_selection:
                    old_item_selection.remove(o + ' ' + s)
                else:
                    new_item_selection.append(o + ' ' + s)
            # Update the ListBox contents
            app.updateListBox(off_pref + o.lower().replace(' ', '_'), sorted(offline))
            app.updateListBox(on_pref + o.lower().replace(' ', '_'), sorted(online))
            # Re-format both of the ListBoxes to their original form (See creation comments for details)
            alternate = True
            for i in range(0, len(app.getAllListItems('offline_items_' + o.lower().replace(' ', '_')))):
                if alternate:
                    pass
                else:
                    app.setListItemAtPosBg(off_pref + o.lower().replace(' ', '_'), i, '#00ffff')
                    app.setListItemAtPosFg(off_pref + o.lower().replace(' ', '_'), i, '#000000')
                alternate = not alternate
            
            alternate = True
            for i in range(0, len(app.getAllListItems('online_items_' + o.lower().replace(' ', '_')))):
                if alternate:
                    pass
                else:
                    app.setListItemAtPosBg(on_pref + o.lower().replace(' ', '_'), i, '#00ffff')
                    app.setListItemAtPosFg(on_pref + o.lower().replace(' ', '_'), i, '#000000')
                alternate = not alternate


# Indicates an item to move from online to offline
def on_to_off(button):
    # Grab the globals needed
    global app, new_item_selection, old_item_selection, origins
    for o in origins:
        # Create a string for the prefix of the items selected
        off_pref = ''
        on_pref = ''
        # If it's in the upload page
        if 'upload' in button:
            off_pref = 'upload_offline_items_'
            on_pref = 'upload_online_items_'
        # Otherwise
        else:
            off_pref = 'offline_items_'
            on_pref = 'online_items_'
        # Get the currently selected items from the online list
        selected = app.getListBox(on_pref + o.lower().replace(' ', '_'))
        # Get the total list for each side
        offline = app.getAllListItems(off_pref + o.lower().replace(' ', '_'))
        online = app.getAllListItems(on_pref + o.lower().replace(' ', '_'))
        if selected is not None:
            # For every selected item
            for s in selected:
                # Append it to offline
                offline.append(s)
                # Remove it from online
                online.remove(s)
                # Work with the global lists as necessary
                if s in new_item_selection:
                    new_item_selection.remove(o + ' ' + s)
                else:
                    old_item_selection.append(o + ' ' + s)
            # Update the ListBox items
            app.updateListBox(off_pref + o.lower().replace(' ', '_'), sorted(offline))
            app.updateListBox(on_pref + o.lower().replace(' ', '_'), sorted(online))
            # Re-format both of the ListBoxes to their original form (See creation comments for details)
            alternate = True
            for i in range(0, len(app.getAllListItems(off_pref + o.lower().replace(' ', '_')))):
                if alternate:
                    pass
                else:
                    app.setListItemAtPosBg(off_pref + o.lower().replace(' ', '_'), i, '#00ffff')
                    app.setListItemAtPosFg(off_pref + o.lower().replace(' ', '_'), i, '#000000')
                alternate = not alternate
            
            alternate = True
            for i in range(0, len(app.getAllListItems(on_pref + o.lower().replace(' ', '_')))):
                if alternate:
                    pass
                else:
                    app.setListItemAtPosBg(on_pref + o.lower().replace(' ', '_'), i, '#00ffff')
                    app.setListItemAtPosFg(on_pref + o.lower().replace(' ', '_'), i, '#000000')
                alternate = not alternate


# Refreshes the required updates by restarting the app
def refresh_updates(button):
    # Grab the globals needed
    global app, items_to_be_updated
    restart_application()


# Updates indicated current items and uploads indicated new items
def update_items(button):
    # Grab the globals needed
    global app
    # If the overall load is completed
    # if start_progress > 99.9:
    # Ask to confirm
    if app.yesNoBox('Update Database', 'Are you sure you want to update? This may take a while!'):
        app.showSubWindow('apply_wait_indicator')
        mythread = ItemUpdatesThread()
        mythread.start()


# endregion

''' Adding new/Editing items '''


# region Adding/Editing

# Populates and edits items as necessary
def edit_contents(tree, *args):
    # Grab the globals we need
    global app, editing_item, jdn, jd
    # Set the item currently being edited
    editing_item = app.getTreeSelected(tree)
    # Save the current properly formatted name
    cn = normalize(editing_item)
    while type(cn) is tuple:
        cn = cn[0]
    cn = normalize(cn)
    # Name
    app.setEntry('new_item_name', cn)
    # Price
    app.setEntry('new_item_price', jd[cn]['price'])
    # SKU
    app.setEntry('new_item_sku', jd[cn]['sku'])
    # Color SKUs
    sks = ''
    app.clearTextArea('new_item_skus')
    for i in jd[cn]['skus']:
        sks += i + '\n'
    app.setTextArea('new_item_skus', sks)
    # Description
    app.clearTextArea('new_item_description')
    app.setTextArea('new_item_description', jd[cn]['description'])
    # Details
    ds = ''
    app.clearTextArea('new_item_details')
    for i in jd[cn]['details']:
        ds += i + '\n'
    app.setTextArea('new_item_details', ds)
    # Colors and Sizes
    cs = ''
    ss = ''
    app.clearTextArea('new_item_colors_new')
    app.clearTextArea('new_item_sizes')
    if jd[cn]['colors'] is not None:
        for i in jd[cn]['colors']:
            if i == 'XXS' or i == 'XS' or i == 'S' or i == 'M' or i == 'L' or i == 'XL' or i == 'XXL' or i == 'XXXL' or i == 'XXXXL' or ' x ' in i:
                ss += i + '\n'
            else:
                cs += i + '\n'
        app.setTextArea('new_item_colors_new', cs)
        app.setTextArea('new_item_sizes', ss)
    # Sizes
    # Images
    iss = ''
    app.setEntry('new_item_images', iss)
    for i in jd[cn]['image_paths']:
        iss += i + ','
    app.setEntry('new_item_images', iss)
    # Origin
    app.setEntry('new_item_origin', jd[cn]['origin'])


# Edits the currently selected item in the original nav tree
def edit_selected(button):
    # Grab the globals
    global editing_item, app
    # Go to the edit tab
    app.setTabbedFrameSelectedTab('Store GUI', 'Create New/Edit Item')
    # Edit the contents, but get the nav tree and not the edit tree
    edit_contents('nav')


# Saves a newly created item
def save_new(button):
    # Grab the globals needed
    global app, jd, jdn, editing_item, upload_these
    # Grab all of the information we want
    # Name
    t_name = app.getEntry('new_item_name')
    # Price
    t_price = app.getEntry('new_item_price')
    # SKU
    t_sku = app.getEntry('new_item_sku')
    # Color SKUs
    t_skus = [x for x in app.getTextArea('new_item_skus').split('\n')]
    # Description
    t_desc = app.getTextArea('new_item_description')
    # Details
    t_details = [x for x in app.getTextArea('new_item_details').split('\n')]
    # Colors
    t_colors = [x for x in app.getTextArea('new_item_colors_new').split('\n')]
    # Check to see which size option is checked
    size_type = app.getRadioButton('size_type')
    # If it's a basic size type
    if size_type == 'Basic':
        t_sizes = [x for x in app.getTextArea('new_item_sizes').split('\n')]
    # Otherwise
    else:
        # Get the first column
        widths = [x for x in app.getTextArea('advanced_item_size_one').split('\n')]
        # Get the second column
        lengths = [x for x in app.getTextArea('advanced_item_size_two').split('\n')]
        # Put them together to make the final strings
        t_sizes = [w + 'x' + l for w in widths for l in lengths]
    # Combine the sizes and the colors
    for s in t_sizes:
        t_colors.append(s)
    # Images
    t_images = [x for x in app.getEntry('new_item_images').split('\n')]
    # Origin
    t_origin = app.getEntry('new_item_origin')
    # If this isn't editing an old item, add this item to the database
    if len(editing_item) == 0:
        jd[t_name] = {'description': t_desc, 'colors': t_colors, 'details': t_details, 'goto': [], 'url': '',
                      'image_paths': t_images, 'image_urls': t_images, 'images': t_images, 'origin': t_origin,
                      'price': t_price, 'sku': t_sku, 'skus': t_skus, 'sizes': t_sizes}
    # Otherwise, just change the current item's information
    else:
        jd[t_name]['price'] = t_price
        jd[t_name]['sku'] = t_sku
        jd[t_name]['skus'] = t_skus
        jd[t_name]['description'] = t_desc
        jd[t_name]['details'] = t_details
        jd[t_name]['colors'] = t_colors
        jd[t_name]['origin'] = t_origin
        jd[t_name]['sizes'] = t_sizes
    # Finally, if the button clicked involved uploading, upload the item
    if 'Upload' in button:
        jd[t_name]['price'] = t_price
        jd[t_name]['sku'] = t_sku
        jd[t_name]['skus'] = t_skus
        jd[t_name]['description'] = t_desc
        jd[t_name]['details'] = t_details
        jd[t_name]['colors'] = t_colors
        jd[t_name]['origin'] = t_origin
        jd[t_name]['sizes'] = t_sizes
    upload_these.append(t_name)
    # noinspection PyUnresolvedReferences
    #jdn[t_name] = Item._make([jd[t_name][k] for k in jd[t_name]])


# Resets entry fields and tree for a new item
def start_new(button):
    global app, editing_item
    editing_item = ''
    # Reset each field
    # Name
    app.setEntry('new_item_name', '')
    # Price
    app.setEntry('new_item_price', '')
    # SKU
    app.setEntry('new_item_sku', '')
    # Color SKUs
    app.clearTextArea('new_item_skus')
    # Description
    app.clearTextArea('new_item_description')
    # Details
    app.clearTextArea('new_item_details')
    # Colors
    app.clearTextArea('new_item_colors_new')
    # Sizes
    app.clearTextArea('new_item_sizes')
    # Images
    app.setEntry('new_item_images', '')
    # Origin
    app.setEntry('new_item_origin', '')


# Method for when different size inputs are selected
def size_option(button):
    if app.getRadioButton('size_type') == 'Basic':
        app.raiseFrame('Basic Sizes')
    else:
        app.raiseFrame('Advanced Sizes')


# Method to send changes of stock to the interface
def stock_changes(button):
    # Grab the globals necessary
    global actual_stocks, initial_stock_values, app
    # Show the wait window
    app.showSubWindow('apply_wait_indicator')
    # Create the dict to send with new information about the products
    updates_required = {}
    # Create a variable to potentially hold a list of items to convert to unlimited items
    make_limited = None
    # First, find out what needs to be updated in terms of stocks
    for k in actual_stocks:
        # If there's no size values for this item
        if type(actual_stocks[k]) is not dict:
            # Then directly check if they're equal
            if actual_stocks[k] != initial_stock_values[k]:
                updates_required[k] = actual_stocks[k]
        # If there are size values
        else:
            # Loop through each one
            for k2 in actual_stocks[k]:
                # If any of them aren't equal
                if actual_stocks[k][k2] != initial_stock_values[k][k2]:
                    # Mark it for updating
                    updates_required[k] = actual_stocks[k]
                    # If this item is becoming unlimited
                    if actual_stocks[k][k2] != -1 and initial_stock_values[k][k2] == -1:
                        # If it's not already made
                        if make_limited is None:
                            # Create the actual list to send over
                            make_limited = []
                        # Append this key to the list
                        make_limited.append(k)
    # Call the appropriate method from the interface
    interface.updateStock(updates_required, now_limited=make_limited)
    print('Done')
    # Hide the app wait window
    app.hideSubWindow('apply_wait_indicator')


# Method that runs threaded class version of above method, preferred so that the app kills itself during a run, but still in testing
def apply_stock_changes(button):
    # Create the thread
    stock_thread = ItemStockUpdatesThread()
    # And run it
    stock_thread.start()


# Method for when a drag/drop operation has begun
def begin_drag(widget):
    print('start: ' + widget)
    pass


# Method for when a drop/drop operation ends
def end_drag(widget):
    print('end: ' + widget)
    pass


# endregion

''' Application Functions '''


# region Application Functions

# Check the git repo and pip for updates
def check_for_updates():
    global app
    app.showSubWindow('update_wait_indicator')
    UpdateGui.main()
    app.hideSubWindow('update_wait_indicator')


# Loads the jd modified from the last usage (stored in the save_data.jon)
def load_user_data(test):
    # Grab the global needed
    global jd
    # Try to restore the jd var
    try:
        # Open the file
        file_save = shelve.open('save_data.jon')
        # Restore the jd
        jd = file_save['jd']
        # Close the file
        file_save.close()
    # It wasn't very effective...
    except:
        # Do nothing, zilch, nada
        pass


# Loads the necessary variables into place
def start_application(button):
    global all_items_uploaded_old, all_items_uploaded, start_progress, app, u_b
    # Get all of the items currently uploaded to the store
    try:
        sf = shelve.open('save_data.jon')
        all_items_uploaded = sf['all_items_uploaded']
        sf.close()
    except:
        all_items_uploaded = interface.get_all_product_names()
    # Start the thread to get the application going
    # app.setStatusbar('')
    refresh_orders(None)
    # order_updates()


# Restarts the application (needed to update the Update Information Page)
def restart_application():
    # If the user confirms a restart
    if app.yesNoBox('Confirm Restart', 'Are you sure you want to restart to update the information?'):
        # Stop the application remotely
        stop_application_remote()
        # Start the application again remotely
        start_window()


# Function for what happens when the app stops
def stop_application():
    # Grab the globals
    global u_b, changes_allowed, cancelled_updates, jd, all_items_uploaded, timer_thread, managed_brands, \
        email_information, app
    # Ask if the user really wants to exit the app, and if so
    if app.yesNoBox('Exit Application', 'Are you sure you want to quit?'):
        # Save everything to one file
        sft = shelve.open('save_data.jon')
        sft['changes_allowed'] = changes_allowed
        sft['jd'] = jd
        sft['cancelled_updates'] = cancelled_updates
        sft['all_items_uploaded'] = all_items_uploaded
        sft['managed_brands'] = managed_brands
        sft.close()
        # Quit the browser in UpdateInfo
        u_b.quit()
        # Stop the browser in this file
        stop_browser()
        app.remove('File')
        app.remove('Orders')
        app.remove('Load')
        app.remove('Brands')
        app.removeAllWidgets(True)
        
        # If there are emails that need to be sent
        if len(email_information) > 0:
            # Import the class for emails
            import email_script
            
            # Use it to email the proper brands
            se = email_script.EmailSending(email_information)
            # And send them off
            se.send_emails(email_information)
        # Stop the timer thread that regularly updates orders
        # timer_thread.cancel()
        # Indicate stopping the app
        return True


# Function for what happens when the app needs to restart
def stop_application_remote():
    # Call the stop_application method
    stop_application()
    # Then actually stop the thing
    app.stop()


# Function that updates the loading message
def update_loading_message():
    # Update the loading message
    app.setLabel('loading_message', SyS.get_loading_message())
    # Python used Rest!
    SyS.slp(10)


# Shows a sub window with a restart message
def restart_needed(subwindow_name):
    test = app.yesNoBox("Confirm Save", "Changes made will only take place after you restart, which may take a while, "
                                        "would you like to do so now?")
    if test:
        restart_application()
    else:
        app.hideSubWindow(subwindow_name)


# Function that starts the Manage Brands window
def start_manage_brands():
    app.showSubWindow('manage_brands')


# Function for when the user exits manage brands
def exit_manage_brands(button):
    # test = app.yesNoBox('Confirm Cancel', 'Are you sure you wish to exit without saving your changes?')
    # if test:
    app.hideSubWindow('manage_brands')


# Function for when the user saves in manage brands
def save_manage_brands(button):
    global managed_brands, app, brand_checks
    managed_brands = []
    for b in brand_checks:
        if app.getCheckBox(b):
            managed_brands.append(" ".join(b.split(" ")[1:]))
    restart_needed('manage_brands')


# Function to start entering brands to email for new brands
def start_email_brands():
    app.showSubWindow('email_new_brands')


# Provides functionality to the button that adds new rows to the email interface
def add_email_brand(button):
    # Grab the row that this interface should add the new inputs on
    global cer
    # Increment that row
    cer += 1
    # Re-open the email frame
    app.openFrame('email_inputs')
    # Create an initial row of inputs
    app.label('brand_name_' + str(cer), 'Brand Name:', pos=(cer, 0), padding=(30, 15))
    app.entry('email_brand_name_' + str(cer), pos=(cer, 1), padding=(30, 15))
    app.label('brand_email_' + str(cer), 'Brand Email Address:', pos=(cer, 2), padding=(30, 15))
    app.entry('email_brand_email_' + str(cer), pos=(cer, 3), padding=(30, 15))
    # Close the frame
    app.stopFrame()


# Function for when the user exits emailing brands
def exit_email_brands(button):
    # Asks for confirmation since information will actually be lost here
    test = app.yesNoBox('Confirm Cancel', 'Are you sure you wish to exit without saving your changes?')
    # If yes
    if test:
        # Hide the window
        app.hideSubWindow('email_new_brands')


# Function for saving and sending emails
def save_email_brands(button):
    # Grab the globals
    global app, email_information
    # Ask first
    ask = app.yesNoBox('Confirm Send Emails', 'Are you sure you\'d like to send emails to these companies?\n'
                                              'Emails will be sent when the application window is closed.')
    # If confirmed
    if ask:
        # Grab the number of brands that are being contacted
        global cer
        # Re-initialize the brand names just to be safe
        brand_names = {}
        # Grab all of the inputs from the entry
        for i in range(cer + 1):
            # Get the name and email for this column
            t_name = app.getEntry('email_brand_name_' + str(i)).title()
            t_email = app.getEntry('email_brand_email_' + str(i))
            app.setEntry('email_brand_name_' + str(i), '')
            app.setEntry('email_brand_email_' + str(i), '')
            if i != 0:
                app.removeLabel('brand_name_' + str(i))
                app.removeEntry('email_brand_name_' + str(i))
                app.removeLabel('brand_email_' + str(i))
                app.removeEntry('email_brand_email_' + str(i))
            # Save it to the dict
            brand_names[t_name] = t_email
        # Debugging print statement
        print(brand_names)
        # Update the entries to email when the window is closed
        email_information.update(brand_names)
        # And finally hide the window
        app.hideSubWindow('email_new_brands')


# endregion

''' Window Start Process '''


# Updated start method
def start_window():
    ## Initialization ##
    # Grab the copy module
    import copy
    # Grab the globals
    global app, jd, jdo, new_item_selection, old_items, item_names, all_items_uploaded, u_b, changes_allowed, \
        items_to_be_updated, cancelled_updates, old_item_names, origins, actual_stocks, initial_stock_values, \
        managed_brands, brand_checks
    
    '''
    ----- Data -----
    '''
    
    # region Data
    # Grab all of the item names currently uploaded to the store
    # u.get_current_urls()
    interface.get_current_urls()
    # Get rid of the size information in the colors of the jd
    sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    jdo = {}
    jd = c.convert('items.json')
    # Try to load the changes allowed variable from the necessary file
    try:
        file_save = shelve.open('save_data.jon')
        changes_allowed = file_save['changes_allowed']
        jdo = file_save['jd']
        managed_brands = file_save['managed_brands']
        file_save.close()
        # Add everything that's not in the current data from the previous data
        for n in jdo:
            if n not in jd:
                jd[n] = jdo[n]
        # If the changes aren't allowed for an item, reset it's data to what it was in the previous run
        for n in changes_allowed:
            if n in jd and not changes_allowed[n]:
                jd[n] = jdo[n]
        # If there is any information missing (mainly description) from this version that wasn't missing from the last
        # version, just use the last version of this data
        for n in jd:
            try:
                if jd[n]['description'].strip() == '' and jdo[n]['description'].strip() != '':
                    jd[n]['description'] = jdo[n]['description']
            except:
                pass
    # If it doesn't work, don't worry about it
    except:
        pass
    # Python used Iterate!
    for item in jd:
        # Add all items from jd not currently in changes_allowed to it
        if item not in changes_allowed:
            changes_allowed[item] = {}
            # Python used Iterate!
            for ib in jd[item]:
                exec(('changes_allowed[item][\'' + ib + '\'] = True'), globals(), locals())
            # Python used Iterate!
            if jd[item]['colors'] is not None:
                for co in reversed(jd[item]['colors']):
                    if co in sizes:
                        jd[item]['colors'].remove(co)
    # endregion
    
    '''
    ----- Setup -----
    '''
    
    # Get the browser to the right place
    interface.init()
    
    with gui("Lionel Smith Ltd. Interface") as app:
        
        # region Setup
        
        # Set app window size
        app_w = 1000
        app_h = 800
        # Get Current Screen Size
        scr_w = GetSystemMetrics(0)
        scr_h = GetSystemMetrics(1)
        # Calculate x and y from the previous 4 vars
        app_x = (scr_w / 2) - (app_w / 2)
        app_y = ((scr_h / 2) - (app_h / 2))
        # Set the Title, Font, and other properties
        app.setTitle('Lionel Smith Ltd. Online Store Interface')
        app.setIcon('imgs/storeicon.ico')
        app.setFont(10)
        app.setLocation(app_x, app_y)
        app.setSize(app_w, app_h)
        # app.setResizable(canResize=False)
        app.setSticky('news')
        app.setExpand('both')
        #app.setTtkTheme('arc')
        
        # endregion
        
        '''
        ----- Sub-Windows -----
        '''
        
        # region Sub-Windows
        
        # Wait Indicator Sub-Window
        with app.subWindow('apply_wait_indicator', title='One Moment...', modal=True):
            # Create the frame to hold the message in
            with app.frame('wait_frame', inPadding=(30, 10)):
                # Initialize the basic prompt
                app.label('wait_message', 'Please wait as changes are applied to your data', 0, 0, inPadding=(30, 10))
                # And give a random, completely unnecessary loading message
                app.label('apply_loading_message', SyS.get_loading_message(), 1, 0, inPadding=(30, 10))

        # JSON Error Update
        with app.subWindow('json_update_indicator', title='One Moment...', modal=True):
            # Create the frame to hold the message in
            with app.frame('json_frame', inPadding=(30, 10)):
                # Initialize the basic prompt
                app.label('json_message', 'WARNING\nYour database file is not up to date!\n'
                                          'To fix this, please ensure that Kitematic is running (click its icon '
                                          'in the start menu, shown below, and wait to ensure that you do not get a loading screen)\n'
                                          'then click inventoryupdate.bat in the Documents folder and wait for the '
                                          'process to complete.\n\n'
                                          'In the meantime, previous data will be displayed...', 0, 0,
                          inPadding=(30, 10))
                app.addImage("example1", "imgs/KitematicExample.png", 1,0)
                app.addImage("example2", "imgs/KitematicOpened.png",1,1)
                # And give a random, completely unnecessary loading message
                app.label('json_loading_message', SyS.get_loading_message(), 2, 0, inPadding=(30, 10))
        
        # Update Indicator Sub-Window
        with app.subWindow('update_wait_indicator', title='One Moment...', modal=True):
            # Create the frame to hold the message in
            with app.frame('update_wait_frame', inPadding=(30, 10)):
                # Initialize the basic prompt
                app.label('update_wait_message', 'Please wait as the application and libraries are updated', 0, 0,
                          inPadding=(30, 10))
                # And give a random, completely unnecessary loading message
                app.label('update_loading_message', SyS.get_loading_message(), 1, 0, inPadding=(30, 10))
        
        # Start Wait Indicator Sub-Window
        with app.subWindow('start_wait_indicator', title='One Moment...', inPadding=(30, 10)):
            # Create the frame to hold the message in
            with app.frame('hold_on_frame', inPadding=(30, 5)):
                # Initialize the basic prompt
                app.label('hold_on', 'Please wait as the application starts...', 0, 0, inPadding=(30, 5))
                # And give a random, completely unnecessary loading message
                app.label('loading_message', SyS.get_loading_message(), 1, 0, inPadding=(30, 5))
        
        # Start Wait Indicator Sub-Window
        with app.subWindow('leave_feedback', title='Feedback', inPadding=(30, 10)):
            # Create the frame to hold the message in
            with app.frame('leave_feedback_frame', inPadding=(30, 5)):
                # Initialize the basic prompt
                app.label('enter_feedback_indicator', 'Enter feedback here:', 0, 0, inPadding=(30, 5))
                # Create the area for the text input
                app.addTextArea('feedback_input', 0, 1, colspan=2)
                # Create the buttons to save/send the feedback
                app.button('Cancel Feedback', exit_feedback, pos=(1, 0))
                app.button('Save Feedback', send_feedback, pos=(1, 2))
        
        # Manage Brands Sub-Window
        with app.subWindow('manage_brands', title='Manage Brands', modal=True):
            # Create the frame to hold the info in
            with app.frame('manage_brands_frame', inPadding=(10, 30)):
                # Add the label for this window
                app.label('pick_one_already', 'Check the items you would like to manage:', pos=(0, 0), colspan=3)
                # Create the positional variables for the loop
                x = 0
                y = 1
                # For every brand found in the scrapers folder
                for b in brand_names:
                    # Create the checkbox for the current brand
                    app.checkBox('Show ' + b, checked=b in managed_brands, pos=(y, x), padding=(30, 15))
                    # Check it if it's currently managed
                    app.setCheckBox('Show ' + b, b in managed_brands)
                    # Append the name of this checkbox to the list
                    brand_checks.append('Show ' + b)
                    # Increment the x value
                    x += 1
                    # If the table has reached the third column
                    if x == 3:
                        # Reset x
                        x = 0
                        # Increment y
                        y += 1
                # Increment y by 2
                y += 2
                # Add a horizontal line as a separator
                app.addHorizontalSeparator(y - 1, 0, colour="red", colspan=3)
                # Add the buttons needed
                app.button('Cancel Brand Management', exit_manage_brands, pos=(y, 0), padding=(30, 15))
                app.button('Save Brand Changes', save_manage_brands, pos=(y, 2), padding=(30, 15))
        
        # Email New Brands Sub-Window
        with app.subWindow('email_new_brands', title='Enter Brands', modal=True):
            # Create the frame to hold the info in
            with app.frame('new_email_frame', padding=(30, 15)):
                # Create an indicator label
                app.label('Enter the name of the company and email in the fields below:', pos=(0, 0), colspan=4,
                          padding=(30, 15))
                # Create a frame for the inputs to email new brands
                with app.frame('email_inputs', pos=(1, 0), colspan=4, padding=(30, 15)):
                    # Create an initial row of inputs
                    app.label('brand_name_0', 'Brand Name:', pos=(0, 0), padding=(30, 15))
                    app.entry('email_brand_name_0', pos=(0, 1), padding=(30, 15))
                    app.label('brand_email_0', 'Brand Email Address:', pos=(0, 2), padding=(30, 15))
                    app.entry('email_brand_email_0', pos=(0, 3), padding=(30, 15))
                # Create a button that would add another row
                app.button('Add Another Brand', add_email_brand, pos=(2, 1), colspan=2, padding=(30, 15))
                # Create the cancel button
                app.button('Cancel Email', exit_email_brands, pos=(3, 0), colspan=2, padding=(30, 15))
                # Create the submit/send button
                app.button('Submit/Send Emails', save_email_brands, pos=(3, 2), colspan=2, padding=(30, 15))
        
        # Register the string changing method
        # app.registerEvent(update_loading_message())

        date_str = 'items' + \
                        (('0' + str(date.today().month)) if date.today().month < 10 else str(date.today().month)) + \
                        ('0' + str(date.today().day) if date.today().day < 10 else str(date.today().day)) + \
                        str(date.today().year)[2:] + '.json'
        if date_str in glob.glob('*.json'):
            # Start the startup sub-window
            app.showSubWindow('start_wait_indicator')
        else:
            app.showSubWindow('json_update_indicator')
        # Start the thread that reloads the message in the sub window
        # loading_thread = threading.Thread(target=update_loading_message())
        # loading_thread.start()
        
        # endregion
        
        '''
        ----- Menus -----
        '''
        
        # region Menus
        # Create the file menu
        file_menu = ['Open in Chrome...', 'Open Item Source Folder...', 'Open Images Folder...']
        file_functions = [open_home, open_item_folder, open_image_folder]
        app.addMenuList('File', file_menu, file_functions)
        # Create the orders menu
        order_menu = ['Refresh Orders', 'Open Fedex in Chrome...', 'Open Fedex in Firefox...']
        order_functions = [refresh_orders, open_fedex, open_fedex_firefox]
        app.addMenuList('Orders', order_menu, order_functions)
        # Data Restoration Menu
        load_menu = ['Load Previous Data', 'Upload Changes']
        load_functions = [load_user_data, update_items]
        app.addMenuList('Load', load_menu, load_functions)
        # Brands Menu
        brands_menu = ['Configure Brands...', 'Email New Brands...']
        brands_functions = [start_manage_brands, start_email_brands]
        app.addMenuList('Brands', brands_menu, brands_functions)
        # Help Menu
        help_menu = ['Open Manual...', 'Check for updates...', 'Leave Feedback...', 'Update Driver...', 'About...']
        help_functions = [GuiManual.main, check_for_updates, leave_feedback, SpS.update_driver, aboutMe]
        app.addMenuList('Help', help_menu, help_functions)
        # Create the Splash Screen
        # app.showSplash('Lionel Smith Ltd. Store Manager', fill='teal', stripe='white', fg='blue', font=44)
        # endregion
        
        '''
        ----- Main Frame -----
        '''
        
        ## Begin Tabbed Frame ##
        with app.tabbedFrame('Store GUI'):
            
            '''
            ----- Orders -----
            '''
            
            # region Orders
            
            ## Begin Order Management Tab ##
            with app.tab('Orders'):
                
                ## Start Order Selection/Information Editing Pane ##
                with app.panedFrame('Order Management', width=app_w / 3):
                    # Order Choice Label and Input
                    app.label('oc', 'Choose an order:', 0, 0)
                    app.option('orders', ['', ''], 1, 0, colspan=2)
                    app.setOptionBoxChangeFunction('orders', change_contents)
                    # Shipping Label and Input
                    app.label('si', 'Shipping #:', 2, 0)
                    app.entry('shipping_num', pos=(3, 0), colspan=2)
                    # Complete Order Button
                    app.button('Complete Order', complete_item, 4, 0, colspan=2)
                    # Save and Continue Button
                    app.button('Save and Continue', save_item, 5, 0, colspan=2)
                    # Complete Button
                    app.button('Submit All Completed', complete_items, 6, 0, colspan=2)
                    
                    ## Start Order View/Refresh Pane ##
                    with app.panedFrame('Order Misc',vertical=True):
                        # Refresh Orders Button
                        app.button('Refresh Orders', refresh_orders, 0, 0)
                        # Open in Chrome Button
                        app.button('Open in Chrome', open_home, 0, 1)
                        
                        ## Start Order Information Pane ##
                        with app.panedFrame('Order Information', width=app_w * 2 / 3):
                            # Name of Customer Label and Information
                            app.label('cn', 'Name:', 0, 0)
                            app.label('customer', '', 0, 1)
                            # app.addImage('product_image', 'icon.jpg')
                            # Shipping Address Label and Information
                            app.label('sa', 'Shipping Address:', 1, 0)
                            app.label('shipping_addr', '', 1, 1)
                            # Items Label and Information
                            app.label('il', 'Items:', 2, 0, rowspan=2)
                            app.label('order_items', '', 2, 1, rowspan=2)
                        
                        ## Stop Order View/Refresh Pane ##
                    
                    ## Stop Order Information Pane ##
                
                ## Stop Order Selection/Information Editing Pane ##
            
            ## Stop Orders Tab ##
            
            # endregion
            
            '''
            ----- Inventory -----
            '''
            
            # region Stock
            
            ## Begin Inventory Checker Tab ##
            with app.tab('Items Database'):
                
                ## Begin Tree Frame ##
                # Begin by creating the first paned frame
                with app.panedFrame('items'):
                    
                    # Then put the item tree based on the formatted string given
                    tree_xml = format_json()
                    app.addTree('nav', tree_xml)
                    app.setTreeColours('nav', 'black', 'white', 'blue', 'yellow')
                    app.setTreeEditable('nav', False)
                    # Add the tree-clicking functionality
                    app.setTreeDoubleClickFunction('nav', display_info)
                    
                    ## Begin Item Contents Pane ##
                    # Create the second paned frame
                    with app.panedFrame('info'):
                        with app.scrollPane('infoScrollPane'):
                            
                            # Name label and info
                            app.checkBox('Item Name:', pos=(0, 0))
                            app.label('name', '', pos=(0, 1))
                            # Image and info
                            app.image('item_image', 'imgs/icon.gif', pos=(0, 2), rowspan=2)
                            app.zoomImage('item_image', -5)
                            # Url label and info
                            app.checkBox('URL:', pos=(1, 0))
                            app.label('url', '', pos=(1, 1))
                            # Origin label and info
                            app.checkBox('Store of origin:', pos=(2, 0))
                            app.label('origin', '', pos=(2, 1), colspan=2)
                            # Sku label and info
                            app.checkBox('SKU:', pos=(3, 0))
                            app.label('sku', '', pos=(3, 1), colspan=2)
                            # Price label and info
                            app.checkBox('Price:', pos=(4, 0))
                            app.label('price', '', pos=(4, 1), colspan=2)
                            # Description label and info
                            app.checkBox('Description:', pos=(5, 0))
                            app.message('description', '', pos=(5, 1), colspan=2)
                            # Details label and info
                            app.checkBox('Details:', pos=(6, 0))
                            app.listBox('details', [], pos=(6, 1), colspan=2)
                            # Image path label and info
                            app.checkBox('Image Paths:', pos=(7, 0))
                            app.listBox('image_paths', [], pos=(7, 1), colspan=2)
                            app.button('Edit Item', edit_selected, pos=(8, 0), colspan=3)
                            
                            # Update the shown image if that image is clicked in its list
                            def update_image(img_list):
                                # Grab the global/local app (either one works, but using global just in case)
                                global app
                                # Get the selected image in the list
                                sel = app.getListItems('image_paths')
                                # As long as an image was found
                                if sel is not None:
                                    if len(sel) != 0:
                                        # Open the image given
                                        im = Image.open('C:/imgJson/' + sel[0])
                                        # Save it as a gif to allow for easier opening
                                        im.save('imgs/item.gif', 'GIF')
                                        # Reload the image in the GUI
                                        app.reloadImage('item_image', 'imgs/item.gif')
                                        # Scale the image to make it an appropriate size
                                        app.zoomImage('item_image', -3)
                                # If that doesn't work
                                else:
                                    # Do nothing
                                    pass
                        
                        # Set the list item click function to the one above
                        app.setListBoxChangeFunction('image_paths', update_image)
                    
                    ## Stop Item Info Pane ##
                
                ## Stop Item Select pane ##
            
            ## Stop Inventory Tab ##
            
            # endregion
            
            '''
            ----- Updates -----
            '''
            
            # region Updates
            
            ## Begin Update Tab ##
            with app.tab('Updates'):
                
                ## Begin Item Update Selection Pane ##
                with app.panedFrame('Item Updates'):
                    
                    ## Begin Data Obtaining Stage ##
                    xml_string = obtain_data()
                    ## End Data Obtaining Stage ##
                    
                    # Set the current names to be uploaded to the item names referenced by the changes needed
                    items_to_be_updated = item_names
                    # Try to load the previous cancelled updates
                    try:
                        s_f = shelve.open('save_data.jon')
                        cancelled_updates = s_f['cancelled_updates']
                        s_f.close()
                    # If there aren't any, create a dict for the cancelled updates
                    except:
                        # Python used Iterate!
                        for i in items_to_be_updated:
                            cancelled_updates[i] = False
                    
                    ## Item Selection Contents ##
                    #app.setSticky('news')
                    
                    # Updated Items Tree
                    app.addTree('update_tree', xml_string)
                    app.setTreeColours('update_tree', 'black', 'white', 'blue', 'yellow')
                    app.setTreeEditable('update_tree', False)
                    # Add the tree-clicking functionality
                    app.setTreeDoubleClickFunction('update_tree', update_contents)
                    
                    ## Start Update Button Pane ##
                    with app.panedFrame('Update Buttons',vertical=True):
                        
                        # Disable Update Button (singular)
                        app.addButton('Disable Update', disable_update, 0, 0, colspan=2)
                        # Refresh Updates Button
                        app.addButton('Refresh Updates', refresh_updates, 0, 2, colspan=2)
                        # Separator for visual clarity
                        app.addHorizontalSeparator(1, 0, 4, colour='lightblue')
                        # Submit/Update Store Button
                        app.addButton('Update Store', update_items, 2, 0, colspan=4)
                        
                        ## Start Other Update Information/Operations Pane ##
                        with app.panedFrame('Update Misc'):
                            # Label for clarity
                            app.addLabel('item_prompt', 'Comparing Item Data', 0, 0, colspan=2)
                            # Separator for clarity
                            app.addHorizontalSeparator(1, 0, 2, colour='lightblue')
                            
                            # Start the Old Item Information
                            with app.labelFrame('Old Item', 2, 0):
                                # Display Old Name
                                app.addLabel('old_item_name', 'Name: ' + item_names[0], 0, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(1, 0, colour='lightblue')
                                # Display Old Description Label
                                app.addLabel('old_item_desc_label', 'Description:', 2, 0)
                                # Display Old Description
                                app.addMessage('old_item_desc',
                                               remove_html(
                                                   old_items[item_names[0]]['description'].replace('&nbsp;', '')), 3, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(4, 0, colour='lightblue')
                                # Display Old Details Label
                                app.addLabel('old_item_dets_label', 'Details:', 5, 0)
                                # Display Old Details
                                app.addListBox('old_item_details', old_items[item_names[0]]['details'], 6, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(7, 0, colour='lightblue')
                                # Display Old Details Label
                                app.addLabel('old_item_colors_label', 'Colors:', 8, 0)
                                # Display Old Details
                                app.addListBox('old_item_colors', sorted(old_items[item_names[0]]['colors']), 9, 0)
                            # Stop Old Item Information
                            
                            # Start New Item Information
                            with app.labelFrame('New Item:', 2, 1):
                                # Display New Item Name
                                app.addLabel('new_item_name', 'Name: ' + normalize(item_names[0]), 0, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(1, 0, colour='lightblue')
                                # Display New Description Label
                                app.addLabel('new_item_desc_label', 'Description:', 2, 0)
                                # Display New Description
                                app.addMessage('new_item_desc', jd[item_names[0]]['description'], 3, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(4, 0, colour='lightblue')
                                # Display New Details Label
                                app.addLabel('new_item_dets_label', 'Details:', 5, 0)
                                # Display New Details
                                app.addListBox('new_item_details',
                                               [s.replace('\xa0', ' ').replace('\xe9', 'e') for s in
                                                jd[item_names[0]]['details']], 6, 0)
                                # Separator for clarity
                                app.addHorizontalSeparator(7, 0, colour='lightblue')
                                # Display Old Details Label
                                app.addLabel('new_item_colors_label', 'Colors:', 8, 0)
                                # Display Old Details
                                app.addListBox('new_item_colors', sorted(jd[item_names[0]]['colors']), 9, 0)
                            # Stop New Item Information
                        
                        ## Stop Update Information/Operations Pane ##
                    
                    ## Stop Update Buttons Frame ##
                
                ## Stop Item Update Selection Pane ##
            
            ## End Update Tab ##
            
            # endregion'''
            
            '''
            ----- Inventory Management -----
            '''
            
            # region Inventory Management
            
            ## Begin Store Inventory Management Tab ##
            with app.tab('Inventory Management'):
                
                # region Data Setup
                # Create an array to store items not currently online
                not_online_items = []
                # Create a list to store currently uploaded items
                uploaded_items = []
                # Set up dicts to hold the items sorted by origin store
                origin_items_online = {}
                origin_items_offline = {}
                origin_items_uploaded = {}
                origin_items_not_uploaded = {}
                shown = []
                # Set the origin to UpdateInfo's origins variable
                # origins = u.origins
                origins = interface.origins
                # Get the list of items currently uploaded to the store
                current_store_items = SpS.get_item_names()
                try:
                    assert (len(current_store_items) > 0)
                except:
                    print('No store items obtained')
                # Python used Iterate!
                for o in origins:
                    # Create the arrays within each dict
                    origin_items_online[o] = []
                    origin_items_offline[o] = []
                    origin_items_not_uploaded[o] = []
                # Python used Iterate!
                for i in jd:
                    # Populate the arrays
                    if i not in item_names:
                        # If it's actually online
                        if i in current_store_items or jd[i]['origin'] + ' ' + i in current_store_items:
                            # Append it to the total uploaded items
                            uploaded_items.append(jd[i]['origin'] + ' - ' + i)
                            # And to the dict of items by origin
                            try:
                                origin_items_offline[jd[i]['origin']].append(i)
                            except:
                                origin_items_offline[jd[i]['origin']] = []
                                origin_items_offline[jd[i]['origin']].append(i)
                        # If it's not online
                        else:
                            # Add it to the proper dict
                            not_online_items.append(jd[i]['origin'] + ' - ' + i)
                            # And to the dict sorted by origin
                            try:
                                origin_items_not_uploaded[jd[i]['origin']].append(i)
                            except:
                                origin_items_not_uploaded[jd[i]['origin']] = []
                                origin_items_not_uploaded[jd[i]['origin']].append(i)
                    # If it's uploaded and not hidden
                    else:
                        # Add it to the list of appended items
                        uploaded_items.append(jd[i]['origin'] + ' - ' + i)
                        shown.append(jd[i]['origin'] + ' - ' + i)
                        # And to the dict of uploaded items by origin
                        try:
                            origin_items_online[jd[i]['origin']].append(i)
                        except:
                            origin_items_online[jd[i]['origin']] = []
                            origin_items_online[jd[i]['origin']].append(i)
                
                # Find all of the currently uploaded out of season items
                out_of_season = []
                # Python used Iterate!
                for a in shown:
                    try:
                        if a.split(' - ')[1] not in list(jd.keys()):
                            out_of_season.append(a)
                    except:
                        if a not in list(jd.keys()):
                            out_of_season.append(a)
                
                # Find all of the not currently uploaded in-season items
                in_season = []
                # Python used Iterate!
                for j in jd:
                    if j not in all_items_uploaded:
                        in_season.append(j)
                
                # Set the old item names (backup variable) to item names
                old_item_names = item_names
                # Variable to keep track of which row we're on
                current_row = 0
                
                # endregion
                
                # Start the internal tabbed frame
                with app.tabbedFrame('Inventory Management Tabs'):
                    
                    # region Show/Hide Tab
                    
                    with app.tab('Show/Hide Online Items'):
                        
                        # Start the first Paned Frame
                        with app.panedFrame('In-Season Offline Item Boxes', sash=10):
                            # Start the scroll pane for this section
                            with app.scrollPane('In-Season Offline Item Scroll Pane'):
                                
                                # Set the sticky value
                                app.setSticky('news')
                                
                                # Python used Iterate!
                                for o in origins:
                                    # Set the stretch and sticky attributes
                                    # app.setStretch('row')
                                    hname = 'Hidden ' + o.title() + ' Items:'
                                    space = '' * int((60-len(hname))/2)
                                    hname = space + hname + space
                                    # Add the offline labels
                                    app.label('offline_label_' + o.lower().replace(' ', '_'),
                                              hname, current_row, 0)
                                    # Set stretch
                                    app.setStretch('both')
                                    # Add the offline items ListBox
                                    app.listbox('offline_items_' + o.lower().replace(' ', '_'),
                                                sorted(origin_items_offline[o]),
                                                current_row + 1, 0, drag=[begin_drag, end_drag])
                                    # Add a horizontal separator if it's not the last box
                                    if origins.index(o) != len(origins) - 1:
                                        app.addHorizontalSeparator(current_row + 2, 0, colour="red")
                                        # Increment the current row
                                        current_row += 3
                            
                            # Start the second Paned Frame for the transfer arrows
                            #app.setSticky('news')
                            with app.panedFrame('Arrows', vertical=True, width=app_w/2): #, sash=67, stretch='ew'
                                # Set sticky
                                app.setSticky('nesw')
                                # Add offline to online button label
                                app.label('offtoon', 'Show', 0, 0)
                                # Set sticky
                                app.setSticky('')
                                # Set padding inside the widget
                                app.setInPadding([30, 10])
                                # Add offline to online button
                                app.button('->', off_to_on, 1, 0)
                                # Set sticky
                                app.setSticky('s')
                                # Set padding
                                app.setInPadding([0, 0])
                                # Add online to offline move button label
                                app.label('ontooff', 'Hide', 2, 0)
                                # Set sticky
                                app.setSticky('')
                                # Set padding
                                app.setInPadding([30, 10])  #
                                # Add online to offline move button
                                app.button('<-', on_to_off, 3, 0)
                                # Set padding
                                app.setInPadding([0, 0])
                                # Set sticky to nothing
                                app.setSticky('')
                                # Set padding
                                app.setPadding([20, 20])
                                # app.setPadding([150, 0])
                                # Set inside padding
                                # app.setInPadding([10, 10])
                                app.setInPadding([30, 20])
                                # Add apply button
                                app.button('Apply', hide_unhide, 6, 0)
                                # Set padding
                                app.setInPadding([0, 0])
                                # Set sticky
                                app.setSticky('nesw')
                                # End Buttons Panel
                                
                                # Add the list of out of season items if necessary
                                if len(out_of_season) != 0:
                                    # Set the stretch to both
                                    app.setStretch('both')
                                    # Start the out of season items frame
                                    app.startPanedFrame('Out of Season Items')
                                    # Set the stretch
                                    # app.setStretch('row')
                                    # Add the label for the items
                                    app.addLabel('oos', 'Out of Season Items:', 0, 0)
                                    # Add the list
                                    app.addListBox('oosi', sorted(out_of_season), 1, 0)
                                    # Stop the out of season items frame
                                    app.stopPanedFrame()
                                
                                # Stop the arrow Paned Frame
                            
                            # Reset the current row variable
                            current_row = 0
                            app.setPaneSashPosition(67, 'Arrows')
                            app.setSticky('nes')
                            # Start the Online Items Paned Frame
                            with app.panedFrame('Online Item Boxes'):
                                
                                # Start the ScrollPane for this section
                                with app.scrollPane('In-Season Online Item Scroll Pane'):
                                    
                                    # Reset the sticky
                                    app.setSticky('news')
                                    # Python used Iterate!
                                    for o in origins:
                                        # Set the stretch and sticky attributes
                                        # app.setStretch('row')
                                        sname = 'Shown/Live ' + o.title() + ' Items:'
                                        space = '' * int((60-len(sname))/2)
                                        sname = space + sname + space
                                        # Add the online labels
                                        app.label('online_label_' + o.lower().replace(' ', '_'),
                                                  sname, current_row)
                                        # Set the stretch
                                        app.setStretch('both')
                                        # Add online items ListBox
                                        app.listbox('online_items_' + o.lower().replace(' ', '_'),
                                                    sorted(origin_items_online[o]),
                                                    current_row + 1, drag=[begin_drag, end_drag])
                                        # Add a horizontal separator if it's not the last box
                                        if origins.index(o) != len(origins) - 1:
                                            app.addHorizontalSeparator(current_row + 2, colour="red")
                                            # Increment the current row
                                            current_row += 3
                                    
                                    # - Begin formatting ListBoxes -#
                                    # Create variable to indicate alternating rows
                                    alternate = True
                                    # Python used Iterate!
                                    for o in origins:
                                        # Reset the alternating variable
                                        alternate = True
                                        # Python used Iterate!
                                        for i in range(0, len(
                                                app.getAllListItems('offline_items_' + o.lower().replace(' ', '_')))):
                                            # If it's not the alternated row
                                            if alternate:
                                                # Do nothing
                                                pass
                                            # If it is
                                            else:
                                                # Reformat this row
                                                app.setListItemAtPosBg('offline_items_' + o.lower().replace(' ', '_'),
                                                                       i,
                                                                       '#00ffff')
                                                app.setListItemAtPosFg('offline_items_' + o.lower().replace(' ', '_'),
                                                                       i,
                                                                       '#000000')
                                            # Toogle the alternating variable
                                            alternate = not alternate
                                    
                                    # Reset alternating variable
                                    alternate = True
                                    # Python used Iterate!
                                    for o in origins:
                                        # Rest the alternating variable
                                        alternate = True
                                        # Python used Iterate!
                                        for i in range(0,
                                                       len(app.getAllListItems(
                                                           'online_items_' + o.lower().replace(' ', '_')))):
                                            # If it's not the alternated row
                                            if alternate:
                                                # Do nothing
                                                pass
                                            # If it is
                                            else:
                                                # Reformat this row
                                                app.setListItemAtPosBg('online_items_' + o.lower().replace(' ', '_'), i,
                                                                       '#00ffff')
                                                app.setListItemAtPosFg('online_items_' + o.lower().replace(' ', '_'), i,
                                                                       '#000000')
                                            # Toogle the alternating variable
                                            alternate = not alternate
                                    # - End formatting ListBoxes -#
                                # End ScrollPane
                            
                            # End Online Panel
                        
                        # End Offline Panel
                    
                    # endregion
                    
                    # region Upload Tab
                    
                    # Start offline item management tab
                    with app.tab('Upload Offline Items'):
                        
                        # Start the first Paned Frame
                        with app.panedFrame('Upload In-Season Offline Item Boxes', width=app_w / 3):
                            
                            with app.scrollPane('Upload In-Season Offline Item Scroll', sticky='nesw'):
                                
                                # Set the sticky value
                                app.setSticky('nesw')
                                
                                # Python used Iterate!
                                for o in origins:
                                    # Set the stretch and sticky attributes
                                    # app.setStretch('row')
                                    # Add the offline labels
                                    app.label('upload_offline_label_' + o.lower().replace(' ', '_'),
                                              'Offline ' + o.title() + ' Items:',
                                              current_row, 0)
                                    # Set stretch
                                    app.setStretch('both')
                                    # Add the offline items ListBox
                                    app.listbox('upload_offline_items_' + o.lower().replace(' ', '_'),
                                                sorted(origin_items_not_uploaded[o]),
                                                current_row + 1, 0, drag=[begin_drag, end_drag])
                                    # Add a horizontal separator if it's not the last box
                                    if origins.index(o) != len(origins) - 1:
                                        app.addHorizontalSeparator(current_row + 2, 0, colour="red")
                                        # Increment the current row
                                        current_row += 3
                            # End Scroll Pane
                            
                            # Start the second Paned Frame for the transfer arrows
                            with app.panedFrame('Upload Arrows', width=app_w / 3, vertical=True):
                                
                                # Set sticky
                                app.setSticky('s')
                                # Add offline to online button label
                                app.label('upload_offtoon', 'Upload', 0, 0)
                                # Set sticky
                                app.setSticky('')
                                # Set padding inside the widget
                                app.setInPadding([30, 10])
                                # Add offline to online button
                                app.addNamedButton('->', 'upload', off_to_on, 1, 0)
                                '''
                                # Set sticky
                                app.setSticky('s')
                                # Set padding
                                app.setInPadding([0, 0])
                                # Add online to offline move button label
                                app.addLabel('upload_ontooff', 'Remove from Store', 2, 0)
                                # Set sticky
                                app.setSticky('')
                                # Set padding
                                app.setInPadding([30, 10])  #
                                # Add online to offline move button
                                app.addNamedButton('<-', 'unupload', on_to_off, 3, 0)
                                #'''
                                # Set padding
                                app.setInPadding([0, 0])
                                # Set sticky
                                app.setSticky('nesw')
                                
                                # Set padding
                                app.setPadding([20, 20])
                                # Set inside padding
                                app.setInPadding([30, 20])
                                app.setSticky('')
                                # Add apply button
                                app.addNamedButton('Apply', 'apply_upload', hide_unhide, 6, 0)
                                # Set padding
                                app.setInPadding([0, 0])
                                # Set sticky
                                app.setSticky('nesw')
                                # End Buttons Panel
                                
                                # Add the list of out of season items if necessary
                                if len(out_of_season) != 0:
                                    # Set the stretch to both
                                    app.setStretch('both')
                                    # Start the out of season items frame
                                    app.startPanedFrame('Uploaded Out of Season Items')
                                    # Set the stretch
                                    # app.setStretch('row')
                                    # Add the label for the items
                                    app.addLabel('uoos', 'Out of Season Items:', 0, 0)
                                    # Add the list
                                    app.addListBox('uoosi', sorted(out_of_season), 1, 0)
                                    # Stop the out of season items frame
                                    app.stopPanedFrame()
                            # Stop the arrow Paned Frame
                            
                            # Reset the current row variable
                            current_row = 0
                            
                            # Start the Online Items Paned Frame
                            with app.panedFrame('Upload Online Item Boxes', width=app_w / 3):
                                
                                # Start the scroll pane for these items
                                with app.scrollPane('Upload Online Item Boxes Scroll', sticky='nesw'):
                                    
                                    # Reset the sticky
                                    app.setSticky('nesw')
                                    # Python used Iterate!
                                    for o in origins:
                                        # Set the stretch and sticky attributes
                                        # app.setStretch('row')
                                        # Add the online labels
                                        app.label('upload_online_label_' + o.lower().replace(' ', '_'),
                                                  'Uploaded ' + o.title() + ' Items:',
                                                  current_row, 0)
                                        # Set the stretch
                                        app.setStretch('both')
                                        # Create a temporary list to hold all uploaded items
                                        temp_online = []
                                        # Populate said list
                                        for o0 in origin_items_online[o]:
                                            temp_online.append(o0)
                                        for o0 in origin_items_offline[o]:
                                            temp_online.append(o0)
                                        # Add online items ListBox
                                        app.listbox('upload_online_items_' + o.lower().replace(' ', '_'),
                                                    sorted(temp_online),
                                                    current_row + 1, 0, drag=[begin_drag, end_drag])
                                        # Add a horizontal separator if it's not the last box
                                        if origins.index(o) != len(origins) - 1:
                                            app.addHorizontalSeparator(current_row + 2, 0, colour="red")
                                            # Increment the current row
                                            current_row += 3
                                    
                                    # - Begin formatting ListBoxes -#
                                    # Create variable to indicate alternating rows
                                    alternate = True
                                    # Python used Iterate!
                                    for o in origins:
                                        # Reset the alternating variable
                                        alternate = True
                                        # Python used Iterate!
                                        for i in range(0, len(
                                                app.getAllListItems(
                                                    'upload_offline_items_' + o.lower().replace(' ', '_')))):
                                            # If it's not the alternated row
                                            if alternate:
                                                # Do nothing
                                                pass
                                            # If it is
                                            else:
                                                # Reformat this row
                                                app.setListItemAtPosBg(
                                                    'upload_offline_items_' + o.lower().replace(' ', '_'), i,
                                                    '#00ffff')
                                                app.setListItemAtPosFg(
                                                    'upload_offline_items_' + o.lower().replace(' ', '_'), i,
                                                    '#000000')
                                            # Toogle the alternating variable
                                            alternate = not alternate
                                    
                                    # Reset alternating variable
                                    alternate = True
                                    # Python used Iterate!
                                    for o in origins:
                                        # Rest the alternating variable
                                        alternate = True
                                        # Python used Iterate!
                                        for i in range(0, len(
                                                app.getAllListItems(
                                                    'upload_online_items_' + o.lower().replace(' ', '_')))):
                                            # If it's not the alternated row
                                            if alternate:
                                                # Do nothing
                                                pass
                                            # If it is
                                            else:
                                                # Reformat this row
                                                app.setListItemAtPosBg(
                                                    'upload_online_items_' + o.lower().replace(' ', '_'), i,
                                                    '#00ffff')
                                                app.setListItemAtPosFg(
                                                    'upload_online_items_' + o.lower().replace(' ', '_'), i,
                                                    '#000000')
                                            # Toogle the alternating variable
                                            alternate = not alternate
                                    # - End formatting ListBoxes -#
                                # End Scroll Pane
                            # End Online Panel
                        # End Offline Panel
                    # End offline item management tab
                    
                    # endregion
                    
                    # region Stock Management tab
                    
                    # Start stock management tab
                    with app.tab('Stock Management'):
                        
                        #app.setSticky('NESW')
                        #app.setStretch('BOTH')
                        
                        # Start the Scroll Pane for the items
                        with app.scrollPane('Item Stock Management'):
                            
                            #app.setScrollPaneWidth('Item Stock Management', app_w)
                            
                            # Create the function for stock handling
                            def change_in_stock(button):
                                # Get the name of the entry to change
                                entry_name = 'stock_' + '_'.join(button.split('_')[1:])
                                # If its a minus button
                                if 'minus_' in button:
                                    # Decrement the value
                                    app.setEntry(entry_name, int(app.getEntry(entry_name)) - 1 if int(
                                        app.getEntry(entry_name)) >= -1 else int(
                                        app.getEntry(entry_name)))
                                # Otherwise
                                else:
                                    # Increment the value
                                    app.setEntry(entry_name, int(app.getEntry(entry_name)) + 1)
                                # Modify the value of the stock that's been changed
                                try:
                                    actual_stocks[' '.join(entry_name.split('_')[1:-1])][
                                        entry_name.replace('_', ' ').split(' ')[-1]] = app.getEntry(entry_name)
                                except:
                                    actual_stocks[' '.join(entry_name.split('_')[1:])] = app.getEntry(entry_name)
                            
                            # Get the stocks by name
                            items_stock_dict = SpS.get_item_names(get_stocks=True)
                            # Grab the actual item stocks from the new method
                            actual_stocks = SpS.get_item_stocks()
                            initial_stock_values = copy.deepcopy(actual_stocks)
                            
                            # For every uploaded item (since they're the only ones relevant)
                            for k in sorted(list(actual_stocks.keys())):
                                # Create the value for the total stock for this item
                                current_item_stock = -1
                                # Loop through the items list
                                for k2 in items_stock_dict:
                                    # And find the stock value for the current item
                                    try:
                                        if k.split(' - ')[1] in k2 or (' - ' not in k and k in k2):
                                            current_item_stock = items_stock_dict[k]
                                            break
                                    except:
                                        current_item_stock = -1
                                sil = (170-len(k)) / 2
                                empty_string = ' ' * int(sil)
                                # Create the toggle frame for this item
                                with app.toggleFrame(empty_string + k + ':' + empty_string, list(actual_stocks.keys()).index(k), width=app_w):
                                    
                                    try:
                                        current_row = 0
                                        for k2 in actual_stocks[k].keys():
                                            # Add the label for that item
                                            app.label(
                                                'stock_' + k.replace(' ', '_') + '_' + k2.replace(' ', '_'),
                                                k + ' ' + k2 + ':', current_row, 0)
                                            # Add the minus button
                                            app.addNamedButton('-', 'minus_' + k.replace(' ', '_') + '_' +
                                                               k2.replace(' ', '_'), change_in_stock, current_row, 1)
                                            # Add and set the stock entry
                                            app.entry('stock_' + k.replace(' ', '_') + '_' + k2.replace(' ', '_'),
                                                      pos=(current_row, 2), kind="numeric")
                                            try:
                                                app.setEntry(
                                                    'stock_' + k.replace(' ', '_') + '_' + k2.replace(' ', '_'),
                                                    int(actual_stocks[k][k2]))
                                            except:
                                                try:
                                                    app.setEntry(
                                                        'stock_' + k.replace(' ', '_') + '_' + k2.replace(' ', '_'),
                                                        int(actual_stocks[k]))
                                                except:
                                                    app.setEntry(
                                                        'stock_' + k.replace(' ', '_') + '_' + k2.replace(' ', '_'), -1)
                                            # Add the plus button
                                            app.addNamedButton('+', 'plus_' + k.replace(' ', '_') + '_' +
                                                               k2.replace(' ', '_'), change_in_stock, current_row, 3)
                                            current_row += 1
                                    except:
                                        try:
                                            # Add the label for that item
                                            app.label(
                                                'stock_' + k.replace(' ', '_'), k + ':', 0, 0)
                                            # Add the minus button
                                            app.addNamedButton('-', 'minus_' + k.replace(' ', '_'), change_in_stock, 0,
                                                               1)
                                            # Add and set the stock entry
                                            app.entry('stock_' + k.replace(' ', '_'), pos=(0, 2), kind="numeric")
                                            app.setEntry('stock_' + k.replace(' ', '_'), int(actual_stocks[k]))
                                            # Add the plus button
                                            app.addNamedButton('+', 'plus_' + k.replace(' ', '_'), change_in_stock, 0,
                                                               3)
                                        except:
                                            # Add the label for that item
                                            app.label('stock_' + k.replace(' ', '_'), k + ':', 0, 0)
                                            # Add the minus button
                                            app.addNamedButton('-', 'minus_' + k.replace(' ', '_'), change_in_stock, 0,
                                                               1)
                                            # Add and set the stock entry
                                            app.entry('stock_' + k.replace(' ', '_'), pos=(0, 2), kind="numeric")
                                            try:
                                                app.setEntry('stock_' + k.replace(' ', '_'), int(current_item_stock))
                                            except:
                                                app.setEntry('stock_' + k.replace(' ', '_'), -1)
                                            # Add the plus button
                                            app.addNamedButton('+', 'plus_' + k.replace(' ', '_'), change_in_stock, 0,
                                                               3)
                                # End current toggle pane
                        # End the scroll pane
                        # Start the frame for the apply button
                        with app.frame('Apply Stock', height=150):
                            app.setSticky('')
                            app.setInPadding(['30', '15'])
                            # Add the apply button
                            app.addNamedButton('Apply', 'apply_stock', stock_changes)
                            app.setSticky('nesw')
                        # End the frame
                    
                    # End stock management tab
                    
                    # endregion
                
                # End internal tab frame
            
            ## End Store Inventory Management Tab ##
            
            # endregion
            
            '''
            ----- Adding/Editing -----
            '''
            
            # region Adding/Editing
            
            ## Begin Item Creation Tab ##
            with app.tab('Create New/Edit Item'):
                
                # - Start the Item Select Pane -#
                with app.panedFrame('Item_Select'):
                    # Item Select Tree #
                    app.tree('item_edit_tree', tree_xml)
                    # Tree Properties #
                    app.setTreeColours('item_edit_tree', 'black', 'white', 'blue', 'yellow')
                    app.setTreeEditable('item_edit_tree', False)
                    # Add the tree-clicking functionality
                    app.setTreeDoubleClickFunction('item_edit_tree', edit_contents)
                    
                    def generate_sku():
                        from faker import Faker
                        fake = Faker()
                        app.setEntry('new_item_sku', str(fake.random_int(1000, 10000)))
                    
                    # Start the Item Information Entry #
                    with app.panedFrame('Item_Edit', vertical=True):
                        
                        app.setSticky('')
                        
                        # Start the Buttons Paned Frame #
                        with app.frame('Buttons'):
                            # Start a New Item #
                            app.button('Start New Item', start_new, 0, 0)
                            # Save the Current Item #
                            app.button('Save Changes', save_new, 0, 1)
                            # Save and upload the item#
                            # app.addButton('Save and Upload', save_new, 0, 2)
                        
                        # End Button Pane #
                        
                        app.setSticky('nesw')
                        with app.panedFrame('ItemEditPane'):
                            # Start the scroll pane for the edit items thing
                            with app.scrollPane('ItemEditScroll', sticky='nesw'):
                                # Name
                                app.label('new_item_name_label', "Item Name:", pos=(0, 0))
                                app.entry('new_item_name', pos=(0, 1))
                                # Price
                                app.label('new_item_price_label', 'Item Price:', pos=(0, 2))
                                app.entry('new_item_price', pos=(0, 3))
                                # SKU
                                app.button('Item SKU:', generate_sku, pos=(1, 0))
                                app.entry('new_item_sku', pos=(1, 1))
                                # Color SKUs
                                app.label('new_item_skus_label', 'Color SKUs:', pos=(1, 2))
                                app.addScrolledTextArea('new_item_skus', 1, 3)
                                # Origin
                                app.label('new_item_origin_label', 'Item Origin Store:', pos=(2, 0))
                                app.entry('new_item_origin', pos=(2, 1))
                                # Images
                                app.label('new_item_images_label', 'Item Images:', pos=(2, 2))
                                app.addFileEntry('new_item_images', 2, 3)
                                # Description
                                app.label('new_item_description_label', 'Item Description:', pos=(3, 0), colspan=2)
                                app.addScrolledTextArea('new_item_description', 3, 2, colspan=2)
                                # Details
                                app.label('new_item_details_label', 'Item Details:', pos=(4, 0), colspan=2)
                                app.addScrolledTextArea('new_item_details', 4, 2, colspan=2)
                                # Colors
                                app.label('new_item_colors_label_new', 'Item Colors:', pos=(5, 0), colspan=2)
                                app.addScrolledTextArea('new_item_colors_new', 5, 2, colspan=2)
                                # Sizes
                                app.label('new_item_sizes_label', 'Item Sizes:', pos=(6, 0), rowspan=2, colspan=2)
                                # Button to choose size type
                                app.addRadioButton('size_type', 'Basic', 6, 2)
                                app.addRadioButton('size_type', 'Advanced', 7, 2)
                                app.setRadioButtonChangeFunction('size_type', size_option)
                                
                                # Create a frame for Advanced sizes
                                with app.frame('Advanced Sizes', 6, 3, colspan=2, rowspan=2):
                                    app.addScrolledTextArea('advanced_item_size_one', 0, 0)
                                    app.addScrolledTextArea('advanced_item_size_two', 0, 1)
                                # Stop Advanced Size frame
                                
                                # And a frame for Basic sizes
                                with app.frame('Basic Sizes', 6, 3, colspan=2, rowspan=2):
                                    app.addScrolledTextArea('new_item_sizes')
                                # Stop Basic Size frame
                            # Stop the Scroll Pane
                    
                    # End Entry Pane #
                
                # End Tree Pane #
            
            ## End Item Creation Tab ##
            
            # endregion
        
        ## End Tabbed Frame ##
        # endregion

        # Check for the appropriate file again
        if date_str in glob.glob('*.json'):
            # Hide the startup sub-window
            app.hideSubWindow('start_wait_indicator')
        else:
            app.hideSubWindow('json_update_indicator')
        
        # Set what happend after the app closes
        app.setStopFunction(stop_application)
        
        # Start the app
        start_application(None)
        app.go()
        # loading_thread.join()
        # u_b.quit()


# Thread to get all product names once the application starts
class ItemNameThread(threading.Thread):
    
    # Runs the algorithm
    def run(self):
        global start_progress, all_items_uploaded, app, u, u_b
        # Start the process by getting the first url
        # u_b.get(u.urls[0])
        if u_b.current_url != interface.urls[0]:
            u_b.visit(interface.urls[0])
        # Make sure to be logged in as well, won't do any good if it's not
        # if not u.logged_in: #
        if not interface.logged_in:
            interface.login()
            # u.login()
        # Python used Rest!
        slp(3)
        # Save the current url
        cu = u_b.current_url
        # For every url
        for url in interface.urls:  # for url in u.urls:
            # Create a temporary array of items to use
            temp_items = []
            if u_b.current_url != url:
                # Go to the current url
                u_b.get(url)
                # Python used Rest!
                slp(3)
            # Grab the item names from this page
            # temp_items = u.get_item_names()
            temp_items = SpS.get_item_names()
            # Append each item found to the total item array
            for t in temp_items:
                if t not in all_items_uploaded:
                    all_items_uploaded.append(t)
            # start_progress += (100.0 / float(len(u.urls)))
            start_progress += (100.0 / float(len(interface.urls)))
            app.setStatusbar('Startup is {:.2f}'.format(start_progress) + '% Complete')
            print(str(start_progress) + '% Complete')
        # Return to the original url, just to be safe
        # u_b.get(cu)
        if usb.url != cu:
            usb.visit(cu)
        # all_items_uploaded = u.get_all_product_names()
        # app.hideSubWindow('Start Application')


# Thread to apply the updates needed
class ItemUpdatesThread(threading.Thread):
    
    # Thread running method
    def run(self):
        global app, items_to_be_updated, updates_needed, \
            upload_these, all_items_uploaded, u, jd, start_progress
        # Create a dict to the put the items that need updating in
        item_updates = {}
        # Loop through the list of items
        for i in items_to_be_updated:
            # And append that item to the dict
            try:
                item_updates.setdefault(i, updates_needed[i])
            except:
                pass
        # Comment to put break_point on
        break_point = None
        # Update the status bar as appropriate
        app.setStatusbar('Store Update in Progress...')
        print('Store Update in Progress...')
        # Then add items as necessary
        # u.addNewItemsGivenWithData(upload_these, jd)
        interface.add_new_items(upload_these, jd)
        for i in upload_these:
            all_items_uploaded.append(i)
        # And update the store appropriately
        interface.update_store(item_updates, jd)
        # Hide and unhide all appropriate items
        hide_unhide(None)
        # Update the status bar as appropriate
        app.setStatusbar('Store Update is complete')
        app.hideSubWindow('apply_wait_indicator')


# Thread to run stock updates without killing the app thread
class ItemStockUpdatesThread(threading.Thread):
    
    # Thread running method
    def run(self):
        # Grab the globals necessary
        global actual_stocks, initial_stock_values, app
        # Show the wait window
        # app.showSubWindow('apply_wait_indicator')
        # Change the sub-window's wait message
        app.setLabel('apply_loading_message', SyS.get_loading_message())
        # Create the dict to send with new information about the products
        updates_required = {}
        # Create a variable to potentially hold a list of items to convert to unlimited items
        make_limited = None
        # First, find out what needs to be updated in terms of stocks
        for k in actual_stocks:
            # If there's no size values for this item
            if type(actual_stocks) is not dict:
                # Then directly check if they're equal
                if actual_stocks[k] != initial_stock_values[k]:
                    updates_required[k] = actual_stocks[k]
            # If there are size values
            else:
                # Loop through each one
                for k2 in actual_stocks[k]:
                    # If any of them aren't equal
                    if actual_stocks[k][k2] != initial_stock_values[k][k2]:
                        # Mark it for updating
                        updates_required[k] = actual_stocks[k]
                        # If this item is becoming unlimited
                        if actual_stocks[k][k2] != -1 and initial_stock_values[k][k2] == -1:
                            # Create the actual list to send over if it's not already made
                            if make_limited is None:
                                make_limited = []
                            # Append this key to the list
                            make_limited.append(k)
        # Call the appropriate method from the interface
        interface.updateStock(updates_required, now_limited=make_limited)
        # Hide the app wait window
        # app.hideSubWindow('apply_wait_indicator')

def main():
    # Check the overall program for updates
    # check_for_updates()
    
    # Import the classes to do some cleanup
    import datetime, glob
    
    # Get the current date
    current = datetime.datetime.now()
    # And save each field
    day = current.strftime('%d')
    month = current.strftime('%m')
    year = current.strftime('%y')
    # Find all of the logs for this month
    this_months_logs = glob.glob(month + '_*_' + year + '*.log')
    # Create the string for the last month
    lm = str(int(month) - 1)
    if int(lm) < 10:
        lm = '0' + lm
    if int(lm) == 0:
        lm = '12'
    # Create the string for the current month
    cm = str(int(month))
    if int(cm) < 10:
        cm = '0' + cm
    # Get the last month's logs
    last_months_logs = glob.glob(lm + '_*_' + year + '*.log')
    # If there are remaining logs from last month
    if len(last_months_logs) > 1:
        # Add all except one to this months (for legacy checking)
        for i in range(len(last_months_logs) - 1):
            this_months_logs.append(last_months_logs[i])
    # Find all of the jsons for this month
    this_months_jsons = glob.glob('items' + cm + '*' + year + '.json')
    # And the remaining jsons from last month
    last_months_jsons = glob.glob(
        'items' + lm + '*' + year + '*.log')
    # If there are remaining jsons from last month
    if len(last_months_jsons) > 1:
        # Add all except one to this months (for legacy checking)
        for i in range(len(last_months_jsons) - 1):
            this_months_jsons.append(last_months_jsons[i])
    # If there are sufficient logs and jsons to warrant deleting
    if len(this_months_jsons) > 7 and int(day) > 27:
        # For all except the latest log
        for i in range(len(this_months_logs) - 1):
            # Delete the log
            os.remove(this_months_logs[i])
        # For all except the latest json
        for i in range(len(this_months_jsons) - 1):
            # Delete the json
            os.remove(this_months_jsons[i])
        # If this goes through, save the current work directory
        current_dir = os.getcwd()
        # Navigate to the logs for the scrapers
        os.chdir('C://Users//Shipping//Documents//LiClipse Workspace//ScrapyDerp//LSL_Scrapers//scrapers//scrapers')
        # Find the scraper logs
        scraper_logs = glob.glob(month + '*.log')
        # Loop through all but one for this month
        for i in range(len(scraper_logs) - 1):
            os.remove(scraper_logs[i])
        # Then move back to the original directory
        os.chdir(current_dir)
    # Create the start thread
    # start_thread = threading.Thread(target=start_window())
    # start_thread.start()
    # Start the GUI
    start_window()
    
# Lets this program run by itself
if __name__ == '__main__':
    main()