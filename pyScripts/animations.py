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


class InfiniteCountingLoading(Scene):
    def construct(self):
        # --- Part 1: Counting numbers ---
        count_title = Text("Counting all numbers starting from 1...", font_size=36)
        self.play(Write(count_title))
        self.wait(0.8)

        # Show a few numbers appearing quickly
        numbers = VGroup()
        for i in range(1, 7):
            num = Text(str(i), font_size=48)
            numbers.add(num)
        numbers.arrange(RIGHT, buff=0.5)
        numbers.next_to(count_title, DOWN, buff=1.0)

        for num in numbers:
            self.play(Write(num), run_time=0.2)
            self.wait(0.1)

        # Add an ellipsis to indicate infinity
        ellipsis = Text("...", font_size=60)
        ellipsis.next_to(numbers, RIGHT, buff=0.3)
        self.play(Write(ellipsis))
        self.wait(0.5)

        # Conclusion: it would take infinite time
        infinity_text = Text("would take ∞ time", font_size=36, color=YELLOW)
        infinity_text.next_to(numbers, DOWN, buff=1.0)
        self.play(Write(infinity_text))
        self.wait(2)

        # Transition: fade out counting elements
        self.play(FadeOut(VGroup(count_title, numbers, ellipsis, infinity_text)))
        self.wait(0.5)

        # --- Part 2: Loading bar that never reaches 100% ---
        bar_title = Text("Loading...", font_size=36)
        bar_title.to_edge(UP)
        self.play(Write(bar_title))

        # Outer border
        border = RoundedRectangle(
            width=6,
            height=0.8,
            corner_radius=0.2,
            stroke_color=WHITE,
            stroke_width=4,
            fill_opacity=0,
        )
        border.next_to(bar_title, DOWN, buff=1.0)
        self.play(Create(border))

        # Inner fill rectangle
        fill = Rectangle(
            width=0, height=0.6, fill_color=BLUE, fill_opacity=1, stroke_width=0
        )
        fill.align_to(border, LEFT)
        fill.align_to(border, UP)  # flush top edges
        fill.shift(UP * 0.1)  # align inside border
        self.add(fill)

        # Percentage text (always updated)
        percent_text = Text("0%", font_size=32, color=WHITE)
        percent_text.move_to(border.get_center())

        # Update function for percent text and fill width
        def update_bar(mob, alpha):
            # alpha goes from 0 to 1 as the animation progresses
            # We use a function that approaches 100 but never reaches it: 100*(1 - exp(-5*alpha))
            percent = 100 * (1 - np.exp(-5 * alpha))
            # Cap at 99.99 to avoid display rounding to 100
            capped = min(percent, 99.99)
            # Update fill width
            fill.stretch_to_fit_width(border.width * capped / 100)
            fill.align_to(border, LEFT)
            # Update text
            new_text = Text(f"{capped:.2f}%", font_size=32, color=WHITE)
            new_text.move_to(border.get_center())
            percent_text.become(new_text)

        # Animation: the bar grows slowly but asymptotically
        self.play(
            UpdateFromAlphaFunc(
                VGroup(fill, percent_text), update_bar, run_time=8, rate_func=linear
            )
        )

        # Final message
        never_text = Text("It never reaches 100%", font_size=30, color=RED)
        never_text.next_to(border, DOWN, buff=1.0)
        self.play(Write(never_text))
        self.wait(2)


