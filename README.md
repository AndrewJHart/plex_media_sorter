Python 3 version coming
=======================
Haven't had much time to really work on side projects, however I plan on doing quite a bit with this little script. I'll
be releasing a python 3.7 version soon and removing some unused bits as well as adding some goodies that could really be useful. Check back :)


Origin
==========

The idea for this script originated from the need to elegantly organize the different types of media that I download & then
ensure that they were moved into the correct folders so that plex media server would know whether the media was a movie, tv show, or somethign else. 

If you haven't heard of [plex](http://plex.tv) then I suggest you check it out because its amazing (like having your own personal netflix for your media). Plex will automatically scrape all the media content, for example the synopsis, and give you a beautiful UI for navigating that content. **However its one requirement** is that a tv show must go into the folders linked to the tv show libraries & movies must belong in the folder libraries configured for movies. If they are all thrown together in one folder plex will not be able to discern whats a show vs movie. 

Video Sort
===========

Video sort is a simple script that is to be executed after the media download has completed. For example, I use transmission to download all of my media, which has an option to run a script after a file has completed downloaded. This is where `video_sort.py` comes into play.

> you may need to name the file video_sort.command and make it executable. There should be one in one of the other branches if
> you want to just download it. 

Once a torrent has completed & the script is invoked it will (and very successfully i might add) determine the type of the various file(s) and then begin to sort that media by its type (episode, movie, subtitle, etc..), finally moving the media to specified folders that are set in the configuration. 

> This library makes heavy use of the python `guessit` library, which is
> an amazingly effective tool for extracting metadata from a media file or filename. Guessit can be found [here](https://github.com/guessit-io/guessit)

Installation
============

I Recommend creating a virtual environment using `virtualenv` (named venv) & installing the packages within like so:

```bash
$ virtualenv venv --no-site-packages
```

Then activate the virtual environment:

```bash
$ . venv/bin/activate
```

Install the pip packages:

```bash
$ pip install -r requirements.txt
```

Use
===

For now, because of a lack of `settings.py` configuration script, you will need to manually adjust the paths to suit your own machine. I configure transmission to download everything to a `tmp` folder & then configure a tuple of glob paths for `video_sort` to look within for finding media.

If you want to run the script manually then you can run it directly just like any python script:

```bash
$ python video_sort.py
```

The file has been modified to be executable but in case you need to do this
manually simply run:

```bash
chmod +x video_sort.py
```

Then you u can configure transmission to auto-run the python utility upon completion. 

It can also be ran direclty like so after be set as executable: 

```bash
./video_sort.py
```

Todo
===========

- A configuration file to replace the hardcoded defaults at the top of script.
- add cleanup function to remove folders once media has been moved
- bash script that will build the python script, set as executable file, 
  and rename it - so that transmission (or any program) can invoke it.
- consider moving this into a class or more OOP pattern

Notes
=====

This is a very early version of this & i basically wrote this in a day & then tweaked it over the course of a couple weeks. I can confidently say though that it works very very well at determining the types & organizing the media into the proper libraries so that
plex can recognize them.

More documentation is forthcoming & i'm very open to ideas to improve this script. 
