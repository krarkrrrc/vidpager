Vidpager is simple python tool to save subtitles from youtube videos and search in
them.

Either saved or automatically recognized subtitles are supported,
currently only in english.

# Dependencies
    - python3
    - pafy (arch package community/python-pafy )
    - sqlalchemy (arch package community/python-sqlalchemy)
    - youtube-dl (arch package community/youtube-dl) - only if get_auto_subs=True parameter in GetSubtitles.get_yt_dict() is used


# Instal
Simply clone the repo and install dependencies.

If you are using Arch Linux just download python-pafy, python-sqlalchemy and youtube-dl, otherwise install pafy and sqlalchemy via pip, ideally in new virtualenv to keep your system clean.

If you will use get_auto_subs in GetSubtitles module you need, see [youtube-dl/download](https://rg3.github.io/youtube-dl/download.html). If you don't want to save auto subs(not recommended, lots of ideos are with auto_subs), change get_auto_subs=True to False on line 86 in vidpager.py

# Usage
To store and search in one video id:
```bash
python vidpager.py $target_string $youtube_id
```
To search in all stored videos with subtitles
```bash
python vidpager.py $target_string
```
NOTE:
- target_string can be anything, searching is case insensitive
  - use ^SAVE_ONLY^ if you want to skip searching, just save
  - use qoutes if you are searching for phrase with spaces e.g "President Trump"
  - patterns and searching for multiple words is not supported yet
- youtube_id is any youtube url as long as its has 11 chars youtube id in it

## TestCase

13 videos with subtitles
Run this to save these 13 videos with subtitles
```bash
a=(jJZ66hPQLe4 7iup9-xtYuE VdmQp9M9jUo q_qdC6grfIA 5iszUCmLyW4 3NxKH1MK4z8 dFccny3iGbo f_4Q9Iv7_Ao PKfR6bAXr-c K9G9lfA8fa8 z2DpcdYuRGo s9yoGGIF6lQ 3_5rRtarU-Y)
for i in ${a[*]}; do python vidpager.py ^SAVE_ONLY^ $i; done
```