class CS2MindMapWithLoadingBars(Scene):
    def construct(self):
        # ==============================================================
        # ORIGINAL TREE CONSTRUCTION (unchanged)
        # ==============================================================
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
        first_level.arrange(RIGHT, buff=1.0)
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

        # Add Time Management, then centre all five first‑level labels
        time_mgmt = Text("Time Management", font_size=28)
        time_mgmt.next_to(mechanics, RIGHT, buff=1.0)
        all_labels = VGroup(communication, economy, strategy, mechanics, time_mgmt)
        target_center = UP * 0.8
        shift = target_center - all_labels.get_center()

        self.add(time_mgmt)

        anims = []
        for label in all_labels:
            anims.append(label.animate.shift(shift))
        for label, line in zip(first_level_labels, first_level_lines):
            target_top = label.get_top() + shift
            anims.append(
                line.animate.put_start_and_end_on(cs2.get_bottom(), target_top)
            )
        line_time = Line(cs2.get_bottom(), cs2.get_bottom(), stroke_width=4)
        self.add(line_time)
        target_top_time = time_mgmt.get_top() + shift
        anims.append(
            line_time.animate.put_start_and_end_on(cs2.get_bottom(), target_top_time)
        )
        self.play(AnimationGroup(*anims), run_time=1.2)

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

        # ==============================================================
        # NEW: LOADING BARS FOR EVERY NODE (LaTeX‑free)
        # ==============================================================
        percentages = {
            communication: 80,
            economy: 70,
            strategy: 50,  # lowest among siblings
            mechanics: 85,
            time_mgmt: 60,
            early_round: 30,  # lowest
            mid_round: 50,
            afterplant: 40,
            information: 20,  # lowest
            map_control: 35,
            jiggle: 10,
            jumpspot: 15,
            pixel_angle: 12,
            awp_hold: 14,
        }

        all_nodes = [
            communication,
            economy,
            strategy,
            mechanics,
            time_mgmt,
            early_round,
            mid_round,
            afterplant,
            information,
            map_control,
            jiggle,
            jumpspot,
            pixel_angle,
            awp_hold,
        ]

        trackers = []  # (ValueTracker, target percentage)
        pct_texts = []  # Text mobjects that display the percentage

        for node in all_nodes:
            pct_target = percentages[node]

            # Background rectangle
            bg_rect = Rectangle(
                width=node.get_width() + 0.6,
                height=node.get_height() + 0.4,
                stroke_color=WHITE,
                stroke_width=1,
                fill_opacity=0.15,
                fill_color=GREY,
                z_index=-1,
            )
            bg_rect.move_to(node.get_center())

            # Yellow fill rectangle (starts empty)
            fill_rect = Rectangle(
                width=0,
                height=bg_rect.get_height(),
                fill_color=YELLOW,
                fill_opacity=0.7,
                stroke_width=0,
                z_index=0,
            )
            fill_rect.align_to(bg_rect, LEFT)
            fill_rect.align_to(bg_rect, UP)
            fill_rect.shift(UP * 0.01)  # nudge to sit inside border

            # Percentage text (plain Text, no LaTeX)
            pct_text = Text("0%", font_size=12, color=WHITE, z_index=1)
            # Position it to the right of the bar, and keep it there with an updater
            pct_text.next_to(bg_rect, RIGHT, buff=0.1)

            # Value tracker for this node
            tracker = ValueTracker(0)

            # --- Updater functions ---
            def make_fill_updater(fr=fill_rect, bg=bg_rect, tr=tracker):
                def updater(mob):
                    mob.stretch_to_fit_width(bg.width * tr.get_value() / 100)
                    mob.align_to(bg, LEFT)

                return updater

            def make_text_updater(txt=pct_text, tr=tracker):
                def updater(mob):
                    val = int(round(tr.get_value()))
                    mob.become(Text(f"{val}%", font_size=12, color=WHITE))
                    # Keep it anchored to the right of the background
                    mob.next_to(bg_rect, RIGHT, buff=0.1)

                return updater

            fill_rect.add_updater(make_fill_updater())
            pct_text.add_updater(make_text_updater())

            self.add(bg_rect, fill_rect, pct_text)

            trackers.append((tracker, pct_target))

        self.wait(0.5)

        # Animate all trackers from 0 → target percentages
        anims = []
        for tracker, target in trackers:
            anims.append(tracker.animate.set_value(target))
        self.play(AnimationGroup(*anims), run_time=3, rate_func=smooth)
        self.wait(2)


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
