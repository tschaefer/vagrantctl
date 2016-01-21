# vagrantctl
vagrantctl - Control the Vagrant virtual machines

## Introduction
**vagrantctl** is a simple script to list, start and stop Vagrant managed virtual
machines in a given subfolder.

## Usage
```
$ vagrantctl -h
usage: vagrantctl [-h] [-b BASE_DIRECTORY] {list,up,halt,status} ...

vagrantctl

positional arguments:
  {list,up,halt,status}

  optional arguments:
    -h, --help            show this help message and exit
    -b BASE_DIRECTORY, --base-directory BASE_DIRECTORY
                          vm base directory
```

The base-directory can also be configured with in a configuration file
*.vagrantctl* located in the user home directory.
```
[vagrantctl]
base-directory=/Users/tschaefer/.vagrant.d/container
```

## License

[BSD 3-clause](http://choosealicense.com/licenses/bsd-3-clause/)

## Is it any good?

[Yes](https://news.ycombinator.com/item?id=3067434)
