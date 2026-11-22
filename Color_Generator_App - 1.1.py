import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, 
                             QColorDialog, QScrollArea, QFrame, QFileDialog)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class ColorGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("颜色代码生成器")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_color_data()  # 先初始化颜色数据
        self.init_ui()         # 再初始化UI
        
    def init_ui(self):
        if not hasattr(self, 'color_data'):  # 如果color_data不存在
            self.init_color_data()           # 先初始化颜色数据

        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 顶部控制区域
        control_layout = QHBoxLayout()
        
        # 色系选择
        self.color_system_label = QLabel("选择色系分类:")
        self.color_system_combo = QComboBox()
        self.color_system_combo.addItems([
            "基础色系（基于色相）",
            "中性色系（无彩色+低饱和度色）",
            "按色调分类",
            "流行色系（现代设计常用）",
            "特殊色系",
            "文化/情绪色系"
        ])
        self.color_system_combo.currentIndexChanged.connect(self.update_color_type_combo)
        
        # 颜色类型选择
        self.color_type_label = QLabel("选择颜色类型:")
        self.color_type_combo = QComboBox()
        
        # 颜色数量
        self.color_count_label = QLabel("生成颜色数量:")
        self.color_count_spin = QSpinBox()
        self.color_count_spin.setRange(1, 50)
        self.color_count_spin.setValue(10)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成颜色")
        self.generate_btn.clicked.connect(self.generate_colors)
        
        # 添加到控制布局
        control_layout.addWidget(self.color_system_label)
        control_layout.addWidget(self.color_system_combo)
        control_layout.addWidget(self.color_type_label)
        control_layout.addWidget(self.color_type_combo)
        control_layout.addWidget(self.color_count_label)
        control_layout.addWidget(self.color_count_spin)
        control_layout.addWidget(self.generate_btn)
        
        # 预览区域
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_widget = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_widget.setLayout(self.preview_layout)
        self.preview_scroll.setWidget(self.preview_widget)
        
        # 代码输出区域
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存到文件")
        self.save_btn.clicked.connect(self.save_to_file)
        self.copy_btn = QPushButton("复制代码")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_output)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.clear_btn)
        
        # 添加到主布局
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.preview_scroll, 1)
        main_layout.addWidget(self.code_output, 1)
        main_layout.addLayout(button_layout)
        
        # 初始化颜色类型下拉框
        self.update_color_type_combo()
        
    def init_color_data(self):
        # 颜色数据库
        self.color_data = {
            "基础色系（基于色相）": {
                "红色系": [
                    {"name": "正红", "rgb": (255, 0, 0)},
                    {"name": "酒红", "rgb": (136, 0, 21)},
                    {"name": "玫红", "rgb": (255, 0, 127)},
                    {"name": "珊瑚红", "rgb": (255, 127, 80)},
                    {"name": "番茄红", "rgb": (255, 99, 71)},
                    {"name": "铁锈红", "rgb": (183, 65, 14)},
                    {"name": "砖红", "rgb": (203, 65, 84)},
                    {"name": "胭脂红", "rgb": (210, 4, 45)}
                ],
                "橙色系": [
                    {"name": "橘红", "rgb": (255, 69, 0)},
                    {"name": "南瓜橙", "rgb": (255, 117, 24)},
                    {"name": "杏色", "rgb": (251, 206, 177)},
                    {"name": "琥珀色", "rgb": (255, 176, 0)},
                    {"name": "蜜橙", "rgb": (255, 165, 79)},
                    {"name": "焦糖色", "rgb": (210, 125, 45)},
                    {"name": "姜黄", "rgb": (255, 153, 51)}
                ],
                "黄色系": [
                    {"name": "柠檬黄", "rgb": (255, 255, 0)},
                    {"name": "芥末黄", "rgb": (255, 219, 88)},
                    {"name": "金黄", "rgb": (255, 215, 0)},
                    {"name": "香槟色", "rgb": (247, 231, 206)},
                    {"name": "鹅黄", "rgb": (255, 241, 175)},
                    {"name": "土黄", "rgb": (210, 180, 140)},
                    {"name": "麦秆黄", "rgb": (234, 218, 151)}
                ],
                "绿色系": [
                    {"name": "墨绿", "rgb": (0, 66, 37)},
                    {"name": "薄荷绿", "rgb": (62, 180, 137)},
                    {"name": "橄榄绿", "rgb": (107, 142, 35)},
                    {"name": "牛油果绿", "rgb": (86, 130, 3)},
                    {"name": "松绿", "rgb": (0, 128, 128)},
                    {"name": "翡翠绿", "rgb": (0, 168, 107)},
                    {"name": "苔藓绿", "rgb": (77, 93, 83)}
                ],
                "蓝色系": [
                    {"name": "天蓝", "rgb": (135, 206, 235)},
                    {"name": "宝蓝", "rgb": (0, 35, 102)},
                    {"name": "藏青", "rgb": (0, 15, 137)},
                    {"name": "克莱因蓝", "rgb": (0, 47, 167)},
                    {"name": "湖蓝", "rgb": (0, 168, 225)},
                    {"name": "孔雀蓝", "rgb": (0, 128, 128)},
                    {"name": "钴蓝", "rgb": (0, 71, 171)}
                ],
                "紫色系": [
                    {"name": "薰衣草紫", "rgb": (181, 126, 220)},
                    {"name": "葡萄紫", "rgb": (75, 0, 130)},
                    {"name": "梅子色", "rgb": (120, 24, 74)},
                    {"name": "丁香紫", "rgb": (206, 160, 227)},
                    {"name": "紫罗兰", "rgb": (138, 43, 226)},
                    {"name": "紫水晶", "rgb": (153, 102, 204)},
                    {"name": "木槿紫", "rgb": (191, 148, 228)}
                ],
                "粉色系": [
                    {"name": "樱花粉", "rgb": (255, 183, 197)},
                    {"name": "玫粉", "rgb": (255, 0, 127)},
                    {"name": "鲑鱼粉", "rgb": (255, 145, 164)},
                    {"name": "灰粉", "rgb": (201, 169, 166)},
                    {"name": "蜜桃粉", "rgb": (255, 209, 220)},
                    {"name": "藕粉", "rgb": (237, 209, 216)},
                    {"name": "珊瑚粉", "rgb": (255, 111, 97)}
                ]
            },
            "中性色系（无彩色+低饱和度色）": {
                "黑白灰": [
                    {"name": "纯白", "rgb": (255, 255, 255)},
                    {"name": "象牙白", "rgb": (251, 249, 240)},
                    {"name": "炭黑", "rgb": (20, 20, 20)},
                    {"name": "高级灰（莫兰迪灰）", "rgb": (128, 128, 128)},
                    {"name": "珍珠白", "rgb": (248, 246, 240)},
                    {"name": "银灰", "rgb": (192, 192, 192)},
                    {"name": "石墨黑", "rgb": (40, 40, 40)}
                ],
                "大地色系": [
                    {"name": "米白", "rgb": (245, 245, 220)},
                    {"name": "卡其色", "rgb": (195, 176, 145)},
                    {"name": "驼色", "rgb": (193, 154, 107)},
                    {"name": "咖啡棕", "rgb": (74, 44, 42)},
                    {"name": "沙色", "rgb": (194, 178, 128)},
                    {"name": "可可棕", "rgb": (112, 79, 56)},
                    {"name": "胡桃木色", "rgb": (93, 68, 44)}
                ],
                "莫兰迪色系": [
                    {"name": "雾霾蓝", "rgb": (178, 200, 212)},
                    {"name": "灰豆绿", "rgb": (169, 188, 168)},
                    {"name": "燕麦色", "rgb": (211, 203, 186)},
                    {"name": "灰粉", "rgb": (201, 169, 166)},
                    {"name": "灰紫", "rgb": (183, 172, 188)},
                    {"name": "灰蓝", "rgb": (172, 182, 196)},
                    {"name": "灰黄", "rgb": (200, 190, 170)}
                ]
            },
            "按色调分类": {
                "暖色系": [
                    {"name": "红橙黄及衍生色", "rgb": (255, 100, 100)},
                    {"name": "暖色系变体1", "rgb": (255, 150, 100)},
                    {"name": "暖色系变体2", "rgb": (255, 200, 100)}
                ],
                "冷色系": [
                    {"name": "蓝绿紫及衍生色", "rgb": (100, 100, 255)},
                    {"name": "冷色系变体1", "rgb": (100, 200, 255)},
                    {"name": "冷色系变体2", "rgb": (100, 255, 200)}
                ],
                "中性色系": [
                    {"name": "黑白灰棕", "rgb": (150, 150, 150)},
                    {"name": "中性色变体1", "rgb": (200, 200, 200)},
                    {"name": "中性色变体2", "rgb": (100, 100, 100)}
                ]
            },
            "流行色系（现代设计常用）": {
                "马卡龙色系": [
                    {"name": "baby蓝", "rgb": (137, 207, 240)},
                    {"name": "樱花粉", "rgb": (255, 183, 197)},
                    {"name": "薄荷绿", "rgb": (162, 228, 184)},
                    {"name": "薰衣草紫", "rgb": (220, 208, 255)},
                    {"name": "柠檬黄", "rgb": (255, 247, 153)},
                    {"name": "棉花糖粉", "rgb": (255, 209, 220)},
                    {"name": "天空蓝", "rgb": (178, 226, 255)}
                ],
                "荧光色系": [
                    {"name": "霓虹绿", "rgb": (57, 255, 20)},
                    {"name": "荧光粉", "rgb": (255, 20, 147)},
                    {"name": "电光紫", "rgb": (191, 0, 255)},
                    {"name": "荧光橙", "rgb": (255, 95, 31)},
                    {"name": "荧光黄", "rgb": (255, 255, 0)},
                    {"name": "荧光蓝", "rgb": (0, 255, 255)},
                    {"name": "荧光红", "rgb": (255, 0, 0)}
                ],
                "复古色系": [
                    {"name": "勃艮第红", "rgb": (128, 0, 32)},
                    {"name": "芥末黄", "rgb": (218, 165, 32)},
                    {"name": "孔雀蓝", "rgb": (0, 128, 128)},
                    {"name": "祖母绿", "rgb": (0, 107, 60)},
                    {"name": "酒红", "rgb": (136, 0, 21)},
                    {"name": "橄榄绿", "rgb": (107, 142, 35)},
                    {"name": "琥珀色", "rgb": (255, 176, 0)}
                ],
                "自然色系": [
                    {"name": "砂岩色", "rgb": (194, 178, 128)},
                    {"name": "苔藓绿", "rgb": (77, 93, 83)},
                    {"name": "陶土红", "rgb": (203, 109, 81)},
                    {"name": "海水蓝", "rgb": (0, 105, 148)},
                    {"name": "树皮棕", "rgb": (102, 68, 34)},
                    {"name": "岩石灰", "rgb": (140, 140, 140)},
                    {"name": "沙漠黄", "rgb": (237, 201, 175)}
                ]
            },
            "特殊色系": {
                "金属色系": [
                    {"name": "金色", "rgb": (212, 175, 55)},
                    {"name": "银色", "rgb": (192, 192, 192)},
                    {"name": "古铜色", "rgb": (205, 127, 50)},
                    {"name": "玫瑰金", "rgb": (183, 110, 121)},
                    {"name": "铂金色", "rgb": (229, 228, 226)},
                    {"name": "铜色", "rgb": (184, 115, 51)},
                    {"name": "铁灰色", "rgb": (100, 100, 100)}
                ],
                "渐变色系": [
                    {"name": "日落渐变1", "rgb": (255, 100, 100)},
                    {"name": "日落渐变2", "rgb": (255, 150, 100)},
                    {"name": "日落渐变3", "rgb": (255, 200, 100)},
                    {"name": "海洋渐变1", "rgb": (0, 50, 100)},
                    {"name": "海洋渐变2", "rgb": (0, 100, 150)},
                    {"name": "海洋渐变3", "rgb": (0, 150, 200)},
                    {"name": "森林渐变1", "rgb": (0, 50, 0)},
                    {"name": "森林渐变2", "rgb": (0, 100, 50)},
                    {"name": "森林渐变3", "rgb": (50, 150, 100)}
                ],
                "透明色系": [
                    {"name": "冰蓝色", "rgb": (200, 230, 255, 150)},
                    {"name": "透明粉", "rgb": (255, 200, 220, 150)},
                    {"name": "透明绿", "rgb": (200, 255, 220, 150)},
                    {"name": "透明黄", "rgb": (255, 255, 200, 150)},
                    {"name": "透明紫", "rgb": (220, 200, 255, 150)},
                    {"name": "透明橙", "rgb": (255, 220, 200, 150)},
                    {"name": "透明灰", "rgb": (220, 220, 220, 150)}
                ]
            },
            "文化/情绪色系": {
                "中国传统色": [
                    {"name": "朱砂红", "rgb": (159, 39, 29)},
                    {"name": "黛青", "rgb": (66, 82, 101)},
                    {"name": "月白", "rgb": (214, 236, 240)},
                    {"name": "秋香黄", "rgb": (217, 182, 17)},
                    {"name": "胭脂", "rgb": (157, 41, 51)},
                    {"name": "石青", "rgb": (0, 128, 128)},
                    {"name": "绛紫", "rgb": (128, 0, 64)}
                ],
                "日本和风色": [
                    {"name": "若竹色", "rgb": (120, 190, 150)},
                    {"name": "樱色", "rgb": (255, 200, 200)},
                    {"name": "朽叶色", "rgb": (210, 150, 0)},
                    {"name": "蓝鼠", "rgb": (92, 84, 112)},
                    {"name": "山吹色", "rgb": (255, 164, 0)},
                    {"name": "抚子色", "rgb": (226, 165, 166)},
                    {"name": "露草色", "rgb": (30, 144, 255)}
                ],
                "忧郁色系": [
                    {"name": "深蓝", "rgb": (0, 0, 139)},
                    {"name": "暗紫", "rgb": (102, 0, 102)},
                    {"name": "灰绿", "rgb": (100, 120, 100)},
                    {"name": "雾灰", "rgb": (150, 150, 150)},
                    {"name": "深灰蓝", "rgb": (47, 79, 79)},
                    {"name": "暗红", "rgb": (139, 0, 0)},
                    {"name": "暗褐", "rgb": (101, 67, 33)}
                ]
            }
        }
    
    def update_color_type_combo(self):
        current_system = self.color_system_combo.currentText()
        self.color_type_combo.clear()
        
        if current_system in self.color_data:
            color_types = list(self.color_data[current_system].keys())
            self.color_type_combo.addItems(color_types)
    
    def generate_colors(self):
        # 清除之前的预览
        for i in reversed(range(self.preview_layout.count())): 
            self.preview_layout.itemAt(i).widget().setParent(None)
        
        # 获取用户选择
        color_system = self.color_system_combo.currentText()
        color_type = self.color_type_combo.currentText()
        color_count = self.color_count_spin.value()
        
        # 获取基础颜色
        if color_system in self.color_data and color_type in self.color_data[color_system]:
            base_colors = self.color_data[color_system][color_type]
        else:
            base_colors = [{"name": "默认", "rgb": (255, 255, 255)}]
        
        # 生成颜色代码
        color_codes = []
        for i in range(color_count):
            # 从基础颜色中循环选择
            base_color = base_colors[i % len(base_colors)]
            r, g, b = base_color["rgb"][:3]  # 只取前三个值，忽略可能的alpha
            
            # 生成变体 - 简单示例，实际可以根据需要实现更复杂的算法
            if color_count > 1:
                factor = i / (color_count - 1)
                r = max(0, min(255, int(r * (1 - factor * 0.2) + 50 * factor)))
                g = max(0, min(255, int(g * (1 - factor * 0.2) + 50 * factor)))
                b = max(0, min(255, int(b * (1 - factor * 0.2) + 50 * factor)))
            
            color_name = f"{base_color['name']}_变体{i+1}"
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            code_line = f"QColor({r}, {g}, {b}),  {hex_code}  // {color_name}"
            color_codes.append(code_line)
            
            # 添加到预览
            color_frame = QFrame()
            color_frame.setFixedHeight(30)
            color_frame.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); border: 1px solid black;")
            
            color_label = QLabel(f"{color_name} {hex_code}")
            if (r*0.299 + g*0.587 + b*0.114) > 150:  # 根据亮度调整文字颜色
                color_label.setStyleSheet("color: black;")
            else:
                color_label.setStyleSheet("color: white;")
            
            frame_layout = QHBoxLayout()
            frame_layout.addWidget(color_label)
            color_frame.setLayout(frame_layout)
            
            self.preview_layout.addWidget(color_frame)
        
        # 更新代码输出
        self.code_output.setPlainText("\n".join(color_codes))
    
    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存颜色代码", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.code_output.toPlainText())
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_output.toPlainText())
    
    def clear_output(self):
        self.code_output.clear()
        for i in reversed(range(self.preview_layout.count())): 
            self.preview_layout.itemAt(i).widget().setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorGeneratorApp()
    window.show()
    sys.exit(app.exec_())