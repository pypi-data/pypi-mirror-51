![Python](https://img.shields.io/badge/python-3.7.2-green.svg)
![Version](https://img.shields.io/badge/version-0.1.1-yellow.svg)

# Todo1

Commandline `todo` application for internship assignment.

## Requirements

This project requires `Python 3.7.2` or newer run-time.

## Install


```sh
$ cd $home  
$ git clone  https://github.com/FatmanurEraslan/Todo1.git
$ cd Todo1
$ python 3 setup.py install
```

or

```sh

$ pip install FNEtodo  

```



## License

This project is licensed under MIT

## Usage
```sh

$ todo add 'Buy a ticket'

```

   Buy a ticket is added .

   0001 : Buy a ticket

```sh

$  todo add 'Clean the house'

```

  Clean the house is added .

  0001 : Buy a ticket
  0002 : Clean the house


```sh

$  todo complete 1

```

  Buy a ticket is completed!

  0001 : Clean the house


```sh

$  todo list

```
  0001 : Clean the house


```sh

$  todo completed

```

  0001 : Buy a ticket


```sh

$  todo add 'Visit grandpa' 'Go to shopping mall'

```
  Visit grandpa is added .

  Go to shopping mall is added .

  0001 : Clean the house
  0002 : Visit grandpa
  0003 : Go to shopping mall

## Contributer(s)

- [Fatmanur Eraslan](https://github.com/FatmanurEraslan) - Creator, maintainer
- [Uğur "vigo" Özyılmazel](https://github.com/vigo) - Mentor

## Contribute

All PR’s are welcome!

1. `fork` (https://github.com/FatmanurEraslan/Todo1/fork)
1. Create your `branch` (`git checkout -b my-features`)
1. `commit` yours (`git commit -am 'added killer options'`)
1. `push` your `branch` (`git push origin my-features`)
1. Than create a new **Pull Request**!

## Change Log

**2019-09-03**

- Removed irrelevant files
- Added `.gitignore`
- Updated `README.md`

**2019-08-28**

- Initial start
