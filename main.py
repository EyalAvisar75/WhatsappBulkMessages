from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

messages_to_contacts = []

def create_browser():
    return webdriver.Chrome('C:\Program Files (x86)\webdrivers\chromedriver.exe')

def enter_whatsapp(browser):
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')
    sleep(2)

def enter_QRCode():
    input('scan whatsapp QR code on the login screen'
          ' and press enter to continue')


def send_message(browser, message, mail_counter, recipient_counter):
    is_contact = get_contact(browser, mail_counter, recipient_counter)
    if not is_contact:
        return
    fill_message(browser, message)
    press_send(browser)


def press_send(browser):
    send_button = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/'
                                                'div[3]/button/span')
    send_button.click()


def fill_message(browser, message):
    message_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/'
                                                'div[2]/div/div[2]')
    sleep(3)
    message_box.send_keys(message)


def get_contact(browser, mail_counter, recipient_counter):
    recipient = messages_to_contacts[mail_counter][1][recipient_counter]
    selector = 'span[title="' + recipient + '"]'
    try:
        contact_title = browser.find_element_by_css_selector(selector)
    except NoSuchElementException:
        print(f"{recipient} not found")
        return False

    sleep(2)
    contact_title.click()
    sleep(2)
    return True



def search_contact_and_send_message(browser):
    search_xpath = '/html/body/div[1]/div/div/div[3]' \
                   '/div/div[1]/div/label/div/div[2]'
    search_box = WebDriverWait(browser, 500).until(
    EC.presence_of_element_located((By.XPATH, search_xpath)))
    sleep(3)

    mail_counter = 0
    for message_to_contacts in messages_to_contacts:
        recipient_counter = 0
        for contact in messages_to_contacts[mail_counter][1]:
            search_box.send_keys(contact)
            sleep(2)
            send_message(browser, message_to_contacts[mail_counter], mail_counter, recipient_counter)
            sleep(2)
            search_box.clear()
            sleep(2)
            recipient_counter += 1
        mail_counter += 1


def write_message_to_contact():
    while True:
        message = input("Please enter a message: ")
        messages_to_contacts.append((message, []))
        index = len(messages_to_contacts) - 1
        while True:
            if message == '':
                messages_to_contacts.pop()
                break
            print("Press enter if you are "
                  "done with contacts")
            contact = input("Whom to send the message: ")
            if len(contact) == 0:
                break
            messages_to_contacts[index][1].append(contact)
        if len(messages_to_contacts) > 0:
            if len(messages_to_contacts[-1][1]) == 0:
                messages_to_contacts.pop()
        stop = input("Enter y for more messages ")
        if len(stop) > 0:
            if stop[0].lower() != 'y':
                break
        else: break


def run_whatsapp_bulk_messaging():
    browser = create_browser()
    enter_whatsapp(browser)
    enter_QRCode()
    while True:
        write_message_to_contact()
        search_contact_and_send_message(browser)


run_whatsapp_bulk_messaging()