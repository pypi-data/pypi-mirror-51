# Get MyAnimeList! `(*°▽°*)`
Returns the data of a particular anime list and status in JSON.

### Install
`pip install getmal`

### Status codes:
```
7: All Anime
1: Currently Watching
2: Completed
3: On Hold
4: Dropped
6: Plan to Watch
```

### Examples
```bash
# Get valsaven's dropped anime
getmal valsaven 4

# Get valsaven's all anime and export it to valsaven.json
getmal valsaven 7 -o valsaven.json
```


### Build
```bash
python setup.py sdist bdist_wheel
```
