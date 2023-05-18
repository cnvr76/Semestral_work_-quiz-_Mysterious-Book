import textwrap, random
import PySimpleGUI
from TriviaAPI_questions import request_q
import input_questions as iq

## Parameters ---------------------------------------------------------
from config import *
## Main function ---------------------------------------------------------
def main():
    global FPS, ticks, intro_video_run, input_text, input_active, \
        themes_dict, objects, blue_check, red_check, TURN, \
        blue_score, red_score, can_answer, round_count, base_color_btn, \
        answered_correctly, Round, End, answer_input_active, rules_clicked

    intro_video_run = False
    run = True
    End = False

    # setting up the score here for replay ability
    blue_score, red_score = 0, 0

    # setting up basic parameters for button check and turn
    TURN = ["Red", "Blue"]
    round_count = 0
    can_answer = False
    blue_check, red_check = False, False

    # start of the main loop
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.03)
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # running intro (up to rules)
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not intro_video_run:
                intro_video_run = True
                video_play(2)
                input_active = True

            # checking if mouse clicked to show the rules
            if event.type == pg.MOUSEBUTTONDOWN and not rules_clicked and ticks == 2:
                ticks = 10
                input_active = False
                rules_clicked = True
            elif event.type == pg.MOUSEBUTTONDOWN and ticks == 10:
                rules_clicked = False
                input_active = True
                screen.blit(bg_image_mid, (0, 0))
                ticks = 2

            # theme topic input
            if event.type == pg.KEYDOWN and input_active:
                if event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]
                    screen.blit(bg_image_mid, (0, 0))
                else:
                    if len(input_text) < 2 and event.unicode.isdigit():
                        input_text += event.unicode

            # running to the end of animation
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and input_active:
                try:
                    if int(input_text) in list(themes_dict.values()):
                        video_play(3)
                        input_active = False
                        if not red_check and not blue_check:
                            labels("keys")
                            labels("hint")
                            screen.blit(B_normal, B_pos)
                            screen.blit(R_normal, R_pos)
                    else:
                        screen.blit(bg_image_mid, (0, 0))
                        labels(404)
                except ValueError:
                    screen.blit(bg_image_mid, (0, 0))
                    labels(400)

            # if starter buttons were clicked -> showing question
            if red_check and blue_check and ticks == 4:
                pg.time.wait(1000)
                new_question()

            # checking who clicked faster (needs to be a function)
            if not red_check and not blue_check and ticks >= 4 and can_answer:
                screen.blit(bg_image_end_btn, (0, 0))
                screen.blit(B_normal, B_pos_2)
                screen.blit(R_normal, R_pos_2)
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    blue_check = button_click_game("blue")
                    if blue_check and not red_check:
                        TURN = TURN[::-1]
                        labels("turn")
                        can_answer = False
                        if Q_TYPE == 3 and Round != 5:
                            answer_input_active = True

                if event.type == pg.KEYDOWN and event.key == pg.K_0:
                    red_check = button_click_game("red")
                    if red_check and not blue_check:
                        labels("turn")
                        can_answer = False
                        if Q_TYPE == 3:
                            answer_input_active = True

            # checking if "READY" buttons were clicked (both)
            if event.type == pg.KEYDOWN:
                if not blue_check and ticks == 3 and event.key == pg.K_1:
                    blue_check = button_click_contract("blue")
                    if blue_check and not red_check:
                        screen.blit(R_normal, R_pos)
                    if red_check and blue_check:
                        all_clicked()
                        labels("hint")
                        labels("signed")
                        ticks = 4

                if not red_check and ticks == 3 and event.key == pg.K_0:
                    red_check = button_click_contract("red")
                    if red_check and not blue_check:
                        screen.blit(B_normal, B_pos)
                    if red_check and blue_check:
                        all_clicked()
                        labels("hint")
                        labels("signed")
                        ticks = 4

                # handling text input events
                if ticks == 6:
                    text = input_answer.handle_event(event)
                    if text is not None:
                        print(f" * Entered text: {text}")
                        get_option(text.title())

        # starting screen (waiting until pressing "Space")
        if ticks == 0:
            video_play(1)
            labels(1)
        # still frame for rules and entering the topic
        if ticks == 2:
            labels(2)
            FastLabel("Mouse click to read the rules", WIDTH / 2, HEIGHT-60, rules_font, color="white", wrap=False)
            input_text_label = theme_font.render(input_text, 1, (37, 13, 5))
            screen.blit(input_text_label, (WIDTH/2 + 83, HEIGHT/2 - input_text_label.get_height()/6))
        # showing rules
        if ticks == 10:
            screen.blit(bg_image_mid, (0, 0))
            screen.blit(rules_image, (70, 20))
            FastLabel("Mouse click to close", WIDTH / 2 + 40, HEIGHT-60, rules_font, color="white")
        # still frame for buttons for variants
        if not can_answer:
            pg.display.flip()
            if ticks == 4:
                # drawing buttons (multiple choice)
                opt_1 = Button("A", 120, 350, 50, 50)
                opt_2 = Button("B", 120, 450, 50, 50)
                opt_3 = Button("C", 350, 350, 50, 50)
                opt_4 = Button("D", 350, 450, 50, 50)
            elif ticks == 5:
                # drawing buttons (boolean)
                opt_T = Button("True", 120, 350, 100, 50)
                opt_F = Button("False", 320, 350, 100, 50)
            elif ticks == 6:
                # drawing input box (text-type)
                input_answer.update()
                input_answer.draw(screen)
            elif ticks == 7:
                # drawing button to restart the game
                screen.blit(bg_image_end_btn, (0, 0))
                screen.blit(bg_image_end_cut, (0, 0))
                screen.blit(contract, (WIDTH/2+50, 25))
                opt_again = Button("Revive?", 220, HEIGHT-200, 100, 50, func=video_play)

        pg.display.flip()

