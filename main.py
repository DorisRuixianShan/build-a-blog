#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class FrontPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, LC101 Members!")

class Post (db.Model):
    title=db.StringProperty(required=True)
    post=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class NewPost(webapp2.RequestHandler):
    def get(self):
        t=jinja_env.get_template("newpost.html")
        title=self.request.get("title")
        post=self.request.get("post")
        error = self.request.get("error")

        content = t.render(title=title,post=post,error=error)
        self.response.write(content)

    def post(self):
        title=self.request.get("title")
        post=self.request.get("post")

        if title and post:
            a=Post(title=title, post=post)
            a.put()
            self.redirect("/blog")
            self.response.write("it workds")
        else:
            error="We need both a title and a body!"
            self.response.write(title, post, error=error)


class MainPage(webapp2.RequestHandler):
    def get(self):
        posts=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t=jinja_env.get_template("mainpage.html")
        content=t.render(posts=posts)
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/',FrontPage),
    ('/blog', MainPage),
    ('/blog/newpost', NewPost)
], debug=True)
