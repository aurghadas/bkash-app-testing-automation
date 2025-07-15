import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.connectiontype import ConnectionType



def type_and_enter(driver, text, delay=1):
    # Find the textbox and send the desired text that we want to type
    driver.find_element(
        AppiumBy.CLASS_NAME,
        "android.widget.EditText"
    ).send_keys(text)
    time.sleep(delay)

    # Press the enter key
    driver.press_keycode(AndroidKey.ENTER)
    time.sleep(delay)


def swipe(driver, start_x, start_y, end_x, end_y, duration=0):
    # Swipe from the start point to the end point
    driver.swipe(start_x, start_y, end_x, end_y, duration)


def search_and_click(driver, search_text, delay=1):
    # Find the element that contains the search text and click on it
    selector = f'new UiSelector().descriptionContains("{search_text}")'
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
    time.sleep(delay)

def is_network_connected(driver):
    return driver.network_connection != ConnectionType.NO_CONNECTION

def network_status(driver):
    # Quick network‐up check
    if not is_network_connected(driver):
        print("No network — retrying in 3s")
        time.sleep(3)
        if not is_network_connected(driver):
            raise RuntimeError("Network unavailable, aborting login")


# Added explicit delay newly, need to be updated on app_test2 and app_test1
def login(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at login start"
        print("[✔] Network is connected")

        # wait until the merchant-login screen node appears in the UI
        try:
            wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("বিকাশ মার্চেন্ট লগইন")'
            )))
            merchant_login = True
        except TimeoutException:
            merchant_login = False

        if merchant_login:
            # Assert merchant login screen is visible
            assert driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("বিকাশ মার্চেন্ট লগইন")'
            ), "Merchant login screen should be visible"
            print("[✔] Merchant login screen is visible")

            # PIN flow
            for digit in ("1", "3", "1", "3", "1"):
                # Assert each PIN digit button exists before clicking
                pin_selector = f'new UiSelector().descriptionContains("{digit}")'
                assert driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    pin_selector
                ), f'PIN digit "{digit}" button not found'
                print(f"[✔] PIN digit '{digit}' button found")
                search_and_click(driver, digit, delay=0.5)

            # Assert "নিশ্চিত করুন" button exists before clicking
            confirm_selector = 'new UiSelector().descriptionContains("নিশ্চিত করুন")'
            assert driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                confirm_selector
            ), '"Confirm it" button not found'
            print("[✔] 'Confirm it' button found")

            # click "নিশ্চিত করুন" button
            search_and_click(driver, "নিশ্চিত করুন")
            print("[✔] PIN entry completed and confirmed")

            print("\n---------- LOGIN COMPLETED SUCCESSFULLY ----------\n")
            return

        # otherwise wait for the "লগইন" button to be present & clickable
        try:
            login_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("লগইন")'
            )))
            # Assert login button is displayed
            assert login_btn.is_displayed(), '"লগইন" button is not displayed'
            print("[✔] 'লগইন' button is displayed and clickable")
            login_btn.click()
        except TimeoutException:
            print("[✖] Login button never appeared")
            return

        # Enter phone number
        # Assert phone input field is ready
        try:
            phone_field = driver.find_element(
                AppiumBy.CLASS_NAME, "android.widget.EditText"
            )
            assert phone_field.is_displayed(), "Phone input field is not visible"
            print("[✔] Phone input field is visible")
            type_and_enter(driver, "01854580120")
            print("[✔] Phone number entered successfully")
        except Exception as e:
            print(f"[✖] Error while entering phone number: {e}")


        # wait & click “পরবর্তী ধাপে যান”
        try:
            next_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("পরবর্তী ধাপে যান")'
            )))
            # Assert “পরবর্তী ধাপে যান” button is present
            assert next_btn.is_displayed(), '"পরবর্তী ধাপে যান" button not found'
            print("[✔] 'পরবর্তী ধাপে যান' button is visible")
            next_btn.click()
        except TimeoutException:
            print("[✖] 'পরবর্তী ধাপে যান' button never appeared")

        # wait & click Allow
        try:
            allow_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Allow").className("android.widget.Button").clickable(true)'
            )))
            # Assert Allow button is visible
            assert allow_btn.is_displayed(), '"Allow" button is not visible'
            print("[✔] 'Allow' button is visible and clickable")
            allow_btn.click()
        except TimeoutException:
            print("[✖] 'Allow' button never appeared")

        # final “পরবর্তী ধাপে যান”
        try:
            final_next_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("পরবর্তী ধাপে যান")'
            )))
            # Assert final “পরবর্তী ধাপে যান” button is present
            assert final_next_btn.is_displayed(), 'Final "পরবর্তী ধাপে যান" button not found'
            print("[✔] Final 'পরবর্তী ধাপে যান' button is visible")
            final_next_btn.click()
        except TimeoutException:
            print("[✖] Final 'পরবর্তী ধাপে যান' button never appeared")

        # post-login PIN flow
        try:
            wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("বিকাশ মার্চেন্ট লগইন")'
            )))
            # Assert post-login merchant screen appearance
            assert driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("বিকাশ মার্চেন্ট লগইন")'
            ), "Post-login merchant screen is missing"
            print("[✔] Post-login merchant screen is visible")

            for digit in ("1", "3", "1", "3", "1"):
                # Assert each PIN digit button exists using descriptionContains
                pin_selector = f'new UiSelector().descriptionContains("{digit}")'
                assert driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    pin_selector
                ), f'PIN digit "{digit}" button not found'
                print(f"[✔] PIN digit '{digit}' button found")
                search_and_click(driver, digit, delay=0.5)

            # Assert "নিশ্চিত করুন" button exists before clicking
            confirm_selector = 'new UiSelector().descriptionContains("নিশ্চিত করুন")'
            assert driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                confirm_selector
            ), '"Confirm it" button not found'
            print("[✔] 'Confirm it' button found")

            # Click "নিশ্চিত করুন" button
            search_and_click(driver, "নিশ্চিত করুন")
            print("[✔] Post-login PIN entry completed and confirmed")

            print("\n---------- LOGIN COMPLETED SUCCESSFULLY ----------\n")
        except TimeoutException:
            print("[✖] Post-login merchant screen didn't appear")
    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during login: {e}")
    else:
        print("\n---------- LOGIN COMPLETED SUCCESSFULLY ----------\n")


