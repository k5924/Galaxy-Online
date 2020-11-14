from django import forms
# imports form method
from django.contrib.auth.models import User
# imports user table from database
from django.contrib.auth.forms import UserCreationForm
# imports UserCreationForm to use when users sign up
from .models import YearGroup, Interests, PostCode, Town, Posts, Comment
# imports database tables from models.py


class RegisterForm(UserCreationForm):
    # creates registration form
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # creates email field with placeholder of email
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    # creates first_name field as a character field with placeholder of Firstname
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    # creates last_namefield as a character field with placeholder Lastname
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    # creates username as character field with placeholder as username

    class Meta():
        model = User
        # connects to User table in database
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name']
        # calls these fields to use in forms. Im not customising the password inputs so calling the fields is sufficient

    def clean(self):
        # creates method to clean data
        cleaned_data = super().clean()
        # stores cleaned data as a variable
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")
        # gets cleaned data in form to use for validation
        with open("Galaxy-Online/Home/banned words.txt") as file:
            # opens banned words text file as file
            lines = [line.strip() for line in file]
            # appends banned words to a list
        for word in lines:
            # for word in lines list
            if (word in email):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            elif (word in first_name):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            elif (word in last_name):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            elif (word in username):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
                # raise a validation error if the word is any of the recieved inputs
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email is already assigned to a user")
            # raise a validation error is the email is already assigned to a user
        elif "@hfed.net" not in email:
            raise forms.ValidationError("This web app only allows hfed users")
            # raise a validation error if the user doenst have @hfed.net in their eail
        elif (any(char.isdigit() for char in first_name)) == True:
            raise forms.ValidationError("Remove the number from your first name")
            # raise a validation error if the firstname has a number in it
        elif (any(char.isdigit() for char in last_name)) == True:
            raise forms.ValidationError("Remove the number from your last name")
            # raise a validation error if the last name has a number in it
        return cleaned_data
        # return the cleaned data


class YearGroupForm(forms.ModelForm):
    # creates year group form
    options = [(year, year) for year in range(7, 14)]
    # stores options to select for yeargroup
    year = forms.ChoiceField(label="Year Group", choices=options)
    # creates dropdown field with label for yeargroup with the specified choices

    class Meta():
        model = YearGroup
        # connects to YearGroup table in database
        fields = ('year',)
        # accessed field is year

    def clean(self):
        # defines clean method to clean data
        cleaned_data = super().clean()
        # stores cleaned data as a variable
        year = cleaned_data.get("year")
        # gets cleaned data from form
        YearGroup.objects.get_or_create(year=year)
        # gets or creates the object in the YearGroup table
        return cleaned_data
        # returns the cleaned data


class InterestsForm(forms.ModelForm):
    # creates interests form
    choice = (("Music", "Music"), ("Reading", "Reading"), ("Tv or Movies", "Tv or Movies"), ("Video Games", "Video Games"), ("Art", "Art"),)
    # stores choices for interests
    interest = forms.ChoiceField(choices=choice, label="Interest")
    # creates dropdown for interests with label as interest

    class Meta():
        model = Interests
        # connects to interests table in database
        fields = ("interest",)
        # accessed field is interest

    def clean(self):
        # creates clean method to clean data
        cleaned_data = super().clean()
        # stores cleaned data as a varaiable
        interest = cleaned_data.get("interest")
        # get cleaned data from form
        Interests.objects.get_or_create(interest=interest)
        # get or create object in interest table
        return cleaned_data
        # returns cleaned data


class PostCodeForm(forms.ModelForm):
    # creates postcode form
    postcode = forms.CharField(max_length=7, min_length=6, label="Postcode")
    # postcode is a character field with length between 6 and 7 characters and has the label postcode

    class Meta():
        model = PostCode
        # connects to the PostCode table in the database
        fields = ('postcode',)
        # accessed field is postcode

    def clean(self):
        # creates clean method to clean data
        cleaned_data = super().clean()
        # store cleaned data as variable
        postcode = cleaned_data.get("postcode")
        # get cleaned data from form
        with open("Galaxy-Online/Home/banned words.txt") as file:
            # open banned words as a text file
            lines = [line.strip() for line in file]
            # store words in text file as a list
        for word in lines:
            # for each word in the banned words list
            if (word in postcode):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )  # raise a validation error is the word is in the field
        PostCode.objects.get_or_create(postcode=postcode.upper())
        # get or create object in PostCode table
        return cleaned_data
        # return cleaned data


class TownForm(forms.ModelForm):
    # creates town form
    town = forms.CharField(label="Town")
    # town is a character field with label town

    class Meta():
        model = Town
        # connects to Town table in database
        fields = ('town',)
        # accessed field is Town

    def clean(self):
        # creates clean method to clean data
        cleaned_data = super().clean()
        # stores cleaned data in a variable
        town = cleaned_data.get("town")
        # get cleaned data from form
        with open("Galaxy-Online/Home/banned words.txt") as file:
            # open banned words as a text file
            lines = [line.strip() for line in file]
            # store banned words in a list
        for word in lines:
            # for each word in the list
            if (word in town):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )  # raise a validation error if a banned word is in the field
        Town.objects.get_or_create(town=town.lower())
        # get or create an object in the Town table
        return cleaned_data
        # return cleaned data


class PostsForm(forms.ModelForm):
    # creates posts form

    class Meta():
        model = Posts
        # connects to Posts table in database
        fields = ('title', 'content', 'image',)
        # accessed fields are title, content and image
        # title and content are text fields, image is an image field

    def clean(self):
        # creates method to clean data
        cleaned_data = super().clean()
        # stores cleaned data as a variable
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        # gets cleaned data from form
        with open("Galaxy-Online/Home/banned words.txt") as file:
            # open banned words are a text file
            lines = [line.strip() for line in file]
            # store each word in list
        for word in lines:
            # each each word in list
            if (word in title):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            elif (word in content):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            # raise validation error if banned word is in one of the fields


class CommentForm(forms.ModelForm):
    # creates comment form

    class Meta:
        model = Comment
        # connects to comment table in database
        fields = ('content',)
        # field accessed is content

    def clean(self):
        # create method to clean data
        cleaned_data = super().clean()
        # store cleaned data in a variable
        content = cleaned_data.get("content")
        # get cleaned data from form
        with open("Galaxy-Online/Home/banned words.txt") as file:
            # opens banned words as a text file
            lines = [line.strip() for line in file]
            # appends words to text list
        for word in lines:
            # if word in list
            if (word in content):
                raise forms.ValidationError(
                    "Banned word was used. Please remove the word '{}' and try again".format(word)
                )
            # raise validation error that banned word is in field