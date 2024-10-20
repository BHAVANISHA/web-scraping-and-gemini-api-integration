import socket
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_yasg.generators import OpenAPISchemaGenerator

hostname = socket.gethostname()
IPAddr = "15.207.242.99"


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            # {
            #     "name": "logging",
            #     "description": "These Operations refer to the process of registering an account, as well as the login and logout functionalities. "
            # },
           ]

        return swagger


content = "Vivyahire"

schema_view = get_schema_view(

    openapi.Info(
        title="webscraping",
        default_version='v1',
        hideHostname=False,
        description="Description: " + content + " \n \n Logfile Link: http://" + IPAddr + "/webscraping.log "
                                                                                          "\n \n Environment - Dev ",
        terms_of_service="https://www.dellainfotech.com/",
        contact=openapi.Contact(email="PythonTeam@dellainfotech.com"),
        license=openapi.License(name="VR Della IT Services"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=CustomOpenAPISchemaGenerator,

)