def check_balance(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at check_balance start"
        print("[✔] Network is connected")

        # Find the "ব্যালেন্স দেখুন" button
        balance_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ব্যালেন্স দেখুন")'
        )

        # Wait for and tap the button if it appears
        try:
            balance_element = wait.until(EC.element_to_be_clickable(balance_locator))
            
            # Assert "ব্যালেন্স দেখুন" button is visible and clickable
            assert balance_element.is_displayed(), '"Show Balance" button is not visible'
            print("[✔] 'Show Balance' button is visible and clickable")
            balance_element.click()
            print("[✔] 'Show Balance' button clicked")
        except TimeoutException:
            print("[✖] Balance button not found")
            return

        # Wait for the balance to present and disappear
        time.sleep(8)
        print("[✔] Waited for balance display to complete")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during check_balance: {e}")
    else:
        print("\n---------- CHECK BALANCE COMPLETED SUCCESSFULLY----------\n")



# Added explicit delay newly, need to be updated on app_test2 and app_test1
def check_inbox(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at check_inbox start"
        print("[✔] Network is connected")

        # Wait for the header to be present, then grab it
        try:
            header_locator = (AppiumBy.ACCESSIBILITY_ID, "Shop Local 96")
            header = wait.until(EC.presence_of_element_located(header_locator))
            
            # Assert header is present
            assert header.is_displayed(), '"Shop Local 96" header not found'
            print("[✔] 'Shop Local 96' header is visible")
        except TimeoutException:
            print("[✖] 'Shop Local 96' header not found within timeout")
            return

        # Find & wait for the inbox icon within the header to be clickable, then tap it
        try:
            icon_locator = (AppiumBy.CLASS_NAME, "android.widget.ImageView")
            inbox_icon = header.find_element(*icon_locator)
            
            # Assert inbox icon is present
            assert inbox_icon.is_displayed(), "Inbox icon not found in header"
            print("[✔] Inbox icon found in header")

            wait.until(EC.element_to_be_clickable(icon_locator))
            
            # Assert inbox icon is clickable
            assert inbox_icon.is_enabled(), "Inbox icon is not clickable"
            print("[✔] Inbox icon is clickable")
            inbox_icon.click()
            print("[✔] Inbox icon clicked")
        except TimeoutException:
            print("[✖] Inbox icon not found or not clickable")
            return

        # Perform the swipe to open the notice section
        before_swipe = driver.page_source
        swipe(driver, 700, 500, 100, 500)
        time.sleep(2)
        after_swipe = driver.page_source
        assert before_swipe != after_swipe, "Swipe did not open notice section"
        print("[✔] Performed swipe to open notice section")

        # Return to home
        driver.press_keycode(AndroidKey.BACK)
        print("[✔] Returned to home screen using BACK key")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during check_inbox: {e}")
    else:
        print("\n---------- CHECK INBOX COMPLETED SUCCESSFULLY----------\n")


# This method has not been checked yet 
def login_error_check(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Create a short explicit wait for error popup check
        short_wait = WebDriverWait(driver, 2)  # Only wait max 3 seconds

        # Wait and check if the specific texts are visible
        login_again_locator = (
            AppiumBy.ACCESSIBILITY_ID,
            "অনুগ্রহ করে আপনার নেটওয়ার্ক চেক করুন"
        )
        login_again1_locator = (
            AppiumBy.ACCESSIBILITY_ID,
            "অনুগ্রহ করে আবার লগইন করুন"
        )

        # Try waiting for either of these elements (whichever appears first)
        found_login_again = False
        try:
            short_wait.until(EC.presence_of_element_located(login_again_locator))
            found_login_again = True
        except TimeoutException:
            try:
                short_wait.until(EC.presence_of_element_located(login_again1_locator))
                found_login_again = True
            except TimeoutException:
                found_login_again = False

        # If found, click the cross button and call login
        if found_login_again:
            cross_button_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.Button")'
            )
            short_wait.until(EC.element_to_be_clickable(cross_button_locator)).click()
        else:
            pass

    except Exception as e:
        print(f"[login_error_check] Exception occurred: {e}")
        # Optional: re-raise or handle silently
        pass



# Added explicit delay newly, need to be updated on app_test2 and app_test1
def check_transactions(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at check_transactions start"
        print("[✔] Network is connected")

        # Wait for and click the "লেনদেনসমূহ" button
        try:
            transaction_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("লেনদেনসমূহ")'
            )))
            assert transaction_button.is_displayed(), '"Transactions" button is not visible'
            print("[✔] 'Transactions' button is visible and clickable")
            transaction_button.click()
            print("[✔] 'Transactions' button clicked")
        except TimeoutException:
            print("[✖] 'Transactions' button was not found within the timeout")

        # Wait for and click the "ফি" button
        try:
            fee_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("ফি")'
            )))
            assert fee_button.is_displayed(), '"Fee" button is not visible'
            print("[✔] 'Fee' button is visible and clickable")
            fee_button.click()
            print("[✔] 'Fee' button clicked")
        except TimeoutException:
            print("[✖] 'Fee' button was not found within the timeout")

        # Scroll down and up
        before_source = driver.page_source
        swipe(driver, 100, 900, 100, 10)
        swipe(driver, 100, 600, 100, 1300)
        after_source = driver.page_source
        assert before_source != after_source, "Scroll down did not change the page source"
        print("[✔] Performed scroll down and up")

        # Wait for and click the "-আউট" button
        try:
            out_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("আউট")'
            )))
            assert out_button.is_displayed(), '"Cash-out" button is not visible'
            print("[✔] 'Cash-out' button is visible and clickable")
            out_button.click()
            print("[✔] 'Cash-out' button clicked")
        except TimeoutException:
            print("[✖] 'Cash-out' button was not found within the timeout")

        # Scroll down and up again
        before_source = driver.page_source
        swipe(driver, 100, 900, 100, 10)
        swipe(driver, 100, 600, 100, 1300)
        after_source = driver.page_source
        assert before_source != after_source, "Scroll down did not change the page source"
        print("[✔] Performed second scroll up and down")

        # Wait for and click the "+ ইন" button
        try:
            in_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("+ ইন")'
            )))
            assert in_button.is_displayed(), '"Cash-in" button is not visible'
            print("[✔] 'Cash-in' button is visible and clickable")
            in_button.click()
            print("[✔] 'Cash-in' button clicked")
        except TimeoutException:
            print("[✖] 'Cash-in' button was not found within the timeout")

        # Scroll down and up once more
        before_source = driver.page_source
        swipe(driver, 100, 900, 100, 10)
        swipe(driver, 100, 600, 100, 1300)
        after_source = driver.page_source
        assert before_source != after_source, "Scroll down did not change the page source"
        print("[✔] Performed third scroll up and down")

        # Swipe left to transaction synopsis
        before_source = driver.page_source
        swipe(driver, 700, 500, 100, 500)
        after_source = driver.page_source
        assert before_source != after_source, "Swipe left did not change the page source"
        print("[✔] Performed swipe left to transaction synopsis")

        # Wait for and click the "মাসিক সার-সংক্ষেপ" button
        try:
            monthly_summary_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("মাসিক সার-সংক্ষেপ")'
            )))
            assert monthly_summary_button.is_displayed(), '"Monthly Synopsis" button is not visible'
            print("[✔] 'Monthly Synopsis' button is visible and clickable")
            monthly_summary_button.click()
            print("[✔] 'Monthly Synopsis' button clicked")
        except TimeoutException:
            print("[✖] 'Monthly Synopsis' button was not found within the timeout")

        # Wait for and click the "Jun 25" button
        try:
            jun25_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("Jun 25")'
            )))
            assert jun25_button.is_displayed(), '"Jun 25" button is not visible'
            print("[✔] 'Jun 25' button is visible and clickable")
            jun25_button.click()
            print("[✔] 'Jun 25' button clicked")
        except TimeoutException:
            print("[✖] 'Jun 25' button was not found within the timeout")

        # Wait for and click the "দৈনিক সার-সংক্ষেপ" button
        try:
            daily_summary_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("দৈনিক সার-সংক্ষেপ")'
            )))
            assert daily_summary_button.is_displayed(), '"Daily synopsis" button is not visible'
            print("[✔] 'Daily synopsis' button is visible and clickable")
            daily_summary_button.click()
            print("[✔] 'Daily synopsis' button clicked")
        except TimeoutException:
            print("[✖] 'Daily synopsis' button was not found within the timeout")

        # Wait for and click the "13" button
        try:
            five_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("13")'
            )))
            assert five_button.is_displayed(), '"13" button is not visible'
            print("[✔] '13' button is visible and clickable")
            five_button.click()
            print("[✔] '13' button clicked")
        except TimeoutException:
            print("[✖] '13' button was not found within the timeout")


        # Wait for and click the "হোম" button
        try:
            home_button = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("হোম")'
            )))
            assert home_button.is_displayed(), '"Home" button is not visible'
            print("[✔] 'Home' button is visible and clickable")
            home_button.click()
            print("[✔] 'Home' button clicked")
        except TimeoutException:
            print("[✖] 'Home' button was not found within the timeout")      
    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error: {e}")
    else:
        print("\n---------- CHECK TRANSACTIONS COMPLETED SUCCESSFULLY ----------\n")
    



