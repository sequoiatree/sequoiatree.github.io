# Sequoia Tree

The official personal website for Sequoia Eyzaguirre, student researcher and instructor at UC Berkeley.

## Setting up

To contribute to this repository, first clone it as you would any `git` repository. Then set up a virtual environment and install the requirements.

```bash
git clone https://github.com/sequoia-tree/sequoia-tree.github.io.git
cd sequoia-tree.github.io
virtualenv -p python3 webenv
pip install -r requirements.txt
```

If you tend to make a lot of virtual environments, I recommend aliasing a `mkenv` command to speed up the process. Here's how to do it on a Mac:

```bash
cd ~
open .bash_profile
```

Then add the line `mkenv() { virtualenv -p python3 $1; }`. In the future, you'll be able to set up your virtual environment for this project by simply executing `mkenv webenv`.

## Making edits

After you're all set up, you can make changes to your local clone of the repository.

### Writing chapters and practice sections

In your editor of choice, you can write chapters and their corresponding practice sections in markdown. Chapters should be named 'Chapter.md' and practice sections should be named 'Practice.md'. These should go in a directory corresponding the appropriate textbook and topic, such as `src/textbooks/techniques-in-computer-science/variables`.

If you're publishing a brand new chapter, you should also add the name of the topic directory to the file called `published.py` in the textbook directory.

If you're editing a chapter or practice section that has already been published before, remember to delete the corresponding HTML file, called something like `variables.html` or `variables-practice.html`. Next time you run the app, it will automatically create a new version to replace it.

### Including assets and images

To include an HTML or SVG asset, use the macro `ASSET example`. See below for more details.

To include an image, use  the macro `IMG-PNG example` for `.png` images, `IMG-JPEG example` for `.jpeg` images, and so on.

### Including pyagrams

To include pyagrams, you can use the following syntax.

```
STARTPYAGRAM example

This is the caption for the first frame.

---

This is the caption for the second frame.

---

This is the caption for the third frame.

ENDPYAGRAM
```

Note that in the example above you would also have to include a file containing the corresponding frames of the pyagram (one frame per caption), stored as SVGs separated by linebreaks, in the respective `assets` folder. It would have to be named `example.svg`.

Also take note of the script `src/compile.py`. Use it as such to convert SVGs named `1.svg`, `2.svg`, `3.svg`, etc. into a single properly formatted SVG:

```
$ python3 compile.py example
```

Assuming your constituent SVGs are in the same directory as the script, it will convert them into a single properly formatted SVG named `example.svg`. It will stitch them together in reverse order, so in this example `3.svg` should represent the first frame of the pyagram, `2.svg` should represent the second frame of the pyagram, and `1.svg` should represent the third (and last) frame of the pyagram.

### Writing assets, utils, and macros

There are a few ways to change the way the app processes and renders content.

* To add assets to a chapter or practice section, navigate to the appropriate topic directory and create a new directory called `assets`. Within this directory, you can add HTML and SVG files. For instance, consider adding a file called `example.html` to `assets`. Then you could include the contents of `example.html` from within a chapter or practice section by writing `ASSET example`. Note that all assets must be HTML files or SVG files. In the case of SVG files that include SVGs separated by linebreaks, the asset will be stored as a tuple of SVGs.
* To add utils usable from within Jinja templating for chapters and practice sections, navigate to `src/textbook_utils.py`. Then add your desired utils to the `UTILS` dictionary in the `get_utils` function. This dictionary will be imported to `src/models.py` and later passed as `**kwargs` to Flask's `render_template` function in `src/views.py`. For example, consider the mapping `UTILS['h1'] = lambda text: text.upper()`. You could make use of this function from within a chapter or practice section by writing `{{ h1('header') }}`, which would render the text "HEADER" on the page.
* To add macros usable from within Jinja templating throughout the website, navigate to `src/templates/macros.py`. Specify your macros here, using the proper Jinja syntax. Then make use of your macro wherever you desire.

### Validating edits

If you want to see how your changes affect the website, navigate to the `src` directory from within your terminal and execute `python3 run.py`. Then, using a web browser, go to the URL `localhost:5000/`.

## Deploying edits

Github Pages can only host static content. To make sure your changes are actually reflected on [sequoia-tree.github.io](sequoia-tree.github.io), you need to freeze the dynamic Flask app. From within `src`, run `python3 freeze.py`. This will build the entire website's static content in the root directory. Then you can commit and push your changes to Github. Note that if you have added any files to the root directory not specified in the `SRC_FILES` set defined in `src/freeze.py`, then **those files will be deleted**.

## License

All content on this repository is protected under a [Creative Commons BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/).