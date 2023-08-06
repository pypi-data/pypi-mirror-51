<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-github-colors.svg?longCache=True)](https://pypi.org/project/django-github-colors/)

#### Installation
```bash
$ [sudo] pip install django-github-colors
```

#### `settings.py`
```python
INSTALLED_APPS+ = [
    "django_github_colors",
]
```

#### Examples
```html
{% load github_colors %}

{% github_colors repo.language %}
```

```html
<span class="repo-language-color ml-0" style="background-color:{% github_colors repo.language %}"></span>
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>