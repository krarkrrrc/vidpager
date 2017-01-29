# Dependencies
    - pafy (arch package community/python-pafy )
    - sqlalchemy (arch package community/python-sqlalchemy)
    - youtube-dl (arch package community/youtube-dl) - only if GetSubtitles.get_yt_dict(input_url, get_asr_subitles=True) is used
# Usage
To search in certain video id and to store it
use ^SAVE_ONLY^ if you want to skip searching, just save
```bash
python vidpager.py $target_string $youtube_id
```
To search in all stored videos with subtitles
```bash
python vidpager.py $target_string
```
NOTE:
- target_string can be only words and spaces, no special characters
- youtube_id is any youtube url as long as its has 11 chars youtube id in it
- subtitles passed via asr can be searched only with youtube_id, see
  CONST.test_urlids_for_asr for some tests

#TestCase
13 videos with subtitles
```bash
a=(jJZ66hPQLe4 7iup9-xtYuE VdmQp9M9jUo q_qdC6grfIA 5iszUCmLyW4 3NxKH1MK4z8 dFccny3iGbo f_4Q9Iv7_Ao PKfR6bAXr-c K9G9lfA8fa8 z2DpcdYuRGo s9yoGGIF6lQ 3_5rRtarU-Y)
for i in ${a[*]}; do python vidpager.py ^SAVE_ONLY^ $i; done
```
