from manim import *


class CS2MindMap(Scene):
    def construct(self):
        # Main title
        cs2 = Text("CS2", font_size=72)
        cs2.move_to(UP * 3)
        self.play(Write(cs2))

        # First level (tighter buff so all five fit later)
        communication = Text("Communication", font_size=28)
        economy = Text("Economy", font_size=28)
        strategy = Text("Strategy", font_size=28)
        mechanics = Text("Mechanics", font_size=28)

        first_level_labels = [communication, economy, strategy, mechanics]
        first_level = VGroup(*first_level_labels)
        first_level.arrange(RIGHT, buff=1.0)  # smaller buff
        first_level.move_to(UP * 0.8)

        cs2_to_strategy_line = None
        first_level_lines = []

        for label in first_level_labels:
            line = Line(cs2.get_bottom(), cs2.get_bottom(), stroke_width=4)
            self.add(line)
            if label is strategy:
                cs2_to_strategy_line = line
            first_level_lines.append(line)
            self.play(
                line.animate.put_start_and_end_on(cs2.get_bottom(), label.get_top()),
                run_time=0.8,
            )
            self.play(Write(label), run_time=0.3)

        # Strategy → Early Round, Mid Round, Afterplant
        early_round = Text("Early Round", font_size=22)
        mid_round = Text("Mid Round", font_size=22)
        afterplant = Text("Afterplant", font_size=22)
        strategy_children = VGroup(early_round, mid_round, afterplant)
        strategy_children.arrange(RIGHT, buff=0.8)
        strategy_children.next_to(strategy, DOWN, buff=1.2)

        strategy_to_early_round_line = None
        for label in strategy_children:
            line = Line(strategy.get_bottom(), strategy.get_bottom(), stroke_width=3)
            self.add(line)
            if label is early_round:
                strategy_to_early_round_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    strategy.get_bottom(), label.get_top()
                ),
                run_time=0.6,
            )
            self.play(Write(label), run_time=0.3)

        # Third level: Early Round → Information, Map Control
        information = Text("Information", font_size=20)
        map_control = Text("Map Control", font_size=20)
        early_round_children = VGroup(information, map_control)
        early_round_children.arrange(RIGHT, buff=0.6)
        early_round_children.next_to(early_round, DOWN, buff=0.8)

        early_round_to_information_line = None
        for label in early_round_children:
            line = Line(
                early_round.get_bottom(), early_round.get_bottom(), stroke_width=2
            )
            self.add(line)
            if label is information:
                early_round_to_information_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    early_round.get_bottom(), label.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        # Fourth level: Information → jiggle, jumpspot, pixel angle, awp hold
        jiggle = Text("jiggle", font_size=18)
        jumpspot = Text("jumpspot", font_size=18)
        pixel_angle = Text("pixel angle", font_size=18)
        awp_hold = Text("awp hold", font_size=18)
        info_children = VGroup(jiggle, jumpspot, pixel_angle, awp_hold)
        info_children.arrange(RIGHT, buff=0.5)
        info_children.next_to(information, DOWN, buff=0.8)

        info_child_lines = []
        for label in info_children:
            line = Line(
                information.get_bottom(), information.get_bottom(), stroke_width=2
            )
            self.add(line)
            info_child_lines.append(line)
            self.play(
                line.animate.put_start_and_end_on(
                    information.get_bottom(), label.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        # Yellow cascade down the Strategy pathway
        self.play(cs2.animate.set_color(YELLOW), run_time=0.4)
        self.play(cs2_to_strategy_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(strategy.animate.set_color(YELLOW), run_time=0.4)
        self.play(strategy_to_early_round_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(early_round.animate.set_color(YELLOW), run_time=0.4)
        self.play(
            early_round_to_information_line.animate.set_stroke(YELLOW), run_time=0.4
        )
        self.play(information.animate.set_color(YELLOW), run_time=0.4)

        for line, label in zip(info_child_lines, info_children):
            self.play(line.animate.set_stroke(YELLOW), run_time=0.3)
            self.play(label.animate.set_color(YELLOW), run_time=0.3)

        self.wait(2)


class ManyQuestionMarks(Scene):
    def construct(self):
        # --- Root ---
        cs2 = Text("CS2", font_size=72, color=BLUE)
        cs2.move_to(UP * 3.5)
        self.play(Write(cs2))
        self.wait(0.2)

        # --- Level 1: three direct children ---
        level1_nodes = VGroup(*[Text("?", font_size=36) for _ in range(3)])
        level1_nodes.arrange(RIGHT, buff=2.0)
        level1_nodes.move_to(UP * 1.5)

        level1_lines = VGroup()
        for node in level1_nodes:
            line = Line(cs2.get_bottom(), node.get_top(), stroke_width=4)
            level1_lines.add(line)
            self.play(Create(line), Write(node), run_time=0.4)
        self.wait(0.3)

        current_parents = list(level1_nodes)
        # Font sizes and horizontal spreads for 4 more generations
        font_sizes = [24, 18, 14, 12]
        spread_factors = [1.0, 0.7, 0.5, 0.35]  # how far children move left/right

        all_bottom_lines = VGroup()  # to later highlight the final connections

        for depth, (fs, spread) in enumerate(zip(font_sizes, spread_factors)):
            new_parents = []
            for parent in current_parents:
                left_child = Text("?", font_size=fs)
                right_child = Text("?", font_size=fs)
                # Place children below parent, shifted horizontally
                offset = spread * 1.5  # small for readability
                left_child.move_to(parent.get_bottom() + DOWN * 0.5 + LEFT * offset)
                right_child.move_to(parent.get_bottom() + DOWN * 0.5 + RIGHT * offset)

                line_left = Line(
                    parent.get_bottom(), left_child.get_top(), stroke_width=1.2
                )
                line_right = Line(
                    parent.get_bottom(), right_child.get_top(), stroke_width=1.2
                )

                # Animate
                self.play(
                    Create(line_left),
                    Write(left_child),
                    Create(line_right),
                    Write(right_child),
                    run_time=0.25,
                )
                new_parents.append(left_child)
                new_parents.append(right_child)

                if depth == len(font_sizes) - 1:  # last layer
                    all_bottom_lines.add(line_left, line_right)

            current_parents = new_parents
            self.wait(0.1)

        # --- Highlight the deepest level as "fundamental" ---
        deepest_nodes = VGroup(*current_parents)
        self.play(
            deepest_nodes.animate.set_color(YELLOW),
            all_bottom_lines.animate.set_stroke(YELLOW),
            run_time=1.2,
        )
        fundamental_text = Text("Fundamental aspects", font_size=28, color=YELLOW)
        fundamental_text.next_to(deepest_nodes, DOWN, buff=1.2)
        self.play(Write(fundamental_text))
        self.wait(2)


class Restaurant(Scene):
    def construct(self):
        # -------------------------------------------------------
        # PART 1 – FIVE RESTAURANTS OPENING SIMULTANEOUSLY
        # -------------------------------------------------------
        title = Text("5 Simultaneous Restaurant Openings", font_size=44, color=YELLOW)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP))

        ground = Line(LEFT * 6, RIGHT * 6, stroke_width=4, color=GREY)
        ground.to_edge(DOWN, buff=1.5)
        self.play(Create(ground))

        restaurants = VGroup()
        for _ in range(5):
            restaurants.add(self.create_restaurant())
        restaurants.arrange(RIGHT, buff=1.5)
        restaurants.next_to(ground, UP, buff=0)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.5) for r in restaurants], lag_ratio=0.2)
        )
        self.wait(0.5)

        open_signs = VGroup()
        for r in restaurants:
            sign = Text("OPEN", font_size=24, color=GREEN, weight=BOLD)
            sign.next_to(r, UP, buff=0.25)
            open_signs.add(sign)
        self.play(LaggedStart(*[Write(s) for s in open_signs], lag_ratio=0.1))
        self.wait(0.8)

        problems = [
            ("Hiring wrong\npeople", "🙅"),
            ("Payroll\nissues", "💰"),
            ("No walk-in\ncustomers", "🚶"),
        ]

        problem_stacks = [VGroup() for _ in range(5)]
        # Store only the y-coordinate (float) of the top of each stack
        problem_tops = [open_signs[i].get_top()[1] for i in range(5)]

        for prob_text, prob_emoji in problems:
            central_prob = self.create_problem_mobject(prob_text, prob_emoji, scale=1.6)
            central_prob.move_to(ORIGIN)
            self.play(FadeIn(central_prob, scale=0.5))
            self.wait(0.8)

            small_probs = []
            for i, r in enumerate(restaurants):
                small = self.create_problem_mobject(prob_text, prob_emoji, scale=0.7)
                # Place above the current top of the stack
                new_y = problem_tops[i] + small.get_height() / 2 + 0.2
                small.move_to(ORIGIN)
                small.align_to(open_signs[i], LEFT)
                small.shift(UP * new_y)
                small_probs.append(small)
                problem_stacks[i].add(small)
                # Update top y-coordinate for next iteration
                problem_tops[i] = small.get_top()[1]

            self.play(
                FadeOut(central_prob),
                *[FadeIn(small, shift=UP * 0.1) for small in small_probs],
                run_time=1.0,
            )
            self.wait(0.6)

        final_restaurant_msg = Text(
            "Every location suffers the same fate.", font_size=28, color=YELLOW
        )
        final_restaurant_msg.next_to(restaurants, DOWN, buff=1.2)
        self.play(Write(final_restaurant_msg))
        self.wait(3)

        # Fade out everything
        all_elements = VGroup(
            ground, restaurants, open_signs, *problem_stacks, final_restaurant_msg
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.wait(0.5)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def create_restaurant(self, color=BLUE, scale=1.0):
        building = RoundedRectangle(
            width=1.4,
            height=1.8,
            corner_radius=0.1,
            fill_color=color,
            fill_opacity=0.6,
            stroke_color=WHITE,
            stroke_width=2,
        )
        door = Rectangle(width=0.35, height=0.8, fill_color=DARKER_GREY, stroke_width=1)
        door.move_to(building.get_bottom() + UP * 0.4)
        window = Rectangle(width=0.3, height=0.3, fill_color=WHITE, stroke_width=1)
        window.move_to(building.get_top() + DOWN * 0.4 + RIGHT * 0.3)
        sign = Text("RESTAURANT", font_size=14, color=WHITE)
        sign.move_to(building.get_top() + DOWN * 0.5 + LEFT * 0.2)
        return VGroup(building, door, window, sign)

    def create_problem_mobject(self, text, emoji, scale=1.0):
        circ = Circle(radius=0.4, color=RED, fill_opacity=0.85, stroke_width=2)
        emoji_text = Text(emoji, font_size=int(32 * scale))
        emoji_text.move_to(circ.get_center())
        icon = VGroup(circ, emoji_text)
        label = Text(text, font_size=int(16 * scale), color=WHITE, weight=BOLD)
        label.next_to(icon, DOWN, buff=0.15)
        group = VGroup(icon, label)
        group.scale(scale)
        return group


class ProficiencyBars(Scene):
    # --- Customizable data: override in subclasses ---
    LABELS = ["Communication", "Economy", "Strategy", "Mechanics"]
    PROFICIENCIES = [0.5, 0.7, 0.25, 0.5]
    COLORS = [BLUE, GREEN, PURPLE, RED]
    TITLE_TEXT = "Skill Proficiency Levels"
    # ----------------------------------------------

    def construct(self):
        bar_width = 1.0
        max_height = 4.0
        bar_bottom = -2.5
        x_positions = [-4.5, -1.5, 1.5, 4.5]

        # Title
        title = Text(self.TITLE_TEXT, font_size=42)
        title.to_edge(UP)
        self.add(title)

        rects = []
        percent_trackers = []
        percent_displays = []

        for i in range(len(self.LABELS)):
            rect = Rectangle(
                width=bar_width,
                height=0,
                fill_color=self.COLORS[i],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2,
            )
            rect.move_to([x_positions[i], bar_bottom, 0])
            rects.append(rect)

            label = Text(self.LABELS[i], font_size=30)
            label.next_to(rect, DOWN, buff=0.2)
            self.add(label)

            tracker = ValueTracker(0)
            percent_trackers.append(tracker)

            # Capturing loop variables by default argument
            def make_percent_text(t=tracker, r=rect):
                val = int(t.get_value())
                txt = Text(f"{val}%", font_size=28, color=WHITE)
                txt.next_to(r, UP, buff=0.15)
                return txt

            percent_display = always_redraw(make_percent_text)
            percent_displays.append(percent_display)

        self.add(*rects, *percent_displays)

        # --- Animate bars and trackers ---
        bar_animations = []
        for rect, p in zip(rects, self.PROFICIENCIES):
            target_height = p * max_height
            target_rect = Rectangle(
                width=bar_width,
                height=target_height,
                fill_color=rect.fill_color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2,
            )
            target_rect.move_to(
                [rect.get_center()[0], bar_bottom + target_height / 2, 0]
            )
            bar_animations.append(Transform(rect, target_rect))

        tracker_animations = [
            tracker.animate.set_value(p * 100)
            for tracker, p in zip(percent_trackers, self.PROFICIENCIES)
        ]

        self.play(
            LaggedStart(*bar_animations, lag_ratio=0.2),
            LaggedStart(*tracker_animations, lag_ratio=0.2),
            run_time=2.5,
        )

        # --- Highlight the lowest proficiency permanently ---
        lowest_idx = self.PROFICIENCIES.index(min(self.PROFICIENCIES))
        low_rect = rects[lowest_idx]
        low_percent_display = percent_displays[lowest_idx]

        self.play(
            Indicate(low_rect, scale_factor=1.2, color=YELLOW),
            Indicate(low_percent_display, scale_factor=1.2, color=YELLOW),
        )

        low_percent_display.clear_updaters()
        final_val = int(self.PROFICIENCIES[lowest_idx] * 100)
        highlighted_percent = Text(f"{final_val}%", font_size=28, color=YELLOW)
        highlighted_percent.move_to(low_percent_display.get_center())

        glow_rect = low_rect.copy()
        glow_rect.set_stroke(color=YELLOW, width=10, opacity=0.6)
        glow_rect.set_fill(opacity=0)
        glow_rect.scale(1.1)
        glow_rect.set_z_index(low_rect.z_index - 1)

        self.play(
            low_rect.animate.set_stroke(color=YELLOW, width=6),
            Transform(low_percent_display, highlighted_percent),
            FadeIn(glow_rect),
            run_time=0.5,
        )

        self.wait(5)


class Strategy(ProficiencyBars):
    LABELS = ["Early Round", "Mid Round", "Afterplant"]
    PROFICIENCIES = [0.3, 0.3, 0.3]
    COLORS = [BLUE, YELLOW, RED]
    TITLE_TEXT = "Strategy Proficiency Levels"


class EarlyRound(ProficiencyBars):
    LABELS = ["Information", "Map Control"]
    PROFICIENCIES = [0.1, 0.4]
    COLORS = [BLUE, YELLOW]
    TITLE_TEXT = "Early Round Proficiency Levels"


class Information(ProficiencyBars):
    LABELS = ["Jiggle", "Jumpspot", "Pixel Angle", "AWP Hold"]
    PROFICIENCIES = [0, 0.5, 0.1, 0.5]
    COLORS = [BLUE, YELLOW, RED, ORANGE]
    TITLE_TEXT = "Information Proficiency Levels"


class ProgressLadders(Scene):
    def construct(self):
        # Positions
        left_x = -4
        right_x = 4

        # --- Build left ladder (beginner) ---
        left_rail1 = Line([left_x - 0.4, -2, 0], [left_x - 0.4, 2, 0], color=GREEN)
        left_rail2 = Line([left_x + 0.4, -2, 0], [left_x + 0.4, 2, 0], color=GREEN)
        left_y_positions = [-2, -1, 0, 1, 2]  # 5 rungs
        left_rungs = VGroup()
        for y in left_y_positions:
            left_rungs.add(
                Line([left_x - 0.4, y, 0], [left_x + 0.4, y, 0], color=GREEN)
            )

        # --- Build right ladder (expert) ---
        right_rail1 = Line([right_x - 0.4, -2, 0], [right_x - 0.4, 2, 0], color=BLUE)
        right_rail2 = Line([right_x + 0.4, -2, 0], [right_x + 0.4, 2, 0], color=BLUE)
        right_y_positions = np.linspace(-2, 2, 21)  # 21 tiny rungs
        right_rungs = VGroup()
        for y in right_y_positions:
            right_rungs.add(
                Line([right_x - 0.4, y, 0], [right_x + 0.4, y, 0], color=BLUE)
            )

        # Animate construction
        self.play(
            Create(left_rail1),
            Create(left_rail2),
            Create(right_rail1),
            Create(right_rail2),
        )
        self.play(
            Create(left_rungs, lag_ratio=0.1, run_time=1),
            Create(right_rungs, lag_ratio=0.02, run_time=4),
        )

        # --- Climbers ---
        left_dot = Dot(point=[left_x, -2, 0], color=GREEN, radius=0.12)
        right_dot = Dot(point=[right_x, -2, 0], color=BLUE, radius=0.12)
        self.play(FadeIn(left_dot), FadeIn(right_dot))

        # Paths along rung heights
        def climb_path(x, y_list):
            points = [np.array([x, y_list[0], 0])]
            for y in y_list[1:]:
                points.append(np.array([x, y, 0]))
            return VMobject().set_points_as_corners(points)

        left_path = climb_path(left_x, left_y_positions)
        right_path = climb_path(right_x, right_y_positions)

        # Simultaneous climb – green finishes much faster
        self.play(
            MoveAlongPath(left_dot, left_path, run_time=2, rate_func=linear),
            MoveAlongPath(right_dot, right_path, run_time=8, rate_func=linear),
        )

        self.wait(0.5)

        # --- Reveal texts (labels now at midpoint: 2.4) ---
        title = Text("0 → 50 is often easier than 95 → 99", font_size=42).to_edge(UP)

        left_label = Text("0 → 50", font_size=36, color=GREEN)
        left_label.move_to(LEFT * 4 + UP * 2.4)  # exact middle between 2.0 and 2.8
        right_label = Text("95 → 99", font_size=36, color=BLUE)
        right_label.move_to(RIGHT * 4 + UP * 2.4)

        footer = Text(
            "Each improvement gets harder as you approach mastery", font_size=26
        ).to_edge(DOWN)

        self.play(
            FadeIn(title),
            FadeIn(left_label),
            FadeIn(right_label),
            FadeIn(footer),
        )
        self.wait(3)


class MechanicsTree(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Root
        # ------------------------------------------------------------
        mechanics = Text("Mechanics", font_size=48)
        mechanics.move_to(UP * 3)
        self.play(Write(mechanics))

        # ------------------------------------------------------------
        # First level: Aim & Movement
        # ------------------------------------------------------------
        aim = Text("Aim", font_size=28)
        movement = Text("Movement", font_size=28)
        first_children = VGroup(aim, movement)
        first_children.arrange(RIGHT, buff=1.5)
        first_children.next_to(mechanics, DOWN, buff=1.2)

        mech_to_aim_line = None
        mech_to_movement_line = None

        for child in [aim, movement]:
            line = Line(mechanics.get_bottom(), mechanics.get_bottom(), stroke_width=4)
            self.add(line)
            if child is aim:
                mech_to_aim_line = line
            else:
                mech_to_movement_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    mechanics.get_bottom(), child.get_top()
                ),
                run_time=0.8,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Second level: Aim's four children
        # ------------------------------------------------------------
        xhair = Text("Xhair Placement", font_size=20)
        tracking = Text("Tracking", font_size=20)
        spraying = Text("Spraying", font_size=20)
        reflexes = Text("Reflexes", font_size=20)

        aim_children = VGroup(xhair, tracking, spraying, reflexes)
        aim_children.arrange(RIGHT, buff=0.6)
        aim_children.next_to(aim, DOWN, buff=1.0)

        aim_lines = {}
        for child in [xhair, tracking, spraying, reflexes]:
            line = Line(aim.get_bottom(), aim.get_bottom(), stroke_width=3)
            self.add(line)
            aim_lines[child] = line
            self.play(
                line.animate.put_start_and_end_on(aim.get_bottom(), child.get_top()),
                run_time=0.6,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Third level: Spraying → Shape Knowledge / Real Time Execution
        # ------------------------------------------------------------
        shape_know = Text("Shape\nKnowledge", font_size=16, line_spacing=0.7)
        real_time = Text("Real Time\nExecution", font_size=16, line_spacing=0.7)
        spray_leaves = VGroup(shape_know, real_time)
        spray_leaves.arrange(RIGHT, buff=0.8)
        spray_leaves.next_to(spraying, DOWN, buff=1.0)

        spray_lines = {}
        for child in [shape_know, real_time]:
            line = Line(spraying.get_bottom(), spraying.get_bottom(), stroke_width=2)
            self.add(line)
            spray_lines[child] = line
            self.play(
                line.animate.put_start_and_end_on(
                    spraying.get_bottom(), child.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Yellow cascade: Mechanics → Aim → Spraying → its two leaves
        # ------------------------------------------------------------
        self.play(mechanics.animate.set_color(YELLOW), run_time=0.4)
        self.play(mech_to_aim_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(aim.animate.set_color(YELLOW), run_time=0.4)

        # Aim → Spraying
        self.play(aim_lines[spraying].animate.set_stroke(YELLOW), run_time=0.3)
        self.play(spraying.animate.set_color(YELLOW), run_time=0.3)

        # Spraying → leaves
        for child in [shape_know, real_time]:
            self.play(spray_lines[child].animate.set_stroke(YELLOW), run_time=0.3)
            self.play(child.animate.set_color(YELLOW), run_time=0.3)

        self.wait(2)


class PracticeOnlyPlateauBars(Scene):
    def construct(self):
        BAR_WIDTH = 11

        # Title hidden initially
        title = Text("Practice Alone", font_size=42).to_edge(UP)

        self.play(FadeIn(title))

        # --------------------
        # HOURS BAR (BLUE)
        # --------------------
        hours_outline = Rectangle(width=BAR_WIDTH, height=0.7).shift(UP * 1.2)

        hours_fill = Rectangle(
            width=0.01, height=0.62, fill_color=BLUE, fill_opacity=1, stroke_opacity=0
        )
        hours_fill.move_to(hours_outline.get_left() + RIGHT * 0.005)

        # --------------------
        # SKILL BAR (GREEN)
        # --------------------
        skill_outline = Rectangle(width=BAR_WIDTH, height=0.7).shift(DOWN * 1.0)

        skill_fill = Rectangle(
            width=0.01, height=0.62, fill_color=GREEN, fill_opacity=1, stroke_opacity=0
        )
        skill_fill.move_to(skill_outline.get_left() + RIGHT * 0.005)

        self.play(Create(hours_outline), Create(skill_outline))

        self.add(hours_fill, skill_fill)

        # Hours keep increasing
        hour_progress = [
            0.10,
            0.20,
            0.35,
            0.50,
            0.65,
            0.80,
            0.90,
            1.00,
        ]

        # Skill caps at 60%
        skill_progress = [
            0.20,
            0.35,
            0.48,
            0.56,
            0.60,
            0.60,
            0.60,
            0.60,
        ]

        for h, s in zip(hour_progress, skill_progress):

            new_hours = Rectangle(
                width=max(0.01, BAR_WIDTH * h),
                height=0.62,
                fill_color=BLUE,
                fill_opacity=1,
                stroke_opacity=0,
            )
            new_hours.move_to(hours_outline.get_left() + RIGHT * (new_hours.width / 2))

            new_skill = Rectangle(
                width=max(0.01, BAR_WIDTH * s),
                height=0.62,
                fill_color=GREEN,
                fill_opacity=1,
                stroke_opacity=0,
            )
            new_skill.move_to(skill_outline.get_left() + RIGHT * (new_skill.width / 2))

            self.play(
                Transform(hours_fill, new_hours),
                Transform(skill_fill, new_skill),
                run_time=0.7,
            )

        self.wait(0.3)

        # 60% ceiling marker
        ceiling_x = skill_outline.get_left()[0] + BAR_WIDTH * 0.60

        ceiling_line = DashedLine(
            [ceiling_x, -2.2, 0], [ceiling_x, 2.2, 0], color=YELLOW
        )

        self.play(Create(ceiling_line))

        self.wait(0.5)

        # Reveal meaning only at end
        time_label = Text("TIME", color=BLUE, font_size=42, weight=BOLD).next_to(
            hours_outline, UP, buff=0.35
        )

        skill_label = Text("SKILL", color=GREEN, font_size=42, weight=BOLD).next_to(
            skill_outline, UP, buff=0.35
        )

        limit_label = Text(
            "PRACTICE-ONLY LIMIT", color=YELLOW, font_size=34, weight=BOLD
        ).to_edge(DOWN)

        self.play(
            FadeIn(time_label), FadeIn(skill_label), FadeIn(limit_label), run_time=1.5
        )

        self.wait(3)

        review_fill = Rectangle(
            width=BAR_WIDTH * 0.40,
            height=0.62,
            fill_color=RED,
            fill_opacity=1,
            stroke_opacity=0,
        )

        review_fill.move_to(
            skill_outline.get_left()
            + RIGHT * (BAR_WIDTH * 0.60 + review_fill.width / 2)
        )

        review_text = Text(
            "Targeted Review + Fix + Repeat", color=RED, font_size=30, weight=BOLD
        ).next_to(skill_outline, DOWN, buff=1.1)

        self.play(FadeIn(review_fill), FadeIn(review_text), run_time=1.5)

        self.wait(2)


class SkillMindMap(Scene):
    def construct(self):
        # --------------------------------------------------------
        # 1. Define percentages (leaf nodes, then compute upwards)
        # --------------------------------------------------------
        leaf_pct = {
            "jiggle": 20,
            "jumpspot": 40,
            "pixel angle": 60,
            "awp hold": 80,
            "Map Control": 70,
            "Mid Round": 50,
            "Afterplant": 60,
            "Communication": 80,
            "Economy": 60,
            "Mechanics": 70,
        }

        info_pct = round(
            np.mean(
                [
                    leaf_pct["jiggle"],
                    leaf_pct["jumpspot"],
                    leaf_pct["pixel angle"],
                    leaf_pct["awp hold"],
                ]
            )
        )
        early_round_pct = round(np.mean([info_pct, leaf_pct["Map Control"]]))
        strategy_pct = round(
            np.mean(
                [
                    early_round_pct,
                    leaf_pct["Mid Round"],
                    leaf_pct["Afterplant"],
                ]
            )
        )
        cs2_pct = round(
            np.mean(
                [
                    leaf_pct["Communication"],
                    leaf_pct["Economy"],
                    strategy_pct,
                    leaf_pct["Mechanics"],
                ]
            )
        )

        pct_dict = {
            "CS2": cs2_pct,
            "Communication": leaf_pct["Communication"],
            "Economy": leaf_pct["Economy"],
            "Strategy": strategy_pct,
            "Mechanics": leaf_pct["Mechanics"],
            "Early Round": early_round_pct,
            "Mid Round": leaf_pct["Mid Round"],
            "Afterplant": leaf_pct["Afterplant"],
            "Information": info_pct,
            "Map Control": leaf_pct["Map Control"],
            "jiggle": leaf_pct["jiggle"],
            "jumpspot": leaf_pct["jumpspot"],
            "pixel angle": leaf_pct["pixel angle"],
            "awp hold": leaf_pct["awp hold"],
        }

        # Helper to create a node: name text + percentage text below
        def make_node(name, font_size):
            main = Text(name, font_size=font_size)
            pct_text = Text(f"{pct_dict[name]}%", font_size=font_size * 0.5)
            pct_text.next_to(main, DOWN, buff=0.1)
            return VGroup(main, pct_text)

        # --------------------------------------------------------
        # 2. Build the mind map (unchanged positions, lines use main text)
        # --------------------------------------------------------
        # Root
        cs2 = make_node("CS2", 72)
        cs2.move_to(UP * 3)
        self.play(Write(cs2))

        # Level 1
        communication = make_node("Communication", 28)
        economy = make_node("Economy", 28)
        strategy = make_node("Strategy", 28)
        mechanics = make_node("Mechanics", 28)

        first_level_labels = [communication, economy, strategy, mechanics]
        first_level = VGroup(*first_level_labels)
        first_level.arrange(RIGHT, buff=1.0)
        first_level.move_to(UP * 0.8)

        cs2_to_strategy_line = None
        for label in first_level_labels:
            line = Line(cs2[0].get_bottom(), cs2[0].get_bottom(), stroke_width=4)
            self.add(line)
            if label is strategy:
                cs2_to_strategy_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    cs2[0].get_bottom(), label[0].get_top()
                ),
                run_time=0.8,
            )
            self.play(Write(label), run_time=0.3)

        # Level 2 (Strategy children)
        early_round = make_node("Early Round", 22)
        mid_round = make_node("Mid Round", 22)
        afterplant = make_node("Afterplant", 22)
        strategy_children = VGroup(early_round, mid_round, afterplant)
        strategy_children.arrange(RIGHT, buff=0.8)
        strategy_children.next_to(strategy[0], DOWN, buff=1.2)

        strategy_to_early_round_line = None
        for label in strategy_children:
            line = Line(
                strategy[0].get_bottom(), strategy[0].get_bottom(), stroke_width=3
            )
            self.add(line)
            if label is early_round:
                strategy_to_early_round_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    strategy[0].get_bottom(), label[0].get_top()
                ),
                run_time=0.6,
            )
            self.play(Write(label), run_time=0.3)

        # Level 3 (Early Round children)
        information = make_node("Information", 20)
        map_control = make_node("Map Control", 20)
        early_round_children = VGroup(information, map_control)
        early_round_children.arrange(RIGHT, buff=0.6)
        early_round_children.next_to(early_round[0], DOWN, buff=0.8)

        early_round_to_information_line = None
        for label in early_round_children:
            line = Line(
                early_round[0].get_bottom(), early_round[0].get_bottom(), stroke_width=2
            )
            self.add(line)
            if label is information:
                early_round_to_information_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    early_round[0].get_bottom(), label[0].get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        # Level 4 (Information children)
        jiggle = make_node("jiggle", 18)
        jumpspot = make_node("jumpspot", 18)
        pixel_angle = make_node("pixel angle", 18)
        awp_hold = make_node("awp hold", 18)
        info_children = VGroup(jiggle, jumpspot, pixel_angle, awp_hold)
        info_children.arrange(RIGHT, buff=0.5)
        info_children.next_to(information[0], DOWN, buff=0.8)

        info_to_jiggle_line = None
        for label in info_children:
            line = Line(
                information[0].get_bottom(), information[0].get_bottom(), stroke_width=2
            )
            self.add(line)
            if label is jiggle:
                info_to_jiggle_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    information[0].get_bottom(), label[0].get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        self.wait(0.5)

        # --------------------------------------------------------
        # 3. Set up cosine graph (no LaTeX)
        # --------------------------------------------------------
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "stroke_width": 1.5},
        )
        axes.to_corner(DR, buff=0.5).shift(UP * 0.5)

        # Plain text axis labels
        x_label = Text("x", font_size=24).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("cos(x + p)", font_size=24)  # 'p' instead of Greek phi
        y_label.next_to(axes.y_axis, LEFT, buff=0.2).rotate(90 * DEGREES)

        axes_group = VGroup(axes, x_label, y_label)

        phase_tracker = ValueTracker(0)

        # Graph and dot (always redraw)
        graph = always_redraw(
            lambda: axes.plot(
                lambda x: np.cos(x + phase_tracker.get_value()),
                color=BLUE,
                stroke_width=2,
            )
        )
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(0, np.cos(phase_tracker.get_value())),
                color=RED,
                radius=0.08,
            )
        )

        self.add(axes_group, graph, dot)

        # --------------------------------------------------------
        # 4. Simultaneous yellow cascade + cosine animation
        # --------------------------------------------------------
        # Highlight sequence: nodes and lines along the path to jiggle (lowest leaf)
        highlight_sequence = Succession(
            cs2.animate(run_time=0.4).set_color(YELLOW),
            cs2_to_strategy_line.animate(run_time=0.4).set_stroke(YELLOW),
            strategy.animate(run_time=0.4).set_color(YELLOW),
            strategy_to_early_round_line.animate(run_time=0.4).set_stroke(YELLOW),
            early_round.animate(run_time=0.4).set_color(YELLOW),
            early_round_to_information_line.animate(run_time=0.4).set_stroke(YELLOW),
            information.animate(run_time=0.4).set_color(YELLOW),
            info_to_jiggle_line.animate(run_time=0.3).set_stroke(YELLOW),
            jiggle.animate(run_time=0.3).set_color(YELLOW),
        )

        cascade_duration = 7 * 0.4 + 2 * 0.3  # = 3.4 seconds

        # Cosine phase animation: from 0 (max) to π (min)
        phase_anim = phase_tracker.animate(run_time=cascade_duration).set_value(PI)

        self.play(AnimationGroup(highlight_sequence, phase_anim))

        self.wait(2)