# Added explicit delay newly, need to be updated on app_test2 and app_test1
def namaz_roja_details(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at namaz_roja_details start"
        print("[✔] Network is connected")

        # Wait for the header to be present before swipping
        try:
            header_locator = (AppiumBy.ACCESSIBILITY_ID, "Shop Local 96")
            header = wait.until(EC.presence_of_element_located(header_locator))
            
            # Assert header is present
            assert header.is_displayed(), '"Shop Local 96" header not found'
            print("[✔] 'Shop Local 96' header is visible")
        except TimeoutException:
            print("[✖] 'Shop Local 96' header not found within timeout")
            return

        # Scroll down into view
        swipe(driver, 100, 900, 100, 10)
        print("[✔] Performed initial swipe to bring 'Details' into view")

        # Wait for and click the “বিস্তারিত” button if it appears
        detail_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("বিস্তারিত")'
        )
        try:
            detail_button = wait.until(EC.element_to_be_clickable(detail_locator))
            
            # Assert “বিস্তারিত” button is visible and clickable
            assert detail_button.is_displayed(), '"Details" button is not visible'
            print("[✔] 'Details' button is visible and clickable")
            detail_button.click()
            print("[✔] 'Details' button clicked")
        except TimeoutException:
            print("[✖] 'Details' button was not found within the timeout")
            return

        # Scroll twice on the details page
        swipe(driver, 100, 900, 100, 10)
        print("[✔] Performed first swipe on details page")
        swipe(driver, 100, 900, 100, 10)
        print("[✔] Performed second swipe on details page")

        # Press back to return home
        driver.press_keycode(AndroidKey.BACK)
        print("[✔] BACK key pressed to return home")

        # Wait until the home header is present again
        home_header = (
            AppiumBy.ACCESSIBILITY_ID,
            "Shop Local 96"
        )
        try:
            home_element = wait.until(EC.presence_of_element_located(home_header))
            
            # Assert home header is visible
            assert home_element.is_displayed(), "'Shop Local 96' home header not visible after returning"
            print("[✔] Home header 'Shop Local 96' is visible again")

            print("\n----------CHECK NAMAZ ROJA DETAILS COMPLETED SUCCESSFULLY----------\n")
        except TimeoutException:
            print("[✖] Home header did not reappear in time")
    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error: {e}")





