from telegram_agent.config.strings import info_strings
from langdetect import detect


def get_localized_answer(answer_he: str, answer_en: str, user_input: str) -> str:
    """Return Hebrew or English answer based on detected language."""
    try:
        if user_input and detect(user_input) == "he":
            return answer_he
        else:
            return answer_en
    except Exception:
        # Default to Hebrew if detection fails
        return answer_he


def get_working_hours(input: str = None) -> str:
    """Get business working hours information."""
    return get_localized_answer(
        info_strings.WORKING_HOURS_ANSWER_HE,
        info_strings.WORKING_HOURS_ANSWER_EN,
        input
    )


def get_shipping_info(order_id: str = None) -> str:
    """Get shipping policy and delivery time information."""
    return get_localized_answer(
        info_strings.SHIPPING_ANSWER_HE,
        info_strings.SHIPPING_ANSWER_EN,
        order_id
    )


def get_refund_policy(input: str = None) -> str:
    """Get refund and return policy information."""
    return get_localized_answer(
        info_strings.REFUND_ANSWER_HE,
        info_strings.REFUND_ANSWER_EN,
        input
    )


def get_faq(question: str = None) -> str:
    """Get answers to frequently asked questions."""
    return get_localized_answer(
        info_strings.FAQ_ANSWER_HE,
        info_strings.FAQ_ANSWER_EN,
        question
    )


def get_support_contact(input: str = None) -> str:
    """Get customer support contact information."""
    return get_localized_answer(
        info_strings.SUPPORT_ANSWER_HE,
        info_strings.SUPPORT_ANSWER_EN,
        input
    )