from manim import *
import numpy as np


# ----------------------------------------------------------------
# All your existing scenes (unchanged) ...
# ----------------------------------------------------------------
class CS2MindMap(Scene):
    def construct(self):
        # Main title
        cs2 = Text("CS2", font_size=72)
        cs2.move_to(UP * 3)
        self.play(Write(cs2))

        # First level (tighter buff so all five fit later)
        communication = Text("Communication", font_size=28)
        economy = Text("Economy", font_size=28)
        strategy = Text("Strategy", font_size=28)
        mechanics = Text("Mechanics", font_size=28)

        first_level_labels = [communication, economy, strategy, mechanics]
        first_level = VGroup(*first_level_labels)
        first_level.arrange(RIGHT, buff=1.0)  # smaller buff
        first_level.move_to(UP * 0.8)

        cs2_to_strategy_line = None
        first_level_lines = []

        for label in first_level_labels:
            line = Line(cs2.get_bottom(), cs2.get_bottom(), stroke_width=4)
            self.add(line)
            if label is strategy:
                cs2_to_strategy_line = line
            first_level_lines.append(line)
            self.play(
                line.animate.put_start_and_end_on(cs2.get_bottom(), label.get_top()),
                run_time=0.8,
            )
            self.play(Write(label), run_time=0.3)

        # Strategy → Early Round, Mid Round, Afterplant
        early_round = Text("Early Round", font_size=22)
        mid_round = Text("Mid Round", font_size=22)
        afterplant = Text("Afterplant", font_size=22)
        strategy_children = VGroup(early_round, mid_round, afterplant)
        strategy_children.arrange(RIGHT, buff=0.8)
        strategy_children.next_to(strategy, DOWN, buff=1.2)

        strategy_to_early_round_line = None
        for label in strategy_children:
            line = Line(strategy.get_bottom(), strategy.get_bottom(), stroke_width=3)
            self.add(line)
            if label is early_round:
                strategy_to_early_round_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    strategy.get_bottom(), label.get_top()
                ),
                run_time=0.6,
            )
            self.play(Write(label), run_time=0.3)

        # Third level: Early Round → Information, Map Control
        information = Text("Information", font_size=20)
        map_control = Text("Map Control", font_size=20)
        early_round_children = VGroup(information, map_control)
        early_round_children.arrange(RIGHT, buff=0.6)
        early_round_children.next_to(early_round, DOWN, buff=0.8)

        early_round_to_information_line = None
        for label in early_round_children:
            line = Line(
                early_round.get_bottom(), early_round.get_bottom(), stroke_width=2
            )
            self.add(line)
            if label is information:
                early_round_to_information_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    early_round.get_bottom(), label.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        # Fourth level: Information → jiggle, jumpspot, pixel angle, awp hold
        jiggle = Text("jiggle", font_size=18)
        jumpspot = Text("jumpspot", font_size=18)
        pixel_angle = Text("pixel angle", font_size=18)
        awp_hold = Text("awp hold", font_size=18)
        info_children = VGroup(jiggle, jumpspot, pixel_angle, awp_hold)
        info_children.arrange(RIGHT, buff=0.5)
        info_children.next_to(information, DOWN, buff=0.8)

        info_child_lines = []
        for label in info_children:
            line = Line(
                information.get_bottom(), information.get_bottom(), stroke_width=2
            )
            self.add(line)
            info_child_lines.append(line)
            self.play(
                line.animate.put_start_and_end_on(
                    information.get_bottom(), label.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(label), run_time=0.3)

        # Yellow cascade down the Strategy pathway
        self.play(cs2.animate.set_color(YELLOW), run_time=0.4)
        self.play(cs2_to_strategy_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(strategy.animate.set_color(YELLOW), run_time=0.4)
        self.play(strategy_to_early_round_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(early_round.animate.set_color(YELLOW), run_time=0.4)
        self.play(
            early_round_to_information_line.animate.set_stroke(YELLOW), run_time=0.4
        )
        self.play(information.animate.set_color(YELLOW), run_time=0.4)

        for line, label in zip(info_child_lines, info_children):
            self.play(line.animate.set_stroke(YELLOW), run_time=0.3)
            self.play(label.animate.set_color(YELLOW), run_time=0.3)

        self.wait(2)


class ManyQuestionMarks(Scene):
    def construct(self):
        # --- Root ---
        cs2 = Text("CS2", font_size=72, color=BLUE)
        cs2.move_to(UP * 3.5)
        self.play(Write(cs2))
        self.wait(0.2)

        # --- Level 1: three direct children ---
        level1_nodes = VGroup(*[Text("?", font_size=36) for _ in range(3)])
        level1_nodes.arrange(RIGHT, buff=2.0)
        level1_nodes.move_to(UP * 1.5)

        level1_lines = VGroup()
        for node in level1_nodes:
            line = Line(cs2.get_bottom(), node.get_top(), stroke_width=4)
            level1_lines.add(line)
            self.play(Create(line), Write(node), run_time=0.4)
        self.wait(0.3)

        current_parents = list(level1_nodes)
        # Font sizes and horizontal spreads for 4 more generations
        font_sizes = [24, 18, 14, 12]
        spread_factors = [1.0, 0.7, 0.5, 0.35]  # how far children move left/right

        all_bottom_lines = VGroup()  # to later highlight the final connections

        for depth, (fs, spread) in enumerate(zip(font_sizes, spread_factors)):
            new_parents = []
            for parent in current_parents:
                left_child = Text("?", font_size=fs)
                right_child = Text("?", font_size=fs)
                # Place children below parent, shifted horizontally
                offset = spread * 1.5  # small for readability
                left_child.move_to(parent.get_bottom() + DOWN * 0.5 + LEFT * offset)
                right_child.move_to(parent.get_bottom() + DOWN * 0.5 + RIGHT * offset)

                line_left = Line(
                    parent.get_bottom(), left_child.get_top(), stroke_width=1.2
                )
                line_right = Line(
                    parent.get_bottom(), right_child.get_top(), stroke_width=1.2
                )

                # Animate
                self.play(
                    Create(line_left),
                    Write(left_child),
                    Create(line_right),
                    Write(right_child),
                    run_time=0.25,
                )
                new_parents.append(left_child)
                new_parents.append(right_child)

                if depth == len(font_sizes) - 1:  # last layer
                    all_bottom_lines.add(line_left, line_right)

            current_parents = new_parents
            self.wait(0.1)

        # --- Highlight the deepest level as "fundamental" ---
        deepest_nodes = VGroup(*current_parents)
        self.play(
            deepest_nodes.animate.set_color(YELLOW),
            all_bottom_lines.animate.set_stroke(YELLOW),
            run_time=1.2,
        )
        fundamental_text = Text("Fundamental aspects", font_size=28, color=YELLOW)
        fundamental_text.next_to(deepest_nodes, DOWN, buff=1.2)
        self.play(Write(fundamental_text))
        self.wait(2)


class Restaurant(Scene):
    def construct(self):
        # -------------------------------------------------------
        # PART 1 – FIVE RESTAURANTS OPENING SIMULTANEOUSLY
        # -------------------------------------------------------
        title = Text("5 Simultaneous Restaurant Openings", font_size=44, color=YELLOW)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP))

        ground = Line(LEFT * 6, RIGHT * 6, stroke_width=4, color=GREY)
        ground.to_edge(DOWN, buff=1.5)
        self.play(Create(ground))

        restaurants = VGroup()
        for _ in range(5):
            restaurants.add(self.create_restaurant())
        restaurants.arrange(RIGHT, buff=1.5)
        restaurants.next_to(ground, UP, buff=0)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.5) for r in restaurants], lag_ratio=0.2)
        )
        self.wait(0.5)

        open_signs = VGroup()
        for r in restaurants:
            sign = Text("OPEN", font_size=24, color=GREEN, weight=BOLD)
            sign.next_to(r, UP, buff=0.25)
            open_signs.add(sign)
        self.play(LaggedStart(*[Write(s) for s in open_signs], lag_ratio=0.1))
        self.wait(0.8)

        problems = [
            ("Hiring wrong\npeople", "🙅"),
            ("Payroll\nissues", "💰"),
            ("No walk-in\ncustomers", "🚶"),
        ]

        problem_stacks = [VGroup() for _ in range(5)]
        # Store only the y-coordinate (float) of the top of each stack
        problem_tops = [open_signs[i].get_top()[1] for i in range(5)]

        for prob_text, prob_emoji in problems:
            central_prob = self.create_problem_mobject(prob_text, prob_emoji, scale=1.6)
            central_prob.move_to(ORIGIN)
            self.play(FadeIn(central_prob, scale=0.5))
            self.wait(0.8)

            small_probs = []
            for i, r in enumerate(restaurants):
                small = self.create_problem_mobject(prob_text, prob_emoji, scale=0.7)
                # Place above the current top of the stack
                new_y = problem_tops[i] + small.get_height() / 2 + 0.2
                small.move_to(ORIGIN)
                small.align_to(open_signs[i], LEFT)
                small.shift(UP * new_y)
                small_probs.append(small)
                problem_stacks[i].add(small)
                # Update top y-coordinate for next iteration
                problem_tops[i] = small.get_top()[1]

            self.play(
                FadeOut(central_prob),
                *[FadeIn(small, shift=UP * 0.1) for small in small_probs],
                run_time=1.0,
            )
            self.wait(0.6)

        final_restaurant_msg = Text(
            "Every location suffers the same fate.", font_size=28, color=YELLOW
        )
        final_restaurant_msg.next_to(restaurants, DOWN, buff=1.2)
        self.play(Write(final_restaurant_msg))
        self.wait(3)

        # Fade out everything
        all_elements = VGroup(
            ground, restaurants, open_signs, *problem_stacks, final_restaurant_msg
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.wait(0.5)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def create_restaurant(self, color=BLUE, scale=1.0):
        building = RoundedRectangle(
            width=1.4,
            height=1.8,
            corner_radius=0.1,
            fill_color=color,
            fill_opacity=0.6,
            stroke_color=WHITE,
            stroke_width=2,
        )
        door = Rectangle(width=0.35, height=0.8, fill_color=DARKER_GREY, stroke_width=1)
        door.move_to(building.get_bottom() + UP * 0.4)
        window = Rectangle(width=0.3, height=0.3, fill_color=WHITE, stroke_width=1)
        window.move_to(building.get_top() + DOWN * 0.4 + RIGHT * 0.3)
        sign = Text("RESTAURANT", font_size=14, color=WHITE)
        sign.move_to(building.get_top() + DOWN * 0.5 + LEFT * 0.2)
        return VGroup(building, door, window, sign)

    def create_problem_mobject(self, text, emoji, scale=1.0):
        circ = Circle(radius=0.4, color=RED, fill_opacity=0.85, stroke_width=2)
        emoji_text = Text(emoji, font_size=int(32 * scale))
        emoji_text.move_to(circ.get_center())
        icon = VGroup(circ, emoji_text)
        label = Text(text, font_size=int(16 * scale), color=WHITE, weight=BOLD)
        label.next_to(icon, DOWN, buff=0.15)
        group = VGroup(icon, label)
        group.scale(scale)
        return group


class ProficiencyBars(Scene):
    # --- Customizable data: override in subclasses ---
    LABELS = ["Communication", "Economy", "Strategy", "Mechanics"]
    PROFICIENCIES = [0.5, 0.7, 0.25, 0.5]
    COLORS = [BLUE, GREEN, PURPLE, RED]
    TITLE_TEXT = "Skill Proficiency Levels"
    # ----------------------------------------------

    def construct(self):
        bar_width = 1.0
        max_height = 4.0
        bar_bottom = -2.5
        x_positions = [-4.5, -1.5, 1.5, 4.5]

        # Title
        title = Text(self.TITLE_TEXT, font_size=42)
        title.to_edge(UP)
        self.add(title)

        rects = []
        percent_trackers = []
        percent_displays = []

        for i in range(len(self.LABELS)):
            rect = Rectangle(
                width=bar_width,
                height=0,
                fill_color=self.COLORS[i],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2,
            )
            rect.move_to([x_positions[i], bar_bottom, 0])
            rects.append(rect)

            label = Text(self.LABELS[i], font_size=30)
            label.next_to(rect, DOWN, buff=0.2)
            self.add(label)

            tracker = ValueTracker(0)
            percent_trackers.append(tracker)

            # Capturing loop variables by default argument
            def make_percent_text(t=tracker, r=rect):
                val = int(t.get_value())
                txt = Text(f"{val}%", font_size=28, color=WHITE)
                txt.next_to(r, UP, buff=0.15)
                return txt

            percent_display = always_redraw(make_percent_text)
            percent_displays.append(percent_display)

        self.add(*rects, *percent_displays)

        # --- Animate bars and trackers ---
        bar_animations = []
        for rect, p in zip(rects, self.PROFICIENCIES):
            target_height = p * max_height
            target_rect = Rectangle(
                width=bar_width,
                height=target_height,
                fill_color=rect.fill_color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2,
            )
            target_rect.move_to(
                [rect.get_center()[0], bar_bottom + target_height / 2, 0]
            )
            bar_animations.append(Transform(rect, target_rect))

        tracker_animations = [
            tracker.animate.set_value(p * 100)
            for tracker, p in zip(percent_trackers, self.PROFICIENCIES)
        ]

        self.play(
            LaggedStart(*bar_animations, lag_ratio=0.2),
            LaggedStart(*tracker_animations, lag_ratio=0.2),
            run_time=2.5,
        )

        # --- Highlight the lowest proficiency permanently ---
        lowest_idx = self.PROFICIENCIES.index(min(self.PROFICIENCIES))
        low_rect = rects[lowest_idx]
        low_percent_display = percent_displays[lowest_idx]

        self.play(
            Indicate(low_rect, scale_factor=1.2, color=YELLOW),
            Indicate(low_percent_display, scale_factor=1.2, color=YELLOW),
        )

        low_percent_display.clear_updaters()
        final_val = int(self.PROFICIENCIES[lowest_idx] * 100)
        highlighted_percent = Text(f"{final_val}%", font_size=28, color=YELLOW)
        highlighted_percent.move_to(low_percent_display.get_center())

        glow_rect = low_rect.copy()
        glow_rect.set_stroke(color=YELLOW, width=10, opacity=0.6)
        glow_rect.set_fill(opacity=0)
        glow_rect.scale(1.1)
        glow_rect.set_z_index(low_rect.z_index - 1)

        self.play(
            low_rect.animate.set_stroke(color=YELLOW, width=6),
            Transform(low_percent_display, highlighted_percent),
            FadeIn(glow_rect),
            run_time=0.5,
        )

        self.wait(5)


class Strategy(ProficiencyBars):
    LABELS = ["Early Round", "Mid Round", "Afterplant"]
    PROFICIENCIES = [0.3, 0.3, 0.3]
    COLORS = [BLUE, YELLOW, RED]
    TITLE_TEXT = "Strategy Proficiency Levels"


class EarlyRound(ProficiencyBars):
    LABELS = ["Information", "Map Control"]
    PROFICIENCIES = [0.1, 0.4]
    COLORS = [BLUE, YELLOW]
    TITLE_TEXT = "Early Round Proficiency Levels"


class Information(ProficiencyBars):
    LABELS = ["Jiggle", "Jumpspot", "Pixel Angle", "AWP Hold"]
    PROFICIENCIES = [0, 0.5, 0.1, 0.5]
    COLORS = [BLUE, YELLOW, RED, ORANGE]
    TITLE_TEXT = "Information Proficiency Levels"


class ProgressLadders(Scene):
    def construct(self):
        # Positions
        left_x = -4
        right_x = 4

        # --- Build left ladder (beginner) ---
        left_rail1 = Line([left_x - 0.4, -2, 0], [left_x - 0.4, 2, 0], color=GREEN)
        left_rail2 = Line([left_x + 0.4, -2, 0], [left_x + 0.4, 2, 0], color=GREEN)
        left_y_positions = [-2, -1, 0, 1, 2]  # 5 rungs
        left_rungs = VGroup()
        for y in left_y_positions:
            left_rungs.add(
                Line([left_x - 0.4, y, 0], [left_x + 0.4, y, 0], color=GREEN)
            )

        # --- Build right ladder (expert) ---
        right_rail1 = Line([right_x - 0.4, -2, 0], [right_x - 0.4, 2, 0], color=BLUE)
        right_rail2 = Line([right_x + 0.4, -2, 0], [right_x + 0.4, 2, 0], color=BLUE)
        right_y_positions = np.linspace(-2, 2, 21)  # 21 tiny rungs
        right_rungs = VGroup()
        for y in right_y_positions:
            right_rungs.add(
                Line([right_x - 0.4, y, 0], [right_x + 0.4, y, 0], color=BLUE)
            )

        # Animate construction
        self.play(
            Create(left_rail1),
            Create(left_rail2),
            Create(right_rail1),
            Create(right_rail2),
        )
        self.play(
            Create(left_rungs, lag_ratio=0.1, run_time=1),
            Create(right_rungs, lag_ratio=0.02, run_time=4),
        )

        # --- Climbers ---
        left_dot = Dot(point=[left_x, -2, 0], color=GREEN, radius=0.12)
        right_dot = Dot(point=[right_x, -2, 0], color=BLUE, radius=0.12)
        self.play(FadeIn(left_dot), FadeIn(right_dot))

        # Paths along rung heights
        def climb_path(x, y_list):
            points = [np.array([x, y_list[0], 0])]
            for y in y_list[1:]:
                points.append(np.array([x, y, 0]))
            return VMobject().set_points_as_corners(points)

        left_path = climb_path(left_x, left_y_positions)
        right_path = climb_path(right_x, right_y_positions)

        # Simultaneous climb – green finishes much faster
        self.play(
            MoveAlongPath(left_dot, left_path, run_time=2, rate_func=linear),
            MoveAlongPath(right_dot, right_path, run_time=8, rate_func=linear),
        )

        self.wait(0.5)

        # --- Reveal texts (labels now at midpoint: 2.4) ---
        title = Text("0 → 50 is often easier than 95 → 99", font_size=42).to_edge(UP)

        left_label = Text("0 → 50", font_size=36, color=GREEN)
        left_label.move_to(LEFT * 4 + UP * 2.4)  # exact middle between 2.0 and 2.8
        right_label = Text("95 → 99", font_size=36, color=BLUE)
        right_label.move_to(RIGHT * 4 + UP * 2.4)

        footer = Text(
            "Each improvement gets harder as you approach mastery", font_size=26
        ).to_edge(DOWN)

        self.play(
            FadeIn(title),
            FadeIn(left_label),
            FadeIn(right_label),
            FadeIn(footer),
        )
        self.wait(3)


class MechanicsTree(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Root
        # ------------------------------------------------------------
        mechanics = Text("Mechanics", font_size=48)
        mechanics.move_to(UP * 3)
        self.play(Write(mechanics))

        # ------------------------------------------------------------
        # First level: Aim & Movement
        # ------------------------------------------------------------
        aim = Text("Aim", font_size=28)
        movement = Text("Movement", font_size=28)
        first_children = VGroup(aim, movement)
        first_children.arrange(RIGHT, buff=1.5)
        first_children.next_to(mechanics, DOWN, buff=1.2)

        mech_to_aim_line = None
        mech_to_movement_line = None

        for child in [aim, movement]:
            line = Line(mechanics.get_bottom(), mechanics.get_bottom(), stroke_width=4)
            self.add(line)
            if child is aim:
                mech_to_aim_line = line
            else:
                mech_to_movement_line = line
            self.play(
                line.animate.put_start_and_end_on(
                    mechanics.get_bottom(), child.get_top()
                ),
                run_time=0.8,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Second level: Aim's four children
        # ------------------------------------------------------------
        xhair = Text("Xhair Placement", font_size=20)
        tracking = Text("Tracking", font_size=20)
        spraying = Text("Spraying", font_size=20)
        reflexes = Text("Reflexes", font_size=20)

        aim_children = VGroup(xhair, tracking, spraying, reflexes)
        aim_children.arrange(RIGHT, buff=0.6)
        aim_children.next_to(aim, DOWN, buff=1.0)

        aim_lines = {}
        for child in [xhair, tracking, spraying, reflexes]:
            line = Line(aim.get_bottom(), aim.get_bottom(), stroke_width=3)
            self.add(line)
            aim_lines[child] = line
            self.play(
                line.animate.put_start_and_end_on(aim.get_bottom(), child.get_top()),
                run_time=0.6,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Third level: Spraying → Shape Knowledge / Real Time Execution
        # ------------------------------------------------------------
        shape_know = Text("Shape\nKnowledge", font_size=16, line_spacing=0.7)
        real_time = Text("Real Time\nExecution", font_size=16, line_spacing=0.7)
        spray_leaves = VGroup(shape_know, real_time)
        spray_leaves.arrange(RIGHT, buff=0.8)
        spray_leaves.next_to(spraying, DOWN, buff=1.0)

        spray_lines = {}
        for child in [shape_know, real_time]:
            line = Line(spraying.get_bottom(), spraying.get_bottom(), stroke_width=2)
            self.add(line)
            spray_lines[child] = line
            self.play(
                line.animate.put_start_and_end_on(
                    spraying.get_bottom(), child.get_top()
                ),
                run_time=0.5,
            )
            self.play(Write(child), run_time=0.3)

        # ------------------------------------------------------------
        # Yellow cascade: Mechanics → Aim → Spraying → its two leaves
        # ------------------------------------------------------------
        self.play(mechanics.animate.set_color(YELLOW), run_time=0.4)
        self.play(mech_to_aim_line.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(aim.animate.set_color(YELLOW), run_time=0.4)

        # Aim → Spraying
        self.play(aim_lines[spraying].animate.set_stroke(YELLOW), run_time=0.3)
        self.play(spraying.animate.set_color(YELLOW), run_time=0.3)

        # Spraying → leaves
        for child in [shape_know, real_time]:
            self.play(spray_lines[child].animate.set_stroke(YELLOW), run_time=0.3)
            self.play(child.animate.set_color(YELLOW), run_time=0.3)

        self.wait(2)


class PracticeOnlyPlateauBars(Scene):
    def construct(self):
        BAR_WIDTH = 11

        # Title hidden initially
        title = Text("Practice Alone", font_size=42).to_edge(UP)

        self.play(FadeIn(title))

        # --------------------
        # HOURS BAR (BLUE)
        # --------------------
        hours_outline = Rectangle(width=BAR_WIDTH, height=0.7).shift(UP * 1.2)

        hours_fill = Rectangle(
            width=0.01, height=0.62, fill_color=BLUE, fill_opacity=1, stroke_opacity=0
        )
        hours_fill.move_to(hours_outline.get_left() + RIGHT * 0.005)

        # --------------------
        # SKILL BAR (GREEN)
        # --------------------
        skill_outline = Rectangle(width=BAR_WIDTH, height=0.7).shift(DOWN * 1.0)

        skill_fill = Rectangle(
            width=0.01, height=0.62, fill_color=GREEN, fill_opacity=1, stroke_opacity=0
        )
        skill_fill.move_to(skill_outline.get_left() + RIGHT * 0.005)

        self.play(Create(hours_outline), Create(skill_outline))

        self.add(hours_fill, skill_fill)

        # Hours keep increasing
        hour_progress = [
            0.10,
            0.20,
            0.35,
            0.50,
            0.65,
            0.80,
            0.90,
            1.00,
        ]

        # Skill caps at 60%
        skill_progress = [
            0.20,
            0.35,
            0.48,
            0.56,
            0.60,
            0.60,
            0.60,
            0.60,
        ]

        for h, s in zip(hour_progress, skill_progress):

            new_hours = Rectangle(
                width=max(0.01, BAR_WIDTH * h),
                height=0.62,
                fill_color=BLUE,
                fill_opacity=1,
                stroke_opacity=0,
            )
            new_hours.move_to(hours_outline.get_left() + RIGHT * (new_hours.width / 2))

            new_skill = Rectangle(
                width=max(0.01, BAR_WIDTH * s),
                height=0.62,
                fill_color=GREEN,
                fill_opacity=1,
                stroke_opacity=0,
            )
            new_skill.move_to(skill_outline.get_left() + RIGHT * (new_skill.width / 2))

            self.play(
                Transform(hours_fill, new_hours),
                Transform(skill_fill, new_skill),
                run_time=0.7,
            )

        self.wait(0.3)

        # 60% ceiling marker
        ceiling_x = skill_outline.get_left()[0] + BAR_WIDTH * 0.60

        ceiling_line = DashedLine(
            [ceiling_x, -2.2, 0], [ceiling_x, 2.2, 0], color=YELLOW
        )

        self.play(Create(ceiling_line))

        self.wait(0.5)

        # Reveal meaning only at end
        time_label = Text("TIME", color=BLUE, font_size=42, weight=BOLD).next_to(
            hours_outline, UP, buff=0.35
        )

        skill_label = Text("SKILL", color=GREEN, font_size=42, weight=BOLD).next_to(
            skill_outline, UP, buff=0.35
        )

        limit_label = Text(
            "PRACTICE-ONLY LIMIT", color=YELLOW, font_size=34, weight=BOLD
        ).to_edge(DOWN)

        self.play(
            FadeIn(time_label), FadeIn(skill_label), FadeIn(limit_label), run_time=1.5
        )

        self.wait(3)

        review_fill = Rectangle(
            width=BAR_WIDTH * 0.40,
            height=0.62,
            fill_color=RED,
            fill_opacity=1,
            stroke_opacity=0,
        )

        review_fill.move_to(
            skill_outline.get_left()
            + RIGHT * (BAR_WIDTH * 0.60 + review_fill.width / 2)
        )

        review_text = Text(
            "Targeted Review + Fix + Repeat", color=RED, font_size=30, weight=BOLD
        ).next_to(skill_outline, DOWN, buff=1.1)

        self.play(FadeIn(review_fill), FadeIn(review_text), run_time=1.5)

        self.wait(2)


class Cos(Scene):

    def construct(self):
        # Axes – only positive x
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=11,
            y_length=4,
            axis_config={"include_tip": False},
        )
        axes.center()

        x_label = Text("x", font_size=28).next_to(axes.x_axis, DOWN, buff=0.2)
        self.add(axes, x_label)

        # Hierarchy words at fixed y‑values
        word_y_data = [1.2, 0.6, 0.0, -0.6, -1.2]
        word_labels = ["CS2", "Strategy", "Early Round", "Information", "Jiggle"]

        hierarchy_words = VGroup()
        for word, y in zip(word_labels, word_y_data):
            txt = Text(word, font_size=22)
            txt.move_to(axes.c2p(0, y)).shift(LEFT * 0.8)
            hierarchy_words.add(txt)

        self.add(hierarchy_words)

        A = (max(word_y_data) - min(word_y_data)) / 2  # amplitude = 1.2
        B = 0  # centre at y=0

        phase = ValueTracker(0)

        # Cosine wave scaled to match the words’ vertical span
        wave = always_redraw(
            lambda: axes.plot(
                lambda x: A * np.cos(x + phase.get_value()) + B,
                x_range=[0, axes.x_range[1]],
                color=BLUE,
                stroke_width=4,
            )
        )

        # Red dot at the left border (x=0)
        dot = always_redraw(
            lambda: Dot(
                point=axes.c2p(0, A * np.cos(phase.get_value()) + B),
                color=RED,
                radius=0.12,
            )
        )

        # Highlight the word nearest to the dot
        def update_highlight(mob):
            current_y = A * np.cos(phase.get_value()) + B
            distances = [abs(current_y - y) for y in word_y_data]
            closest_idx = distances.index(min(distances))
            for i, word in enumerate(hierarchy_words):
                word.set_color(YELLOW if i == closest_idx else WHITE)

        hierarchy_words.add_updater(update_highlight)
        update_highlight(hierarchy_words)  # initial highlight

        self.add(wave, dot)

        # Phase from 0 to 2π → dot goes down (CS2 → Jiggle) and then back up
        self.play(phase.animate.set_value(2 * PI), run_time=12, rate_func=linear)
        self.wait(2)


class LearningCycleBars(Scene):
    def construct(self):
        # ----- Stage 1: Show the key words -----
        text_try = Text("try", color=RED, font_size=72)
        text_review = Text("review", color=BLUE, font_size=72)
        text_fix = Text("fix", color=ORANGE, font_size=72)

        self.play(Write(text_try))
        self.wait(0.4)
        self.play(FadeOut(text_try))

        self.play(Write(text_review))
        self.wait(0.4)
        self.play(FadeOut(text_review))

        self.play(Write(text_fix))
        self.wait(0.4)
        self.play(FadeOut(text_fix))

        # ----- Stage 2: Sequence of colored bars -----
        # Colors representing the steps (the cycle repeats)
        colors = [RED, BLUE, ORANGE, RED, BLUE, ORANGE]

        bar_width = 0.3
        bar_height = 0.8
        spacing = 0.9  # center-to-center distance
        total_bars = len(colors)
        total_width = total_bars * bar_width + (total_bars - 1) * (spacing - bar_width)
        start_x = -total_width / 2 + bar_width / 2
        y_pos = -1.0

        bars = VGroup()
        for i, color in enumerate(colors):
            rect = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            rect.move_to([start_x + i * spacing, y_pos, 0])
            bars.add(rect)

        # Animate the bars appearing one after another
        for bar in bars:
            self.play(GrowFromCenter(bar), run_time=0.3)
            self.wait(0.15)

        # ----- Optional loop arrow back to the beginning -----
        last_bar = bars[-1]
        first_bar = bars[0]
        arrow_start = last_bar.get_right() + RIGHT * 0.3
        arrow_end = first_bar.get_left() + LEFT * 0.3

        loop_arrow = CurvedArrow(
            arrow_start,
            arrow_end,
            angle=-PI / 2,
            color=YELLOW,
            stroke_width=3,
        )
        self.play(Create(loop_arrow))
        self.wait(1.5)


class EquilateralTriangleFromBase(Scene):

    def construct(self):
        # ------------------------------------------------------------
        # 1. INITIAL LARGE TRIANGLE (the one that later expands & fades)
        # ------------------------------------------------------------
        base_left = np.array([-1, -1, 0])
        base_right = np.array([1, -1, 0])
        height = np.linalg.norm(base_right - base_left) * np.sqrt(3) / 2  # ~1.732
        top = np.array([0, -1 + height, 0])

        base_line = Line(base_left, base_right, color=WHITE, stroke_width=6)
        left_side = Line(base_left, top, color=WHITE, stroke_width=6)
        right_side = Line(base_right, top, color=WHITE, stroke_width=6)
        apex_dot = Dot(top, color=WHITE, radius=0.1)

        fundamentals = Text("fundamentals", font_size=36, color=YELLOW)
        fundamentals.next_to(base_line, DOWN, buff=0.3)

        cs2_apex = Text("CS2", font_size=48, color=RED, weight=BOLD)
        cs2_apex.next_to(top, UP, buff=0.3)

        # --- Build the initial triangle ---
        self.play(Create(base_line))
        self.wait(0.3)
        self.play(FadeIn(fundamentals, shift=UP * 0.1))
        self.wait(0.2)
        self.play(base_line.animate.set_color(YELLOW))
        self.wait(0.1)
        self.play(
            AnimationGroup(
                Create(left_side), Create(right_side), Create(apex_dot), lag_ratio=0
            )
        )
        self.wait(0.3)
        self.play(Write(cs2_apex))
        self.wait(0.2)
        self.play(apex_dot.animate.set_color(RED))
        self.wait(0.5)

        # --- Fade out sides, apex, CS2 ---
        self.play(
            FadeOut(left_side),
            FadeOut(right_side),
            FadeOut(apex_dot),
            FadeOut(cs2_apex),
        )
        self.wait(0.3)

        # --- Move base line and "fundamentals" downward ---
        self.play(
            base_line.animate.shift(DOWN * 2),
            fundamentals.animate.shift(DOWN * 2),
            run_time=1.5,
        )
        self.wait(0.3)

        # --- Expand to full screen edges (linear) ---
        current_y = base_line.get_center()[1]
        half_w = config.frame_width / 2
        target_left = np.array([-half_w, current_y, 0])
        target_right = np.array([half_w, current_y, 0])
        target_line = Line(target_left, target_right, color=YELLOW, stroke_width=6)

        text_target = target_line.get_center() + DOWN * (0.3 + fundamentals.height / 2)
        self.play(
            Transform(base_line, target_line),
            fundamentals.animate.move_to(text_target),
            rate_func=linear,
            run_time=4,
        )
        self.wait(0.3)

        # --- Remove bar and text, show red circle at top center ---
        self.play(FadeOut(base_line), FadeOut(fundamentals))
        top_center = np.array([0, config.frame_height / 2 - 0.3, 0])
        red_circle = Circle(radius=0.2, color=RED, fill_opacity=1)
        red_circle.move_to(top_center)
        self.play(FadeIn(red_circle, scale=0.5))
        self.wait(2)

        # --- Free fall of red circle (gravity-like) ---
        bottom_y = -config.frame_height / 2 + 0.3
        fall_dist = top_center[1] - bottom_y
        self.play(
            red_circle.animate.shift(DOWN * fall_dist),
            rate_func=lambda t: t**2,  # accelerating
            run_time=1.5,
        )
        self.wait(0.1)

        # --- Shatter the circle into particles ---
        impact = red_circle.get_center()
        particles = VGroup(*[Dot(impact, radius=0.04, color=RED) for _ in range(30)])
        self.add(particles)
        self.remove(red_circle)

        rng = np.random.default_rng(42)
        offsets = []
        for _ in particles:
            angle = rng.uniform(0, 2 * PI)
            mag = rng.uniform(0.5, 2.5)
            offsets.append(np.array([mag * np.cos(angle), mag * np.sin(angle), 0]))

        self.play(
            AnimationGroup(
                *[p.animate.shift(off).fade(1) for p, off in zip(particles, offsets)],
                lag_ratio=0,
                run_time=1.0,
            )
        )
        self.wait(0.5)

        # ================================================================
        # 2. NEW SMALLER YELLOW BASE SLIDES IN FROM LEFT (towards bottom)
        # ================================================================
        small_base_len = 1.5
        final_base_center = np.array([-2, -1.8, 0])
        final_left = final_base_center + np.array([-small_base_len / 2, 0, 0])
        final_right = final_base_center + np.array([small_base_len / 2, 0, 0])

        # Start off-screen left, a bit higher
        start_center = np.array([-5.5, -0.5, 0])
        start_left = start_center + np.array([-small_base_len / 2, 0, 0])
        start_right = start_center + np.array([small_base_len / 2, 0, 0])

        start_base = Line(start_left, start_right, color=YELLOW, stroke_width=6)
        final_base = Line(final_left, final_right, color=YELLOW, stroke_width=6)

        self.add(start_base)
        self.play(Transform(start_base, final_base), run_time=1.5)
        self.wait(0.3)

        # Build the small equilateral triangle on this base
        self.small_base = start_base  # now at final position
        small_left = self.small_base.get_left()  # (-2.75, -1.8)
        small_right = self.small_base.get_right()  # (-1.25, -1.8)
        small_height = small_base_len * np.sqrt(3) / 2  # ≈1.299
        small_apex = np.array(
            [final_base_center[0], final_base_center[1] + small_height, 0]
        )

        self.small_left_side = Line(small_left, small_apex, color=WHITE, stroke_width=6)
        self.small_right_side = Line(
            small_right, small_apex, color=WHITE, stroke_width=6
        )
        self.small_apex_dot = Dot(small_apex, color=RED, radius=0.1)

        self.play(
            AnimationGroup(
                Create(self.small_left_side), Create(self.small_right_side), lag_ratio=0
            )
        )
        self.wait(0.2)
        self.play(FadeIn(self.small_apex_dot, scale=0.5))
        self.wait(0.5)

        # ================================================================
        # 3. EXPAND THE BASE A LITTLE, THEN TO DOUBLE THE ORIGINAL LENGTH
        # ================================================================
        # First, expand a little (0.8) – as previously requested
        extension_small = 0.8
        expanded_right_1 = small_right + np.array([extension_small, 0, 0])
        expanded_base_1 = Line(
            small_left, expanded_right_1, color=YELLOW, stroke_width=6
        )
        self.play(Transform(self.small_base, expanded_base_1), run_time=1.0)
        self.wait(0.3)

        # Then expand to double the original size (3.0)
        double_length = 2 * small_base_len  # 3.0
        final_double_right = small_left + np.array(
            [double_length, 0, 0]
        )  # x = -2.75+3.0 = 0.25
        expanded_base_double = Line(
            small_left, final_double_right, color=YELLOW, stroke_width=6
        )
        self.play(Transform(self.small_base, expanded_base_double), run_time=1.5)
        self.wait(0.3)

        # ================================================================
        # 4. DRAW THE NEW TRIANGLE ON THE DOUBLED BASE (overlapping the old)
        # ================================================================
        # Left endpoint remains the same, right endpoint is final_double_right
        new_left = small_left
        new_right = final_double_right
        new_midpoint = (new_left + new_right) / 2
        new_height = double_length * np.sqrt(3) / 2  # ≈2.598
        new_apex = np.array([new_midpoint[0], new_left[1] + new_height, 0])

        # Create the new triangle sides and apex dot
        new_left_side = Line(new_left, new_apex, color=WHITE, stroke_width=6)
        new_right_side = Line(new_right, new_apex, color=WHITE, stroke_width=6)
        new_apex_dot = Dot(new_apex, color=RED, radius=0.1)

        # Draw the new triangle – it will overlap the old one (old stays visible)
        self.play(
            AnimationGroup(Create(new_left_side), Create(new_right_side), lag_ratio=0)
        )
        self.wait(0.2)
        self.play(FadeIn(new_apex_dot, scale=0.5))
        self.wait(1)