# Added explicit delay newly, need to be updated on app_test2 and app_test1
def send_money(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at send_money start"
        print("[✔] Network is connected")

        # Wait for and tap the "সেন্ড মানি" button
        send_locator = (AppiumBy.ACCESSIBILITY_ID, "সেন্ড মানি\n\n")
        try:
            send_button = wait.until(EC.element_to_be_clickable(send_locator))
            assert send_button.is_displayed(), '"Send Money" button not visible'
            print("[✔] 'Send Money' button is visible and clickable")
            send_button.click()
        except TimeoutException:
            print("[✖] 'Send Money' button was not found within the timeout")
            return

        # Enter recipient number
        try:
            type_and_enter(driver, "01521257282")
            print("[✔] Recipient number entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter recipient number: {e}")
            return

        # Wait for and tap “এগিয়ে যান” button
        next_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("এগিয়ে যান")'
        )
        try:
            next_button = wait.until(EC.element_to_be_clickable(next_locator))
            assert next_button.is_displayed(), '"Next" button not visible'
            print("[✔] 'Next' button is visible and clickable")
            next_button.click()
        except TimeoutException:
            print("[✖] 'Next' button was not found after entering recipient")
            return

        # Enter amount
        try:
            type_and_enter(driver, "5")
            print("[✔] Amount entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter amount: {e}")
            return

        # Again wait for and tap “এগিয়ে যান” button
        try:
            next_button = wait.until(EC.element_to_be_clickable(next_locator))
            assert next_button.is_displayed(), '"Next" button not visible after amount entry'
            print("[✔] 'Next' button is visible and clickable (after amount)")
            next_button.click()
        except TimeoutException:
            print("[✖] 'Next' button was not found after entering amount")
            return

        # Enter PIN
        for digit in ("1", "3", "1", "3", "1"):
            digit_locator = (AppiumBy.ACCESSIBILITY_ID, digit)
            try:
                digit_button = wait.until(EC.element_to_be_clickable(digit_locator))
                assert digit_button.is_displayed(), f'PIN digit "{digit}" button not visible'
                print(f"[✔] PIN digit '{digit}' button is found")
                digit_button.click()
            except TimeoutException:
                print(f"[✖] PIN digit '{digit}' button was not found within timeout")
                return

        # Wait for and tap “নিশ্চিত করুন” button
        confirm_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("নিশ্চিত করুন")'
        )
        try:
            confirm_button = wait.until(EC.element_to_be_clickable(confirm_locator))
            assert confirm_button.is_displayed(), '"Confirm" button not visible'
            print("[✔] 'Confirm' button is visible and clickable")
            confirm_button.click()
        except TimeoutException:
            print("[✖] 'Confirm' button was not found within timeout")
            return

        # Wait for the drag element
        drag_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ট্যাপ করে ধরে রাখুন")'
        )
        try:
            drag_element = wait.until(EC.presence_of_element_located(drag_locator))
            assert drag_element.is_displayed(), '"Tap and Hold" element not visible'
            print("[✔] 'Tap and Hold' element is visible")
        except TimeoutException:
            print("[✖] 'Tap and Hold' element not found within timeout")
            return

        # Perform dragGesture (tap & hold)
        try:
            size = driver.get_window_size()
            max_y = size['height']
            desired_y = max_y - 150
            driver.execute_script(
                "mobile: dragGesture",
                {
                    "startX": 360, "startY": desired_y,
                    "endX": 361, "endY": desired_y,
                    "speed": 1
                }
            )
            print("[✔] Drag gesture performed successfully")
        except Exception as e:
            print(f"[✖] Failed to perform drag gesture: {e}")
            return

        # Wait for and tap “হোম-এ ফিরে যাই” button
        home_back = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("হোম-এ ফিরে যাই")'
        )
        try:
            home_button = wait.until(EC.element_to_be_clickable(home_back))
            assert home_button.is_displayed(), '"Back to Home" button not visible'
            print("[✔] 'Back to Home' button is visible and clickable")
            home_button.click()
        except TimeoutException:
            print("[✖] 'Back to Home' button was not found within timeout")
            return

        print("\n---------- SEND MONEY COMPLETED SUCCESSFULLY ----------\n")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error: {e}")


# Added explicit wait, need to be updated on app_test2 and app_test1
def logout(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at logout start"
        print("[✔] Network is connected")

        # Delay to ensure that if the message pop up appeared, it is gone by now.
        time.sleep(5)

        # Find the "3 bars" button and click it
        try:
            bars_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(0)'
            )
            bars_element = wait.until(EC.visibility_of_element_located(bars_locator))
            
            # Assert "3 bars" button is visible
            assert bars_element.is_displayed(), '"3 bars" button is not visible'
            print("[✔] '3 bars' menu button is visible")
            bars_element.click()
        except TimeoutException:
            print("[✖] '3 bars' menu button was not found within the timeout")
            return

        # Find the "লগ আউট" button and click it
        try:
            logout_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("লগ আউট")'
            )
            logout_element = wait.until(EC.element_to_be_clickable(logout_locator))
            
            # Assert "লগ আউট" button is visible and clickable
            assert logout_element.is_displayed(), '"Log out" button is not visible'
            print("[✔] 'Log out' button is visible")
            logout_element.click()
        except TimeoutException:
            print("[✖] 'Log out' button was not found within the timeout")
            return

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during logout: {e}")
    else:
        print("\n----------LOG OUT COMPLETED SUCCESSFULLY----------\n")


def check_QR_code(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at check_QR_code start"
        print("[✔] Network is connected")

        # Find the "QR code" icon and click on it
        try:
            qr_icon = driver.find_element(
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView'
            )
            assert qr_icon.is_displayed(), '"QR code" icon is not visible'
            print("[✔] 'QR code' icon is visible")

            wait.until(EC.element_to_be_clickable(qr_icon))
            qr_icon.click()
            print("[✔] 'QR code' icon clicked")
        except TimeoutException:
            print("[✖] 'QR code' icon not found or not clickable")
            return

        # Wait for the "আমার QR" section to be present before swipe
        amar_qr_locator = (
            AppiumBy.ACCESSIBILITY_ID,
            "আমার QR\nTab 2 of 2"
        )
        try:
            amar_qr_element = wait.until(EC.presence_of_element_located(amar_qr_locator))
            assert amar_qr_element.is_displayed(), '"My QR" section not visible'
            print("[✔] 'My QR' section is visible")
        except TimeoutException:
            print("[✖] 'My QR' section not found within timeout")
            return

        # Swipe to the left to open the "আমার QR" section
        page_source = driver.page_source
        swipe(driver, 700, 500, 100, 500)
        after_swipe_page_source = driver.page_source
        assert page_source != after_swipe_page_source, "No swipe performed"
        print("[✔] Performed swipe to open 'My QR' section")

        # Wait for the download button to be present before clicking gesture
        download_button_locator = (
            AppiumBy.XPATH,
            '//android.widget.ImageView[@content-desc="QR ডাউনলোড করুন"]/android.view.View/android.widget.ImageView[2]'
        )
        try:
            download_button = wait.until(EC.presence_of_element_located(download_button_locator))
            assert download_button.is_displayed(), '"Download QR" button not visible'
            print("[✔] 'Download QR' button is visible")
        except TimeoutException:
            print("[✖] 'Download QR' button not found within timeout")
            return

        # Press the download button to download the QR code
        driver.execute_script(
            "mobile: clickGesture",
            {"x": 360, "y": 1343}
        )

        # Wait for the download confirmation popup
        download_post_popup = (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="মার্চেন্ট QR কোড ডাউনলোড সফল হয়েছে"]'
        )
        try:
            success_popup = wait.until(EC.presence_of_element_located(download_post_popup))
            assert success_popup.is_displayed(), 'Download success popup not visible'
            print("[✔] Download success popup is visible")
        except TimeoutException:
            print("[✖] Download success popup not found within timeout")
            return

        # Press the back button to return to the homepage
        driver.press_keycode(AndroidKey.BACK)
        time.sleep(3)
        print("[✔] BACK key pressed to return home")

        # Wait for and assert that the home header is visible
        home_header_locator = (AppiumBy.ACCESSIBILITY_ID, "Shop Local 96")
        try:
            home_header = wait.until(EC.presence_of_element_located(home_header_locator))
            assert home_header.is_displayed(), "'Shop Local 96' header not visible after BACK"
            print("[✔] 'Shop Local 96' header is visible after returning home")
        except TimeoutException:
            print("[✖] 'Shop Local 96' header not found after pressing BACK")
            return

        print("\n----------CHECK QR CODE COMPLETED SUCCESSFULLY----------\n")
    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error: {e}")



