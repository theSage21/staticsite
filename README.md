# StaticSite

Super simple static site builder.

1. Create a folder called `src`.
2. Put your Jinja templates there.
3. Run `python -m staticsite build --src src --target www`
4. Static site has been built and provided in `www` folder.
5. Create a `staticsite.yaml` file to specify variables and plugins.

``` bash
$ mkdir src
$ cat << EOF >> src/.base.html
> <!doctype html>
> <html lang='en'>
>   <body>
>       <h1>Example</h1>
>     {% block content %}{% endblock %}
>   </body>
> </html>
> EOF
$ cat << EOF >> src/index.html
> {% extends '.base.html' %}
> {% block content %}
> Hi
> {% endblock %}
> EOF
$ python -m staticsite build --target docs
$ tree
.
├── src
│   ├── .base.html  # Files starting with . are ignored
│   └── index.html
│
└── docs
    ├── index.html
```

[Documentation](https://thesage21.github.io/staticsite/)
