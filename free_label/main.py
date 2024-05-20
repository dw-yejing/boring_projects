import sys
import os
import re
from pathlib import Path
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, qApp, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap, QImage, QCursor, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint, QRect
import tempfile
pattern = re.compile(r"[\s\S]*\.(png|jpg)$", re.IGNORECASE)
def is_img(fname):
    return pattern.match(fname)
     

class Canvas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMinimumSize(800, 600)
        self.setMaximumSize(4000, 4000)
        self.showMaximized()
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.label_boxes = []
        self.radius = 10
        self.save_path = tempfile.gettempdir()
        self.box_size = 10

    def init_stat(self):
        self.label_boxes = []

    def initUI(self):    
        self.setWindowTitle("Image Viewer")
        
        # 设置状态栏
        # 调用 QtGui.QMainWindow 类的 statusBar() 方法，创建状态栏
        self.statusBar().showMessage('Ready')
        self.label_box_size_text = "已经标注了 0 个"
        self.label_box_size_label = QLabel(self.label_box_size_text, self)
        self.statusBar().addWidget(self.label_box_size_label)

        # 设置菜单栏
        # QAction 是菜单栏、工具栏或者快捷键的动作的组合

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.open_action = QAction("Open Folder", self)
        self.open_action.triggered.connect(self.open_image)
        
        self.save_action = QAction("Setting Save Path", self)
        self.save_action.triggered.connect(self.save_image)
        
        self.prev_action = QAction("Previous Image", self)
        self.prev_action.setShortcut('a')
        self.prev_action.triggered.connect(self.prev_image)
        
        self.next_action = QAction("Next Image", self)
        self.next_action.setShortcut('d')
        self.next_action.triggered.connect(self.next_image)

        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut('r')
        self.redo_action.triggered.connect(self.redo)

        self.back_action = QAction("Back", self)
        self.back_action.setShortcut('b')
        self.back_action.triggered.connect(self.back)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut('s')
        self.save_action.triggered.connect(self.save)

        self.bs_setting_action = QAction("BoxSize Setting", self)
        self.bs_setting_action.triggered.connect(self.set_size)
        
        self.radius_setting_action = QAction("Radius Setting", self)
        self.radius_setting_action.triggered.connect(self.set_radius)
        
        self.save_setting_action = QAction("Save Path Setting", self)
        self.save_setting_action.triggered.connect(self.set_save)

        # menuBar() 创建菜单栏。这里创建了一个菜单栏，并用 addMenu() 在上面添加了一个 file 菜单，用 addAction() 关联了点击退出应用的事件。
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        setting_menu = menubar.addMenu("Setting")
        setting_menu.addAction(self.bs_setting_action)
        setting_menu.addAction(self.radius_setting_action)
        setting_menu.addAction(self.save_setting_action)
        
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addAction(self.prev_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addAction(self.redo_action)
        self.toolbar.addAction(self.back_action)
        self.toolbar.addAction(self.save_action)
        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.images = []  # 存储图片路径
        self.image_names = []
        self.current_image_index = 0  # 当前显示图片的索引
    
    def open_image(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        files = os.listdir(folder_path)
        files = [fname for fname in files if is_img(fname)]
        if len(files)<1:
            self.show_message_box('no image')
            return
        # 初始化
        self.images = []
        self.image_names = []
        self.init_stat()

        ffiles = [str(Path(folder_path, fname)) for fname in files] # full-path-name file
        self.images.extend(ffiles)
        self.image_names.extend(files)
        self.current_image_index = 0  # 更新当前显示图片的索引
        self.show_image()
    
    def save_image(self):
        if not self.image:
            self.show_message_box('no image')
        pixmap = self.image_label.pixmap()
        if pixmap:
            pixmap.save(str(Path(self.save_path, self.image_name)))
        res_data = [(item[0], item[1], self.box_size, self.box_size)  for item in self.label_boxes]
        with open(str(Path(self.save_path, self.image_name+".txt")), 'w') as f:
            for line in res_data:
                line = " ".join([str(item) for item in line])
                f.write(line+'\n')
                
            

    def prev_image(self):
        if self.current_image_index < 1:
            self.show_message_box('this is the first image')
            return
        self.save_image()
        self.init_stat()
        self.current_image_index -= 1
        self.show_image()
    
    def next_image(self):
        if self.current_image_index >= len(self.images) - 1:
            self.show_message_box('this is the last image')
            return
        self.save_image()
        self.init_stat()
        self.current_image_index += 1
        self.show_image()

    def redo(self):
        self.init_stat()
        self.draw_all_label_box()

    def back(self):
        if self.label_boxes:
            self.label_boxes.pop()
        self.draw_all_label_box()

    def set_size(self):
        text, ok = QInputDialog.getText(self, 'Input Box Scale', 'Box Size:')
        if ok:
            self.box_size = int(text)

    def set_radius(self):
        text, ok = QInputDialog.getText(self, 'Input Point Radius', 'Radius:')
        if ok:
            self.radius = int(text)

    def set_save(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")

    def save(self):
        self.save_image()
        self.show_message_box(f"文件保存成功，保存路径：{self.save_path}")
        # if self.current_image_index >= len(self.images) - 1:
        #     self.show_message_box('this is the last image')
        #     return
        # self.current_image_index += 1
        # self.show_image()   

    def mouseReleaseEvent(self, event):
        if not self.image:
            return
        mouse_pos = event.pos()  # 获取鼠标点击事件发生的坐标
        label_pos = self.image_label.mapFrom(self, mouse_pos)  # 获取鼠标点击位置相对于 QLabel 的坐标
         # 获取图片的尺寸
        image_width = self.image.width()
        image_height = self.image.height()

        # 获取 QLabel 的尺寸
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        # 计算偏移
        offset_x = self.image_label.width()//2 - self.pixmap.width()//2
        offset_y = self.image_label.height()//2 - self.pixmap.height()//2

        # 计算鼠标点击位置相对于原始图片的坐标
        image_x = int((label_pos.x()-offset_x)/ pixmap_width * image_width)
        image_y = int((label_pos.y()-offset_y) / pixmap_height * image_height)
        if image_x<0 or image_x>image_width or image_y<0 or image_y> image_height:
            return

        self.label_boxes.append((image_x, image_y))
        self.label_box_size_label.setText(f"已经标注了{str(len(self.label_boxes)) }个")

        
        print(f'image_x:{image_x} image_y:{image_y} pos_x:{event.pos().x()} pos_y:{event.pos().y()} label_x:{label_pos.x()} label_y:{label_pos.y()}')
 
        # 绘制标注框
        self.draw_all_label_box()

    # 根据列表内容绘制所有的标注框
    def draw_all_label_box(self):
        if not self.image:
            return
        pixmap = QPixmap.fromImage(self.image)
        pen = QPen(Qt.GlobalColor.blue, 0)
        brush = QBrush(Qt.GlobalColor.blue)  # 设置画刷颜色为蓝色
        
        with QPainter(pixmap) as painter:
            painter.setPen(pen)
            painter.setBrush(brush)
            for label_box in self.label_boxes:
                r = self.radius 
                x,y = label_box[0]-r, label_box[1]-r 
                center = QPoint(*label_box)
                painter.drawEllipse(center, r, r)
                print(f'draw pt: {x}, {y}')
        pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)


    def onLineEditChanged(self, text):
        self.label.setText("标注尺寸为: " + text + " x " + text)
        self.label.adjustSize()
        self.label_box_size = int(text) 
    
    def show_image(self):
        self.overrideCursor(Qt.CrossCursor)
        image = QImage(self.images[self.current_image_index])
        self.image = image
        self.image_name = self.image_names[self.current_image_index]
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.pixmap = pixmap
        self.image_label.setPixmap(pixmap)
        pass

    def show_message_box(self, text, title="Message Box", icon=QMessageBox.Information):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    def mouseMoveEvent(self, event):
        # 设置全局鼠标光标形状为十字形
        self.overrideCursor(Qt.CrossCursor)

    def overrideCursor(self, cursor):
        self.restoreCursor()
        self._cursor = cursor
        QApplication.setOverrideCursor(cursor)

    def restoreCursor(self):
        QApplication.restoreOverrideCursor()    

   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Canvas()
    window.show()
    sys.exit(app.exec_())
