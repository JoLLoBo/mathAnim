from manim import *


class CS2MindMap(Scene):
    def construct(self):
        # Main title
        cs2 = Text("CS2", font_size=72)
        cs2.move_to(UP * 3)

        self.play(Write(cs2))

        # First level
        communication = Text("Communication", font_size=28)
        economy = Text("Economy", font_size=28)
        strategy = Text("Strategy", font_size=28)
        mechanics = Text("Mechanics", font_size=28)

        first_level = VGroup(communication, economy, strategy, mechanics)
        first_level.arrange(RIGHT, buff=1.5)
        first_level.move_to(UP * 0.8)

        cs2_to_strategy_line = None

        for label in first_level:
            line = Line(cs2.get_bottom(), cs2.get_bottom(), stroke_width=4)
            self.add(line)
            if label is strategy:
                cs2_to_strategy_line = line

            self.play(
                line.animate.put_start_and_end_on(cs2.get_bottom(), label.get_top()),
                run_time=0.8,
            )
            self.play(Write(label), run_time=0.3)

        # ========================
        # Strategy Branch (first)
        # ========================
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

        # ========================
        # Communication Branch
        # ========================
        blaming = Text("Blaming", font_size=22)
        flaming = Text("Flaming", font_size=22)
        shouting = Text("Shouting", font_size=22)

        communication_children = VGroup(blaming, flaming, shouting)
        communication_children.arrange(RIGHT, buff=0.8)
        communication_children.next_to(communication, DOWN, buff=1.2)

        left_margin = 0.5
        if communication_children.get_left()[0] < -config.frame_width / 2 + left_margin:
            shift_amount = (
                -config.frame_width / 2 + left_margin
            ) - communication_children.get_left()[0]
            communication_children.shift(RIGHT * shift_amount)

        for label in communication_children:
            line = Line(
                communication.get_bottom(), communication.get_bottom(), stroke_width=3
            )
            self.add(line)
            self.play(
                line.animate.put_start_and_end_on(
                    communication.get_bottom(), label.get_top()
                ),
                run_time=0.6,
            )
            self.play(Write(label), run_time=0.3)

        # ========================
        # Third level: Early Round → Information, Map Control
        # ========================
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

        # ========================
        # Yellow cascade down the entire pathway
        # ========================
        # 1. CS2 text
        self.play(cs2.animate.set_color(YELLOW), run_time=0.4)
        # 2. Line CS2 → Strategy
        self.play(cs2_to_strategy_line.animate.set_stroke(YELLOW), run_time=0.4)
        # 3. Strategy text
        self.play(strategy.animate.set_color(YELLOW), run_time=0.4)
        # 4. Line Strategy → Early Round
        self.play(strategy_to_early_round_line.animate.set_stroke(YELLOW), run_time=0.4)
        # 5. Early Round text
        self.play(early_round.animate.set_color(YELLOW), run_time=0.4)
        # 6. Line Early Round → Information
        self.play(
            early_round_to_information_line.animate.set_stroke(YELLOW), run_time=0.4
        )
        # 7. Information text
        self.play(information.animate.set_color(YELLOW), run_time=0.4)

        self.wait(2)
