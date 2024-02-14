# Create a file filters.py in your Django app
# app_name/filters.py
from django import template
from django.contrib.auth.models import User
import re
from webpush import send_user_notification  

register = template.Library()


@register.filter
def mention_bold(value):
    # Extract words with '@' using regular expression
    mentioned_users = re.findall(r'@(\w+)', value)

    # Wrap mentioned users in <strong> tags
    for user in mentioned_users:
        try:
            User.objects.get(username=user)
            value = value.replace(f'@{user}', f'<strong style="color:#000; background-color:gainsboro; padding:2px 3px; border-radius:3px;">@{user}</strong>')
        except User.DoesNotExist:
            pass  # Do nothing if the user does not exist
    return value


# payload = {"head": "Clipping!", "body": "User Clipped Successfully"}
# send_user_notification(user=user, payload=payload, ttl=1000)