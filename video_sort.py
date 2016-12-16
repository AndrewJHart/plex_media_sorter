#!/usr/bin/python

# simple script that does its best to determine type
# video file being checked and moves it to the most
# appropriate folder e.g. movie => movies, tv => tv_shows
import os
import glob
import shutil
import json

# using guessit 1.x not 2
from guessit import guess_file_info

# import pync for osX notifications
from pync import Notifier

# import requests for elegant http requests to transmission rpc api
import requests as http_request

# transmission (t) rpc api
t_proto     = 'http'          # http protocol
t_host      = '127.0.0.1'     # localhost only
t_port      = '9091'          # t server port
t_path      = 'transmission'  # url path
t_session   = ''              # session key
t_endpoint  = 'rpc'           # resource endpoint

# transmission (t) ENV vars
t_tor_id = os.getenv('TR_TORRENT_ID')      # torrent id
t_tor_dir = os.getenv('TR_TORRENT_DIR')    # torrent directory
t_tor_hash = os.getenv('TR_TORRENT_HASH')  # torrent hash
t_tor_name = os.getenv('TR_TORRENT_NAME')  # torrent name

# build rpc api url at run time
t_api = '%s://%s:%s/%s/%s/' % (
    t_proto,
    t_host,
    t_port,
    t_path,
    t_endpoint
)

# initialize some global props for http sessions
session = http_request.Session()

# base & source paths
base_path = '/Users/michelle/'
source_path = os.path.join(base_path, 'tmp/')

# destination paths
movies_path = 'Movies/'
shows_path = 'TV Shows/'

# tuple of globs to handle various levels
# of nesting with downloaded files
paths = (
    '%s**/**/*' % source_path,
    '%s**/*' % source_path,
    '%s*' % source_path
)

# mask for allowed extensions
allowed_extensions = (
    'mkv',
    'mp4',
    'avi',
    'idx',
    'sub',
    'srt'
)

# immutable list/tuple of filenames to ignore or skip
# some of these qre required because they bypass allowed
# extensions e.g. rarbg.com.mp4
excluded_filenames = (
    '.part',
    'sample',
    'sample.avi',
    'sample.mkv',
    'sample.mp4',
    'etrg.mp4',
    'rarbg.com.mp4',
    'rarbg.com.txt',
    'rarbg.txt'
)

# todo whitelist allowed types
allowed_types = ()


# ----------------
# helper functions

"""
helper utility that returns a filename only
from a full path containing path & filename.
Performs 1 split & always returns last value in list

in: '/path/to/movies/movie_name_folder/movie_name.movie'
                                       ----------------
out: 'move_name.movie'
"""
get_filename_from_path = lambda f: f.rsplit('/', 1)[1]


"""
helper utility that returns a path only from
a full path containing both path & filename.
Performs 1 split & returns first value in results list

in: '/path/to/movies/movie_name_folder/movie_name.movie'
     ---------------------------------
                                            
out: '/path/to/movies/movie_name_folder'
"""
get_path_from_filename = lambda f: f.rsplit('/', 1)[0]


"""
helper utility that tries to return the movie filename
by splitting up the path & using the folder name as filename.
Performs 2 splits resulting in list of 3 slots & always returns
the middle slot at position 1

in: '/path/to/movies/movie_name_folder/movie_name.movie'
                      ---------------
out: 'move_name_folder'
"""
build_filename_from_path = lambda f: f.rsplit('/', 2)[1]


"""
helper utility that will extract the file
extension from the provided filename. Because we use
reverse split this function will work properly for 
both single filenames & full path + filename strings.

in: 'movie_name.movie'
in: '/path/to/movies/movie_name_folder/movie_name.movie'
                                                  -----
out: 'movie'
"""
get_extension_from_filename = lambda f: f.rsplit('.', 1)[1]


# ----------------------
# entry point for script

def main():
    """
    The main loop

    uses configured paths & globs to find any files in them - 
    iterating over the found files & gathering metadata
    to perform best guess as to where a media file should
    be moved.
    """
    # display some welcome text to the user
    print '\n\n'
    print ' ===================================================='
    print ' = LETS GET TO SORTING & MOVING YOUR MEDIA FILES :) ='
    print ' ===================================================='
    print '\n'

    # get session key & prep
    t_session = get_session_key()

    # iterate over paths tuple & look for files
    for path in paths:
        # iterate over the glob matches
        for name in glob.glob(path):
            # wrap in try/catch
            try:
                print '\n<---------------------->\n'
                print 'Found: \n %s' % get_filename_from_path(name)

                # get media metadata for this file
                metadata = guess_file_info(name)

                # get & check media type from metadata
                media_type = get_media_type(metadata)
                
                # if 1st return val is true move media
                if media_type:
                    print '\nType: %s ..' % media_type
                    move_media_by_type(media_type, name)
                else:
                    # remove unneeded files & continue
                    remove_non_media(name)
                    continue

            except Exception as e:
                raise Exception(e)


def get_session_key():
    """
    @note This is not currently used & was added for subsequent
     version. Could be deprecated - have no decided if want to 
     to use the transmission RPC API yet. 
     
    Makes initial request to transmission rpc API to store
     the value of the current session for use in all subsequent
    requests to the API.

    Requests to transmission API require the session-id & as such
     will always be met with a responding status code of
    409 due to missing `X-Transmission-Session-Id` header 
     value(s). Ergo we must make 1 request to get the session-id 
    so that we can append it to subsequent requests.

    @return  {str}  returns the current session key as string
    """

    # make initial request & get header value from response
    return session.get(t_api).headers.get(
        'X-Transmission-Session-Id'
    )