# Added explicit wait and it needs to be updated on app_test2 and app_test1
def pay_bills(driver, wait):
    try:
        # Network status check
        network_status(driver)
        assert is_network_connected(driver), "Network is not connected at pay_bills start"
        print("[✔] Network is connected")

        # Find & tap the "পে বিল" button
        pay_bill_locator = (AppiumBy.ACCESSIBILITY_ID, "পে বিল\n\n")
        try:
            pay_bill_btn = wait.until(EC.element_to_be_clickable(pay_bill_locator))
            assert pay_bill_btn.is_displayed(), "'পে বিল' button is not visible"
            print("[✔] 'Pay Bill' button is visible and clickable")
            pay_bill_btn.click()
        except TimeoutException:
            print("[✖] 'Pay Bill' button not found within timeout")
            return
        time.sleep(2)

        # Find & tap the "ইন্টারনেট" button
        internet_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ইন্টারনেট")'
        )
        try:
            internet_btn = wait.until(EC.element_to_be_clickable(internet_locator))
            assert internet_btn.is_displayed(), "'Internet' button is not visible"
            print("[✔] 'Internet' button is visible and clickable")
            internet_btn.click()
        except TimeoutException:
            print("[✖] 'Internet' button not found within timeout")
            return

        # Find & tap the "Link3" button
        link3_locator = (AppiumBy.ACCESSIBILITY_ID, "Link3\nইন্টারনেট")
        try:
            link3_btn = wait.until(EC.element_to_be_clickable(link3_locator))
            assert link3_btn.is_displayed(), "'Link3' button is not visible"
            print("[✔] 'Link3' button is visible and clickable")
            link3_btn.click()
        except TimeoutException:
            print("[✖] 'Link3' button not found within timeout")
            return
        time.sleep(2)

        # Enter subscriber ID
        try:
            subscriber_ID = wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(0)'
            )))
            assert subscriber_ID.is_displayed(), "Subscriber ID field is not visible"
            subscriber_ID.click()
            subscriber_ID.send_keys("L3R120")
            print("[✔] Subscriber ID entered successfully")
        except TimeoutException:
            print("[✖] Subscriber ID field not found within timeout")
            return

        # Enter contact number
        try:
            contact_number = wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(1)'
            )))
            assert contact_number.is_displayed(), "Contact number field is not visible"
            contact_number.click()
            contact_number.send_keys("01765614227")
            print("[✔] Contact number entered successfully")
        except TimeoutException:
            print("[✖] Contact number field not found within timeout")
            return
        time.sleep(2)

        # Click "পে বিল করতে এগিয়ে যান"
        proceed_locator = (AppiumBy.ACCESSIBILITY_ID, "পে বিল করতে এগিয়ে যান")
        try:
            proceed_btn = wait.until(EC.element_to_be_clickable(proceed_locator))
            assert proceed_btn.is_displayed(), "'Go ahead to pay bills' button is not visible"
            print("[✔] 'Go ahead to pay bills' button is visible and clickable")
            proceed_btn.click()
        except TimeoutException:
            print("[✖] 'Go ahead to pay bills' button not found within timeout")
            return
        time.sleep(2)

        # Enter payment amount
        try:
            amount_field = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText")'
            )))
            assert amount_field.is_displayed(), "Amount field is not visible"
            amount_field.click()
            type_and_enter(driver, "10")
            print("[✔] Amount entered successfully")
        except TimeoutException:
            print("[✖] Amount field not found within timeout")
            return
        time.sleep(2)

        # Click "পরের ধাপে যেতে ট্যাপ করুন"
        next_step_locator = (AppiumBy.ACCESSIBILITY_ID, "পরের ধাপে যেতে ট্যাপ করুন")
        try:
            next_step_btn = wait.until(EC.element_to_be_clickable(next_step_locator))
            assert next_step_btn.is_displayed(), "'Tap to go to the next step' button is not visible"
            print("[✔] 'Tap to go to the next step' button is visible and clickable")
            next_step_btn.click()
        except TimeoutException:
            print("[✖] 'Tap to go to the next step' button not found within timeout")
            return
        time.sleep(5)

        # Enter PIN digits
        for digit in ("1", "3", "1", "3", "1"):
            digit_locator = (AppiumBy.ACCESSIBILITY_ID, digit)
            try:
                pin_btn = wait.until(EC.element_to_be_clickable(digit_locator))
                assert pin_btn.is_displayed(), f"PIN digit '{digit}' button is not visible"
                print(f"[✔] PIN digit '{digit}' button is found")
                pin_btn.click()
            except TimeoutException:
                print(f"[✖] PIN digit '{digit}' button not found within timeout")
                return

        # Click "নিশ্চিত করুন"
        confirm_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("নিশ্চিত করুন")'
        )
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable(confirm_locator))
            assert confirm_btn.is_displayed(), "'Confirm it' button is not visible"
            print("[✔] 'Confirm it' button is visible and clickable")
            confirm_btn.click()
        except TimeoutException:
            print("[✖] 'Confirm it' button not found within timeout")
            return
        time.sleep(2)

        # Wait for drag element
        drag_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ট্যাপ করে ধরে রাখুন")'
        )
        try:
            drag_element = wait.until(EC.presence_of_element_located(drag_locator))
            assert drag_element.is_displayed(), "'Tap & Hold' element is not visible"
            print("[✔] 'Tap & Hold' element is visible")
        except TimeoutException:
            print("[✖] 'Tap & Hold' element not found within timeout")
            return

        # Perform the tap & hold drag gesture
        size = driver.get_window_size()
        desired_y = int(size['height'] - 150)
        driver.execute_script(
            "mobile: dragGesture",
            {"startX": 360, "startY": desired_y, "endX": 361, "endY": desired_y, "speed": 1}
        )
        time.sleep(5)

        # Find & tap the "হোম এ ফিরে যাই" button
        home_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("হোম এ ফিরে যাই")'
        )
        try:
            home_btn = wait.until(EC.element_to_be_clickable(home_locator))
            assert home_btn.is_displayed(), "'Go back to home' button is not visible"
            print("[✔] 'Go back to home' button is visible and clickable")
            home_btn.click()
        except TimeoutException:
            print("[✖] 'Go back to home' button not found within timeout")
            return
        time.sleep(10)

        print("\n---------- PAY BILLS COMPLETED SUCCESSFULLY ----------\n")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during pay_bills: {e}")



