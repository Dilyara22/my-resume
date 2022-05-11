
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest 
from time import sleep
# from get_excel_data import login_form_parameters
from get_db_data import login_form_parameters
import logging 

############# TEST FUNCTIONS #######################

logging.basicConfig(filename='C:\AUTOMATION\PROJECT\logs\info.log',
                    encoding='utf-8',
                    level=logging.INFO,
                    force=True,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def launch_swaglabs():
    logging.info('Launching the swaglabs page')
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.saucedemo.com/')    

# login_form_parameters = [
#     ('locked_out_user','secret_sauce', 'Sorry, this user has been locked out'),
#     ('test','test', 'Username and password do not match any user in this service')
#     ] 

@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)
def test_login_invalid_credentials(username, password, checkpoint):
    launch_swaglabs()
    if username != None: driver.find_element(By.ID,'user-name').send_keys(username)
    if password != None: driver.find_element(By.NAME,'password').send_keys(password)
    driver.find_element(By.CLASS_NAME,'submit-button').click()
    # sleep(5)
    capture_evidence()
    assert checkpoint.lower() in driver.page_source.lower()
    driver.quit()


def valid_login_swaglabs():
    global driver
    driver.find_element(By.ID,'user-name').send_keys('standard_user')
    driver.find_element(By.NAME,'password').send_keys('secret_sauce')
    driver.find_element(By.CLASS_NAME,'submit-button').click()

def capture_evidence():
    image_name=fr"C:\AUTOMATION\PROJECT\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

# ################ TEST CASES WITH SETUP AND TEARDOWN #######################
    
#the following code runs before each test
@pytest.fixture()
def setup(request):
    launch_swaglabs()
    valid_login_swaglabs()

    #the following code runs after each test
    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)


def test_login_valid_credentials(setup): 
    assert 'products' in driver.page_source.lower()
   

def test_view_product_details(setup):
    product_names=driver.find_elements(By.CLASS_NAME,'inventory_item_name')
    product_names[0].click()
    assert 'back-to-products' in driver.page_source.lower()

def test_add_item_to_cart(setup):
    product_names=driver.find_elements(By.CLASS_NAME,'inventory_item_name')
    product_names[0].click()
    driver.find_element(By.ID,'add-to-cart-sauce-labs-backpack').click()
    assert 'remove' in driver.page_source.lower()

def test_open_cart(setup):
    logging.info('Opening shopping cart')
    product_names=driver.find_elements(By.CLASS_NAME,'inventory_item_name')
    product_names[0].click()
    driver.find_element(By.ID,'add-to-cart-sauce-labs-backpack').click()
    driver.find_element(By.ID,'shopping_cart_container').click()
    assert 'your cart' in driver.page_source.lower() 
