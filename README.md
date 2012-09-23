wordyclock-plasmoid
===================

WordyClock plasmoid for KDE4.

![wordyclock-plasmoid screenshot. English](https://github.com/bielfrontera/wordyclock-plasmoid/blob/master/Screenshots/wordyclock-screenshot-en.png)\

![wordyclock-plasmoid screenshot. Catalan](https://github.com/bielfrontera/wordyclock-plasmoid/blob/master/Screenshots/wordyclock-screenshot-ca.png)\

![wordyclock-plasmoid screenshot. Spanish](https://github.com/bielfrontera/wordyclock-plasmoid/blob/master/Screenshots/wordyclock-screenshot-es.png)\


Credits
-------

This plasmoid is based on previous work of Ken Lin. I've adapted his [pyWordyClock](http://kenlim.github.com/pyWordyClock/) to use as a plasmoid and to be multilingual.

This is my first plasmoid, so I've also used [KDE TechBase Tutorial](http://techbase.kde.org/Development/Tutorials/Plasma/Python/GettingStarted) and some code of other plasmoids as [gmail-plasmoid](http://code.google.com/p/gmail-plasmoid)


Install this plasmoid in your kde desktop
-----------------------------------------
 
Download WordyClock-plasmoid source:

    $ git clone https://github.com/bielfrontera/wordyclock-plasmoid

Zip the content:

    $ cd wordyclock_plasmoid/ &&  zip -r ../wordyclock_plasmoid.zip . && cd ..

Install the plasmoid;

    $ plasmapkg -i wordyclock_plasmoid.zip

You can also rename wordyclock_plasmoid.zip to wordyclok.plasmoid, and add it from 'Add widgets dialog'. 

You can test the plasmoid from command line:

    $ plasmoidviewer wordyclock_plasmoid