def get_media_type(metadata):
    """
    Sorts the type of media (e.g. movie/episode/etc..)

    @param  {dict}  `metadata`  metadata on particular media
    @return [dict or False]     returns dict of type info or False if none
    """

    return metadata.get('type') if 'unknown' not in metadata['type'] else False


def move_media_by_type(media_type, filename):
    """
    moves media of filename to the proper directory based on type

    @param [str] `media_type`  string value representing type of media
    @param [str] `filemame`    string representing the current filename
    """ 

    # extra filename from full path
    name = get_filename_from_path(filename)

    extension = get_extension_from_filename(name)

    tmp_path, tmp_filename = None, None

    # ensure that this is the proper file type first & not an excluded filename
    # if any(word for word in excluded_filenames)
    print "checking %s to lower %s compared with %s" % (name, name.lower(), excluded_filenames)
    if extension in allowed_extensions and name.lower() not in excluded_filenames:
        # catch subtitles that are not named the same as movie & correct for plex
        if 'eng' in name.lower() and '.srt' in name.lower():
            # strip the extension from filename, get the path, & build the filename
            # we have to guess the filename from the final folder in the path due to 
            # the fact that we are currently processing in the loop outside of the actual
            # movie/episode name (working on English.srt) & therefore do not have access 
            # to the movie name.. We don't know if the movie is processed before or after
            # the subtitles either & it could be alphabetical so this is the best method
            # currently for performing a best guess at the file name to rename subtitles to
            tmp_path = get_path_from_filename(filename)
            tmp_filename = build_filename_from_path(filename)

            # print info about op & updated filename for subtitles
            print '\nThis subtitle has a name that plex does not recognize.. Renaming %s to %s.srt' % (name, tmp_filename)

            # rename the subs to the episode name with srt extension
            shutil.move(filename, '%s/%s.srt' % (tmp_path, tmp_filename))

        if media_type == 'unknown':
            print 'This is unknown.. a folder maybe? skipping..'
            return

        if media_type == 'episode' or media_type == 'episodesubtitle':
            # cache destination path
            dest_path = os.path.join(base_path, shows_path)
            
            print 'moving %s %s from %s to %s' % (media_type, filename, name, dest_path)

            # move the file
            try:
                # copy to tv shows directory
                shutil.move(filename, dest_path)
            except Exception as e:
                # file must have been renamed.. try the updated subtitle name
                shutil.move(
                    '%s/%s.srt' % (tmp_path, tmp_filename), 
                    dest_path
                )

                # reset the tmp vars
                tmp_filename = None
                tmp_path = None

            # notify end-user that move was accomplished
            Notifier.notify(
                'Moved %s %s to %s' % (media_type, name, dest_path),
                title='Video Sort',
                sound='Ping'
            )


        elif media_type == 'movie' or media_type == 'moviesubtitle':
            # cache destination path
            dest_path = os.path.join(base_path, movies_path)

            print 'moving %s %s to %s' % (media_type, name, dest_path)

            Notifier.notify(
                'Moved %s %s to %s' % (media_type, name, dest_path),
                title='Video Sort',
                sound='Ping'
            )
            
            # move the file
            try:
                shutil.move(filename, dest_path)
            except Exception as e:
                # file must have been renamed.. try the updated subtitle name
                shutil.move(
                    '%s/%s.srt' % (tmp_path, tmp_filename), 
                    dest_path
                )

                # reset the tmp vars
                tmp_filename = None
                tmp_path = None

        else:
            print '\nNot a media file %s or unknown media. Unable to determine type..' % (name,)
    else:
        # remove the "undesirables" (baskets of deplorables lol)
        remove_non_media(filename)

    return


def remove_non_media(filename):
    """
    Simple wrapper around os.remove() for single files or empty
     directories with a few additional checks to ensure files 
    that are being removed should be removed.

    @param  {str}  `filename`  string representing the current filename
    """
    if os.path.isdir(filename):
        # os.remove() chokes on directories mostly.. @todo working on
        print "This was a directory.. skipping.. %s" % (filename,)

        return

    # attempt to remove the files that are non-media or subtitles
    try:
        # extra filename from full path
        name = get_filename_from_path(filename)

        # yet again get the extension
        extension = get_extension_from_filename(name)

        if os.path.isfile(filename):
            # double check that we aren't somehow removing a valid file
            # this will likely be removed as we should never reach this gate
            if extension == '.part':
                return Notifier.notify(
                    'Skipping %s - not finished downloading' % (filename),
                    title='Video Sort',
                    sound='Frog'
                )
            else:
                print 'Oops!! %s is an excluded filename.. removing' % (name,)

                # remove the file
                os.remove(filename)

    except Exception as e:
        # os.remove will not remove directories nor do we want it to
        # in this use case - will need to run a cleanup script afterwards
        print "error deleting file, swallowing exception. Original error %s" % e


def cleanup(path):
    """
    @todo Complete & test; Do not use this yet - unfinished!

    removes the folder & any leftover files within a dir
     that has already been processed. We currently have 
    no state or model to use as indicator of what has been
     handled so its important that this function is invoked 
    in proper order after the media files have been moved.
    """
    if os.path.isfile(path):
        # we need the outermost folder; return
        return

    if os.path.isdir(path):
        # iterate over files within folder & ensure safe to rm
        for filename in glob.glob(path):
            # ensure the extension is allowed to be removed
            extension = get_extension_from_filename(filename)

            if extension in allowed_extensions:
                return
            else:
                shutil.rmtree(path)


    pass


if __name__ == '__main__': 
    main()
