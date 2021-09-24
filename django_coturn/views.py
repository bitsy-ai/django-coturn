from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .services import create_turn_api_credentials


@method_decorator(login_required, name="dispatch")
class CreateCoturnCredential(View):
    """
    Generate a token conforming to TURN REST Server API spec outlined in draft-uberti-behave-turn-rest-00
    https://www.ietf.org/proceedings/87/slides/slides-87-behave-10.pdf
    """

    def get(self, request):
        username, password = create_turn_api_credentials(request.user.email)


create_coturn_credential = CreateCoturnCredential.as_view()
