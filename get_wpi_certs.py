# This file is used to obtain the CA certificates for connecting to WPI's wireless network.
# These certificates can be obtained manually from https://wpi-wireless-setup.wpi.edu/enroll/start.
# It requires valid WPI user credentials.
#
# Jeff Martin - jamartin@wpi.edu
# April 12, 2018

import mechanize

# URLS to WPI specific Pages
WPI_ACCEPTABLE_USE_POLICY = "https://www.wpi.edu/about/policies/acceptable-use"
WPI_NETWORK_SETUP = "https://wpi-wireless-setup.wpi.edu/enroll/start"
# Names of the forms used on WPI's web pages.
# Discovered through trial and error with Mechanize.
FORM_KEYWORD_1 = "message"
FORM_KEYWORD_2 = "acceptableUsePolicy"
CONTROL_KEYWORD_1 = "acceptAup"
FORM_KEYWORD_3 = "credential"
CONTROL_KEYWORD_2 = "username"
CONTROL_KEYWORD_3 = "password"
FORM_KEYWORD_4 = "message"
REDIRECT_LINK_1 = "authorize2"
REDIRECT_LINK_2 = "proceed to the download page."
PUBLIC_CERT_LINK = "PEM"
PRIVATE_CERT_LINK = "Step 2: Install Your CertificateClick to Install Your Certificate"


def get_wpi_certs(username, password, accepted, public_cert_file, private_cert_file, status):
    log_status(status, "Retrieving Your WPI Wireless Certificates:")
    if not accepted:
        print "Your must accept WPI's acceptable use policy in order to continue."
        return False
    log_status(status, "\tInitializing Browser Instance...")
    browser = initialize_browser_instance()
    log_status(status, "\tNavigating to Network Setup Web Page...")
    navigate_to_wpi_network_setup_homepage(browser, WPI_NETWORK_SETUP)
    log_status(status, "\tBeginning Network Setup...")
    begin_network_setup(browser, FORM_KEYWORD_1)
    log_status(status, "\tAccepting Use Policy...")
    accept_use_policy(browser, FORM_KEYWORD_2, CONTROL_KEYWORD_1)
    log_status(status, "\tAuthenticating with User Credentials...")
    authenticated = authenticate(browser, FORM_KEYWORD_3, FORM_KEYWORD_4,
                                 CONTROL_KEYWORD_2, CONTROL_KEYWORD_3, username, password)
    if not authenticated:
        log_status(status, "\tFailed to authenticate with WPI network setup platform.\n\t Be sure the credentials you "
                           "entered are correct.")
        return False
    log_status(status, "\tContinuing to Download Page...")
    continue_to_certificate_page(browser, FORM_KEYWORD_4, REDIRECT_LINK_1, REDIRECT_LINK_2)
    log_status(status, "\tDownloading Certificates...")
    download_certificates(browser, PUBLIC_CERT_LINK, PRIVATE_CERT_LINK, public_cert_file, private_cert_file)
    log_status(status, "\tSuccess!")
    return True


def log_status(status, message):
    if status:
        print "[STATUS] " + message


def initialize_browser_instance():
    browser = mechanize.Browser()
    mechanize.CookieJar.clear(browser.cookiejar)
    return browser


def navigate_to_wpi_network_setup_homepage(browser, homepage_url):
    browser.open(homepage_url)


def begin_network_setup(browser, form):
    browser.select_form(name=form)
    browser.click()
    browser.submit()


def accept_use_policy(browser, form, control):
    browser.select_form(name=form)
    browser.find_control(control).items[0].selected = True
    browser.click()
    browser.submit()


def authenticate(browser, form1, form2, control1, control2, username, password):
    browser.select_form(name=form1)
    browser.find_control(control1).value = username
    browser.find_control(control2).value = password
    browser.click()
    browser.submit()
    try:
        browser.select_form(name=form2)
        return True
    except mechanize.FormNotFoundError:
        return False


def continue_to_certificate_page(browser, form, redirect_link1_name, redirect_link2_name):
    browser.select_form(name=form)
    browser.click()
    browser.submit()
    redirect_link = browser.find_link(text=redirect_link1_name)
    browser.follow_link(redirect_link)
    redirect_link = browser.find_link(text=redirect_link2_name)
    browser.follow_link(redirect_link)


def download_certificates(browser, public_cert_link_name, private_cert_link_name, public_cert_file, private_cert_file):
    # Download the certificates by following links
    pub_cert_link = browser.find_link(text=public_cert_link_name)
    prv_cert_link = browser.find_link(text=private_cert_link_name)
    browser.retrieve(pub_cert_link.absolute_url, public_cert_file)
    browser.retrieve(prv_cert_link.absolute_url, private_cert_file)
