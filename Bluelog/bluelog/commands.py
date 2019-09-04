# -*- coding: utf-8 -*-
import click

from bluelog import db
from bluelog.models import Admin, Category


def register_init_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login')
    @click.password_option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                           help='The password user to login.')
    def init(username, password):
        """Building Bluelog,just for you"""
        click.echo('Creating the temporary administrator account...')
        db.create_all()
        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists,updating...')
            admin.username = username
            admin.password = password
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(username=username,
                          blog_title='Bluelog',
                          blog_sub_title='No, Im the real thing.',
                          name='Admin',
                          about='Anything about you.',
                          password=password,
                          confirmed=1
                          )

            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories')
    @click.option('--post', default=50, help='Quantity of Posts')
    @click.option('--comment', default=500, help='Quantity of comments')
    def forge(category, post, comment):
        """Generates the fake categories,posts and comments"""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
        db.drop_all()
        db.create_all()
        click.echo('Generating The administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts' % post)
        fake_posts(post)

        click.echo('Generating %d comments' % comment)
        fake_comments(comment)

        click.echo('Done')

    @app.cli.command()
    def test():
        """Run the unit tests."""
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
