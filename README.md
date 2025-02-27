# **omniparser_pyautogui_demo**


## **Integrating OmniParser with PyAutoGUI for automation.**

### **Content** 

* [Ⅰ. Purpose](#1)
* [Ⅱ. Tools or Software](#2)
* [Ⅲ. Statement](#3)
* [Ⅳ. Results](#4)
* [Ⅴ. References](#5)

<br>

---

<h4 id="1">Ⅰ. Purpose</h4>
This project will provide you with the foundation to integrate OmniParser with PyAutoGUI for automation.
<br><br>

<h4 id="2">Ⅱ. Tools or Software</h4>

OmniParser V2, PyAutoGUI.
<br><br>

<h4 id="3">Ⅲ. Statement</h4>

The main steps are as follows.<br>
(1)Use PyAutoGUI to take a screenshot for OmniParser.<br>
(2)OmniParser scans and parses the image file.<br>
(3)PyAutoGUI would operate mouse and keyborad according to coordinates converted from parsed content by OmniParser.<br>
<br>

<h4 id="4">Ⅳ. Results</h4>

As you can see below, after clicking icon "iTerm" on dock of MacOS, final step would let mouse move to terminal, write shell script command and press "Enter" to execute "omni_parser.sh". Then, the result would be shown on terminal.<br>

![avatar](./README_png/results.png)
<br><br>

__The above provides the foundation to integrate OmniParser with PyAutoGUI for automation. Definitely, that can be expanded, improved and applied.<br>In the future, computers may judge screen content just like humans and then perform targeted operations.__<br>

(Concerning to the details, please refer to the files of this project)

<br>

---

<h4 id="5">Ⅴ. References</h4>

[1] [microsoft/OmniParser
](<https://github.com/microsoft/OmniParser>) 

[2] [microsoft/OmniParser-v2.0](<https://huggingface.co/microsoft/OmniParser-v2.0>)

[3] [Ultralytics YOLO Docs](<https://docs.ultralytics.com/>)

[4] [Welcome to PyAutoGUI’s documentation](<https://pyautogui.readthedocs.io/en/latest/#>)