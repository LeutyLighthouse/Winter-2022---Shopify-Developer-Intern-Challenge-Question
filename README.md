# Image Repository for Shopify
### Winter 2022 - Shopify Developer Intern Challenge Question
### Made by Ross Robertson

This is a simple web app made with Flask that lets the user post images
to an image repository as listings that can be seen through the web app.
The user can make their listings private so that only
they can see them if they wish. Users can also see all of the public images
that are publicly available in the repo and if they choose they can decide
to remove all of their images all at once. 

## Dependencies
- python3
- python3-pip
- flask
- pytest
- flask-sqlalchemy
- flask-login
- werkzeug

The dependencies can be installed by simply typing:
`pip install <dependency name>`
for example:
`pip install flask-login`

## Installation & Usage

For this app you will just need to have the dependencies above and python3
on your machine. Once you have those, you only need to run:
`python3 server.py`
and the app will begin running!

This will create a database file, if it doesn't already exist, and start running
the server for the web app which can be accessed at "localhost:5000" in your
web browser.

Once you can see the app in your browser it will present you with a login screen.
You can then click the link above to register, and once registered and logged in
you will have access to the repository! Here you can add new images, which will require a
name, contact info, and a price (the description is optional). The contact info is
simply text so that it can be whatever you want it to be. You can also
choose here whether or not you want your image to be private. If it's set as private
then other users won't be able to see or delete your image. For any images that you
can see on the home page, you can choose to delete them if you wish by clicking the
remove button on the right side of the listing. If you want to remove all of your
images at once simply click the "Erase My Images" link. If you want to change
to another user simply click the "Log Out" link and the web app will automatically
take you to the login page afterward.

If you would like to run the tests you only need to run:
`python3 -m pytest`

## Potential Future Features

We could add the capability for a search function in this web application, such that
a search bar is at the top of the home page that allows us to search via filenames
or by the name given to the listing. We could also train a convolutional neural network
to recognize similar images so that we could have the user upload an image to search by
similarity.

Another feature that we could implement is to keep track of the transactions on the web
app and provide a UI that makes the user experience smoother in that regard. We would
simply need to add a table to our database that keeps track of the transactions that
occur on the web app and add more functionality to the UI that would allow for tracking
agreed payments or to implement payment processing in the web application. We may also
want to add an element to our listings table that keeps track of how many of items are
left so that if the item runs low then we can notify the user of this.