# DND Markdown

## Install

Install using the Pipfile.

```
$ pipenv install
```

## Use

### Convert all files

```
$ pipenv run dndmd convert-all /path/to/md/ /path/to/html/
```

### Convert single file

```
$ pipenv run dndmd convert /path/to/md/file.md -o /path/to/html/file.html
```

### Watch for changes

```
$ pipenv run dndmd watch /path/to/md/ /path/to/html/
```

## Syntax

In addition to [gmbinder.com](https://gmbinder.com/) syntax, includes the following:

- `[somename]:<>` &mdash; Inserts and empty anchor with name "somename" (`<a name="somename"></a>`)
- `~~Some text~~` &mdash; Strikethrough (`<del>Some text</del>`)
