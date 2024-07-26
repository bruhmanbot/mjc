<h1>Mjc</h1>
<h2>Welcome to this probably useless repository</h2>
<p>This is a mahjong score counter for taiwanese rules and score counting. The program is available in both python and javascript (bundled as a website)</p>
<p>The python version's development is considered to be complete. Some features are still being ported to the website version</p>
<p>Feel free to report any bugs you find to me (if you really care)</p>

<h3>Python version</h3>
<p>The main file you will be using is userGUI.py execute the file and you should find a pretty intuitive UI to enter your tiles in. Due to the limitations with tkinter, you may need to resize your window so the scrolling function can keep up with the new page size.</p>
<p>Make sure to run the python file in the current working directory ./mjc-main or else the file paths for the images may fail. To ensure doing so, simply run the file by executing counter.bat instead.</p>
<p>Another file you may want to edit is tw_accolades_info.csv you can change then score of each accolade on that.</p>

<h3>js version</h3>
<p>This version is not as robust as the python version, as you do not have the ability to customize the accolade names and scores (unless if you change the content on the json file) This version does not include couting for concealed accolades (cannot differentiate your tiles on whether they are concealed or not when counting). However, as this is essientially the second draft of my code, the javascript code is probably much more efficient.</p>
