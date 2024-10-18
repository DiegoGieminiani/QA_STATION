from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from functional_tests.selenium_test.base_action import BaseAction

class SwitchTabAction(BaseAction):
    def execute(self, timeout=10, **kwargs):
        try:
            # Save the current window handle
            original_window = self.driver.current_window_handle

            # Wait until a new window/tab is opened
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.window_handles) > 1
            )

            # Get the new window handle (that is not the original one)
            new_window = [window for window in self.driver.window_handles if window != original_window]

            if not new_window:
                raise NoSuchWindowException("Could not find a new tab to switch to.")

            # Switch to the new window/tab
            self.driver.switch_to.window(new_window[0])

            # Return success response
            return self.default_response(
                action='switch_tab',
                element='tab',
                status='success'
            )

        except TimeoutException:
            return self.default_response(
                action='switch_tab',
                element='tab',
                status='fail',
                error="Timeout: A new tab did not open in time."
            )

        except NoSuchWindowException as e:
            return self.default_response(
                action='switch_tab',
                element='tab',
                status='fail',
                error=f"Could not find the new tab: {str(e)}"
            )

        except Exception as e:
            # General exception handling
            return self.default_response(
                action='switch_tab',
                element='tab',
                status='fail',
                error=f"Unexpected error: {str(e)}"
            )