## Functions ---------------------------------------------------------
def button_click_game(color):
    global image, TURN
    if color == "blue":
        image = B_pressed
    elif color == "red":
        image = R_pressed

    screen.blit(bg_image_end_cut, (0, 0))

    labels("score")
    screen.blit(B_pressed if color == "red" else R_pressed, B_pos_2 if color == "red" else R_pos_2)
    screen.blit(image, B_pos_2 if color == "blue" else R_pos_2)
    pg.display.flip()

    return True

# option buttons function
def get_option(opt):
    global correct_option, TURN, blue_score, red_score, answered_correctly, End

    answered_correctly = False

    if opt == correct_option and not End:
        if TURN[0].lower() == "blue":
            blue_score += 1
        else:
            red_score += 1
        TURN.clear()
        answered_correctly = True
    else:
        try:
            TURN.pop(0)
            button_click_game(TURN[0].lower())
            labels('turn')
        except IndexError:
            pass

    # generate another question on this topic
    if not TURN and not End:
        if answered_correctly:
            new_question()
        else:
            FastLabel("No one dared to get the answer right...",
                      B_pos_2[0]+25, HEIGHT/2, rules_font, wrap=False)
            pg.time.wait(1500)
            new_question()

    pg.display.flip()

def new_question():
    global can_answer, blue_check, red_check, TURN, round_count, \
        Round, input_text, blue_score, red_score, objects, Q_TYPE, ticks, \
        generated, input_answer, answer_input_active, q_type_num, End
    # counting what round is it
    q_in_round = 4
    Round = round_count // q_in_round + 1
    if round_count % q_in_round == 0 and Round < 4:
        print(f"Round {Round}")
    if Round == 4:
        input_text = random.choice(list(themes_dict.values()))
        for key, value in themes_dict.items():
            if value == input_text:
                random_theme = key

    # generating
    TURN = ["Red", "Blue"]
    if Round != 5:
        screen.blit(bg_image_end, (0, 0))
        if Q_TYPE == 1 or Q_TYPE == 2 or Q_TYPE == 3:
            q_type_num = random.randint(1, 3)

            if q_type_num == 1:
                ticks = 4
                labels("Q_multiple")
            elif q_type_num == 2:
                ticks = 5
                labels("Q_bool")
                FastLabel(generated[0], 100, 90, game_font)
            elif q_type_num == 3:
                ticks = 6
                input_answer = TextInput(170, 400, 200, 30, font=game_font)
                labels("Q_input")
                FastLabel(generated, 100, 100, game_font)

            Q_TYPE = q_type_num

        labels("score")
        if Round < 4:
            FastLabel(f"Round {Round}", WIDTH / 4 - 25, 40, game_font)
        else:
            FastLabel(f"Theme now is {random_theme.upper()} MUAHAHAHAHAHA!",
                      WIDTH/4-100, 18, game_font, color=(0,0,0))
        can_answer = True
        blue_check, red_check = False, False
    else:
        # counting the score
        End = True
        ticks = 7
        screen.blit(bg_image_end, (0, 0))
        if blue_score > red_score:
            text = "Well, Red, you lost"
        elif red_score > blue_score:
            text = "Well, Blue, you lost"
        else:
            text = "I don't like ties, so, I guess, today you both die"
        FastLabel(f"So, Blue has {blue_score} points", 130, 100, game_font, color=(3, 34, 84))
        FastLabel(f"And Red has {red_score} of those", 130, 130, game_font, color=(84, 3, 19))
        FastLabel(text, 130, 200, game_font)
        return
    round_count += 1
    pg.display.flip()

