Origin
==========

The idea for this script originated from the need to elegantly organize the different types of media that I download & then
ensure that they were moved into the correct folders so that plex media server would know whether the media was a movie, tv show, or somethign else. 

If you haven't heard of [plex](http://plex.tv) then I suggest you check it out because its amazing (like having your own personal netflix for your media). Plex will automatically scrape all the media content, for example the synopsis, and give you a beautiful UI for navigating that content. **However its one requirement** is that a tv show must go into the folders linked to the tv show libraries & movies must belong in the folder libraries configured for movies. If they are all thrown together in one folder plex will not be able to discern whats a show vs movie. 

Video Sort
===========

Video sort is a simple script that is to be executed after the media download has completed. For example, I use transmission which has an option to run a script after a file has completed downloaded. This is where `video_sort.command` comes into play. Once a torrent has completed & the script is invoked it will (and very successfully i might add) determine the type of the various file(s) and then begin to sort that media by its type (episode, movie, subtitle, etc..), finally moving the media to specified folders that are set in the configuration. 


Notes
=====

This is a very early version of this & i basically wrote this in a day & then tweaked it over the course of a couple weeks. I can confidently say though that it works very very well at determining the types & organizing the media into the proper libraries so that
plex can recognize them.

More documentation is forthcoming & i'm very open to ideas to improve this script. 
