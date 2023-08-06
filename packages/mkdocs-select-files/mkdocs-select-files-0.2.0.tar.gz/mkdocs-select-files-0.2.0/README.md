# File filter plugin for mkdocs

`select-files` is a
[mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that filters out
files (pages) using a parametrized regular expression.

The main use case for this plugin is to prepare lectures or assignments
and only publishing them at a given date.

## Quick start

1. Install the module using pip: `pip3 install mkdocs-select-files`

2. In your project, add a plugin configuration to `mkdocs.yml`:

   ```yaml
   plugins:
     - select-files:
      select: '^s(\d+)'
      where: 'lambda x : int(x) <= 5'
      
   ```

  This would search for files named `sNN...` and select only those where `NN` is
  less than or equal to `5`.

## Credits

Thank you to [Lucy Linder](https://github.com/derlin) for her great idea of using parametrized regular expressions.

## Similar plugins

- [mkdocs-exclude](https://github.com/apenwarr/mkdocs-exclude) : exclude arbitrary file paths and patterns from the input