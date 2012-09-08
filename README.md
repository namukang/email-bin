# Email Bin

Because collecting emails should be easy.

## What is it?

A simple dump for your email signups.

## I'm a programmer. Talk nerdy to me.

It's a simple Flask application using Gevent that persists signups in a
MongoDB database. It's meant to be hosted on Heroku with the MongoLab
add-on.

## How do I use it?

1. `git clone https://github.com/dskang/email-bin.git`
2. `heroku create`
3. `heroku addons:add mongolab:starter`
4. `git push heroku master`
5. Once you have the server working, you can simply create a form with a
   text field and submit button anywhere* and set the 'action' attribute
   to HEROKU-APP-URL/signup. Look inside the example directory for help.

*Email Bin allows cross domain requests, so Email Bin does not need to
reside on the same domain as your actual site. This means that
XMLHttpRequests can be invoked from any domain; if you would like to
restrict the domains that are allowed to do this, change the
`ALLOWED_DOMAINS` to the URL of the site containing your form.

## I want to develop locally.

1. `pip install -r requirements.txt`
   If you have issues installing gevent, run `brew install libevent`.
2. Run `heroku config | grep MONGOLAB_URI` and copy the MONGOLAB_URI
   into a new file named .env, using sample.env as a guide.
3. `foreman start`

