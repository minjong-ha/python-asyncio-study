# Python-Asyncio-Study

"python-asyncio-study" is the repository for study in asyncio and rx.
It is important to design light and efficient application and asyncio with rx can support it.
This repository provides a good reference for python: shih-tzu.


# Main Libraries

Followings are main libraries for implementing reactive, asynchrounous application.

## Asyncio

"asyncio" library supports concurrent code execution with async/awaiy syntax.
It can be used in asynchronous frameworks such as network, web-servers, database, distributed task queues and etc.
There are high-level API and low-level API for developers.

[asyncio - Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)

## RX (Reactive X)

"rx" libray is for composing asynchronous and event based programming.
With "rx", developers can handle asynchronous data streams with __observables__.

[ReactiveX - RxPY](https://github.com/ReactiveX/RxPY)

## pytest

"pytest" provides the library for unit test.

# Shih-Tzu: Sample application

For better understanding, this repository provides "Shih-Tzu" application that working like a puppy.
You can create a Shih-Tzu object, execute command for it, and handle state changes for it.
It will run with asyncio and RxPY.

# How to run?

Execute the script "run"

```
./run
```

### Thanks to

Poppi, Toto, Tori.
