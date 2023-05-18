import pygame as pg
from pygamevideo import Video

pg.init()
pg.font.init()

# window size
k = 0.5
WIDTH = 1920 * k
HEIGHT = 1080 * k
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Mysterious book")
icon = pg.image.load("Images/icon.png")
icon = pg.transform.scale(icon, (32, 32))
pg.display.set_icon(icon)
# fonts
font_link = "Fonts/Unutterable.ttf"
game_font = pg.font.Font(font_link, 20)
rules_font = pg.font.Font(font_link, 15)
theme_font = pg.font.Font(font_link, 100)
# input parameters
Q_TYPE = 1
rules_clicked = False
answer_input_active = False
clicked = False
input_active = False
input_text = ""
themes_dict = {'General culture': 9,
               'History': 23,
               'Geography': 22,
               'Music': 12,
               'Cinema': 11,
               'Literature': 10,
               'Science': 17,
               'Computer Science': 18,
               'Sports': 21,
               'Entertainment': 14,
               'Religion': 20,
               'Architecture': 29}
# FPS
FPS = 60
ticks = 0
clock = pg.time.Clock()

# uploading videos
video_intro = Video("Images/phrase+book_intro.mp4")
video_end = Video("Images/phrase+book_end.mp4")
INTRO = Video("Images/INTRO.mp4")
video_again = Video("Images/book_again.mp4")

# uploading music
pg.mixer.music.load('Sounds/scary_ambient.mp3')
pages_sound = pg.mixer.Sound("Sounds/flipping_papers.mp3")
logo_sound = pg.mixer.Sound("Sounds/logo.wav")

# uploading images
bg_image_1 = pg.image.load("Images/zero_frame.png")
bg_image_intro = pg.transform.scale(bg_image_1, (WIDTH, HEIGHT))

bg_image_2 = pg.image.load("Images/mid_frame.png")
bg_image_mid = pg.transform.scale(bg_image_2, (WIDTH, HEIGHT))

bg_image_3 = pg.image.load("Images/end_frame.png")
bg_image_end = pg.transform.scale(bg_image_3, (WIDTH, HEIGHT))

bg_image_4 = pg.image.load("Images/book_end_contract.jpg")
contract_image_end = pg.transform.scale(bg_image_4, (WIDTH, HEIGHT))

bg_image_5 = pg.image.load("Images/end_frame_cut.png")
bg_image_end_cut = pg.transform.scale(bg_image_5, (WIDTH, HEIGHT))

bg_image_6 = pg.image.load("Images/end_frame_cut_2.png")
bg_image_end_btn = pg.transform.scale(bg_image_6, (WIDTH, HEIGHT))

bg_image_7 = pg.image.load("Images/contract.png")
contract = pg.transform.scale(bg_image_7, (WIDTH/2.5, HEIGHT-50))

bg_image_8 = pg.image.load("Images/rules_image.png")
rules_image = pg.transform.scale(bg_image_8, (WIDTH/2.5, HEIGHT-50))

# button images
B_1 = pg.image.load("Images/B_normal.png")
B_2 = pg.image.load("Images/B_pressed.png")
B_3 = pg.image.load("Images/B_chosen.png")

B_normal = pg.transform.scale(B_1, (150, 150))
B_pressed = pg.transform.scale(B_2, (150, 150))
B_chosen = pg.transform.scale(B_3, (150, 150))

R_1 = pg.image.load("Images/R_normal.png")
R_2 = pg.image.load("Images/R_pressed.png")
R_3 = pg.image.load("Images/R_chosen.png")

R_normal = pg.transform.scale(R_1, (150, 150))
R_pressed = pg.transform.scale(R_2, (150, 150))
R_chosen = pg.transform.scale(R_3, (150, 150))

# button position
B_pos = (B_normal.get_width()/2, HEIGHT-B_normal.get_height()*1.6)
R_pos = (WIDTH-R_normal.get_width()*1.5, HEIGHT-R_normal.get_height()*1.6)

B_pos_2 = (WIDTH/2+B_normal.get_width()/3, B_pos[1]+60)
R_pos_2 = (B_pos_2[0] + R_normal.get_width()*1.5, B_pos_2[1])
