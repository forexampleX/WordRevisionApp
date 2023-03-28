# Brief
WordRevision is a simple English word learning software. With WordRevision you can add daily words and revise them according to the Ebbinghaus Forgetting Law.
# Environment

```python
altgraph==0.17.3
contourpy==1.0.7
cycler==0.11.0
fonttools==4.39.2
kiwisolver==1.4.4
matplotlib==3.7.1
numpy==1.24.2
packaging==23.0
pandas==1.5.3
pefile==2023.2.7
Pillow==9.4.0
pyinstaller==5.9.0
pyinstaller-hooks-contrib==2023.1
pyparsing==3.0.9
PySide6==6.4.3
PySide6-Addons==6.4.3
PySide6-Essentials==6.4.3
python-dateutil==2.8.2
pytz==2023.2
pywin32-ctypes==0.2.0
shiboken6==6.4.3
six==1.16.0
```


# Directory

```c
+---.idea
|   \---inspectionProfiles
+---dist
|   \---WordRevisionApp
|       +---asset
|       +---contourpy
|       +---db
|       +---kiwisolver
|       +---matplotlib
|       +---matplotlib.libs
|       +---numpy
|       +---pandas
|       +---PIL
|       +---PySide6
|       +---pytz
|       +---shiboken6
|       +---tcl
|       +---tcl8
|       +---tk
|       \---ui
+---docs
+---src
    |   Dictionary.py
    |   DrawDictionary.py
    |   MainWindow.py
    |   ReadmeWindow.py
    |   RevisionWindow.py
    |   runtimehook.py
    |   Schedule.py
    |   WordRevisionApp.py
    |
    +---asset
    |       logo.ico
    |
    +---db
    |       Readme.md
    |       schedule.csv
    |       wordDictionary.csv
    |
    +---ui
    |       MainWindow.ui
    |       Readme.ui
    |       RevisionWindow.ui
    |
    \---__pycache__
            Dictionary.cpython-311.pyc
            DrawDictionary.cpython-311.pyc
            MainWindow.cpython-311.pyc
            ReadmeWindow.cpython-311.pyc
            RevisionWindow.cpython-311.pyc
            Schedule.cpython-311.pyc
            _MySignals_.cpython-311.pyc
```



# Feature
## Add new words
In "Add new words" tab, you can input a new word and its explanation on the left and see if the word is added successfully on the right. If you have learned this word before, it will tell you when you learned it.
## Revise words
In "Revise word" tab, you can see the number of words to review today. There's also a histogram which displays the number of words learned each day for the last 7 days. You can push the "Refresh" button to refresh the data.
You can push "Revise Today's Words" to review the words you learned today, and push "Revise Former Words" to review the words you learned 1, 2, 4, 7, 15 days ago (according to the Ebbinghaus Forgetting Law).
## Operate dictionary
In "Operate dictionary" tab, you can check dictionary information and update dictionary entries individually.

|command|feature|return|

|----|----|----|

|SELECT ALL|show every words in the dictionary|(word)\n(word)\n...(word)|

|SELECT INFO|show dictionary information|"The dictionary is built at (date).\n The dictionary has (number) words."|

|SELECT (word)|show a word's learning date and explanation|"(word)\n(date)\n(explanation)" Or "(word) is not in the dictionary."|

|DROP (word)|drop a word in the dictionary|"Successfully delete (word)." Or "(word) is not in the dictionary."|

|UPDATE (word)|update a word's explanation(update the explanation showed below)|"(word)'s explanation has been updated to (explanation)." Or "(word) is not in the dictionary."|

|UPDATE BEGINDATE|update the date when the dictionary was built(enter new date below in 'yyyy-MM-dd')|"The dictionary is rebuilt at (date)." Or "Illegal date:(error)"|

|something else|prompt to enter the correct operation|"Please input correct operation."|


# Author
Developed by Zhuo Dai on March 28, 2023.