# Added explicit wait, need to be updated on app_test2 and app_test1
def savings_registration(driver, wait):
    try:
        # Network status check
        network_status(driver)
        assert is_network_connected(driver), "Network is not connected at savings_registration start"
        print("[✔] Network is connected")

        # Click "সেভিংস রেজিস্ট্রেশন"
        try:
            reg_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "সেভিংস রেজিস্ট্রেশন\n\n"
            )))
            assert reg_btn.is_displayed() and reg_btn.is_enabled(), "'Savings Registration' button not visible & clickable"
            print("[✔] 'Savings Registration' button visible & clickable")
            reg_btn.click()
        except TimeoutException:
            print("[✖] 'Savings Registration' button not found within timeout")
            return
        time.sleep(2)

        # Click "নতুন সেভিংস খুলুন"
        try:
            new_savings_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "নতুন সেভিংস খুলুন"
            )))
            assert new_savings_btn.is_displayed() and new_savings_btn.is_enabled(), "'Open new savings' button not visible & clickable"
            print("[✔] 'Open new savings' button visible & clickable")
            new_savings_btn.click()
        except TimeoutException:
            print("[✖] 'Open new savings' button not found within timeout")
            return
        time.sleep(2)

        # Click "আমি গ্রাহককে জানিয়েছি"
        try:
            informed_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "আমি গ্রাহককে জানিয়েছি"
            )))
            assert informed_btn.is_displayed() and informed_btn.is_enabled(), "'I've informed the customer' button not visible"
            print("[✔] 'I've informed the customer' button visible & clickable")
            informed_btn.click()
        except TimeoutException:
            print("[✖] 'I've informed the customer' button not found within timeout")
            return
        time.sleep(2)

        # Enter mobile number
        try:
            type_and_enter(driver, "01765614227")
            print("[✔] Mobile number entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter mobile number: {e}")
            return

        # Click "এগিয়ে যান"
        try:
            proceed_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "এগিয়ে যান"
            )))
            assert proceed_btn.is_displayed() and proceed_btn.is_enabled(), "'Go Ahead' button not visible & clickable"
            print("[✔] 'Go Ahead' button visible & clickable")
            proceed_btn.click()
        except TimeoutException:
            print("[✖] 'Go Ahead' button not found within timeout")
            return
        time.sleep(4)

        # Select "সাধারণ সেভিংস\nমুনাফাভিত্তিক সেভিংস"
        try:
            savings_option = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "সাধারণ সেভিংস\nমুনাফাভিত্তিক সেভিংস"
            )))
            assert savings_option.is_displayed() and savings_option.is_enabled(), "'General Savings' option not visible & clickable"
            print("[✔] 'General Savings' option visible & clickable")
            savings_option.click()
        except TimeoutException:
            print("[✖] 'General Savings' option not found within timeout")
            return
        time.sleep(2)

        # Open time-period selector
        try:
            time_selector = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(2)'
            )))
            assert time_selector.is_displayed() and time_selector.is_enabled(), "Time-period selector not visible & clickable"
            print("[✔] Time-period selector visible & clickable")
            time_selector.click()
        except TimeoutException:
            print("[✖] Time-period selector not found within timeout")
            return
        time.sleep(2)

        # Select "৬ মাস"
        try:
            six_months = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "৬ মাস"
            )))
            assert six_months.is_displayed() and six_months.is_enabled(), "'6 months' option not visible & clickable"
            print("[✔] '6 months' option visible & clickable")
            six_months.click()
        except TimeoutException:
            print("[✖] '6 months' option not found within timeout")
            return
        time.sleep(2)

        # Open savings-type selector
        try:
            savings_type_selector = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(3)'
            )))
            assert savings_type_selector.is_displayed() and savings_type_selector.is_enabled(), "Savings-type selector not visible & clickable"
            print("[✔] Savings-type selector visible & clickable")
            savings_type_selector.click()
        except TimeoutException:
            print("[✖] Savings-type selector not found within timeout")
            return
        time.sleep(2)

        # Select "সাপ্তাহিক"
        try:
            weekly = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "সাপ্তাহিক"
            )))
            assert weekly.is_displayed() and weekly.is_enabled(), "'Weekly' option not visible & clickable"
            print("[✔] 'Weekly' option visible & clickable")
            weekly.click()
        except TimeoutException:
            print("[✖] 'Weekly' option not found within timeout")
            return
        time.sleep(2)

        # Open amount selector
        try:
            amount_selector = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(4)'
            )))
            assert amount_selector.is_displayed() and amount_selector.is_enabled(), "Amount selector not visible & clickable"
            print("[✔] Amount selector visible & clickable")
            amount_selector.click()
        except TimeoutException:
            print("[✖] Amount selector not found within timeout")
            return
        time.sleep(2)

        # Select "৳250"
        try:
            amount_option = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "৳250"
            )))
            assert amount_option.is_displayed() and amount_option.is_enabled(), "'৳250' option not visible & clickable"
            print("[✔] '৳250' option visible & clickable")
            amount_option.click()
        except TimeoutException:
            print("[✖] '৳250' option not found within timeout")
            return
        time.sleep(2)

        # Click "এগিয়ে যান"
        try:
            proceed_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "এগিয়ে যান"
            )))
            assert proceed_btn.is_displayed() and proceed_btn.is_enabled(), "'Go Ahead' button not visible & clickable"
            print("[✔] 'Go Ahead' button visible & clickable")
            proceed_btn.click()
        except TimeoutException:
            print("[✖] 'Go Ahead' button not found within timeout")
            return
        time.sleep(4)

        # Select "Dhaka Bank PLC"
        try:
            bank_option = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Dhaka Bank PLC.\n৳250\nসাপ্তাহিক জমা\n8.5% মুনাফা\n6 মাস\n৳6,645.03\nমোট প্রদান"
            )))
            assert bank_option.is_displayed() and bank_option.is_enabled(), "'Dhaka Bank PLC' option not visible & clickable"
            print("[✔] 'Dhaka Bank PLC' option visible & clickable")
            bank_option.click()
        except TimeoutException:
            print("[✖] 'Dhaka Bank PLC' option not found within timeout")
            return
        time.sleep(2)

        # Enter nominee NID
        try:
            type_and_enter(driver, "1234567890")
            print("[✔] Nominee NID entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter nominee NID: {e}")
            return

        # Open birthday selector and click OK
        try:
            birthday_selector = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(2)'
            )))
            assert birthday_selector.is_displayed() and birthday_selector.is_enabled(), "Birthday selector not visible & clickable"
            print("[✔] Birthday selector visible & clickable") 
            birthday_selector.click()

            ok_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "OK"
            )))
            assert ok_btn.is_displayed() and ok_btn.is_enabled(), "'OK' button not visible & clickable"
            print("[✔] 'OK' button visible & clickable")
            ok_btn.click()
        except TimeoutException:
            print("[✖] Nominee birthday selector or OK button not found")
            return
        time.sleep(2)


        # Open relation selector and select "ভাই/বোন"
        try:
            relation_selector = wait.until(EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.ImageView").instance(3)'
            )))
            assert relation_selector.is_displayed() and relation_selector.is_enabled(), "Relation selector not visible & clickable"
            print("[✔] Relation selector visible & clickable")
            relation_selector.click()

            relation_option = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "ভাই/বোন"
            )))
            assert relation_option.is_displayed() and relation_option.is_enabled(), "'Brother/Sister' option not visible & clickable"
            print("[✔] 'Brother/Sister' option visible & clickable")
            relation_option.click()
        except TimeoutException:
            print("[✖] Nominee relation selector or option not found")
            return
        time.sleep(2)

        # Click "এগিয়ে যান"
        try:
            proceed_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "এগিয়ে যান"
            )))
            assert proceed_btn.is_displayed() and proceed_btn.is_enabled(), "'Go Ahead' button not visible & clickable"
            print("[✔] 'Go Ahead' button visible & clickable")
            proceed_btn.click()
        except TimeoutException:
            print("[✖] 'Go Ahead' button not found within timeout")
            return
        time.sleep(10)

        # Click "নিশ্চিত করুন"
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "নিশ্চিত করুন"
            )))
            assert confirm_btn.is_displayed() and confirm_btn.is_enabled(), "'Confirm it' button not visible & clickable"
            print("[✔] 'Confirm it' button visible & clickable")
            confirm_btn.click()
        except TimeoutException:
            print("[✖] 'Confirm it' button not found within timeout")
            return
        time.sleep(7)

        # Click "হোম-এ ফিরে যান"
        try:
            home_btn = wait.until(EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, "হোম-এ ফিরে যান"
            )))
            assert home_btn.is_displayed() and home_btn.is_enabled(), "'Go back to home' button not visible & clickable"
            print("[✔] 'Go back to home' button visible & clickable")
            home_btn.click()
        except TimeoutException:
            print("[✖] 'Go back to home' button not found within timeout")
            return
        time.sleep(4)

        print("\n---------- SAVINGS REGISTRATION COMPLETED SUCCESSFULLY ----------\n")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during savings_registration: {e}")



