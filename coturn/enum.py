from enum import Enum

class CoturnAuthStrategy(Enum):
    LONG_TERM_CREDENTIALS = "Long Term Credentials"
    TURN_REST_API = "TURN REST API described in https://www.ietf.org/proceedings/87/slides/slides-87-behave-10.pdf"