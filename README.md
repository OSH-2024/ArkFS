# ArkFS
A LLM embeded file system
#### group member
杨柄权、刘明乐、李岱峰、常圣

Yang Bingquan, Liu Mingle, Li Daifeng, Chang Sheng

Saint XK - technical adviser , the professor of USTC


## About the project

Great breakthroughs have been made in the development of large language models in recent years. At present, many researchers have applied large language models to operating systems. For example, the recently published large language model is an important achievement in the application of operating system level. File system is an important part of the operating system, and there are many ways to explore its optimization direction and improvement. The team investigated three large language models and some of the current problems with file systems.


We found that large models have an outstanding ability to parse human sentences, and can parse a complex sentence of text into an action that a computer can understand. Based on this capability, we think we can design a very small system to demonstrate the feasibility of combining the file system with the large language model, which interprets the human manipulation language and then hands it over to the file system for manipulation.


Inspired by AIOS, we embed the big model into the file system, use the big model to understand the user's text semantics, and realize the operation of adding, deleting and searching files. The innovation of this project is to use a large model to understand user needs and form a task queue for file operation without manual intervention. The large model is deployed locally to learn local files and realize vectorization retrieval.


## project schedule

2024.7.6 The project theme has been completed, and voice control at the combined logic level can be realized.

Example: Voice input "Please find some pictures with grass, throw them into a new folder", after the execution is completed, the computer will complete the corresponding operation.

See the demo video for the effects. See the .\docs\final_report\video folder.

## How to use

This project supports windows, please enter the following on the windows command line:
> set GEMINI_API_KEY="your_google_gemini_api_key"

Then switch to the src directory and run
> python main.py

## 后续支持

For any questions, please contact feng1702@mail.ustc.edu.cn

Happy debug!

ArkFs team
