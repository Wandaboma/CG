#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QPushButton,
    QColorDialog,
    QFileDialog,
    QInputDialog,
    QDialog,
    QFormLayout,
    QLabel,
    QSpinBox,
    QDialogButtonBox)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPixmap, QImage, QTransform
from PyQt5.QtCore import QRectF, QSize


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.col = QColor(0, 0, 0)
        
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.origin_list = []
        
    def select_item(self):
        self.status = 'select'

    def start_change_color(self, color):
        self.col = color
    
    def start_reset_canvas(self):
        self.main_window.reset_id()
        if self.status == 'line' or self.status == 'ellipse' or self.status == 'polygon' or self.status == 'curve':
            self.scene().removeItem(self.temp_item)
        for item in self.item_dict:
            self.scene().removeItem(self.item_dict[item])
        self.list_widget.clear()
        self.item_dict = {}
        self.updateScene([self.sceneRect()])
        self.selected_id=''
        self.status=''
        self.temp_item = None
    
    def start_save_canvas(self):
        filename = QFileDialog.getSaveFileName(self, 'Choose File', '', 'Image (*.jpg *.png *.bmp)')
        self.grab(self.sceneRect().toRect()).save(filename[0])
        
    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None
        
    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_id = item_id
        
    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None
        
    def finish_draw_curve(self, item_id):
        if self.temp_item != None:
            if self.status == 'curve' or self.status == 'polygon':
                self.item_dict[item_id] = self.temp_item
                self.list_widget.addItem(item_id)
                self.temp_item = None
                self.finish_draw()
                self.updateScene([self.sceneRect()])
        
    def start_translate(self):
        self.status = 'translate'
        
    def start_rotate(self):
        self.status = 'rotate'
    
    def start_scale(self):
        self.status = 'scale'
        
    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_algorithm = algorithm
    
    def start_polygon_fill(self):
        self.status = 'fill'
        
    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        if selected == '':
                return
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.col, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            #TODO: change into movement
            if self.temp_item == None:
                self.temp_item = MyItem(self.col, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                #print(x)
                #flag = False
                #for i in range(len(self.temp_item.p_list)):
                #    x0, y0 = self.temp_item.p_list[i]
                #    if (x - x0) * (x - x0) + (y - y0) * (y - y0) < 30:
                #        flag = True
                #if flag:
                #    self.item_dict[self.temp_id] = self.temp_item
                #    self.list_widget.addItem(self.temp_id)
                #    self.temp_item = None
                #    self.finish_draw()
                #else:
                self.temp_item.p_list.append((x, y))
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.col, self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'curve':
            if self.temp_item == None:
                self.temp_item = MyItem(self.col, self.temp_id, self.status, [[x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append((x, y))
        elif self.status == 'select':
            selected = self.scene().itemAt(pos, QTransform())
            if self.selected_id != '':
                self.item_dict[self.selected_id].selected = False
                self.item_dict[self.selected_id].update()
            for item in self.item_dict:
                if self.item_dict[item] == selected:
                    self.selected_id = item
            self.item_dict[self.selected_id].selected = True
            self.item_dict[self.selected_id].update()
            self.status = ''
            self.main_window.list_widget.setCurrentRow(int(self.selected_id))
        elif self.status == 'fill':
            self.item_dict[self.selected_id].fill = True
            self.item_dict[self.selected_id].f_list.append((x, y))
        else:
            if self.selected_id != '':
                self.x0 = x
                self.y0 = y  
                self.origin_list = self.item_dict[self.selected_id].p_list    
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'translate':
            if self.selected_id != '':
                temp_list = alg.translate(self.origin_list, x - self.x0, y - self.y0)
                self.item_dict[self.selected_id].p_list = temp_list
        elif self.status == 'rotate':
            if self.selected_id != '':
                if y != self.y0:
                    theta = math.atan(1.0 * (x - self.x0) / (y - self.y0)) * 180 / math.pi
                    temp_list = alg.rotate(self.origin_list, self.x0, self.y0, -int(theta))
                    self.item_dict[self.selected_id].p_list = temp_list
        elif self.status == 'scale':
            if self.selected_id != '':
                t = ((x - self.x0) * (x - self.x0) + (y - self.y0) * (y - self.y0)) ** 0.5    
                t = t / 30
                temp_list = alg.scale(self.origin_list, self.x0, self.y0, t)
                self.item_dict[self.selected_id].p_list = temp_list
        elif self.status == 'clip':
            if self.selected_id != '':
                self.x1 = x
                self.y1 = y
            
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'clip':
            if self.selected_id != '':
                temp_list = alg.clip(self.origin_list, self.x0, self.y0, self.x1, self.y1, self.temp_algorithm)
                self.item_dict[self.selected_id].p_list = temp_list
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_color: QColor, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.col = item_color
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.fill = False
        self.f_list = []

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.col)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.fill == True:
                fill_pixels = alg.fill(self.p_list, self.f_list, item_pixels)
                for p in fill_pixels:
                    painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                
    def boundingRect(self) -> QRectF:
        x = 1000
        y = 1000
        for i in range(len(self.p_list)):
            x0, y0 = self.p_list[i]
            x = min(x0, x)
            y = min(y0, y)
        w = 0
        h = 0
        for i in range(len(self.p_list)):
            x0, y0 = self.p_list[i]
            w = max(w, x0)
            h = max(h, y0)
        w = w - x
        h = h - y
        return QRectF(x - 1, y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        #confirm button
        self.btn = QPushButton('OK', self)
        self.btn.setFixedSize(40, 30)
        
        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')
        addition_func_menu = menubar.addMenu('附加功能')
        select_item_act = addition_func_menu.addAction('选择图元')
        polygon_addition_menu = addition_func_menu.addMenu('多边形')
        polygon_fill_act = polygon_addition_menu.addAction('多边形填充')
        polygon_clip_act = polygon_addition_menu.addAction('多边形裁剪')
        
        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        self.btn.clicked.connect(self.on_click)
        select_item_act.triggered.connect(self.select_item_action)
        polygon_fill_act.triggered.connect(self.polygon_fill_action)
        
        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        #TODO: move button to down below
        self.hbox_layout.addWidget(self.btn)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def reset_id(self):
        self.item_cnt = 0
        
    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
    
    def get_present_id(self):
        _id = str(self.item_cnt)
        return _id 
        
    def set_pen_action(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvas_widget.start_change_color(col)
     
    def reset_canvas_action(self):
        self.canvas_widget.start_reset_canvas()
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
        dialog = QDialog()
        form = QFormLayout(dialog)
        box1 = QSpinBox(dialog)
        box1.setRange(100, 1000)
        box2 = QSpinBox(dialog)
        box2.setRange(100, 1000)
        form.addRow('Width:', box1)
        form.addRow('Height:', box2)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        form.addRow(buttonBox)
        
        if dialog.exec():
            self.w = box1.value()
            self.h = box2.value()
            self.scene.setSceneRect(0, 0, self.w, self.h)
            self.canvas_widget.resize(self.w,self.h)
            self.canvas_widget.setFixedSize(self.w, self.h)
            self.statusBar().showMessage('空闲')
            self.setMaximumHeight(self.h)
            self.setMaximumWidth(self.w)
            self.resize(self.w, self.h)
    
    def save_canvas_action(self):
        self.canvas_widget.start_save_canvas()
    
    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('图元平移')
        
    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('图元旋转')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('图元缩放')
        
    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法对线段裁剪')
        
    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky算法对线段裁剪') 
        
    def on_click(self):
        self.canvas_widget.finish_draw_curve(self.get_present_id())
        
    def select_item_action(self):
        self.canvas_widget.select_item()
        self.statusBar().showMessage('鼠标点击选择图元')
        
    def polygon_fill_action(self):
        self.canvas_widget.start_polygon_fill()
        self.statusBar().showMessage('多边形填充')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
