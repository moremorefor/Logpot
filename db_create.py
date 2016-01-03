#-*- coding: utf-8 -*-

from logpot.auth.models import User
from logpot.entry.models import Entry, Category, Tag
from logpot.app import app
from logpot.ext import db
from logpot.admin.entry import renderMarkdown
import os
import shutil


def init_db():
    db.create_all()


def drop_all(app):
    db.drop_all()
    upload_dir = app.config['UPLOAD_DIRECTORY']
    log_dir = app.config['LOG_DIRECTORY']
    basedir = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(basedir, 'logpot', 'config.yml')
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    if os.path.exists(config_file):
        os.remove(config_file)


def init_admin_user(name, email, password):
    password = User.generate_password_hash(password)
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    db.session.remove()


def init_category():
    c = Category(name='Python')
    db.session.add(c)
    db.session.commit()
    db.session.remove()


def init_tag():
    t = Tag(name='Flask')
    db.session.add(t)
    db.session.commit()
    db.session.remove()


def init_entry():
    u = User.query.get(1)
    c = Category.query.get(1)
    t = Tag.query.get(1)
    s = 'example'
    md_body = (
        example_markdown()
    )

    body = renderMarkdown(s, md_body)

    entries01 = Entry(
        title=u'Example article',
        summary=u'Curabitur blandit tempus porttitor. Maecenas sed diam eget risus varius blandit sit amet non magna.',
        md_body=md_body,
        body=body,
        slug=s,
        category_id=c.id,
        user_id=u.id,
        is_published=True)
    entries01.tags.append(t)
    db.session.add(entries01)
    db.session.commit()
    db.session.remove()


def example_markdown():
    return """
# Headline
Curabitur blandit tempus porttitor. Maecenas sed diam eget risus varius blandit sit amet non magna. Donec sed odio dui. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas sed diam eget risus varius blandit sit amet non magna. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.

## Headline2
Cras justo odio, dapibus ac facilisis in, egestas eget quam. Etiam porta sem malesuada magna mollis euismod. Maecenas faucibus mollis interdum. Vestibulum id ligula porta felis euismod semper.

### Headline3
Etiam porta sem malesuada magna mollis euismod. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Maecenas faucibus mollis interdum. Nullam quis risus eget urna mollis ornare vel eu leo.

#### Headline4
Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Integer posuere erat a ante venenatis dapibus posuere velit aliquet.

##### Headline5
Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.

###### Headline6
Maecenas sed diam eget risus varius blandit sit amet non magna. Etiam porta sem malesuada magna mollis euismod.

### Another Elements
Leave 2 spaces at the end of a line to do a
line break.

Text attributes *italic*, **bold**,`monospace`, <del>strikethrough</del>.

Unordered list:

- Red
- Green
- Blue

Numbered list:

1. apples
1. oranges
1. pears

Definition list:

<dl>
<dt>Coffee</dt><dd>Black hot drink</dd>
<dt>Milk</dt><dd>White cold drink</dd>
</dl>

```python
def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
fib(1000)
```

<!-- dummy comment line for breaking list -->

> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
>
> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
> id sem consectetuer libero luctus adipiscing.

[Wikipedia](https://www.wikipedia.org/ "Link Title")

[Google][a]

[Yahoo][1]


* * *

horizontal rule

***

horizontal rule

*****

horizontal rule

- - -

horizontal rule

---------------------------------------

[a]: http://google.co.jp "Link Title"

[1]: http://www.yahoo.co.jp "Link Title"
"""
