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

        # ==============================================================
        # Add Time Management, then centre all five first‑level labels
        # ==============================================================
        time_mgmt = Text("Time Management", font_size=28)
        # Place it relative to the (still un‑shifted) mechanics
        time_mgmt.next_to(mechanics, RIGHT, buff=1.0)

        # Group all five labels together to compute centring shift
        all_labels = VGroup(communication, economy, strategy, mechanics, time_mgmt)
        target_center = UP * 0.8  # same vertical position
        shift = target_center - all_labels.get_center()

        # Add the new Time Management label to the scene (still at its raw position)
        self.add(time_mgmt)

        # Prepare animations for shifting labels and adjusting lines
        anims = []
        # 1) Move each label (including Time Management) to its final centred spot
        for label in all_labels:
            anims.append(label.animate.shift(shift))

        # 2) Update each of the four existing lines so they stay connected to CS2
        for label, line in zip(first_level_labels, first_level_lines):
            target_top = label.get_top() + shift  # final top of label
            anims.append(
                line.animate.put_start_and_end_on(cs2.get_bottom(), target_top)
            )

        # 3) Create the new line for Time Management and animate it from scratch
        line_time = Line(cs2.get_bottom(), cs2.get_bottom(), stroke_width=4)
        self.add(line_time)
        target_top_time = time_mgmt.get_top() + shift
        anims.append(
            line_time.animate.put_start_and_end_on(cs2.get_bottom(), target_top_time)
        )

        self.play(AnimationGroup(*anims), run_time=1.2)
        # ==============================================================

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
