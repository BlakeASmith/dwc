# Distributed `wc`

A distributed version of the `wc` unix utility, built using [dask](https://dask.org/).

:warning: This project was written with the goal of learning how to use *dask*.
For most use cases, it is better to simply use the built in `wc` utility, or even to 
paralellize it using [GNU parallel](https://www.gnu.org/software/parallel/) or similar.

## Installation

```shell script
git clone https://github.com/BlakeASmith/dwc
cd dwc
pip install .
```

## Usage

The `dwc` command line client supports a similar interface as unix `wc`.

```shell script
Usage: dwc [OPTIONS] FILE...

  A distributed version of the unix wc utility.

  Print newline, word, and byte counts for each FILE, and a total if multiple
  files are specified.

  If no file is given, standard input will be used.

Options:
  -a, --address TEXT  Address of a dask scheduler. A multiprocess scheduler is
                      used by default.
  -l, --lines         Print the line counts.
  -c, --bytes         Print the byte counts.
  -w, --words         Print the word counts.
  --help              Show this message and exit.
```

## Docker Compose

A distributed environment can be simulated using docker-compose.

```shell script
docker-compose up --scale dask_worker=10
```

This will start a single dask scheduler along with 10 workers. The scheduler is bound to `localhost:8786`


Note that a shared filesystem is required between the workers. This could be accomplished using a
distribued file system like [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html), but for
this a docker volume is used. 

Once the dask scheduler and workers are up, we can run a wordcount using the `dwc` command.

```shell script
dwc -a localhost:8786 data/lorem*.txt
```

Resulting in:

```shell script
 3763   216630   1456958  data/lorem1.txt
 3763   216630   1456958  data/lorem2.txt
 3763   216630   1456958  data/lorem3.txt
 3763   216630   1456958  data/lorem4.txt
 3763   216630   1456958  data/lorem5.txt
 3763   216630   1456958  data/lorem6.txt
 3763   216630   1456958  data/lorem.txt
 3763   216630   1456958  data/loremw.txt
30104  1733040  11655664  total
```

## Similar Work

Dask has an example project which counts words in *HDFS* which can be found [here](https://distributed.dask.org/en/latest/examples/word-count.html)