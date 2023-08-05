# russianWebBypass
yeah...

## requirements
Firefox & gockodriver for firefox

## installation

Libs:
* `selenium`

```
pip3 install -U rubypass
```
or
```
pip install -U rubypass
```

## websites in question
[seasonvar](http://seasonvar.ru/)

[animevost](https://animevost.org/)

## docs

### main functions
#### ```seasonvarByPass(url, maxEps=30)```
extracts video urls, season at a time if not maxed out by ```maxEps```, from a provided *seasonvar* url, extracts original dub if possible

Arguments:
* ```url``` - str, a link to a show from seasonvar(required)
* ```maxEps``` - int, maximum amount of episodes to extract, default is 30(optional)


Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```vods``` - list of strings, list of extracted video urls
* ```ep``` - int, maximum amount of episodes available on ```url```

#### ```seasonvarByPassEp(url, ep)```
extracts a video url of a provided episode from a provided *seasonvar* url, extracts original dub if possible

Arguments:
* ```url``` - str, a link to a show from seasonvar(required)
* ```ep``` - int, index of an episode to be extracted, can be lower or higher then episode count of the show(required)

Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```vod``` - str, url to a video source
* ```ep2``` - int, processed ```ep```

#### ```showInfo(url)```
extracts details about the show from a provided *seasonvar* url

Arguments:
* ```url``` - str, a link to a show from seasonvar(required)

Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```lolz``` - list of strings, list of urls to other seasons of the show, if present
* ```ep``` - int, maximum amount of episodes available on ```url```

#### ```animevostBypass(url, maxEps=40)```
extracts video urls, season at a time if not maxed out by ```maxEps```, from a provided *animevost* url

Arguments:
* ```url``` - str, a link to a show from animevost(required)
* ```maxEps``` - int, maximum amount of episodes to extract, default is 40(optional)

Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```lolz``` - list of strings, list of extracted video urls
* ```name[1]``` - int, maximum amount of episodes available on ```url```

#### ```animevostBypassEp(url, ep)```
extracts a video url of a provided episode from a provided *animevost* url

Arguments:
* ```url``` - str, a link to a show from animevost(required)
* ```ep``` - int, index of an episode to be extracted, can be lower or higher then episode count of the show(required)

Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```vod``` - str, url to a video source
* ```ep2``` - int, processed ```ep```

#### ```animevostInfo(url)```
extracts details about the show from a provided *animevost* url

Arguments:
* ```url``` - str, a link to a show from animevost(required)

Returns:
* ```err``` - bool, True if an exception occurred in execution, False otherwise
* ```eps``` - list of ints, min and max values about episodes of the show
* ```name``` - str, name of the show
* ```lolz``` - list of strings, list of urls to other seasons of the show, if present

### helper functions
#### ```klk(elem, driver)```
clicks a selenium web element if it's not obscured by anything

Arguments:
* ```elem``` - selenium web element object
* ```driver``` - selenium webDriver object

Returns: ```None```

#### ```firefoxDriverInit()```
constructs a webDriver object and returns it with parameters
```python
'permissions.default.image' = 2 # images are off
'dom.ipc.plugins.enabled.libflashplayer.so' = False # flash is off
'dom.disable_beforeunload' = True
'media.volume_scale' = '0.0' # volume is 0
```

#### ```firefoxDriverInit2()```
constructs a webDriver object and returns it with parameters
```python
'permissions.default.image' = 2 # images are off
'permissions.default.stylesheet' = 2 # most css is off
'dom.ipc.plugins.enabled.libflashplayer.so' = False # flash is off
'dom.disable_beforeunload' = True
'media.volume_scale' = '0.0' # volume is 0
```

#### ```getVod(driver)```
returns a source url of a first video element on the page

Argument:
* ```driver``` - selenium webDriver object

Returns:
* ```url``` - str, source url of the video element