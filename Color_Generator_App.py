import colorsys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QSpinBox, QSlider, QPushButton, 
                             QTextEdit, QColorDialog, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPalette, QFont

class ColorGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级色彩生成器")
        self.setGeometry(100, 100, 800, 600)
        
        # 主控件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # 布局
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        # 色系选择
        self.color_scheme_label = QLabel("选择色系:")
        self.color_scheme_combo = QComboBox()
        self.color_schemes = [
            "基础色系", "红色系", "橙色系", "黄色系", "绿色系", "蓝色系", 
            "紫色系", "粉色系", "中性色系", "黑白灰", "大地色系", 
            "莫兰迪色系", "暖色系", "冷色系", "流行色系", "马卡龙色系", 
            "荧光色系", "复古色系", "自然色系", "特殊色系", "金属色系", 
            "渐变色系", "透明色系", "文化/情绪色系", "中国传统色", 
            "日本和风色", "忧郁色系", "年度流行色", "对比色系", "同色系"
        ]
        self.color_scheme_combo.addItems(self.color_schemes)
        
        # 颜色数量
        self.num_colors_label = QLabel("颜色数量:")
        self.num_colors_spin = QSpinBox()
        self.num_colors_spin.setRange(1, 1000)
        self.num_colors_spin.setValue(360)
        
        # RGB范围选择
        self.range_label = QLabel("RGB范围:")
        self.range_combo = QComboBox()
        self.range_combo.addItems(["0-255", "0-999"])
        
        # 参数控制
        self.saturation_label = QLabel("饱和度:")
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(0, 100)
        self.saturation_slider.setValue(30)
        
        self.value_label = QLabel("亮度:")
        self.value_slider = QSlider(Qt.Horizontal)
        self.value_slider.setRange(0, 100)
        self.value_slider.setValue(85)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成颜色")
        self.generate_btn.clicked.connect(self.generate_colors)
        
        # 颜色显示区域
        self.colors_display = QTextEdit()
        self.colors_display.setReadOnly(True)
        self.colors_display.setFont(QFont("Courier", 10))
        
        # 颜色预览区域
        self.colors_preview = QWidget()
        self.colors_preview_layout = QHBoxLayout()
        self.colors_preview.setLayout(self.colors_preview_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.colors_preview)
        
        # 布局组织
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.color_scheme_label)
        controls_layout.addWidget(self.color_scheme_combo)
        controls_layout.addWidget(self.num_colors_label)
        controls_layout.addWidget(self.num_colors_spin)
        controls_layout.addWidget(self.range_label)
        controls_layout.addWidget(self.range_combo)
        
        params_layout = QHBoxLayout()
        params_layout.addWidget(self.saturation_label)
        params_layout.addWidget(self.saturation_slider)
        params_layout.addWidget(self.value_label)
        params_layout.addWidget(self.value_slider)
        
        self.layout.addLayout(controls_layout)
        self.layout.addLayout(params_layout)
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(scroll_area, 1)
        self.layout.addWidget(self.colors_display)
    
    def generate_colors(self):
        scheme = self.color_scheme_combo.currentText()
        num_colors = self.num_colors_spin.value()
        rgb_range = self.range_combo.currentText()
        saturation = self.saturation_slider.value() / 100
        value = self.value_slider.value() / 100
        
        if scheme == "马卡龙色系":
            colors = self.generate_macaron_colors(num_colors, saturation, value)
        else:
            colors = self.generate_basic_colors(num_colors, saturation, value)
        
        # 根据范围调整RGB值
        if rgb_range == "0-999":
            colors = [(r*3.92, g*3.92, b*3.92, hex_color) for r, g, b, hex_color in colors]
        
        self.display_colors(colors, rgb_range)
    
    def generate_macaron_colors(self, num_colors, saturation_base, value_base):
        colors = []
        saturation_variation = 0.2
        value_variation = 0.1
        
        for i in range(num_colors):
            hue = (i / num_colors) % 1.0
            saturation = saturation_base + saturation_variation * math.sin(i * 0.1)
            saturation = max(0.0, min(1.0, saturation))
            value = value_base + value_variation * math.cos(i * 0.05)
            value = max(0.0, min(1.0, value))
            
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            colors.append((r, g, b, hex_color))
        
        return colors
    
    def generate_basic_colors(self, num_colors, saturation, value):
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            colors.append((r, g, b, hex_color))
        return colors
    
    def display_colors(self, colors, rgb_range):
        # 清空预览区域
        for i in reversed(range(self.colors_preview_layout.count())): 
            self.colors_preview_layout.itemAt(i).widget().setParent(None)
        
        # 更新文本显示
        self.colors_display.clear()
        text_output = []
        
        for idx, (r, g, b, hex_color) in enumerate(colors):
            # 添加到文本输出
            if rgb_range == "0-255":
                text_output.append(f"QColor({int(r)}, {int(g)}, {int(b)}),  {hex_color}")
            else:
                text_output.append(f"QColor({int(r)}, {int(g)}, {int(b)}),  {hex_color} (0-999)")
            
            # 添加到预览
            color_frame = QFrame()
            color_frame.setFixedSize(QSize(20, 20))
            color_frame.setStyleSheet(f"background-color: {hex_color}; border: 1px solid black;")
            self.colors_preview_layout.addWidget(color_frame)
        
        self.colors_display.setPlainText("\n".join(text_output))

if __name__ == "__main__":
    app = QApplication([])
    window = ColorGeneratorApp()
    window.show()
    app.exec_()