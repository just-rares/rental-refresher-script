# Rental Refresher
This is a small project aimed to ease my search for a room.
<br>
I am a student in ***Delft*** at ***Computer Science*** and finding a room is hard. 
I found a student dorm that offers rooms on a frst come first serve basis. When I asked when the opening dates are, I got a simple *"In the following weeks"*, which annoyed me. 

More about the script now. 

<hr>

### Page Refresher

The `page_refresher.py` script uses selenium to open a chrome window on the specified `WEBSITE_URL`. It then uses the chrome driver to refresh the page at a given rate. It retrieves a specified div and checks whether the number changed compared to the previous number. If it did, it alerts me with sounds and windows popping up.

> ***NOTE*** &nbsp; An interesting thing I did is that the longer it goes without changing, the faster it refreshes.

<hr>

### GUI Application

The `gui.py` script is responsible for opening a small application that has some information about the script. It shows data such as the number of refreshes, the current number of rooms on the website and the current refresh rate, in minutes. It also includes a button that opens the website. 

The way this info is gathered is through the `log.txt` file. The app runs on multiple threads, one is busy refreshing the website, one is busy constantly checkig the `log.txt` file for any updates and another is displaying and updating the interface. 

> ***NOTE*** &nbsp; A challenge I encountered is that if I were to parse the entire file every time, it would take a lot of time when having a small refresh rate. This lead to having to implement a way to check for any *new* updates on the file. 

<hr>

### Extra Information

The app was packaged and installed using `pyinstaller` and now is a standalone `.exe` file. 
<br>
<br>
To run this app you need the `chromedriver` installed and added to the `/bin` path.
<br>
<br>
Extra functionality I wanted to add is a `countdown` that shows the time until the *next* refresh and a *better gui*. One cool thing I would have liked is a way to make my phone ring whenever the rooms are available.