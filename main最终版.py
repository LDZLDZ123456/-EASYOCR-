import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox
from PIL import Image, ImageTk
import cv2
import easyocr
import numpy as np
from pathlib import Path

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR文字识别")  # 设置窗口标题
        self.root.geometry("1000x700")  # 调整窗口大小为 1000x700
        
        # 设置全局字体
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)  # 设置字体大小
        self.root.option_add("*Font", default_font)  # 应用字体设置
        
        # 创建EasyOCR的读取器对象，支持中文简体和英文识别，禁用GPU加速
        self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        
        self.setup_ui()  # 初始化UI界面

    def setup_ui(self):
        # 设置样式
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 12))  # 按钮样式
        style.configure('Title.TLabelframe.Label', font=('Arial', 12, 'bold'))  # 标签框样式
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # 主框架，适当调整内边距
        
        # 按钮区域（顶部）
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))  # 按钮框架，增加上下间距
        
        # 将按钮放在中间
        btn_container = ttk.Frame(btn_frame)
        btn_container.pack(anchor=tk.CENTER)  # 按钮容器
        
        # 选择图片按钮
        self.select_btn = ttk.Button(btn_container, text="选择图片", command=self.select_image, 
                                      width=18, style='Large.TButton')  # 按钮宽度调整
        self.select_btn.pack(side=tk.LEFT, padx=15)  # 左侧按钮
        
        # 开始识别按钮
        self.process_btn = ttk.Button(btn_container, text="开始识别", command=self.process_image, 
                                      width=18, style='Large.TButton')  # 按钮宽度调整
        self.process_btn.pack(side=tk.LEFT, padx=15)  # 右侧按钮
        
        # 保存按钮
        self.save_btn = ttk.Button(btn_container, text="保存识别结果", command=self.save_result, 
                                    width=18, style='Large.TButton')  # 按钮宽度调整
        self.save_btn.pack(side=tk.LEFT, padx=15)  # 保存按钮
        
        # 图像显示区域（中间）
        image_frame = ttk.Frame(main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=15)  # 图像框架，适当增加间距
        
        # 左侧原始图像
        orig_frame = ttk.LabelFrame(image_frame, text="原始图像", style='Title.TLabelframe')
        orig_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))  # 原始图像框
        
        # 创建固定大小的画布用于显示原始图像
        self.orig_canvas = tk.Canvas(orig_frame, width=450, height=350, bg='#F0F0F0')  # 缩小画布尺寸
        self.orig_canvas.pack(padx=10, pady=10)
        
        # 右侧处理后图像
        proc_frame = ttk.LabelFrame(image_frame, text="处理后图像", style='Title.TLabelframe')
        proc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))  # 处理图像框
        
        # 创建固定大小的画布用于显示处理后图像
        self.proc_canvas = tk.Canvas(proc_frame, width=450, height=350, bg='#F0F0F0')  # 缩小画布尺寸
        self.proc_canvas.pack(padx=10, pady=10)
        
        # 识别文本显示区域（底部）
        text_frame = ttk.LabelFrame(main_frame, text="识别结果", style='Title.TLabelframe')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))  # 识别结果框
        
        # 创建文本框和滚动条
        text_container = ttk.Frame(text_frame)
        text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(text_container, height=8, wrap=tk.WORD, 
                                   font=('Arial', 12))  # 显示识别结果的文本框，减少高度
        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, 
                                  command=self.result_text.yview)  # 滚动条
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 文本框放置在左侧
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # 滚动条放置在右侧
        
        self.result_text.configure(yscrollcommand=scrollbar.set)  # 绑定滚动条到文本框
        
        # 初始化变量
        self.current_image_path = None  # 当前图像路径
        self.current_image = None  # 当前图像对象

    def group_text_by_lines(self, results):
        def get_y_coordinate(result):
            points = result[0]
            y_coords = [p[1] for p in points]
            return sum(y_coords) / len(y_coords)
        
        sorted_results = sorted(results, key=get_y_coordinate)
        lines = []
        current_line = [sorted_results[0]] if sorted_results else []
        y_threshold = 20
        
        for result in sorted_results[1:]:
            current_y = get_y_coordinate(result)
            prev_y = get_y_coordinate(current_line[0])
            
            if abs(current_y - prev_y) < y_threshold:
                current_line.append(result)
            else:
                lines.append(current_line)
                current_line = [result]
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.current_image_path = file_path
            self.show_original_image(file_path)
            self.proc_canvas.delete("all")
            self.result_text.delete(1.0, tk.END)
    
    def show_original_image(self, image_path):
        image = Image.open(image_path)
        image = self.resize_image(image, 450, 350)  # 调整图像大小
        photo = ImageTk.PhotoImage(image)
        
        self.orig_canvas.delete("all")
        self.orig_canvas.create_image(225, 175, image=photo, anchor=tk.CENTER)
        self.orig_canvas.image = photo

    def process_image(self):
        if self.current_image_path is None:
            messagebox.showerror("错误", "请先选择一张图片！")
            return
        
        result = self.reader.readtext(self.current_image_path)
        
        if not result:
            messagebox.showinfo("提示", "未识别到任何文本")
            return
        
        img = cv2.imread(self.current_image_path)
        for area in result:
            points = area[0]
            top_left = tuple(map(int, points[0]))
            bottom_right = tuple(map(int, points[2]))
            cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = self.resize_image(img_pil, 450, 350)
        photo = ImageTk.PhotoImage(img_pil)
        
        self.proc_canvas.delete("all")
        self.proc_canvas.create_image(225, 175, image=photo, anchor=tk.CENTER)
        self.proc_canvas.image = photo
        
        self.result_text.delete(1.0, tk.END)
        text_lines = self.group_text_by_lines(result)
        for line in text_lines:
            line_text = " ".join([item[1] for item in line])
            self.result_text.insert(tk.END, f"{line_text}\n")

    def resize_image(self, image, max_width, max_height):
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        ratio = min(width_ratio, height_ratio)
        
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)

    def save_result(self):
        result_text = self.result_text.get(1.0, tk.END)
        if not result_text.strip():
            messagebox.showwarning("警告", "没有可保存的识别结果")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result_text)
            messagebox.showinfo("保存成功", f"文件已保存到 {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