def all_clicked():
    screen.blit(R_chosen, R_pos)
    screen.blit(B_chosen, B_pos)

def button_click_contract(button):
    if button == "blue":
        image = B_pressed
    elif button == "red":
        image = R_pressed

    screen.blit(contract_image_end, (0, 0))
    labels("keys")
    labels("hint")
    screen.blit(image, B_pos if button == "blue" else R_pos)
    pg.display.flip()

    return True

def labels(lab_num):
    global game_font, rules_font, theme_font, btn_font, intro_video_run, \
        input_text, correct_option, TURN, blue_score, red_score, generated

    if lab_num == 1 and not intro_video_run:
        pg.time.wait(500)
        INTRO_label = game_font.render("Press <Space> to start", 1, (255, 255, 255))
        screen.blit(INTRO_label, (WIDTH / 2 - INTRO_label.get_width() / 2, HEIGHT - INTRO_label.get_height() * 2))
    elif lab_num == 2 and intro_video_run:
        themes_label = game_font.render("THEMES:", 1, (255, 255, 255))
        screen.blit(themes_label, (WIDTH/4 + themes_label.get_width()/2, 70))
        Themes = """General culture: 9
                  History: 23
                  Geography: 22
                  Music: 12
                  Cinema: 11
                  Literature: 10
                  Science: 17
                  Computer Science: 18
                  Sports: 21
                  Entertainment: 14
                  Religion: 20
                  Architecture: 29"""
        Themes_wrapped = textwrap.wrap(Themes, 30)
        y = HEIGHT/5
        for line in Themes_wrapped:
            mid_label = rules_font.render(line, 1, (255, 255, 255))
            screen.blit(mid_label, (WIDTH/5, y))
            y += mid_label.get_height() + 5
    elif lab_num == "Q_multiple":
        # receiving and processing the questions
        letters = ["A", "B", "C", "D"]
        generated = request_q(int(input_text), 'multiple')
        correct_option = q_output(generated)
        # showing the question itself on screen
        q_text = textwrap.wrap(generated[0], 27)
        y_1 = 80
        for line in q_text:
            question_label = game_font.render(line, 1, (37, 13, 5))
            screen.blit(question_label, (100, y_1))
            y_1 += question_label.get_height() + 5
        # showing the answers on screen
        for i, line in enumerate(generated[1]):
            answer_label = game_font.render(f"{letters[i]}: {line}", 1, (37, 13, 5))
            screen.blit(answer_label, (100, y_1))
            y_1 += answer_label.get_height() + 5
    elif lab_num == "Q_bool":
        generated = request_q(int(input_text), "boolean")
        correct_option = generated[2]
        print(f"Correct = {correct_option}")
    elif lab_num == "Q_input":
        rnd_index = random.randint(0, len(iq.questions)-1)
        generated = iq.questions[rnd_index]
        correct_option = iq.answers[rnd_index]
        print(f"Correct = {correct_option}")
    elif lab_num == "signed":
        signed_label = game_font.render("Signed", 1, (56, 6, 6))
        screen.blit(signed_label, (WIDTH / 3 + signed_label.get_width() / 2, HEIGHT / 1.3))
    elif lab_num == "keys":
        blue_label = rules_font.render("Blue's key is <1>", 1, (37, 13, 5))
        red_label = rules_font.render("Red's key is <0>", 1, (37, 13, 5))

        screen.blit(blue_label, (B_pos[0]+15, B_pos[1]+B_normal.get_height()+10))
        screen.blit(red_label, (R_pos[0]+15, R_pos[1]+R_normal.get_height()+10))
    elif lab_num == "hint":
        hint_1 = "Click your button as fast as you can to answer first and score points. Friendly reminder: " \
                 "the one with the lowest score by the end meets their doom"
        hint_1_wrapped = textwrap.wrap(hint_1, 23)
        hint_2 = "Well, it doesn't really matter if you know the answer, but remember that speed alone won't" \
                 " be enough to survive :)"
        hint_2_wrapped = textwrap.wrap(hint_2, 23)
        y_2 = HEIGHT / 4.5
        for i in range(max(len(hint_1_wrapped), len(hint_2_wrapped))):
            if i < len(hint_1_wrapped):
                hint_1_label = rules_font.render(hint_1_wrapped[i], 1, (37, 13, 5))
                screen.blit(hint_1_label, (70, y_2))
            if i < len(hint_2_wrapped):
                hint_2_label = rules_font.render(hint_2_wrapped[i], 1, (37, 13, 5))
                screen.blit(hint_2_label, (WIDTH/2+230, y_2))
            y_2 += hint_1_label.get_height()+5
    elif lab_num == "turn":
        pg.time.wait(500)

        screen.blit(R_pressed if TURN[0] == "Blue" else B_pressed, R_pos_2 if TURN[0] == "Blue" else B_pos_2)
        screen.blit(B_chosen if TURN[0] == "Blue" else R_chosen, B_pos_2 if TURN[0] == "Blue" else R_pos_2)
        turn_label = rules_font.render(f"So, it's {TURN[0]}'s turn", 1, (37, 13, 5))
        screen.blit(turn_label, (WIDTH/2+turn_label.get_width(), B_pos_2[1]-turn_label.get_height()*2))
    elif lab_num == "score":
        score_label_1 = game_font.render(f"Blue: {blue_score} points", 1, (3, 34, 84))
        score_label_2 = game_font.render(f"Red: {red_score} points", 1, (84, 3, 19))
        screen.blit(score_label_1, (B_pos_2[0]+score_label_2.get_width()/1.5, HEIGHT / 4))
        screen.blit(score_label_2, (B_pos_2[0]+ score_label_2.get_width()/1.5, HEIGHT / 4 + 25))

    # error labels
    elif lab_num == 404:
        error_label = game_font.render("Theme is not in suggested topics", 1, (214, 101, 9))
        screen.blit(error_label, (WIDTH/2-error_label.get_width()/2, HEIGHT-error_label.get_height()*2))
    elif lab_num == 400:
        error_label = game_font.render("Please, enter a number", 1, (214, 101, 9))
        screen.blit(error_label, (WIDTH / 2 - error_label.get_width() / 2, HEIGHT - error_label.get_height() * 2))

    pg.display.update()

