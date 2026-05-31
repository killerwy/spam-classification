import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from tkinter.font import Font
from model import EmailClassifier

class EmailClassifierApp:
    def __init__(self, root):
        self.root = root
        self.classifier = EmailClassifier()
        
        # 创建自定义字体
        self.bold_font = Font(family="Arial", size=10, weight="bold")
        self.normal_font = Font(family="Arial", size=10)
        self.mono_font = Font(family="Courier New", size=9)
        self.title_font = Font(family="Arial", size=12, weight="bold")
        
        self.setup_ui()
        self.status_var.set("请先选择数据集目录并加载数据")

    def setup_ui(self):
        """设置图形用户界面"""
        self.root.title("垃圾邮件分类系统")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 数据加载区域
        data_frame = ttk.LabelFrame(main_frame, text=" 1. 数据加载 ", padding="10")
        data_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(data_frame, text="数据集路径:").grid(row=0, column=0, sticky=tk.W)
        self.data_path_var = tk.StringVar()
        data_path_entry = ttk.Entry(data_frame, textvariable=self.data_path_var, width=60)
        data_path_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        browse_btn = ttk.Button(data_frame, text="浏览...", command=self.browse_data_dir)
        browse_btn.grid(row=0, column=2, padx=5)
        
        load_btn = ttk.Button(data_frame, text="加载数据", command=self.load_data)
        load_btn.grid(row=0, column=3, padx=5)
        
        # 模型训练区域
        train_frame = ttk.LabelFrame(main_frame, text=" 2. 模型训练 ", padding="10")
        train_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(train_frame, text="选择分类器:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value="Naive Bayes")
        model_combo = ttk.Combobox(train_frame, textvariable=self.model_var, 
                                  values=list(self.classifier.models.keys()),
                                  state="readonly", width=20)
        model_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        train_btn = ttk.Button(train_frame, text="训练模型", command=self.train_model)
        train_btn.grid(row=0, column=2, padx=5)
        
        # 评估结果区域
        self.eval_frame = ttk.LabelFrame(main_frame, text=" 3. 模型评估结果 ", padding="10")
        self.eval_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.eval_text = scrolledtext.ScrolledText(
            self.eval_frame, 
            wrap=tk.WORD, 
            height=12,
            font=self.mono_font,
            background="#f5f5f5",
            padx=10,
            pady=10
        )
        self.eval_text.pack(fill=tk.BOTH, expand=True)
        self.eval_text.insert(tk.END, "模型评估结果将显示在这里...\n", "center")
        
        # 邮件分类区域
        input_frame = ttk.LabelFrame(main_frame, text=" 4. 邮件分类 ", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.email_text = scrolledtext.ScrolledText(
            input_frame, 
            wrap=tk.WORD, 
            height=10,
            font=self.normal_font,
            padx=10,
            pady=10
        )
        self.email_text.pack(fill=tk.BOTH, expand=True)
        self.email_text.insert(tk.END, "在此粘贴邮件内容...")
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="预测", command=self.predict_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="从文件导入", command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.Frame(input_frame)
        result_frame.pack(fill=tk.X, pady=5)
        
        self.result_var = tk.StringVar(value="等待预测结果...")
        ttk.Label(result_frame, textvariable=self.result_var, font=self.title_font).pack(side=tk.LEFT)
        
        self.detail_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.detail_var, font=self.normal_font).pack(side=tk.LEFT, padx=10)
        
        # 状态栏
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 配置文本标签样式
        self.eval_text.tag_config("center", justify="center")
        self.eval_text.tag_config("header", font=self.title_font, foreground="blue")
        self.eval_text.tag_config("metric", font=self.bold_font, foreground="#333")
        self.eval_text.tag_config("value", font=self.mono_font)
        self.eval_text.tag_config("divider", foreground="gray")
        self.eval_text.tag_config("highlight", background="#e6f3ff")

    def browse_data_dir(self):
        """浏览数据集目录"""
        dir_path = filedialog.askdirectory(title="选择数据集目录")
        if dir_path:
            self.data_path_var.set(dir_path)

    def load_data(self):
        """加载数据集"""
        data_dir = self.data_path_var.get()
        if not data_dir:
            messagebox.showwarning("路径为空", "请先选择数据集目录")
            return
        
        try:
            self.status_var.set("正在加载数据集...")
            self.root.update()
            
            emails, labels = self.classifier.load_data(data_dir)
            ham_count = labels.count(0)
            spam_count = labels.count(1)
            
            self.eval_text.delete("1.0", tk.END)
            self.eval_text.insert(tk.END, "数据集加载成功!\n\n", "header")
            self.eval_text.insert(tk.END, f"{'正常邮件数量:':<20}", "metric")
            self.eval_text.insert(tk.END, f"{ham_count}\n", "value")
            self.eval_text.insert(tk.END, f"{'垃圾邮件数量:':<20}", "metric")
            self.eval_text.insert(tk.END, f"{spam_count}\n", "value")
            self.eval_text.insert(tk.END, f"{'总邮件数量:':<20}", "metric")
            self.eval_text.insert(tk.END, f"{len(emails)}\n\n", "value")
            self.eval_text.insert(tk.END, "请点击'训练模型'按钮开始训练\n", "highlight")
            
            self.status_var.set(f"数据集加载完成: 正常邮件 {ham_count} 封, 垃圾邮件 {spam_count} 封")
            
        except Exception as e:
            messagebox.showerror("加载错误", f"加载数据集时出错: {str(e)}")
            self.status_var.set("错误: " + str(e))

    def train_model(self):
        """训练模型"""
        if not self.classifier.data_loaded:
            messagebox.showwarning("数据未加载", "请先加载数据集")
            return
        
        try:
            self.status_var.set("正在训练模型...")
            self.root.update()
            
            results = self.classifier.train(test_size=0.2)
            
            # 显示评估结果
            self.eval_text.delete("1.0", tk.END)
            
            for model_name, metrics in results.items():
                # 添加模型标题
                self.eval_text.insert(tk.END, f"\n=== {model_name} ===\n\n", "header")
                
                # 添加主要指标
                self.eval_text.insert(tk.END, "主要指标:\n", "metric")
                self.eval_text.insert(tk.END, f"{'准确率(Accuracy):':<25}", "metric")
                self.eval_text.insert(tk.END, f"{metrics['accuracy']:.4f}\n", "value")
                self.eval_text.insert(tk.END, f"{'精确率(Precision):':<25}", "metric")
                self.eval_text.insert(tk.END, f"{metrics['precision']:.4f}\n", "value")
                self.eval_text.insert(tk.END, f"{'召回率(Recall):':<25}", "metric")
                self.eval_text.insert(tk.END, f"{metrics['recall']:.4f}\n", "value")
                self.eval_text.insert(tk.END, f"{'F1分数:':<25}", "metric")
                self.eval_text.insert(tk.END, f"{metrics['f1']:.4f}\n\n", "value")
                
                # 添加分类报告
                self.eval_text.insert(tk.END, "详细分类报告:\n", "metric")
                formatted_report = format_classification_report(metrics['report'])
                self.eval_text.insert(tk.END, formatted_report, "value")
                
                # 添加分隔线
                self.eval_text.insert(tk.END, "\n" + "="*70 + "\n", "divider")
            
            self.status_var.set("模型训练完成！")
            
        except Exception as e:
            messagebox.showerror("训练错误", f"训练模型时出错: {str(e)}")
            self.status_var.set("错误: " + str(e))

    def predict_email(self):
        """预测邮件类别"""
        email_content = self.email_text.get("1.0", tk.END).strip()
        if not email_content or email_content == "在此粘贴邮件内容...":
            messagebox.showwarning("输入为空", "请输入邮件内容")
            return
        
        selected_model = self.model_var.get()
        
        try:
            self.status_var.set(f"使用 {selected_model} 模型进行预测...")
            self.root.update()
            
            result, prob = self.classifier.predict(email_content, selected_model)
            self.result_var.set(f"分类结果: {result}")
            
            prob_ham = prob[0] * 100
            prob_spam = prob[1] * 100
            self.detail_var.set(f"正常邮件概率: {prob_ham:.2f}% | 垃圾邮件概率: {prob_spam:.2f}%")
            
            self.status_var.set("预测完成")
        except Exception as e:
            messagebox.showerror("预测错误", str(e))
            self.status_var.set("错误: " + str(e))

    def load_from_file(self):
        """从文件导入邮件内容"""
        file_path = filedialog.askopenfilename(
            title="选择邮件文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.email_text.delete("1.0", tk.END)
                    self.email_text.insert(tk.END, content)
                    self.status_var.set(f"已加载文件: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("文件错误", f"读取文件时出错: {str(e)}")

    def clear_text(self):
        """清空输入框"""
        self.email_text.delete("1.0", tk.END)
        self.result_var.set("等待预测结果...")
        self.detail_var.set("")
        self.status_var.set("输入已清空")

def format_classification_report(report):
    """格式化分类报告为更美观的显示"""
    lines = report.split('\n')
    formatted_lines = []
    
    # 添加标题分隔线
    formatted_lines.append("="*70 + "\n")
    
    for line in lines:
        if line.strip() == '':
            continue
            
        if 'precision' in line and 'recall' in line and 'f1-score' in line:
            # 处理标题行
            parts = [p for p in line.split() if p]
            header = f"{'类别':<15}{parts[0]:^12}{parts[1]:^12}{parts[2]:^12}{parts[3]:^12}\n"
            formatted_lines.append(header)
            formatted_lines.append("-"*70 + "\n")
        elif line.startswith('    '):
            # 处理数据行
            parts = [p for p in line.split() if p]
            if len(parts) >= 5:
                row = f"{parts[0]:<15}{parts[1]:^12}{parts[2]:^12}{parts[3]:^12}{parts[4]:^12}\n"
                formatted_lines.append(row)
        elif 'accuracy' in line:
            # 处理准确率行
            parts = [p for p in line.split() if p]
            formatted_lines.append("-"*70 + "\n")
            formatted_lines.append(f"{'准确率':<15}{'':^12}{'':^12}{parts[1]:^12}{'':^12}\n")
        elif 'avg' in line:
            # 处理平均值行
            parts = [p for p in line.split() if p]
            if 'macro' in parts[0]:
                formatted_lines.append("-"*70 + "\n")
            row = f"{parts[0]:<15}{parts[2]:^12}{parts[3]:^12}{parts[4]:^12}{parts[1]:^12}\n"
            formatted_lines.append(row)
            if 'weighted' in parts[0]:
                formatted_lines.append("="*70 + "\n")
    
    return ''.join(formatted_lines)
