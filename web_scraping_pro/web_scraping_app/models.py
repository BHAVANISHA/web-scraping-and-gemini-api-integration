from django.db import models

class web_scrap( models.Model ):

    user_email = models.EmailField()
    website = models.URLField( max_length=500 )
    query = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True )
