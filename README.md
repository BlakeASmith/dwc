# Distributed `wc`

A distributed version of the `wc` unix utility.

## Usage

The `dwc` command line client supports the same interface as unix `wc`.

:warning: Only the `-w` option is supported at this time.

```shell script
Usage: dwc [OPTIONS] FILE...

  A distributed version of the unix wc utility.

  Print newline, word, and byte counts for each FILE, and a total if multiple
  files are specified.

  If no file is given, standard input will be used.

Options:
  -w, --words  Print the word counts.
  --help       Show this message and exit.
```
