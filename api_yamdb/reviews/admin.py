from django.contrib import admin

from reviews.models import Title, User, Review, Comment

admin.site.register(Title)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
