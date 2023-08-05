# DND Markdown

## Install

Install using the `requirements.txt` file.

```
$ pip install -r requirements.txt
```

## Use

### Convert all files

```
$ python -m dmd convert-all /path/to/md/ /path/to/html/
```

### Convert single file

```
$ python -m dmd convert /path/to/md/file.md -o /path/to/html/file.html
```

### Watch for changes

```
$ python -m dmd watch /path/to/md/ /path/to/html/
```

## Syntax

In addition to [gmbinder.com](https://gmbinder.com/) syntax, includes the following:

- `[somename]:<>` &mdash; Inserts and empty anchor with name "somename" (`<a name="somename"></a>`)
