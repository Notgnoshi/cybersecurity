# cybersecurity
Graduate coursework for CSC792, Cybersecurity

# Converting Jupyter Notebooks to Microsoft Word Documents

This is fairly straightforward after I figured it out, but *does* require some tweaking.

```shell
jupyter-nbconvert --to markdown notebook.ipynb
pandoc notebook.md notebook.docx
```

Then tweak the "Source Text" style. I tried adding a border with a shadow and padding, which looked
pretty good. The next thing was to add a new line between each of the code cells and their output
cells formatted as normal body text. Otherwise the code cell and output are indistinguishable.

The pandoc styles can be tweaked by creating a reference document with

```shell
pandoc --print-default-data-file reference.docx > custom-reference.docx
```
editing it to fit your needs, and using it with the `--reference-doc=<ref>` flag when converting the
markdown document to `.docx`.

Unfortunately, the "Source Text" style is not listed in the reference document, so I'm currently
unsure if that's something I can edit or not. The manpage for `pandoc` states that I probably
shouldn't modify the contents of the generated reference document other than its styles. I'll have
to play with this.
