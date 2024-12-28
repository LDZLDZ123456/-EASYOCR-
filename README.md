OCR文字识别系统

📚 项目简介

本项目是一个基于 Python 和 Tkinter 图形界面库开发的 OCR（光学字符识别）应用程序。它使用 EasyOCR 进行文字识别，并支持中文简体和英文的图像文本提取。用户可以通过简单的图形界面上传图像，进行文本识别，并将识别结果保存为文本文件。

🛠️ 功能特性

📷 图像上传：支持上传常见格式的图像文件（PNG、JPG、JPEG、BMP、GIF、TIFF）。

🔍 OCR识别：基于 EasyOCR，支持中文和英文文本识别。

🖼️ 图像展示：同时展示原始图像和带有识别框的处理图像。

📝 识别结果展示：识别到的文本以可编辑文本框的形式展示。

💾 保存结果：将识别到的文本保存为 .txt 文件。

📦 技术栈

Python：核心编程语言

Tkinter：图形用户界面

EasyOCR：文字识别引擎

OpenCV (cv2)：图像处理

Pillow (PIL)：图像展示与处理

🚀 安装与运行

1. 克隆项目

git clone https://github.com/LDZLDZ123456/EASYocr-text-recognizer.git
cd ocr-text-recognition

2. 安装依赖库

pip install -r requirements.txt

3. 运行程序

python main.py

📂 文件结构

📦 OCR文字识别系统
├── main.py           # 主程序入口
├── requirements.txt  # 所需库依赖
└── README.md         # 项目文档

📝 使用步骤

启动程序后，点击 “选择图片” 上传一张图像。

点击 “开始识别” 进行 OCR 识别。

在 “识别结果” 区域查看文本内容。

点击 “保存识别结果” 将文本保存为 .txt 文件。
![403d9e3993d70b82d44a8c4e336ad77](https://github.com/user-attachments/assets/c5d7723b-25fa-462a-8134-2fb79c952773)


感谢你的使用与支持！🎉
