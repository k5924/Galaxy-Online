from django.contrib.auth.models import User
# imports user table automatically generated by Django
from django.db import models
# imports models for me to use for my database tables
from django.db.models.signals import post_save
# imports post_save to be used after a record has been saved in a table
from django.dispatch import receiver
# can be used to connect signals after a record has been saved in a table
from django.urls import reverse
# can be used to reverse url arguements connected to a database table
# Create your models here.


class YearGroup(models.Model):
    # creates yeargroup table
    year = models.IntegerField(null=True)
    # sets year as a field in the table as an integer field which can be left blank

    def __str__(self):
        return str(self.year)
        # returns string value of field in table


class Interests(models.Model):
    # creates interest table in database
    choice = (("Music", "Music"), ("Reading", "Reading"), ("Tv or Movies", "Tv or Movies"), ("Video Games", "Video Games"), ("Art", "Art"),)
    # stores choices that can be made for interest
    interest = models.CharField(max_length=15, choices=choice)
    # sets interest as a character field with max length of 15 characters with choices specified

    def __str__(self):
        return self.interest
        # returns string value of field in table


class PostCode(models.Model):
    # creates postcode table in database
    postcode = models.CharField(max_length=7)
    # sets postcode as a character field with max length of 7 characters

    def __str__(self):
        return self.postcode
        # returns string value of field in table


class Town(models.Model):
    # creates town table in database
    town = models.CharField(max_length=40)
    # sets town as a character field with max length of 40 characters

    def __str__(self):
        return self.town
        # returns string value of field in table


class UserInformation(models.Model):
    # creates userinformation table in database
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # OneToOne relationship with user table
    year = models.ForeignKey(YearGroup, on_delete=models.PROTECT, null=True)
    # ManyToOne relationship with yeargroup table, value can be blank
    interest = models.ForeignKey(Interests, on_delete=models.PROTECT, null=True)
    # ManyToOne relationship with interests table, value can be blank
    postcode = models.ForeignKey(PostCode, on_delete=models.PROTECT, null=True)
    # ManyToOne relationship with postcode table, value can be blank
    town = models.ForeignKey(Town, on_delete=models.PROTECT, null=True)
    # ManyToOne relationship with town table, value can be blank

    class Meta():
        # specifies customisation to table
        verbose_name_plural = 'User Information'
        # gives a pluralised name to the database table in django admin

    def __str__(self):
        return self.user.username
        # returns string value of users username in table


@receiver(post_save, sender=User)
# when a user signs up to social network
def create_user_information(sender, instance, created, **kwargs):
    # takes parameters to create a user profile
    if created:
        # if a user is created
        UserInformation.objects.create(user=instance)
        # will create a user profile associated to that user


class Posts(models.Model):
    # create posts table in database
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ManyToOne relationship with user
    title = models.CharField(max_length=200)
    # title is a charfield with max length of 200 characters
    content = models.TextField()
    # content is a text field with no max length
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    # installed pillow to use image field
    # image is a image field which will upload an image to post_images
    # this field can be left blank
    publish = models.DateTimeField(auto_now_add=True, auto_now=False)
    # publish is a datetimefield that sets the time as soon as the post is saved to the database
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    # likes is a manytomany relationship with user that can be left blank

    class Meta():
        # specifies customisation to table
        verbose_name_plural = 'Posts'
        # gives pluralised name to the database table in django admin

    def __str__(self):
        return self.title
        # returns string value of field in table

    def get_absolute_url(self):
        return reverse('PostDetail', args=[str(self.id)])
        # returns string that can refer to post via http url

    def total_likes(self):
        return self.likes.count()
        # counts number of likes for each post


class Comment(models.Model):
    # create table in database
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    # ManyToOne field to Posts
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ManyToOne field to Users
    content = models.TextField(max_length=256)
    # content as text field with max length of 256 characters
    publish = models.DateTimeField(auto_now_add=True)
    # publish as a date time field storing the time a comment is made

    def __str__(self):
        return "{}-{}".format(self.post.title, str(self.user.username))
        # returns string value of the posts title and users username in table


class Friend(models.Model):
    # create friend table in database
    users = models.ManyToManyField(User)
    # manytomany relationship with user table
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)
    # ManyToOne relationship with user table as owner of friendship

    @classmethod
    def make_friend(cls, current_user, new_friend):
        # method to make friends
        friend, _created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        # get or create object with owner of friendship and created to add friend

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        # method to lose friend
        friend, _created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        # get or create object with owner of freinship and created to remove friend