def video_play(vid_num):
    global video_intro, video_end, INTRO, video_again, phrase_2, ticks, input_text
    global bg_image_mid, bg_image_intro, bg_image_end, contract_image_end

    if vid_num == 1:
        logo_sound.set_volume(0.05)
        logo_sound.play()
        video = INTRO
    elif vid_num == 2:
        video = video_intro
    elif vid_num == 3:
        pages_sound.play()
        video = video_end
    elif type(vid_num) == str:
        video = video_again

    video.play()
    while video.is_playing:
        video.set_size((WIDTH, HEIGHT))
        frame = video.get_frame()
        if frame is None:
            break
        screen.blit(frame, (0, 0))
        pg.display.update()

    if not video.is_playing:
        try:
            if vid_num == 1:
                image = bg_image_intro
            elif vid_num == 2:
                image = bg_image_mid
            elif vid_num == 3:
                image = contract_image_end
            elif type(vid_num) == str:
                input_text = ""
                ticks = 0
                main()
            screen.blit(image, (0, 0))
        except UnboundLocalError:
            pass

    ticks = vid_num if isinstance(vid_num, int) else ticks

def q_output(generated):
    replace_list = ['&ldquo;', '&rdquo;', "&rsquo;", "&#039;", "&quot;",
                    "&aacute;", "&amp;", "&eacute;"]
    for i in range(len(generated)):
        if isinstance(generated[i], str):
            for replace in replace_list:
                generated[i] = generated[i].replace(replace, "'")
        elif isinstance(generated[i], list):
            for j in range(len(generated[i])):
                for replace in replace_list:
                    generated[i][j] = generated[i][j].replace(replace, "'")

    letters = ["A", "B", "C", "D"]
    correct = generated[2]
    for i in range(4):
        # print(f"{letters[i]}: {generated[1][i]}")
        if generated[1][i] == correct:
            letter_correct = i
    correct_out = f"{letters[letter_correct]}: {correct}"
    print("Correct = ", correct_out)

    return letters[letter_correct]

