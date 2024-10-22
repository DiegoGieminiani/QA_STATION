from functional_tests.selenium_test.actions.alerts import AcceptAlertAction, AlertIsPresentAction, ConfirmAlertAction, DismissAlertAction, EnterPromptAction, PromptAlertAction

from functional_tests.selenium_test.actions.data_extraction import ExtractAttributeAction, ExtractDropdownOptionsAction, ExtractLinksAction, ExtractListItemsAction, ExtractTableDataAction, ExtractTextAction

from functional_tests.selenium_test.actions.forms import EnterDataAction, SelectAction, CheckCheckboxAction, ClearFieldAction, SelectRadioButtonAction, SubmitFormAction

from functional_tests.selenium_test.actions.javascript import ChangeElementStyleAction, ExecuteScriptAction, GetElementPropertyAction, ScrollIntoViewAction

from functional_tests.selenium_test.actions.keyboard_mouse import SendKeysAction, DragAndDropAction, ContextClickAction, DoubleClickAction, ClickAndHoldAction, HoverAction, ReleaseAction, ScrollAction

from functional_tests.selenium_test.actions.modals import CloseModalAction, EnterDataInModalAction, OpenModalAction, SubmitModalFormAction, VerifyModalVisibleAction

from functional_tests.selenium_test.actions.navigation import BackAction, ClickAction, ForwardAction, NavigateToUrlAction, RefreshPageAction, ScrollToElementAction, SwitchTabAction

from functional_tests.selenium_test.actions.verifications import VerifyTextAction, VerifyUrlAction, VerifyAttributeValue, VerifyElementHasChildWithClass, VerifyElementPresence, VerifyElementSelected

class ActionRouter:
    def __init__(self, driver):
        # Mapeo de las acciones con las clases correspondientes
        self.driver = driver
        self.action_map = {
            # Alerts
            "accept_alert": AcceptAlertAction,
            "alert_is_present": AlertIsPresentAction,
            "confirm_alert": ConfirmAlertAction,
            "dismiss_alert": DismissAlertAction,
            "enter_prompt": EnterPromptAction,
            "prompt_alert": PromptAlertAction,
            # Data Extraction
            "extract_attribute": ExtractAttributeAction,
            "extract_dropdown_options": ExtractDropdownOptionsAction,
            "extract_links": ExtractLinksAction,
            "extract_list_items": ExtractListItemsAction,
            "extract_table_data": ExtractTableDataAction,
            "extract_text": ExtractTextAction,
            # Forms
            "enter_data": EnterDataAction,
            "select": SelectAction,
            "check_checkbox": CheckCheckboxAction,
            "clear_field": ClearFieldAction,
            "select_radio_button": SelectRadioButtonAction,
            "submit_form": SubmitFormAction,
            # JavaScript
            "change_element_style": ChangeElementStyleAction,
            "execute_script": ExecuteScriptAction,
            "get_element_property": GetElementPropertyAction,
            "scroll_into_element": ScrollIntoViewAction,
            # Keyboard/Mouse
            "send_keys": SendKeysAction,
            "drag_and_drop": DragAndDropAction,
            "context_click": ContextClickAction,
            "double_click": DoubleClickAction,
            "click_and_hold": ClickAndHoldAction,
            "hover": HoverAction,
            "release": ReleaseAction,
            "scroll": ScrollAction,
            # Modals
            "close_modal": CloseModalAction,
            "enter_data_in_modal": EnterDataInModalAction,
            "open_modal": OpenModalAction,
            "submit_modal_form": SubmitModalFormAction,
            "verify_modal_vision": VerifyModalVisibleAction,
            # Navigation
            "back": BackAction,
            "click": ClickAction,
            "forward": ForwardAction,
            "navigate_to_url": NavigateToUrlAction,
            "refresh": RefreshPageAction,
            "scroll_to_element": ScrollToElementAction,
            "switch_tab": SwitchTabAction,
            # Verifications
            "verify_text": VerifyTextAction,
            "verify_url": VerifyUrlAction,
            "verify_attribute_value": VerifyAttributeValue,
            "verify_element_has_child": VerifyElementHasChildWithClass,
            "verify_element_presence": VerifyElementPresence,
            "verify_element_selected": VerifyElementSelected
        }
    def route_action(self, action_name, params):
        action_class = self.action_map.get(action_name)
        return action_class(self.driver)
