from manim import *
import numpy as np

class FloatingWindTurbine(Scene):
    def construct(self):
        # 设置场景背景为浅蓝色
        self.camera.background_color = "#E6F3FF"
        
        # 创建标题
        title = Text("浮式风力发电机", font_size=32, color=BLACK)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # 显示完整的浮式风力发电机
        self.show_floating_turbine()
        self.wait(3)
    
    def show_floating_turbine(self):
        """显示浮式风力发电机"""
        # 创建海底
        seabed = Rectangle(width=14, height=2, color="#8B4513", fill_opacity=1)
        seabed.to_edge(DOWN, buff=0)
        
        # 创建海水
        water = Rectangle(width=14, height=4, color="#4682B4", fill_opacity=0.7)
        water.move_to(UP*1)
        
        # 创建水面波浪
        water_surface = FunctionGraph(
            lambda x: 0.1 * np.sin(2 * PI * x),
            x_range=[-7, 7],
            color="#87CEEB",
            stroke_width=3
        )
        water_surface.move_to(UP*3)
        
        # 创建浮动平台
        platform = RoundedRectangle(width=2.1, height=0.32, corner_radius=0.06, color="#C9915D", fill_opacity=1)
        platform.move_to(UP*2.85)
        
        # 创建塔架
        tower = Rectangle(width=0.2, height=4, color="#D2D8E0", fill_opacity=1)
        tower.move_to(platform.get_top() + UP*(tower.height/2))
        
        # 创建机舱
        nacelle = RoundedRectangle(width=0.8, height=0.3, corner_radius=0.08, color="#ECEFF4", fill_opacity=1)
        nacelle.move_to(tower.get_top() + UP*0.15 + RIGHT*0.08)
        
        # 创建风机轮毂
        hub = Circle(radius=0.1, color="#59606A", fill_opacity=1)
        hub.move_to(nacelle.get_right() + RIGHT*0.03)
        
        # 创建三个叶片
        blade_length = 1.5
        blade1 = Line(hub.get_center(), 
                     hub.get_center() + UP*blade_length, 
                     stroke_width=6, color="#E3E7ED")
        blade2 = Line(hub.get_center(), 
                     hub.get_center() + np.array([blade_length*np.cos(2*PI/3), blade_length*np.sin(2*PI/3), 0]), 
                     stroke_width=6, color="#E3E7ED")
        blade3 = Line(hub.get_center(), 
                     hub.get_center() + np.array([blade_length*np.cos(4*PI/3), blade_length*np.sin(4*PI/3), 0]), 
                     stroke_width=6, color="#E3E7ED")
        
        blades = VGroup(blade1, blade2, blade3)
        
        # 创建叶片旋转圈（虚线）
        rotor_circle = Circle(radius=blade_length, color="#87CEEB", stroke_width=2)
        rotor_circle.move_to(hub.get_center())
        rotor_circle.set_stroke(opacity=0.5)
        
        # 创建锚链系统
        anchor_chains = VGroup()
        anchor_weights = VGroup()
        
        # 左侧锚链
        left_chain = self.create_anchor_chain(
            start=platform.get_center() + LEFT*0.8 + DOWN*0.15,
            end=LEFT*4 + DOWN*1.5,
            num_links=15
        )
        left_weight = Rectangle(width=0.3, height=0.2, color="#FFD700", fill_opacity=1)
        left_weight.move_to(LEFT*4 + DOWN*1.5)
        
        # 右侧锚链
        right_chain = self.create_anchor_chain(
            start=platform.get_center() + RIGHT*0.8 + DOWN*0.15,
            end=RIGHT*4 + DOWN*1.5,
            num_links=15
        )
        right_weight = Rectangle(width=0.3, height=0.2, color="#FFD700", fill_opacity=1)
        right_weight.move_to(RIGHT*4 + DOWN*1.5)
        
        anchor_chains.add(left_chain, right_chain)
        anchor_weights.add(left_weight, right_weight)
        
        # 添加标注
        labels = VGroup()
        
        # 深度标注
        depth_label = Text("h", font_size=24, color=BLACK)
        depth_label.move_to(RIGHT*6 + UP*1)
        depth_arrow = Arrow(RIGHT*6 + UP*3, RIGHT*6 + DOWN*1, color=BLACK)
        
        # 平台尺寸标注
        platform_label = Text("Lb", font_size=20, color=BLACK)
        platform_label.move_to(UP*2.3)
        
        # 吃水标注
        draft_label = Text("Hb", font_size=20, color=BLACK)
        draft_label.move_to(RIGHT*1.5 + UP*2.7)
        
        # 塔架标注
        tower_label = Text("Lmt", font_size=20, color=BLACK)
        tower_label.move_to(LEFT*0.8 + UP*5)
        
        # 机舱标注
        nacelle_label = Text("Drot", font_size=20, color=BLACK)
        nacelle_label.move_to(UP*7.5)
        
        labels.add(depth_label, depth_arrow, platform_label, draft_label, tower_label, nacelle_label)
        
        # 动画序列
        self.play(
            DrawBorderThenFill(seabed),
            DrawBorderThenFill(water),
            Create(water_surface)
        )
        
        self.play(
            DrawBorderThenFill(platform),
            DrawBorderThenFill(tower),
            DrawBorderThenFill(nacelle),
            DrawBorderThenFill(hub)
        )
        
        self.play(
            Create(blades),
            Create(rotor_circle, run_time=2)
        )
        
        self.play(
            Create(anchor_chains),
            DrawBorderThenFill(anchor_weights)
        )
        
        self.play(
            Write(labels)
        )
        
        # 叶片旋转动画
        self.play(
            Rotate(blades, angle=2*PI, about_point=hub.get_center(), rate_func=linear, run_time=3),
            # 添加轻微的浮动效果
            platform.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back),
            tower.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back),
            nacelle.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back),
            hub.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back),
            blades.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back),
            rotor_circle.animate.shift(UP*0.05).set_rate_func(rate_functions.there_and_back)
        )
    
    def create_anchor_chain(self, start, end, num_links):
        """创建锚链"""
        chain = VGroup()
        
        # 计算链条路径
        start_point = np.array(start)
        end_point = np.array(end)
        
        # 创建悬链线效果
        chain_points = []
        for i in range(num_links):
            t = i / (num_links - 1)
            # 悬链线公式
            x = start_point[0] + t * (end_point[0] - start_point[0])
            y = start_point[1] + t * (end_point[1] - start_point[1])
            # 添加悬链线的下垂效果
            sag = 0.5 * np.sin(PI * t)
            y -= sag
            chain_points.append([x, y, 0])
        
        # 创建链条
        chain_line = VMobject()
        chain_line.set_points_as_corners(chain_points)
        chain_line.set_stroke(color=BLACK, width=3)
        
        return chain_line

# 运行场景的类
if __name__ == "__main__":
    # 可以通过命令行运行: manim main.py FloatingWindTurbine
    pass
