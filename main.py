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

class Post (db.Model):
    title=db.StringProperty(required=True)
    post=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class FrontPage(webapp2.RequestHandler):
    def get(self):
        t=jinja_env.get_template("base.html")
        content=t.render()
        self.response.write(content)


class MainPage(webapp2.RequestHandler):
    def get(self):
        posts=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t=jinja_env.get_template("mainpage.html")
        content=t.render(posts=posts)
        self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):
    def render_form(self, title="", body="", error=""):
        t = jinja_env.get_template("newpost.html")
        content= t.render(title=title, body=body, error=error)
        self.response.write(content)

    def get(self):
        self.render_form()
    # def get(self):
    #     t=jinja_env.get_template("newpost.html")
    #     title=self.request.get("title")
    #     post=self.request.get("post")
    #     error = self.request.get("error")
    #
    #     content = t.render(title=title,post=post,error=error)
    #     self.response.write(content)

    def post(self):
        title=self.request.get("title")
        body=self.request.get("body")

        if title and post:
            a=Post(title=title, body=body)
            a.put()

            id = post.key().id()
            self.redirect("/blog/%s" % id)

        else:
            error = "we need both a title and a body!"
            self.render_form(title, body, error)

class ViewPostHandler(webapp2.RequestHandler):

    def get(self, id):
        """ Render a page with post determined by the id (via the URL/permalink) """

        post = Post.get_by_id(int(id))
        if post:
            t = jinja_env.get_template("post.html")
            content= t.render(post=post)
        else:
            error = "there is no post with id %s" % id
            t = jinja_env.get_template("404error.html")
            content= t.render(error=error)

        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/',FrontPage),
    ('/blog',MainPage),
    ('/blog/newpost',NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