# Added explicit wait, need to be updated on app_test2 and app_test1
def agent_cashout(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at agent_cashout start"
        print("[✔] Network is connected")

        # Wait for & tap the "এজেন্ট ক্যাশ আউট" button
        cashout_locator = (
            AppiumBy.ACCESSIBILITY_ID,
            "এজেন্ট ক্যাশ আউট\n\n"
        )
        try:
            cashout_btn = wait.until(EC.element_to_be_clickable(cashout_locator))
            assert cashout_btn.is_displayed(), "'Agent Cash-out' button is not visible"
            print("[✔] 'Agent Cash-out' button is visible and clickable")
            cashout_btn.click()
        except TimeoutException:
            print("[✖] 'Agent Cash-out' button not found within timeout")
            return

        # Enter agent number
        try:
            type_and_enter(driver, "01810189688")
            print("[✔] Agent number entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter agent number: {e}")
            return

        # Wait for & tap "এগিয়ে যান"
        next_locator = (AppiumBy.ACCESSIBILITY_ID, "এগিয়ে যান")
        try:
            next_btn = wait.until(EC.element_to_be_clickable(next_locator))
            assert next_btn.is_displayed(), "'Go ahead' button is not visible"
            print("[✔] 'Go ahead' button is visible and clickable")
            next_btn.click()
        except TimeoutException:
            print("[✖] 'Go ahead' button not found within timeout")
            return

        # Enter cash-out amount
        try:
            type_and_enter(driver, "10")
            print("[✔] Cash-out amount entered successfully")
        except Exception as e:
            print(f"[✖] Failed to enter cash-out amount: {e}")
            return

        # Wait for & tap "এগিয়ে যান" again
        try:
            next_btn = wait.until(EC.element_to_be_clickable(next_locator))
            assert next_btn.is_displayed(), "'এগিয়ে যান' button is not visible"
            print("[✔] 'Go ahead' button is visible and clickable")
            next_btn.click()
        except TimeoutException:
            print("[✖] 'Go ahead' button not found within timeout (2nd)")
            return

        # Enter PIN digits
        for digit in ("1", "3", "1", "3", "1"):
            digit_locator = (AppiumBy.ACCESSIBILITY_ID, digit)
            try:
                pin_btn = wait.until(EC.element_to_be_clickable(digit_locator))
                assert pin_btn.is_displayed(), f"PIN digit '{digit}' button not visible"
                print(f"[✔] PIN digit '{digit}' button is found")
                pin_btn.click()
            except TimeoutException:
                print(f"[✖] PIN digit '{digit}' button not found within timeout")
                return

        # Wait for & tap "নিশ্চিত করুন"
        confirm_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("নিশ্চিত করুন")'
        )
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable(confirm_locator))
            assert confirm_btn.is_displayed(), "'Confirm it' button not visible"
            print("[✔] 'Confirm it' button is visible and clickable")
            confirm_btn.click()
        except TimeoutException:
            print("[✖] 'Confirm it' button not found within timeout")
            return

        # Wait for the "Tap & Hold" drag element
        drag_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ট্যাপ করে ধরে রাখুন")'
        )
        try:
            drag_element = wait.until(EC.presence_of_element_located(drag_locator))
            assert drag_element.is_displayed(), "'Tap & Hold' element not visible"
            print("[✔] 'Tap & Hold' element is visible")
        except TimeoutException:
            print("[✖] 'Tap & Hold' element not found within timeout")
            return

        # Perform the tap-and-hold drag gesture
        size = driver.get_window_size()
        desired_y = size['height'] - 150
        driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": 360, "startY": desired_y,
                "endX":   361, "endY":   desired_y,
                "speed": 1
            }
        )

        # Wait for & tap the "হোম-এ ফিরে যাই" button
        home_back_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("হোম-এ ফিরে যাই")'
        )
        try:
            home_btn = wait.until(EC.element_to_be_clickable(home_back_locator))
            assert home_btn.is_displayed(), "'হোম-এ ফিরে যাই' button not visible"
            print("[✔] 'Go back to home' button is visible and clickable")
            home_btn.click()
        except TimeoutException:
            print("[✖] 'Go back to home' button not found within timeout")
            return

        print("\n---------- AGENT CASHOUT COMPLETED SUCCESSFULLY ----------\n")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during agent_cashout: {e}")



