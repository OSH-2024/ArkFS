# Label Matching

This directory contains the code for the label matching experiments. An noteworthy thing is that it is just a prototype and is tremendously susceptible to all sorts of bugs and errors. The code is not optimized and is not meant to be used in production. It is just a proof of concept.

sudo apt-get update
sudo apt-get install python3-tk


pip install SpeechRecognition pyaudio   语音处理包
## Search

The latest version of file searching is in the `search` directory. The search is done using the `search.py` script. The script takes in a query and returns the most relevant files. And it is now able to search for a file using contents and time limit.


## 上层返回向量--李岱峰

支持精确搜索，支持模糊搜索，返回向量[[时间], [type], [文件内容或精确化文件名], [操作码]]
操作码'增': '0', '删': '1', '改': '2', '查': '3','细': '4'。
细是精确化搜索，此时的第三个参数就是精确的文件名。


