=================
Django Changelog
=================

Django Changelog is a simple Django app to display a CHANGELOG.md file as a url


Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_changelog',
    ]

2. Include the polls URLconf in your project urls.py like this::
    from changelog.views import ChangelogView
    ...
    path("changelog/", ChangelogView.as_view()),

3. Create a CHANGELOG.md in your BASE_DIR.

4. Start the development server

5. Visit http://127.0.0.1:8000/changelog/ to see your changelog.