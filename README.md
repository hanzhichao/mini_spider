# mini_spider
>Release Date: 2018/1/13  Vision: 0.1

> Part test in Win10 + Python2.7.12 With PyCharm2017

## Project Structure


* conf -- default config file dir
* doc -- tasks and reference documents
* log -- default log dir
* output -- default output dir
* seed -- urls file dir
* test -- test case dir

* mini_spider.py -- main program,
* config_load.py -- load config file
* crawl_thread.py -- multiple threads crawl
* log.py -- log config
* option_parser -- add options for main program: -h/--help, -c/--conf, -v/--version
* seedfile_load.py -- read urls from seed file
* spider.conf -- config file
* webpage_parser.py -- retrieve urls from one url and save pages


## How to Use?

1. copy this project to your slave(Linux or Windows,python env needed)
2. modify the 'spider.conf'
3. cd to the project directory in shell or cmd and run
```
python mini_spider -c spider.conf
```