def merchant_payment(driver, wait):
    try:
        # Network status check
        network_status(driver)

        # Assert network is connected
        assert is_network_connected(driver), "Network is not connected at merchant_payment start"
        print("[✔] Network is connected")

        # Wait for and click the "মার্চেন্ট পেমেন্ট" button
        merchant_payment_btn = (AppiumBy.ACCESSIBILITY_ID, "মার্চেন্ট পেমেন্ট\n\n")
        try:
            button = wait.until(EC.element_to_be_clickable(merchant_payment_btn))
            assert button.is_displayed(), "'Merchant Payment' button is not visible"
            print("[✔] 'Merchant Payment' button is visible and clickable")
            button.click()
        except TimeoutException:
            print("[✖] 'Merchant Payment' button not found within timeout")
            return

        # Type and enter the merchant number
        try:
            type_and_enter(driver, "01800011111")
            print("[✔] Merchant number entered successfully")
        except AssertionError as ae:
            print(f"[✖] Assertion failed while entering merchant number: {ae}")
            return
        except Exception as e:
            print(f"[✖] Failed to enter merchant number: {e}")
            return

        # Wait for and click the "এগিয়ে যান" button
        proceed_btn = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("এগিয়ে যান")'
        )
        try:
            next_btn = wait.until(EC.element_to_be_clickable(proceed_btn))
            assert next_btn.is_displayed(), "'Go ahead' button is not visible"
            print("[✔] 'Go ahead' button is visible and clickable")
            next_btn.click()
        except TimeoutException:
            print("[✖] 'Go ahead' button not found within timeout")
            return

        # Enter amount
        try:
            type_and_enter(driver, "25")
            print("[✔] Amount entered successfully")
        except AssertionError as ae:
            print(f"[✖] Assertion failed while entering amount: {ae}")
            return
        except Exception as e:
            print(f"[✖] Failed to enter amount: {e}")
            return

        # Wait for and click the "এগিয়ে যান" button again
        try:
            next_btn = wait.until(EC.element_to_be_clickable(proceed_btn))
            assert next_btn.is_displayed(), "'Go ahead' button is not visible"
            print("[✔] 'Go ahead' button is visible and clickable")
            next_btn.click()
        except TimeoutException:
            print("[✖] 'Go ahead' button not found within timeout")
            return

        # Enter PIN digits
        for digit in ("1", "3", "1", "3", "1"):
            digit_locator = (AppiumBy.ACCESSIBILITY_ID, digit)
            try:
                pin_btn = wait.until(EC.element_to_be_clickable(digit_locator))
                assert pin_btn.is_displayed(), f"PIN digit '{digit}' button not visible"
                print(f"[✔] PIN digit '{digit}' button found")
                pin_btn.click()
            except TimeoutException:
                print(f"[✖] PIN digit '{digit}' button not found within timeout")
                return

        # Wait for and click “নিশ্চিত করুন”
        confirm_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("নিশ্চিত করুন")'
        )
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable(confirm_locator))
            assert confirm_btn.is_displayed(), "'Confirm it' button not visible"
            print("[✔] 'Confirm it' button is visible and clickable")
            confirm_btn.click()
        except TimeoutException:
            print("[✖] 'Confirm it' button not found within timeout")
            return

        # Wait for the drag element to appear
        drag_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("ট্যাপ করে ধরে রাখুন")'
        )
        try:
            drag_element = wait.until(EC.presence_of_element_located(drag_locator))
            assert drag_element.is_displayed(), "'Tap and Hold' icon not visible"
            print("[✔] 'Tap and Hold' icon is visible")
        except TimeoutException:
            print("[✖] 'Tap and Hold' icon not found within timeout")
            return

        # Perform drag gesture (tap & hold)
        size = driver.get_window_size()
        max_y = size['height']
        desired_y = max_y - 150
        driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": 360, "startY": desired_y,
                "endX":   361, "endY":   desired_y,
                "speed": 1
            }
        )

        # Wait for and click “হোম-এ ফিরে যাই”
        home_back = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("হোম-এ ফিরে যাই")'
        )
        try:
            home_btn = wait.until(EC.element_to_be_clickable(home_back))
            assert home_btn.is_displayed(), "'Go back to home' button not visible"
            print("[✔] 'Go back to home' button is visible and clickable")
            home_btn.click()
        except TimeoutException:
            print("[✖] 'Go back to home' button not found within timeout")
            return

        print("\n---------- MERCHANT PAYMENT COMPLETED SUCCESSFULLY ----------\n")

    except AssertionError as ae:
        print(f"[✖] Assertion failed: {ae}")
    except Exception as e:
        print(f"[✖] Unexpected error during merchant_payment: {e}")



def main():
    # Build UiAutomator2 options
    opts = UiAutomator2Options()
    opts.platform_name               = "Android"
    opts.automation_name             = "UiAutomator2"
    opts.udid                        = "26e3396e"

    # Skip all the init steps that trigger hidden-API errors
    opts.set_capability("skipDeviceInitialization",   True)
    #Remove the next line when other device 1 is connected
    opts.set_capability("skipServerInstallation",     True)
    opts.set_capability("ignoreHiddenApiPolicyError", True)
    #New (to keep the appium alive for long time)
    opts.set_capability("newCommandTimeout", 28800)


    # Don’t uninstall or stop the app on reset
    opts.no_reset = True
    opts.set_capability("dontStopAppOnReset", True)

    # Start the session & open the app
    driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)

    # Adding implicit delay to for looking up for elements
    driver.implicitly_wait(15)

    # Adding explicit wait
    wait = WebDriverWait(driver, 20)

    # Activate and open the app
    driver.activate_app("com.bKash.merchantapp.uat")

    # Login error check
    #login_error_check(driver, wait)

    # perform login
    login(driver, wait)     # Assersion added (DONE)

    # check balance
    check_balance(driver, wait)     # Assersion added (DONE)

    #check inbox
    check_inbox(driver, wait)       # Assersion added (DONE)

    #check transactions
    check_transactions(driver, wait)    # Assersion added (DONE)  

    #check namaz roja details
    namaz_roja_details(driver, wait)    # Assersion added (DONE)

    #check send money
    #send_money(driver, wait)             # Assersion added (DONE)---

    #check merchant payment
    #merchant_payment(driver, wait)       # Assersion added (DONE)---

    #check qr code
    check_QR_code(driver, wait)          #Assersion added (DONE)

    #check pay bills
    #pay_bills(driver, wait)              # Assersion added (DONE)---

    #check savings registration
    savings_registration(driver, wait)   # Assersion added (DONE)

    #check agent cashout
    #agent_cashout(driver, wait)         # Assersion added (DONE)---

    #check logout
    logout(driver, wait)    # Assersion added  (DONE)

    # Press HOME
    driver.press_keycode(AndroidKey.HOME)

    # Close the session
    driver.quit()

if __name__ == "__main__":
    main()
