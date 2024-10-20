from django.urls import path, include
from web_scraping_app import views
from web_scraping_pro import swagger_service


urlpatterns = [

    path('docs/', swagger_service.schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),


    path('logging/', include([
        path('', include([

            path( 'ask_website/', views.WebScrapingAPIView.as_view() ),

        ]))
    ])),]