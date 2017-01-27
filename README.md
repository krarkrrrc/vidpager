# Dependencies
    - pafy (arch package community/python-pafy )
    - sqlalchemy (arch package community/python-sqlalchemy)
# Usage
To search in certain video id and to store it
```bash
python vidpager.py $target_string $youtube_id
```
To search in all stored videos with subtitles
```bash
python vidpager.py $target_string
```
NOTE:
- target_string can be only words and spaces, no special characters
- youtube_id is any youtube url as long as its 11 last characters are its id
