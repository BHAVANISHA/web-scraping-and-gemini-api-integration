import requests
from bs4 import BeautifulSoup
import os

from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as genai
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from web_scraping_app import models, serializers
import logging

_logger = logging.getLogger( __name__ )

# Load environment variables from .env
load_dotenv()

# Configure API Key from environment
API_KEY = os.getenv( "GOOGLE_API_KEY" )

if not API_KEY:
    _logger.error( "Google API Key not found in environment variables!" )
    raise Exception( "Google API Key not found!" )


class GeminiAI:
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = API_KEY

        try:
            genai.configure( api_key=self.api_key )
            self.model = genai.GenerativeModel( self.model_name )
        except Exception as e:
            _logger.error( f"Failed to initialize Gemini: {e}" )
            raise

    def generate_response(self, input_text):
        """Generates a response using the Gemini model"""
        try:
            response = self.model.generate_content( input_text )
            return response
        except Exception as e:
            _logger.error( f"Error generating response: {e}" )
            return None


# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get( url )
        if response.status_code == 200:
            soup = BeautifulSoup( response.text, 'html.parser' )
            return soup.get_text()  # Extract text content from website
        else:
            _logger.error( f"Failed to access the website, status code: {response.status_code}" )
            return None
    except Exception as e:
        _logger.error( f"An error occurred while scraping the website: {e}" )
        return None



# Function to interact with Google Gemini and generate an answer
def ask_question_to_gemini(content, question):
    gemini = GeminiAI( "gemini-pro" )  # Initialize GeminiAI with the desired model
    prompt = f"{content}\n\n{question}"  # Prepare the prompt for the model
    response = gemini.generate_response( input_text=prompt )

    if response:
        for candidate in response.candidates:
            content_parts = getattr( candidate.content, 'parts', [] )
            return ' '.join( [part.text for part in content_parts] ) if content_parts else "No content parts available."
    else:
        return "No response received from the model."


class WebScrapingAPIView( GenericAPIView ):
    ''' This class is used for scraping the website and asking a question via Gemini '''

    serializer_class = serializers.Web_scraping_Serializer

    def post(self, request, *args, **kwargs):
        try:
            website = request.data.get( 'input_website' )
            query = request.data.get( 'ask_query_form_website' )
            user_email = request.data['user_email']
            if not website or not query:
                _logger.error( "Website URL or query not provided." )
                return Response( {
                    'response_code': 400,
                    'message': 'Please provide both the website URL and the query.',
                    'statusFlag': False,
                    'status': 'FAILURE',
                    'errorDetails': 'Invalid input.',
                    'data': []
                } )

            # Scrape the website content
            scraped_content = scrape_website( website )

            if scraped_content:
                _logger.info( "Website content successfully scraped." )
                # Ask the question to Gemini
                answer = ask_question_to_gemini( scraped_content, query )

                # Save the result to the database
                web_scraping_data = models.web_scrap.objects.create(
                    website=website,
                    user_email = user_email,
                    query=query,
                    answer=answer
                )

                _logger.info( "Data saved successfully in the database." )

                return Response( {
                    'response_code': 200,
                    'message': "Question answered and saved successfully.",
                    'statusFlag': True,
                    'status': 'SUCCESS',
                    'data': {
                        'answer': answer
                    }
                } )
            else:
                _logger.error( "Failed to scrape website content." )
                return Response( {
                    'response_code': 500,
                    'message': 'Failed to scrape website content.',
                    'statusFlag': False,
                    'status': 'FAILURE',
                    'errorDetails': 'Could not scrape website content.',
                    'data': []
                } )

        except Exception as e:
            _logger.error( f"Error during scraping and question asking: {e}" )
            return Response( {
                'response_code': 500,
                'message': 'An error occurred.',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            } )
