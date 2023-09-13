from multiprocessing.spawn import _main
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Initialise Chrome Driver
def setup_driver():
    # Using Chrome to access web
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    # driver.maximize_window()
    driver.delete_all_cookies()
    return driver

# Get user details for sign in to STV website, and the time of desired booking
def get_user_details():
    print("Enter University of Bath email: ")
    user_email = input()
    print("Enter STV booking website pin: ")
    user_pin = input()

    while(not is_valid(user_email, user_pin)):
        print("Login Failed")
        print("Enter University of Bath email: ")
        user_email = input()
        print("Enter STV booking website pin: ")
        user_pin = input()

    print("Details Valid.")
    return user_email, user_pin


def get_date_and_time():
    # date = "10/10/2022"
    # time = "11:00:00"
    print("Enter date and time of the booking you would like:")
    print("(Football is currently the only option. More will be added later).")

    # TODO Type checks

    print("Day: ")
    day = input()
    print("Month: ")
    month = input()
    print("Year: ")
    year = input()
    print("Hour: ")
    hour = input()
    return day, month, year, hour


def is_valid(user_email, user_pin):
    driver.get('https://bookings.teambath.com/Connect/MRMLogin.aspx');

    username_box = driver.find_element(By.ID, 'ctl00_MainContent_InputLogin')
    password_box = driver.find_element(By.ID, 'ctl00_MainContent_InputPassword')
    login_box = driver.find_element(By.ID, 'ctl00_MainContent_btnLogin')

    username_box.send_keys(user_email)
    password_box.send_keys(user_pin)
    login_box.click()
    time.sleep(1)
    if(driver.current_url == 'https://bookings.teambath.com/Connect/MRMLogin.aspx'):
        return False  # login details are incorrect
    return True


def start(user_email, user_pin, day, month, year, hour, sport = "Football"):
    driver.get('https://bookings.teambath.com/Connect/MRMLogin.aspx');

    username_box = driver.find_element(By.ID, 'ctl00_MainContent_InputLogin')
    password_box = driver.find_element(By.ID, 'ctl00_MainContent_InputPassword')
    login_box = driver.find_element(By.ID, 'ctl00_MainContent_btnLogin')

    username_box.send_keys(user_email)
    password_box.send_keys(user_pin)
    login_box.click()
    time.sleep(1)

    make_booking_box = driver.find_element(By.ID, 'ctl00_ctl11_Li1')
    make_booking_box.click()
    
    if sport == "Football":
        book_football(day, month, year, hour)
    elif sport == "Badminton":
        book_badminton(day, month, year, hour)


def book_football(day, month, year, hour):
    football_css = "input[value*='Football']"
    football_box = driver.find_element(By.CSS_SELECTOR, football_css)
    football_box.click()

    pitch_options_css = "input[value*='Students Football']"

    # Tries to find a booking for 3 mins.
    t_end = time.time() + 180
    while time.time() < t_end:
    # for some reason i get a stale element reference when i loop through the different football pitch
    # elements. So instead i redefine them every iteration in the for loop.
        for i in range(4):
            football_pitches = driver.find_elements(By.CSS_SELECTOR, pitch_options_css)
            football_pitches[i].click()
            if(is_football_booking_found(day, month, year, hour)):
                print("Successfully booked.")
                break
            else:
                driver.back()
                # driver.execute_script("window.history.go(-1)")

    print("No Booking available")

def is_football_booking_found(day, month, year, hour):
    try:
        fullID = "input[data-qa-id*='Date=" + str(day) + "/" + str(month) + "/" + str(year) + " " + str(hour) + ":00:00 Availability= Available']"
        bookingIDbox = driver.find_element(By.CSS_SELECTOR, fullID)
        bookingIDbox.click()
        time.sleep(1)

        timeID = "input[value*='" + str(hour) + ":00']"
        timeID_box = driver.find_element(By.CSS_SELECTOR, timeID)
        timeID_box.click()
        time.sleep(1)

        bookID = "input[value*='Book']"
        book_box = driver.find_element(By.CSS_SELECTOR, bookID)
        book_box.click()
        return True
    except:
        return False

# TODO FInish this later
def book_badminton(day, month, year, hour):
    sportcss = "input[value*='Badminton']"
    sport_box = driver.find_element(By.CSS_SELECTOR, sportcss)
    sport_box.click()

    student_box = driver.find_element(By.ID, "ctl00_MainContent_activitiesGrid_ctrl2_lnkListCommand")
    student_box.click()


    time.sleep(4)

    bookingID = "button-ActivityID=BADMINFCFREESTU Date=" + str(day) + "/" + str(month) + "/" + str(year) + " " + str(hour) + ":00:00 Availability= Available"
    fullID = "input[data-qa-id='" + bookingID + "']"
    print(fullID)
    bookingIDbox = driver.find_element(By.CSS_SELECTOR, fullID)
    bookingIDbox.click()


def main():
    global driver 
    driver = setup_driver()
    # user_email, user_pin = get_user_details()
    # day, month, year, hour = get_date_and_time()
    # start(user_email, user_pin, day, month, year, hour)


    # Quick start. Email Address and Pin ommited.
    start("USERNAME@bath.ac.uk", "USER_PIN", "30","10","2022","15")


if __name__ == "__main__":
    main()