## Classes ---------------------------------------------------------
class TextInput:
    def __init__(self, x, y, width, height, font=None):
        self.rect = pg.Rect(x, y, width, height)
        self.font = font or pg.font.Font(None, height)
        self.text = ""
        self.color = pg.Color((37, 13, 5))

    def handle_event(self, event):
        global TURN, answer_input_active
        if event.type == pg.KEYDOWN and answer_input_active:
            if event.key == pg.K_RETURN:
                # return text and reset input
                text = self.text
                self.text = ""
                if len(TURN) != 0 and Q_TYPE == 3:
                    answer_input_active = True
                else:
                    answer_input_active = False
                return text
            elif event.key == pg.K_BACKSPACE:
                screen.blit(bg_image_end_btn, (0, 0))
                self.text = self.text[:-1]
            else:
                if len(self.text) < 13 and event.unicode.isalpha():
                    screen.blit(bg_image_end_btn, (0, 0))
                    self.text += event.unicode

    def update(self):
        # render text input box
        txt_surface = self.font.render(self.text, 1, self.color)
        width = max(self.rect.w, txt_surface.get_width()+10)
        self.rect.w = width
        pg.display.update(self.rect)

    def draw(self, screen):
        # draw text input box
        pg.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.font.render(self.text, 1, self.color), (self.rect.x+5, self.rect.y+5))

class FastLabel:
    def __init__(self, text, posx, posy, font, color=(37,13,5), wrap=True):
        self.text = text
        self.posx = posx
        self.posy = posy
        self.font = font
        self.color = color
        self.wrap = wrap
        self.show()
    def show(self):
        if self.wrap:
            replace_list = ['&ldquo;', '&rdquo;', "&rsquo;", "&#039;", "&quot;"]
            for i in range(len(self.text)):
                if isinstance(self.text, str):
                    for replace in replace_list:
                        self.text = self.text.replace(replace, "'")

            wrap_text = textwrap.wrap(self.text, 27)
            wrap_y = self.posy
            for line in wrap_text:
                label_text = self.font.render(line, 1, self.color)
                screen.blit(label_text, (self.posx, wrap_y))
                wrap_y += label_text.get_height() + 5
        else:
            label_text = self.font.render(self.text, 1, self.color)
            screen.blit(label_text, (self.posx, self.posy))
        pg.display.flip()

class Button:
    def __init__(self, text, x, y, width, height, func=get_option, color=(37, 13, 5)):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.func = func
        self.hover_color_B = (3, 65, 166)
        self.hover_color_R = (204, 36, 6)
        self.hover = False
        self.draw()

    def draw(self):
        global clicked, TURN, answered_correctly
        pos = pg.mouse.get_pos()
        action = False
        button_rect = pg.rect.Rect(self.x, self.y, self.width, self.height)

        # Button logic
        if button_rect.collidepoint(pos):
            # Clicking
            if pg.mouse.get_pressed()[0]:
                clicked = True
                self.func(self.text)
            elif not pg.mouse.get_pressed()[0] and clicked:
                clicked = False
                action = True

            # Hovering
            if TURN[0].lower() == "blue":
                opt_color = self.hover_color_B
            else:
                opt_color = self.hover_color_R

            self.hover = True
            pg.draw.rect(screen, opt_color, button_rect, 3, border_radius=5)
        else:
            # Still phase
            pg.draw.rect(screen, self.color, button_rect, 3, border_radius=5)
            self.hover = False

        text_img = game_font.render(self.text, True, self.color if not self.hover else opt_color)
        text_rect = text_img.get_rect(center=button_rect.center)
        screen.blit(text_img, text_rect)

        pg.display.flip()

        return action

## Starting ---------------------------------------------------------
if __name__ == '__main__':
    main()






