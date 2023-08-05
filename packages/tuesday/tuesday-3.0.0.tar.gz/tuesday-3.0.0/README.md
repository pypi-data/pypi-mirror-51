# Tuesday

You can easily automize and control most of the functions of system by your voice.
By using this package u can easily build jarvis like programme, irrespective of your knowledge of coding.
Easy voice commands to work with.
 

## Requirements
You have to follow the steps given below before installing package:
## 1: Install Microsoft Redistributable
[MicrosoftRedistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) select version according to your system.
## 2: Install visual studio build tools c++ 2015 or above
[visual studio build tools c++ 2015](https://www.microsoft.com/en-in/download/details.aspx?id=48159) and should have windows 10
## 3: Download geckodriver version according to your system
[geckodriver](https://github.com/mozilla/geckodriver/releases).
Paste and extract file in your python folder or PATH.
## 4: Download chromedriver version according to your system
[chromedriver](https://chromedriver.chromium.org/downloads).
Paste and extract file in your python folder or PATH.
## 5: Download wheel version according to your python version
[wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/).
Paste this wheel file in your project folder.
## 6: Allow access to less secured apps
[lesssecureapps](https://myaccount.google.com/lesssecureapps).
Allow it.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tuesday.
```python
# step 1: Python should be istalled in "C:\Folder" location
#step 2: Python interpreter should be installed in "C:\new folder" location 
#step 3: Project should be located in "C:\name of project" location
# step 4: Paste the downloaded file in your project folder and in python interpretor use "pip install nameofthewheelfile"
```

## Speak

```python
from tuesday import speech

speech.speak("hello") #speak function
```
## Voice Search

```python
from tuesday import search
search.google()
```
Interactive voice programme

## Send a email through gmail

you can send a mail using your voice
```python
from tuesday import sendmail
sendmail.send()
```
From next update mail can be sent by other email platforms also,
But now it is limited to GMAIL only.

## Jarvis structure
```python
if __name__=='__main__':
    speech.speak("hello my name is tuesday")
    speech.intro()
    
    while True:
        
        comm=speech.takecommand().lower()
        if "open a website" in comm:
            websites.Open(".com") #use capital 'Open'
        elif "google" in comm:
            search.google()
        elif "play youtube" in comm:
            search.youtubeplay()
        elif "search youtube" in comm:
            search.youtubesearch()
        elif "open facebook by mail" in comm:
            social.facebookemail()
        elif "open gmail" in comm:
            social.gmail()
        elif "send a mail" in comm:
            sendmail.send()     
        elif "tuesday stop" in comm:
            sys.exit() 
```
More commands are available try to explore them.
Next update will include many more commands.
Thank you.            