from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_n5zj8s'
    )

# Inside our Profile model, I’m going to  create a Meta class that will return
# our Profile instances in reverse order,  so the most recently created is
# first. This bit relates  to this field name. And the minus sign at
# the beginning of the string, indicates  that we want our results in reverse.
# And in the dunder string method, I’ll return  information about who the
# profile owner is.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


# "... So, I’ll import post_save at  the top from Django’s signals.
# Now I’ll listen for the post_save signal coming  from the User model by
# calling the connect function. Inside, I’ll pass ‘create_profile’, which
# is the function I’d like to run every time and specify User as the
# model we’re expecting to receive the signal from. Now we have to define
# the create_profile function  before we pass it as an argument. Because
# we are passing this function to the post_save.connect  method, it
# requires the following arguments: the sender model, its instance,
# created  - which is a boolean value of whether or not the instance has
# just been created, and  kwargs. Inside the create_profile function,
# if created is True, we’ll create a profile  whose owner is going to
# be that user. Great, now every time a user is created, a signal will
# trigger the Profile model to be created."

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
