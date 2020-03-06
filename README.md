# LSTC Grid Viewer (Lang & Schwarz Trade Center Grid Viewer)

This is a use-case-specific application. It allows user to view and interact with maximum 4 pages from `ls-tc.de` simutanously.
This application will:
- remove the fixed header from the page to give user more space.
- automatically scroll down to chart area.
- rescale pages when the window is moved to another screen.

# DEPENDENCIES
```
python3
pyqt5
```

# USAGE
`python main.py examples/watchlist`
`watchlist` is a file which contains the desired ls-tc.de links to be displayed. Each link is separated by newline.