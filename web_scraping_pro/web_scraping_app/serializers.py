from rest_framework import serializers

from web_scraping_app import models


class Web_scraping_Serializer( serializers.Serializer ):
    user_email= serializers.CharField()
    input_website = serializers.CharField()
    ask_query_form_website = serializers.CharField()


class WebScrapingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.web_scrap
        fields = ['website', 'query', 'answer']