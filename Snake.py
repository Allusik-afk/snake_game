import pygame
import random
import math
import sys
import array
import json
import os
import time
import shutil
import datetime

# ==================== НАСТРОЙКИ ====================
WIDTH, HEIGHT = 900, 720
FIELD_X, FIELD_Y = 50, 110
CELL = 25
COLS, ROWS = 32, 20
FIELD_W = COLS * CELL
FIELD_H = ROWS * CELL
FIELD_RIGHT = FIELD_X + FIELD_W
FIELD_BOTTOM = FIELD_Y + FIELD_H
FPS = 60
SAVE_FILE = "save.json"
BACKUP_FILE = "save_backup.json"

APPLE_RED    = (225, 45, 45)
APPLE_LIGHT  = (255, 140, 140)
APPLE_DARK   = (160, 20, 20)
GOLD_YELLOW  = (255, 210, 60)
GOLD_LIGHT   = (255, 245, 160)
GOLD_DARK    = (200, 140, 20)
STEM         = (110, 65, 30)
LEAF         = (95, 185, 60)
LEAF_DARK    = (55, 130, 35)
ROCK_BASE    = (140, 135, 130)
ROCK_LIGHT   = (185, 180, 175)
ROCK_DARK    = (85, 80, 75)
SPIKE_BASE   = (150, 30, 60)
SPIKE_LIGHT  = (220, 60, 90)
SPIKE_DARK   = (80, 10, 30)
PANEL        = (245, 160, 55)
PANEL_DARK   = (200, 105, 25)
PANEL_LIGHT  = (255, 205, 130)
PANEL_BORDER = (140, 65, 10)
WHITE        = (255, 255, 255)
DARK         = (40, 20, 10)
BLACK        = (0, 0, 0)
SHIELD_COL   = (90, 200, 255)
SLOW_COL     = (140, 120, 255)
MAGNET_COL   = (255, 130, 220)

# Цвета ромбиков HP босса
BOSS_HP_COL = (255, 90, 90)
BOSS_HP_D   = (180, 30, 30)
BOSS_HP_BG  = (60, 40, 40)

BIOMES = {
    1: {"name": "Лужайка", "decor": "grass",
        "ground_light": (124,200,55), "ground_med": (100,175,40), "ground_dark": (70,140,30), "ground_edge": (55,115,25),
        "field": (165,135,75), "field_light": (185,155,100), "field_dark": (130,100,50), "field_edge": (95,70,35),
        "trim": (124,200,55), "trim_edge": (55,115,25)},
    2: {"name": "Зима", "decor": "snow",
        "ground_light": (245,250,255), "ground_med": (225,235,250), "ground_dark": (195,215,240), "ground_edge": (165,185,215),
        "field": (205,225,245), "field_light": (235,248,255), "field_dark": (170,200,225), "field_edge": (120,155,190),
        "trim": (250,253,255), "trim_edge": (170,195,220)},
    3: {"name": "Лес", "decor": "forest",
        "ground_light": (70,150,60), "ground_med": (50,115,45), "ground_dark": (35,85,30), "ground_edge": (25,60,20),
        "field": (105,85,55), "field_light": (135,110,75), "field_dark": (75,60,35), "field_edge": (45,35,20),
        "trim": (80,160,70), "trim_edge": (25,60,20)},
    4: {"name": "Горы", "decor": "mountains",
        "ground_light": (185,185,195), "ground_med": (155,155,170), "ground_dark": (125,125,140), "ground_edge": (95,95,110),
        "field": (140,130,125), "field_light": (175,165,160), "field_dark": (105,95,90), "field_edge": (70,65,60),
        "trim": (200,200,215), "trim_edge": (95,95,110)},
    5: {"name": "Пустыня", "decor": "desert",
        "ground_light": (245,215,140), "ground_med": (225,190,110), "ground_dark": (195,160,85), "ground_edge": (155,125,60),
        "field": (235,205,145), "field_light": (250,225,175), "field_dark": (205,175,115), "field_edge": (155,125,70),
        "trim": (245,215,140), "trim_edge": (155,125,60)},
    6: {"name": "Небо", "decor": "sky",
        "ground_light": (180,220,255), "ground_med": (140,195,245), "ground_dark": (100,155,215), "ground_edge": (70,115,180),
        "field": (200,225,255), "field_light": (230,245,255), "field_dark": (160,195,235), "field_edge": (110,150,200),
        "trim": (210,235,255), "trim_edge": (100,155,215)},
    7: {"name": "Вулкан", "decor": "volcano",
        "ground_light": (100,40,30), "ground_med": (70,25,20), "ground_dark": (45,15,12), "ground_edge": (25,8,6),
        "field": (140,60,30), "field_light": (180,90,50), "field_dark": (90,35,15), "field_edge": (50,15,8),
        "trim": (200,80,40), "trim_edge": (120,30,10)},
    8: {"name": "Океан", "decor": "ocean",
        "ground_light": (60,140,200), "ground_med": (40,100,160), "ground_dark": (25,70,120), "ground_edge": (15,45,80),
        "field": (100,180,220), "field_light": (150,210,240), "field_dark": (60,130,180), "field_edge": (30,80,130),
        "trim": (120,200,240), "trim_edge": (40,90,140)},
    9: {"name": "Космос", "decor": "space",
        "ground_light": (40,30,70), "ground_med": (25,15,45), "ground_dark": (15,8,28), "ground_edge": (8,4,15),
        "field": (60,50,100), "field_light": (100,90,150), "field_dark": (35,25,65), "field_edge": (20,12,40),
        "trim": (120,100,200), "trim_edge": (40,25,80)},
    10: {"name": "Пещера", "decor": "cave",
        "ground_light": (90,70,120), "ground_med": (60,45,85), "ground_dark": (40,28,60), "ground_edge": (22,15,35),
        "field": (80,60,110), "field_light": (120,95,150), "field_dark": (55,38,80), "field_edge": (30,20,50),
        "trim": (150,120,200), "trim_edge": (60,40,95)},
    11: {"name": "Радужный мир", "decor": "rainbow",
        "ground_light": (255,180,220), "ground_med": (200,220,255), "ground_dark": (180,200,240), "ground_edge": (140,160,210),
        "field": (240,230,180), "field_light": (255,245,220), "field_dark": (210,195,145), "field_edge": (160,140,95),
        "trim": (255,200,230), "trim_edge": (160,140,200)},
    12: {"name": "Тёмный замок", "decor": "castle",
        "ground_light": (60,40,70), "ground_med": (40,25,50), "ground_dark": (25,15,32), "ground_edge": (12,8,18),
        "field": (55,40,70), "field_light": (85,65,100), "field_dark": (35,22,45), "field_edge": (18,10,25),
        "trim": (100,80,130), "trim_edge": (35,20,50)},
}

SKINS = {
    "orange":  {"name": "Оранжевая",  "price": 0,   "animated": None,
                "main": (245,150,45), "light": (255,195,110), "dark": (200,100,25), "outline": (150,70,15)},
    "green":   {"name": "Зелёная",    "price": 30,  "animated": None,
                "main": (90,200,90), "light": (170,240,170), "dark": (50,140,50), "outline": (30,90,30)},
    "blue":    {"name": "Ледяная",    "price": 60,  "animated": None,
                "main": (100,180,240), "light": (180,220,255), "dark": (50,110,190), "outline": (30,70,140)},
    "purple":  {"name": "Магическая", "price": 100, "animated": None,
                "main": (180,100,220), "light": (220,170,255), "dark": (120,50,160), "outline": (80,30,110)},
    "red":     {"name": "Огненная",   "price": 150, "animated": None,
                "main": (240,80,60), "light": (255,160,120), "dark": (180,40,30), "outline": (120,20,15)},
    "ghost":   {"name": "Призрачная", "price": 250, "animated": "ghost",
                "main": (220,230,255), "light": (255,255,255), "dark": (180,190,220), "outline": (140,150,190)},
    "neon":    {"name": "Неоновая",   "price": 350, "animated": "neon",
                "main": (60,255,200), "light": (180,255,230), "dark": (20,180,140), "outline": (10,120,90)},
    "rainbow": {"name": "Радужная",   "price": 500, "animated": "rainbow",
                "main": (255,255,255), "light": (255,255,255), "dark": (200,200,200), "outline": (60,60,60)},
}

LEVELS = {
    1:  {"name": "Лужайка",      "biome": 1,  "rocks": 0,  "spikes": 0, "move_delay": 190, "target": 8,  "boss": False},
    2:  {"name": "Зима",         "biome": 2,  "rocks": 6,  "spikes": 0, "move_delay": 175, "target": 10, "boss": False},
    3:  {"name": "Лес",          "biome": 3,  "rocks": 10, "spikes": 1, "move_delay": 160, "target": 12, "boss": False},
    4:  {"name": "Горы",         "biome": 4,  "rocks": 12, "spikes": 2, "move_delay": 150, "target": 14, "boss": False},
    5:  {"name": "Пустыня",      "biome": 5,  "rocks": 8,  "spikes": 3, "move_delay": 140, "target": 16, "boss": True},
    6:  {"name": "Логово Ворона","biome": 6,  "rocks": 6,  "spikes": 4, "move_delay": 132, "target": 20, "boss": True},
    7:  {"name": "Вулкан",       "biome": 7,  "rocks": 10, "spikes": 4, "move_delay": 128, "target": 22, "boss": False},
    8:  {"name": "Океан",        "biome": 8,  "rocks": 8,  "spikes": 5, "move_delay": 125, "target": 24, "boss": False},
    9:  {"name": "Космос",       "biome": 9,  "rocks": 6,  "spikes": 6, "move_delay": 122, "target": 26, "boss": True},
    10: {"name": "Пещера",       "biome": 10, "rocks": 14, "spikes": 4, "move_delay": 120, "target": 28, "boss": False},
    11: {"name": "Радужный мир", "biome": 11, "rocks": 8,  "spikes": 6, "move_delay": 118, "target": 30, "boss": False},
    12: {"name": "Тёмный замок", "biome": 12, "rocks": 10, "spikes": 8, "move_delay": 115, "target": 35, "boss": True, "final": True},
}

ACHIEVEMENTS = {
    "first_apple":  {"name": "Первое яблоко",    "desc": "Съешь 1 яблоко"},
    "apple_100":    {"name": "Сотня",            "desc": "Съешь 100 яблок всего"},
    "apple_500":    {"name": "Пятьсот",          "desc": "Съешь 500 яблок всего"},
    "all_levels":   {"name": "Покоритель",       "desc": "Пройди все 12 уровней"},
    "all_skins":    {"name": "Модник",           "desc": "Купи все скины"},
    "rich":         {"name": "Богач",            "desc": "Накопи 500 монет"},
    "endless_50":   {"name": "Марафонец",        "desc": "50 очков в бесконечном режиме"},
    "combo_master": {"name": "Комбо-мастер",     "desc": "Сделай комбо ×2"},
    "shield_save":  {"name": "Спасён щитом",     "desc": "Щит спас от смерти"},
    "boss_kill":    {"name": "Победитель ворона","desc": "Победи босса"},
}

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
try:
    pygame.mixer.pre_init(44100, -16, 1, 512)
except Exception:
    pass
pygame.init()
try:
    pygame.mixer.init()
except Exception as e:
    print("Микшер недоступен:", e)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Змейка Deluxe 🐍")
clock = pygame.time.Clock()

IS_FULLSCREEN = [False]

font_huge  = pygame.font.SysFont("arial", 66, bold=True)
font_big   = pygame.font.SysFont("arial", 40, bold=True)
font_mid   = pygame.font.SysFont("arial", 26, bold=True)
font_small = pygame.font.SysFont("arial", 20, bold=True)
font_tiny  = pygame.font.SysFont("arial", 15, bold=True)

# ==================== ЗВУКИ ====================
def make_melody(notes, volume=0.25):
    sr = 44100
    buf = array.array('h')
    for freq, dur in notes:
        n = int(sr * dur)
        for i in range(n):
            t = i / sr
            v = math.sin(2 * math.pi * freq * t)
            v += 0.3 * math.sin(4 * math.pi * freq * t)
            env = 1.0 - i / n
            s = int(v * env * volume * 32767)
            buf.append(max(-32768, min(32767, s)))
    return pygame.mixer.Sound(buffer=buf.tobytes())

def make_tone(freq, dur, volume=0.2):
    return make_melody([(freq, dur)], volume)

SOUNDS = {}
try:
    SOUNDS['eat']       = make_melody([(880,0.05),(1320,0.09)], 0.22)
    SOUNDS['eat_gold']  = make_melody([(880,0.05),(1100,0.05),(1320,0.05),(1760,0.12)], 0.25)
    SOUNDS['turn']      = make_tone(520, 0.035, 0.10)
    SOUNDS['death']     = make_melody([(440,0.10),(330,0.10),(220,0.15),(110,0.25)], 0.28)
    SOUNDS['click']     = make_tone(660, 0.05, 0.15)
    SOUNDS['buy']       = make_melody([(660,0.08),(990,0.08),(1320,0.14)], 0.25)
    SOUNDS['complete']  = make_melody([(660,0.10),(880,0.10),(1100,0.10),(1320,0.10),(1760,0.22)], 0.28)
    SOUNDS['powerup']   = make_melody([(880,0.06),(1100,0.06),(1320,0.10)], 0.22)
    SOUNDS['shield']    = make_melody([(440,0.08),(660,0.12),(880,0.15)], 0.28)
    SOUNDS['boss']      = make_melody([(200,0.15),(180,0.15),(160,0.15),(140,0.25)], 0.3)
    SOUNDS['hit_boss']  = make_melody([(400,0.08),(280,0.15)], 0.3)   # ⬅️ НОВЫЙ ЗВУК
    SOUNDS['achievement'] = make_melody([(660,0.08),(880,0.08),(1100,0.08),(1320,0.08),(1760,0.2)], 0.3)
except Exception as e:
    print("Звук недоступен:", e)

GLOBAL_SAVE = None

def play(name):
    if GLOBAL_SAVE is not None and not GLOBAL_SAVE.get("sound_on", True):
        return
    s = SOUNDS.get(name)
    if s:
        try: s.play()
        except: pass

def build_music():
    try:
        notes = []
        base = [262, 294, 330, 349, 392, 349, 330, 294,
                262, 330, 392, 523, 466, 392, 330, 294]
        for n in base:
            notes.append((n, 0.32))
            notes.append((int(n*1.5), 0.08))
        notes += [(0, 0.1)] * 4
        snd = make_melody(notes, volume=0.06)
        return snd
    except Exception as e:
        print("Музыка недоступна:", e)
        return None

MUSIC = None
music_channel = None

def start_music():
    global MUSIC, music_channel
    if GLOBAL_SAVE is not None and not GLOBAL_SAVE.get("music_on", True):
        return
    if MUSIC is None:
        MUSIC = build_music()
    if MUSIC is None:
        return
    try:
        if music_channel is None:
            music_channel = MUSIC.play(loops=-1)
            if music_channel:
                music_channel.set_volume(0.4)
        elif not music_channel.get_busy():
            music_channel = MUSIC.play(loops=-1)
    except Exception:
        pass

def stop_music():
    global music_channel
    if music_channel is not None:
        try:
            music_channel.stop()
        except Exception:
            pass
        music_channel = None

def toggle_fullscreen(save):
    global screen
    new_state = not IS_FULLSCREEN[0]
    try:
        pygame.display.quit()
        pygame.display.init()
        if new_state:
            screen = pygame.display.set_mode(
                (WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(
                (WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Змейка Deluxe 🐍")
        IS_FULLSCREEN[0] = new_state
    except Exception as e:
        print("Ошибка переключения полного экрана:", e)
        try:
            pygame.display.quit()
            pygame.display.init()
            screen = pygame.display.set_mode(
                (WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
            pygame.display.set_caption("Змейка Deluxe 🐍")
            IS_FULLSCREEN[0] = False
        except Exception as e2:
            print("Не удалось восстановить окно:", e2)

    if save is not None:
        save["fullscreen"] = IS_FULLSCREEN[0]
        save_data(save)

# ==================== СОХРАНЕНИЕ ====================
def load_save():
    default = {
        "coins": 0,
        "unlocked_levels": [1],
        "unlocked_skins": ["orange"],
        "current_skin": "orange",
        "best_scores": {},
        "endless_best": 0,
        "achievements": [],
        "stats": {"total_apples": 0, "play_time": 0, "skin_uses": {}},
        "leaderboard": [],
        "last_daily": "",
        "sound_on": True,
        "music_on": True,
        "fullscreen": False,
    }
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in default.items():
            if k not in data:
                data[k] = v
        if 1 not in data["unlocked_levels"]:
            data["unlocked_levels"].append(1)
        if "orange" not in data["unlocked_skins"]:
            data["unlocked_skins"].append("orange")
        if "stats" not in data or not isinstance(data["stats"], dict):
            data["stats"] = default["stats"]
        for k, v in default["stats"].items():
            if k not in data["stats"]:
                data["stats"][k] = v
        return data
    except Exception:
        return default

def save_data(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Не сохранилось:", e)

def grant_achievement(save, key):
    if key in save["achievements"]:
        return False
    if key not in ACHIEVEMENTS:
        return False
    save["achievements"].append(key)
    save_data(save)
    play('achievement')
    return True

def check_achievements(save, game=None):
    st = save["stats"]
    if st["total_apples"] >= 1:
        grant_achievement(save, "first_apple")
    if st["total_apples"] >= 100:
        grant_achievement(save, "apple_100")
    if st["total_apples"] >= 500:
        grant_achievement(save, "apple_500")
    if save["coins"] >= 500:
        grant_achievement(save, "rich")
    if all(lid in save["unlocked_levels"] for lid in LEVELS.keys()):
        grant_achievement(save, "all_levels")
    if all(sid in save["unlocked_skins"] for sid in SKINS.keys()):
        grant_achievement(save, "all_skins")
    if save.get("endless_best", 0) >= 50:
        grant_achievement(save, "endless_50")

def add_leaderboard(save, score, level_name):
    entry = {
        "score": score,
        "level": level_name,
        "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    save["leaderboard"].append(entry)
    save["leaderboard"].sort(key=lambda x: -x["score"])
    save["leaderboard"] = save["leaderboard"][:10]

def try_daily_bonus(save):
    today = datetime.date.today().isoformat()
    if save.get("last_daily", "") != today:
        save["last_daily"] = today
        save["coins"] += 10
        save_data(save)
        return True
    return False

# ==================== ХЕЛПЕРЫ ====================
def draw_panel(surface, rect):
    shadow = rect.move(0, 3)
    pygame.draw.rect(surface, (90, 45, 5), shadow, border_radius=13)
    pygame.draw.rect(surface, PANEL_BORDER, rect, border_radius=13)
    pygame.draw.rect(surface, PANEL_DARK, rect.inflate(-3, -3), border_radius=11)
    pygame.draw.rect(surface, PANEL, rect.inflate(-9, -9), border_radius=9)
    hl = pygame.Rect(rect.x + 10, rect.y + 6, rect.w - 20, 8)
    pygame.draw.rect(surface, PANEL_LIGHT, hl, border_radius=4)

def draw_text_outline(surface, text, font, color, outline_color, pos,
                     outline_w=2, center=False):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)
    rect = base.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx == 0 and dy == 0:
                continue
            surface.blit(outline, (rect.x + dx, rect.y + dy))
    surface.blit(base, rect)

def lerp(a, b, t): return a + (b - a) * t
def smoothstep(t): return t * t * (3 - 2 * t)

def hsv_to_rgb(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if h < 60: r, g, b = c, x, 0
    elif h < 120: r, g, b = x, c, 0
    elif h < 180: r, g, b = 0, c, x
    elif h < 240: r, g, b = 0, x, c
    elif h < 300: r, g, b = x, 0, c
    else: r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def get_skin_colors(skin, t=0.0, index=0):
    anim = skin.get("animated")
    if anim == "rainbow":
        h = (t * 120 + index * 20) % 360
        main = hsv_to_rgb(h, 0.9, 1.0)
        light = hsv_to_rgb((h + 30) % 360, 0.6, 1.0)
        dark = hsv_to_rgb((h - 20) % 360, 0.9, 0.7)
        outline = hsv_to_rgb((h + 180) % 360, 1.0, 0.4)
        return main, light, dark, outline, 255
    elif anim == "ghost":
        alpha = int(140 + 90 * math.sin(t * 2))
        return skin["main"], skin["light"], skin["dark"], skin["outline"], alpha
    elif anim == "neon":
        pulse = 0.7 + 0.3 * math.sin(t * 4)
        main = tuple(int(c * pulse + 40 * (1 - pulse)) for c in skin["main"])
        light = tuple(min(255, int(c * pulse + 80)) for c in skin["light"])
        return main, light, skin["dark"], skin["outline"], 255
    else:
        return skin["main"], skin["light"], skin["dark"], skin["outline"], 255

def draw_coin_icon(surface, cx, cy, r=15):
    pygame.draw.circle(surface, GOLD_DARK, (cx, cy), r)
    pygame.draw.circle(surface, GOLD_YELLOW, (cx, cy - 1), r - 2)
    pygame.draw.circle(surface, GOLD_LIGHT, (cx - r//3, cy - r//3), max(2, r//3))

def draw_coins_display(surface, coins, x=None, y=20):
    rect = pygame.Rect(0, y, 150, 50)
    rect.x = x if x is not None else WIDTH - 20 - 150
    draw_panel(surface, rect)
    cx = rect.x + 28
    cy = rect.centery
    draw_coin_icon(surface, cx, cy, 15)
    text = font_mid.render(str(coins), True, WHITE)
    surface.blit(text, (cx + 25, rect.centery - text.get_height()//2))

# ==================== ФОН ====================
bg_cache = {}
preview_cache = {}

def get_bg(biome_id):
    if biome_id not in bg_cache:
        bg_cache[biome_id] = make_background(biome_id)
    return bg_cache[biome_id]


def make_preview(biome_id, size=(110, 70)):
    w, h = size
    b = BIOMES[biome_id]
    surf = pygame.Surface(size)
    rng = random.Random(100 + biome_id * 7)

    surf.fill(b["ground_med"])
    for _ in range(40):
        x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
        r = rng.randint(1, 2)
        col = rng.choice([b["ground_light"], b["ground_dark"], b["ground_med"]])
        pygame.draw.circle(surf, col, (x, y), r)

    fx, fy = 6, 11
    fw, fh = w - 12, h - 22
    field = pygame.Rect(fx, fy, fw, fh)
    pygame.draw.rect(surf, b["field"], field)
    for _ in range(80):
        x = rng.randint(field.x + 1, field.right - 2)
        y = rng.randint(field.y + 1, field.bottom - 2)
        col = rng.choice([b["field_light"], b["field_dark"]])
        surf.set_at((x, y), col)
    pygame.draw.rect(surf, b["field_dark"], field, 2)
    pygame.draw.rect(surf, b["field_edge"], field, 1)

    tw = 5
    for x in range(field.x, field.right, tw):
        pygame.draw.polygon(surf, b["trim"], [
            (x, field.top), (x + tw // 2, field.top + 3), (x + tw, field.top)])
        pygame.draw.polygon(surf, b["trim"], [
            (x, field.bottom), (x + tw // 2, field.bottom - 3), (x + tw, field.bottom)])
    for y in range(field.y, field.bottom, tw):
        pygame.draw.polygon(surf, b["trim"], [
            (field.left, y), (field.left + 3, y + tw // 2), (field.left, y + tw)])
        pygame.draw.polygon(surf, b["trim"], [
            (field.right, y), (field.right - 3, y + tw // 2), (field.right, y + tw)])

    d = b["decor"]

    if d == "grass":
        pygame.draw.circle(surf, (135, 110, 75), (14, 5), 3)
        pygame.draw.circle(surf, (165, 140, 100), (13, 4), 1)
        pygame.draw.circle(surf, (90, 70, 40), (14, 5), 3, 1)
        pygame.draw.circle(surf, (135, 110, 75), (97, 64), 3)
        pygame.draw.circle(surf, (165, 140, 100), (96, 63), 1)
        for gx in [40, 70]:
            pygame.draw.line(surf, b["ground_edge"], (gx, 8), (gx - 1, 4), 1)
            pygame.draw.line(surf, b["ground_edge"], (gx, 8), (gx + 1, 4), 1)

    elif d == "snow":
        sx, sy = 15, 6
        pygame.draw.circle(surf, (250, 252, 255), (sx, sy + 4), 4)
        pygame.draw.circle(surf, (200, 215, 235), (sx, sy + 4), 4, 1)
        pygame.draw.circle(surf, (250, 252, 255), (sx, sy - 1), 3)
        pygame.draw.circle(surf, (250, 252, 255), (sx, sy - 5), 2)
        pygame.draw.circle(surf, (30, 30, 30), (sx - 1, sy - 5), 1)
        pygame.draw.circle(surf, (240, 140, 50), (sx, sy - 4), 1)
        for _ in range(15):
            x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
            if field.collidepoint(x, y): continue
            surf.set_at((x, y), (255, 255, 255))
        sx, sy = 96, 62
        pygame.draw.circle(surf, (250, 252, 255), (sx, sy + 3), 3)
        pygame.draw.circle(surf, (250, 252, 255), (sx, sy - 1), 2)

    elif d == "forest":
        tx, ty = 14, 10
        pygame.draw.rect(surf, (90, 55, 25), (tx - 1, ty, 3, 3))
        pygame.draw.polygon(surf, b["ground_dark"], [(tx, ty - 8), (tx - 5, ty), (tx + 5, ty)])
        pygame.draw.polygon(surf, b["ground_edge"], [(tx, ty - 8), (tx - 5, ty), (tx + 5, ty)], 1)
        tx, ty = 96, 66
        pygame.draw.rect(surf, (90, 55, 25), (tx - 1, ty, 3, 3))
        pygame.draw.polygon(surf, b["ground_dark"], [(tx, ty - 7), (tx - 4, ty), (tx + 4, ty)])
        pygame.draw.circle(surf, b["ground_light"], (55, 5), 2)
        pygame.draw.circle(surf, b["ground_light"], (70, 6), 2)

    elif d == "mountains":
        pygame.draw.polygon(surf, (140, 135, 130), [(14, 3), (3, 12), (25, 12)])
        pygame.draw.polygon(surf, (245, 250, 255), [(14, 3), (10, 6), (18, 6)])
        pygame.draw.polygon(surf, (85, 80, 75), [(14, 3), (3, 12), (25, 12)], 1)
        pygame.draw.polygon(surf, (140, 135, 130), [(96, 57), (86, 66), (106, 66)])
        pygame.draw.polygon(surf, (245, 250, 255), [(96, 57), (92, 60), (100, 60)])

    elif d == "desert":
        cx, cy = 14, 10
        pygame.draw.rect(surf, (90, 150, 70), (cx - 1, cy - 6, 3, 7))
        pygame.draw.rect(surf, (90, 150, 70), (cx - 4, cy - 3, 3, 2))
        pygame.draw.rect(surf, (90, 150, 70), (cx + 2, cy - 1, 3, 2))
        pygame.draw.rect(surf, (50, 100, 40), (cx - 1, cy - 6, 3, 7), 1)
        cx, cy = 96, 66
        pygame.draw.rect(surf, (90, 150, 70), (cx - 1, cy - 6, 3, 7))
        pygame.draw.rect(surf, (90, 150, 70), (cx - 4, cy - 3, 3, 2))
        pygame.draw.ellipse(surf, b["ground_dark"], (40, 4, 30, 6))

    elif d == "sky":
        for cx, cy in [(14, 6), (95, 63)]:
            pygame.draw.circle(surf, (255, 255, 255), (cx - 4, cy), 3)
            pygame.draw.circle(surf, (255, 255, 255), (cx, cy - 1), 4)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 4, cy), 3)
        for bx, by in [(50, 4), (70, 7)]:
            pygame.draw.arc(surf, (60, 60, 80), (bx, by, 6, 3), 0, math.pi, 1)

    elif d == "volcano":
        pygame.draw.polygon(surf, (55, 25, 20), [(14, 3), (3, 12), (25, 12)])
        pygame.draw.polygon(surf, (30, 12, 10), [(14, 3), (3, 12), (25, 12)], 1)
        pygame.draw.polygon(surf, (255, 100, 30), [(14, 3), (11, 6), (17, 6)])
        for _ in range(8):
            x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
            if field.collidepoint(x, y): continue
            pygame.draw.circle(surf, (255, 100, 30), (x, y), 1)
        pygame.draw.circle(surf, (255, 60, 20), (95, 64), 3)
        pygame.draw.circle(surf, (255, 140, 60), (94, 63), 1)

    elif d == "ocean":
        for _ in range(15):
            x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
            if field.collidepoint(x, y): continue
            pygame.draw.circle(surf, (200, 230, 250), (x, y), 1, 1)
        fx_, fy_ = 15, 6
        pygame.draw.ellipse(surf, (255, 180, 60), (fx_ - 3, fy_ - 2, 7, 5))
        pygame.draw.polygon(surf, (255, 180, 60),
                            [(fx_ + 4, fy_), (fx_ + 8, fy_ - 2), (fx_ + 8, fy_ + 2)])
        pygame.draw.circle(surf, (20, 20, 20), (fx_ - 2, fy_ - 1), 1)
        fx_, fy_ = 94, 63
        pygame.draw.ellipse(surf, (255, 120, 120), (fx_ - 3, fy_ - 2, 7, 5))
        pygame.draw.polygon(surf, (255, 120, 120),
                            [(fx_ + 4, fy_), (fx_ + 8, fy_ - 2), (fx_ + 8, fy_ + 2)])

    elif d == "space":
        for _ in range(25):
            x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
            if field.collidepoint(x, y): continue
            surf.set_at((x, y), (255, 255, 255))
        pygame.draw.ellipse(surf, (220, 200, 160), (7, 2, 14, 5), 1)
        pygame.draw.circle(surf, (220, 120, 100), (14, 5), 4)
        pygame.draw.circle(surf, (255, 200, 180), (13, 4), 1)
        pygame.draw.circle(surf, (140, 160, 220), (96, 64), 3)
        pygame.draw.circle(surf, (200, 220, 255), (95, 63), 1)

    elif d == "cave":
        pygame.draw.polygon(surf, (45, 30, 65), [(8, 0), (14, 0), (11, 7)])
        pygame.draw.polygon(surf, (45, 30, 65), [(20, 0), (25, 0), (22, 5)])
        pygame.draw.polygon(surf, (45, 30, 65), [(92, h), (98, h), (95, h - 6)])
        pygame.draw.polygon(surf, (45, 30, 65), [(102, h), (108, h), (105, h - 4)])
        pygame.draw.polygon(surf, (150, 120, 255), [(15, 4), (18, 7), (15, 10), (12, 7)])
        pygame.draw.polygon(surf, (255, 255, 255), [(15, 4), (18, 7), (15, 10), (12, 7)], 1)
        pygame.draw.polygon(surf, (200, 100, 220), [(96, 60), (99, 63), (96, 66), (93, 63)])

    elif d == "rainbow":
        for k, col in enumerate(_RAINBOW_COLORS[:5]):
            pygame.draw.arc(surf, col,
                            (2 + k * 2, 2 + k * 2, 26 - k * 4, 26 - k * 4),
                            math.pi, math.tau, 2)
        cx, cy = 95, 64
        pygame.draw.circle(surf, (255, 255, 255), (cx - 4, cy), 3)
        pygame.draw.circle(surf, (255, 255, 255), (cx, cy - 1), 4)
        pygame.draw.circle(surf, (255, 255, 255), (cx + 4, cy), 3)
        for _ in range(8):
            x = rng.randint(0, w - 1); y = rng.randint(0, h - 1)
            if field.collidepoint(x, y): continue
            pygame.draw.circle(surf, rng.choice(_RAINBOW_COLORS), (x, y), 1)

    elif d == "castle":
        pygame.draw.circle(surf, (240, 240, 200), (95, 5), 4)
        pygame.draw.circle(surf, (200, 195, 160), (95, 5), 4, 1)
        pygame.draw.circle(surf, b["ground_med"], (93, 3), 3)
        for bx in [15, 22]:
            pygame.draw.arc(surf, (20, 20, 30), (bx, 5, 4, 3), 0, math.pi, 1)
        pygame.draw.rect(surf, (50, 35, 65), (10, h - 14, 8, 14))
        pygame.draw.rect(surf, (25, 15, 35), (10, h - 14, 8, 14), 1)
        for k in range(0, 8, 3):
            pygame.draw.rect(surf, (50, 35, 65), (10 + k, h - 16, 2, 2))
        pygame.draw.rect(surf, (255, 200, 100), (13, h - 9, 2, 3))
        pygame.draw.rect(surf, (50, 35, 65), (100, h - 10, 6, 10))
        pygame.draw.rect(surf, (255, 200, 100), (102, h - 6, 2, 2))

    return surf


def get_preview(biome_id, size=(110, 70)):
    key = (biome_id, size)
    if key not in preview_cache:
        preview_cache[key] = make_preview(biome_id, size)
    return preview_cache[key]


def _in_field(x, y, m=25):
    return (FIELD_X - m < x < FIELD_RIGHT + m and
            FIELD_Y - m < y < FIELD_BOTTOM + m)

def _decor_grass(bg, rng, b):
    for _ in range(180):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 18): continue
        h = rng.randint(5, 10)
        pygame.draw.line(bg, b["ground_edge"], (x, y), (x - 3, y - h), 2)
        pygame.draw.line(bg, b["ground_edge"], (x, y), (x + 3, y - h), 2)
    for px, py in [(25,30),(55,45),(860,25),(875,40),(30,690),(860,690),(200,30),(700,30)]:
        if _in_field(px, py, 30): continue
        pr = rng.randint(8, 12)
        pygame.draw.ellipse(bg, (60, 90, 30), (px - pr, py + pr//2, pr*2, pr))
        pygame.draw.circle(bg, (135, 110, 75), (px, py), pr)
        pygame.draw.circle(bg, (165, 140, 100), (px - pr//3, py - pr//3), pr//2)
        pygame.draw.circle(bg, (90, 70, 40), (px, py), pr, 2)

def _decor_snow(bg, rng, b):
    for _ in range(300):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 18): continue
        r = rng.choice([1, 1, 2, 2, 3])
        pygame.draw.circle(bg, (255, 255, 255), (x, y), r)
    for _ in range(20):
        x = rng.randint(-30, WIDTH + 30)
        y = rng.choice([rng.randint(-10, 60), rng.randint(HEIGHT - 60, HEIGHT + 10)])
        if _in_field(x, y, 30): continue
        w = rng.randint(60, 140); h = rng.randint(20, 40)
        pygame.draw.ellipse(bg, (250, 252, 255), (x, y, w, h))
    for sx, sy in [(60,660),(840,660),(80,40),(830,40)]:
        if _in_field(sx, sy, 40): continue
        pygame.draw.circle(bg, (250, 252, 255), (sx, sy), 22)
        pygame.draw.circle(bg, (200, 215, 235), (sx, sy), 22, 2)
        pygame.draw.circle(bg, (250, 252, 255), (sx, sy - 26), 16)
        pygame.draw.circle(bg, (200, 215, 235), (sx, sy - 26), 16, 2)
        pygame.draw.circle(bg, (250, 252, 255), (sx, sy - 48), 11)
        pygame.draw.circle(bg, (200, 215, 235), (sx, sy - 48), 11, 2)
        pygame.draw.circle(bg, (30, 30, 30), (sx - 3, sy - 51), 2)
        pygame.draw.circle(bg, (30, 30, 30), (sx + 3, sy - 51), 2)
        pygame.draw.circle(bg, (240, 140, 50), (sx, sy - 48), 2)

def _decor_forest(bg, rng, b):
    for _ in range(30):
        x = rng.randint(20, WIDTH - 20)
        y = rng.randint(30, HEIGHT - 30)
        if _in_field(x, y, 45): continue
        size = rng.randint(30, 50)
        pygame.draw.rect(bg, (90, 55, 25), (x - size//8, y, size//4, size//3))
        for k in range(3):
            w = size - k * size//4
            h = size//2
            top_y = y - h - k * (size//3)
            base_y = y - k * (size//3)
            pts = [(x, top_y), (x - w//2, base_y), (x + w//2, base_y)]
            pygame.draw.polygon(bg, b["ground_dark"], pts)
            pygame.draw.polygon(bg, b["ground_edge"], pts, 2)

def _decor_mountains(bg, rng, b):
    for _ in range(15):
        x = rng.randint(20, WIDTH - 20)
        y = rng.randint(20, HEIGHT - 20)
        if _in_field(x, y, 45): continue
        size = rng.randint(28, 50)
        pts = []
        n = 9
        for i in range(n):
            a = i * math.tau / n
            r = size * (0.7 + rng.random() * 0.4)
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        pygame.draw.polygon(bg, (140, 135, 130), pts)
        pygame.draw.polygon(bg, (85, 80, 75), pts, 2)
        snow_pts = []
        for i in range(0, n, 2):
            snow_pts.append((pts[i][0], pts[i][1] - 2))
            if i + 1 < n:
                mx = (pts[i][0] + pts[i+1][0]) / 2
                my = (pts[i][1] + pts[i+1][1]) / 2
                snow_pts.append((mx, my + 2))
        if len(snow_pts) >= 3:
            pygame.draw.polygon(bg, (245, 250, 255), snow_pts)

def _decor_desert(bg, rng, b):
    for _ in range(14):
        x = rng.randint(30, WIDTH - 30)
        y = rng.randint(30, HEIGHT - 30)
        if _in_field(x, y, 40): continue
        size = rng.randint(20, 34)
        pygame.draw.rect(bg, (90, 150, 70), (x - 5, y - size, 10, size), border_radius=5)
        pygame.draw.rect(bg, (50, 100, 40), (x - 5, y - size, 10, size), 2, border_radius=5)
        arm_y = y - size + 6
        pygame.draw.rect(bg, (90, 150, 70), (x - 15, arm_y, 12, 7), border_radius=3)
        pygame.draw.rect(bg, (90, 150, 70), (x + 3, arm_y + 8, 12, 7), border_radius=3)

def _decor_sky(bg, rng, b):
    for _ in range(14):
        x = rng.randint(0, WIDTH - 80)
        y = rng.randint(0, HEIGHT - 40)
        if _in_field(x, y, 40): continue
        w = rng.randint(60, 100)
        h = rng.randint(25, 35)
        for k in range(3):
            pygame.draw.circle(bg, (255, 255, 255), (x + k * w//3, y + h//2), h//2)
        pygame.draw.ellipse(bg, (250, 252, 255), (x, y, w, h))
    for _ in range(10):
        x = rng.randint(20, WIDTH - 20)
        y = rng.randint(20, HEIGHT - 20)
        if _in_field(x, y, 40): continue
        pygame.draw.arc(bg, (60, 60, 80), (x, y, 14, 8), 0, math.pi, 2)
        pygame.draw.arc(bg, (60, 60, 80), (x + 8, y, 14, 8), 0, math.pi, 2)

def _decor_volcano(bg, rng, b):
    for _ in range(60):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 20): continue
        r = rng.randint(3, 8)
        col = rng.choice([(255,120,30),(255,60,20),(200,40,10)])
        pygame.draw.circle(bg, col, (x, y), r)
    for _ in range(12):
        x = rng.randint(30, WIDTH - 30)
        y = rng.randint(30, HEIGHT - 30)
        if _in_field(x, y, 40): continue
        size = rng.randint(20, 40)
        pts = []
        for i in range(7):
            a = i * math.tau / 7
            r = size * (0.7 + rng.random() * 0.4)
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        pygame.draw.polygon(bg, (55, 25, 20), pts)
        pygame.draw.polygon(bg, (30, 12, 10), pts, 2)
    for _ in range(30):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 20): continue
        r = rng.randint(10, 25)
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (60, 40, 50, 100), (r, r), r)
        bg.blit(s, (x-r, y-r))

def _decor_ocean(bg, rng, b):
    for _ in range(200):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 15): continue
        r = rng.randint(2, 6)
        pygame.draw.circle(bg, (200, 230, 250), (x, y), r, 2)
    for _ in range(20):
        x = rng.randint(20, WIDTH - 20)
        y = rng.randint(30, HEIGHT - 30)
        if _in_field(x, y, 40): continue
        h = rng.randint(40, 80)
        for k in range(0, h, 10):
            xo = math.sin(k * 0.3) * 5
            pygame.draw.circle(bg, (50, 150, 80), (x + xo, y + k), 5)
    for _ in range(8):
        x = rng.randint(40, WIDTH - 40)
        y = rng.randint(40, HEIGHT - 40)
        if _in_field(x, y, 40): continue
        col = rng.choice([(255,180,60),(255,120,120),(200,200,60)])
        pygame.draw.ellipse(bg, col, (x-12, y-6, 24, 12))
        pygame.draw.polygon(bg, col, [(x+10,y),(x+18,y-6),(x+18,y+6)])
        pygame.draw.circle(bg, (20,20,20), (x-6, y-2), 2)

def _decor_space(bg, rng, b):
    for _ in range(300):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 15): continue
        r = rng.choice([1, 1, 1, 2])
        pygame.draw.circle(bg, (255, 255, 255), (x, y), r)
    for _ in range(4):
        x = rng.randint(60, WIDTH - 60)
        y = rng.randint(60, HEIGHT - 60)
        if _in_field(x, y, 60): continue
        r = rng.randint(18, 28)
        col = rng.choice([(220,120,100),(140,160,220),(200,180,120)])
        pygame.draw.circle(bg, col, (x, y), r)
        pygame.draw.circle(bg, (255,255,255), (x-r//3, y-r//3), r//3)
        if rng.random() < 0.5:
            rect = pygame.Rect(x-r-8, y-4, (r+8)*2, 8)
            pygame.draw.ellipse(bg, (220,200,160), rect, 2)

def _decor_cave(bg, rng, b):
    for _ in range(30):
        x = rng.randint(0, WIDTH)
        w = rng.randint(15, 30)
        h = rng.randint(20, 50)
        pts = [(x, 0), (x+w, 0), (x+w//2, h)]
        if _in_field(x, h//2, 20): continue
        pygame.draw.polygon(bg, (45, 30, 65), pts)
        pygame.draw.polygon(bg, (25, 15, 40), pts, 2)
    for _ in range(30):
        x = rng.randint(0, WIDTH)
        w = rng.randint(15, 30)
        h = rng.randint(20, 50)
        pts = [(x, HEIGHT), (x+w, HEIGHT), (x+w//2, HEIGHT-h)]
        if _in_field(x, HEIGHT-h//2, 20): continue
        pygame.draw.polygon(bg, (45, 30, 65), pts)
        pygame.draw.polygon(bg, (25, 15, 40), pts, 2)
    for _ in range(15):
        x = rng.randint(30, WIDTH - 30)
        y = rng.randint(30, HEIGHT - 30)
        if _in_field(x, y, 40): continue
        size = rng.randint(15, 25)
        col = rng.choice([(150,120,255),(100,180,255),(200,100,220)])
        pts = [(x, y-size), (x+size//2, y), (x, y+size//2), (x-size//2, y)]
        pygame.draw.polygon(bg, col, pts)
        pygame.draw.polygon(bg, (255,255,255), pts, 1)

_RAINBOW_COLORS = [(255,100,100),(255,180,100),(255,255,100),
                   (100,255,100),(100,200,255),(180,100,255),(255,100,200)]

def _decor_rainbow(bg, rng, b):
    for _ in range(40):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if _in_field(x, y, 20): continue
        r = rng.randint(8, 20)
        col = rng.choice(_RAINBOW_COLORS)
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*col, 100), (r, r), r)
        bg.blit(s, (x-r, y-r))
    for _ in range(10):
        x = rng.randint(20, WIDTH - 60)
        y = rng.randint(20, HEIGHT - 40)
        if _in_field(x, y, 40): continue
        for k in range(3):
            pygame.draw.circle(bg, (255,255,255), (x + k*15, y), 12)

def _decor_castle(bg, rng, b):
    lx, ly = WIDTH - 100, 70
    if not _in_field(lx, ly, 40):
        pygame.draw.circle(bg, (240, 240, 200), (lx, ly), 30)
        pygame.draw.circle(bg, (200, 195, 160), (lx, ly), 30, 2)
        for _ in range(4):
            pygame.draw.circle(bg, (200, 195, 160),
                              (lx + rng.randint(-15, 15), ly + rng.randint(-15, 15)), 3)
    for _ in range(6):
        x = rng.randint(30, WIDTH - 60)
        y = rng.randint(30, HEIGHT - 80)
        if _in_field(x, y, 50): continue
        w = rng.randint(30, 50)
        h = rng.randint(60, 100)
        pygame.draw.rect(bg, (50, 35, 65), (x, y, w, h))
        pygame.draw.rect(bg, (25, 15, 35), (x, y, w, h), 2)
        for k in range(0, w, 10):
            pygame.draw.rect(bg, (50, 35, 65), (x+k, y-6, 6, 6))
        pygame.draw.rect(bg, (255, 200, 100), (x+w//2-4, y+h//2-6, 8, 12))
    for _ in range(15):
        x = rng.randint(20, WIDTH - 20)
        y = rng.randint(20, HEIGHT - 20)
        if _in_field(x, y, 30): continue
        pygame.draw.arc(bg, (20, 20, 30), (x, y, 10, 6), 0, math.pi, 2)

def make_background(biome_id):
    b = BIOMES[biome_id]
    bg = pygame.Surface((WIDTH, HEIGHT))
    rng = random.Random(42 + biome_id)
    bg.fill(b["ground_med"])
    for _ in range(900):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        if (FIELD_X - 14 < x < FIELD_RIGHT + 14 and
                FIELD_Y - 14 < y < FIELD_BOTTOM + 14):
            continue
        r = rng.randint(3, 13)
        color = rng.choice([b["ground_light"], b["ground_dark"], b["ground_light"], b["ground_med"]])
        pygame.draw.circle(bg, color, (x, y), r)

    d = b["decor"]
    if d == "grass": _decor_grass(bg, rng, b)
    elif d == "snow": _decor_snow(bg, rng, b)
    elif d == "forest": _decor_forest(bg, rng, b)
    elif d == "mountains": _decor_mountains(bg, rng, b)
    elif d == "desert": _decor_desert(bg, rng, b)
    elif d == "sky": _decor_sky(bg, rng, b)
    elif d == "volcano": _decor_volcano(bg, rng, b)
    elif d == "ocean": _decor_ocean(bg, rng, b)
    elif d == "space": _decor_space(bg, rng, b)
    elif d == "cave": _decor_cave(bg, rng, b)
    elif d == "rainbow": _decor_rainbow(bg, rng, b)
    elif d == "castle": _decor_castle(bg, rng, b)

    field_rect = pygame.Rect(FIELD_X, FIELD_Y, FIELD_W, FIELD_H)
    pygame.draw.rect(bg, b["field"], field_rect)
    for _ in range(700):
        x = rng.randint(FIELD_X + 4, FIELD_RIGHT - 4)
        y = rng.randint(FIELD_Y + 4, FIELD_BOTTOM - 4)
        r = rng.randint(1, 3)
        color = rng.choice([b["field_light"], b["field_dark"], b["field_light"], b["field"]])
        pygame.draw.circle(bg, color, (x, y), r)
    pygame.draw.rect(bg, b["field_dark"], field_rect, 5)
    pygame.draw.rect(bg, b["field_edge"], field_rect, 2)

    x = FIELD_X
    while x < FIELD_RIGHT:
        w = rng.randint(10, 16); h = rng.randint(8, 16)
        pts = [(x, FIELD_Y), (x + w//2, FIELD_Y + h), (x + w, FIELD_Y)]
        pygame.draw.polygon(bg, b["trim"], pts)
        pygame.draw.polygon(bg, b["trim_edge"], pts, 2)
        x += w - 2
    x = FIELD_X
    while x < FIELD_RIGHT:
        w = rng.randint(10, 16); h = rng.randint(8, 16)
        pts = [(x, FIELD_BOTTOM), (x + w//2, FIELD_BOTTOM - h), (x + w, FIELD_BOTTOM)]
        pygame.draw.polygon(bg, b["trim"], pts)
        pygame.draw.polygon(bg, b["trim_edge"], pts, 2)
        x += w - 2
    y = FIELD_Y
    while y < FIELD_BOTTOM:
        w = rng.randint(10, 16); h = rng.randint(8, 16)
        pts = [(FIELD_X, y), (FIELD_X + h, y + w//2), (FIELD_X, y + w)]
        pygame.draw.polygon(bg, b["trim"], pts)
        pygame.draw.polygon(bg, b["trim_edge"], pts, 2)
        y += w - 2
    y = FIELD_Y
    while y < FIELD_BOTTOM:
        w = rng.randint(10, 16); h = rng.randint(8, 16)
        pts = [(FIELD_RIGHT, y), (FIELD_RIGHT - h, y + w//2), (FIELD_RIGHT, y + w)]
        pygame.draw.polygon(bg, b["trim"], pts)
        pygame.draw.polygon(bg, b["trim_edge"], pts, 2)
        y += w - 2
    return bg

# ==================== ЧАСТИЦЫ ====================
class DeathParticle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(60, 260)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 80
        self.life = random.uniform(0.7, 1.4)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(6, 12)
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 500 * dt
        self.vx *= 0.99
        self.life -= dt
    def draw(self, s):
        if self.life <= 0: return
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * t)
        r = max(1, int(self.size * t))
        surf = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (r+1, r+1), r)
        s.blit(surf, (self.x - r - 1, self.y - r - 1))

class TrailParticle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.life = 0.55
        self.max_life = self.life
        self.size = random.uniform(3, 6)
        self.vx = random.uniform(-15, 15)
        self.vy = random.uniform(-15, 15)
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
    def draw(self, s):
        if self.life <= 0: return
        t = max(0.0, self.life / self.max_life)
        alpha = int(180 * t)
        r = max(1, int(self.size * t))
        surf = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (r+1, r+1), r)
        s.blit(surf, (self.x - r - 1, self.y - r - 1))

class FloatingText:
    def __init__(self, text, x, y, color, size=26):
        self.x, self.y = x, y
        self.life = 70
        self.max_life = 70
        font = pygame.font.SysFont("arial", size, bold=True)
        self.surface = font.render(text, True, color)
    def update(self):
        self.y -= 1.4
        self.life -= 1
    def draw(self, s):
        t = self.life / self.max_life
        surf = self.surface.copy()
        surf.set_alpha(int(255 * t))
        rect = surf.get_rect(center=(self.x, self.y))
        s.blit(surf, rect)

# ==================== ШИП ====================
class MovingSpike:
    def __init__(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.move_timer = 0
        self.angle = 0.0
        self.speed_ms = 420
    def update(self, dt_ms, dt):
        self.angle += dt * 4
        self.move_timer += dt_ms
        if self.move_timer >= self.speed_ms:
            self.move_timer = 0
            nx = self.x + self.dx; ny = self.y + self.dy
            if nx < 0 or nx >= COLS: self.dx = -self.dx; nx = self.x + self.dx
            if ny < 0 or ny >= ROWS: self.dy = -self.dy; ny = self.y + self.dy
            self.x = max(0, min(COLS-1, nx))
            self.y = max(0, min(ROWS-1, ny))
    def cell(self): return (self.x, self.y)
    def pixel_center(self):
        return (self.x*CELL + CELL//2 + FIELD_X, self.y*CELL + CELL//2 + FIELD_Y)

# ==================== БОНУС ====================
class PowerUp:
    KINDS = ["shield", "slow", "magnet"]
    def __init__(self, x, y, kind):
        self.x, self.y = x, y
        self.kind = kind
        self.pulse = 0.0
    def update(self, dt): self.pulse += dt * 4
    def cell(self): return (self.x, self.y)
    def draw(self, s):
        cx = self.x*CELL + CELL//2 + FIELD_X
        cy = self.y*CELL + CELL//2 + FIELD_Y
        r = int(CELL * 0.42 * (1 + 0.1 * math.sin(self.pulse)))
        if self.kind == "shield":
            col = SHIELD_COL; icon = "S"
        elif self.kind == "slow":
            col = SLOW_COL; icon = "T"
        else:
            col = MAGNET_COL; icon = "M"
        glow = pygame.Surface((r*6, r*6), pygame.SRCALPHA)
        for i in range(5, 0, -1):
            rr = r*3 * i // 5
            a = 15 + i * 12
            pygame.draw.circle(glow, (*col, a), (r*3, r*3), rr)
        s.blit(glow, (cx - r*3, cy - r*3))
        pygame.draw.circle(s, (255,255,255), (cx, cy), r+2)
        pygame.draw.circle(s, col, (cx, cy), r)
        pygame.draw.circle(s, (255,255,255), (cx, cy), r, 2)
        t = font_small.render(icon, True, (255,255,255))
        s.blit(t, (cx - t.get_width()//2, cy - t.get_height()//2))

# ==================== БОСС (обновлён: 4 HP + ускорение) ====================
class Boss:
    def __init__(self, x, y, is_final=False):
        self.x, self.y = x, y
        self.angle = 0.0
        self.vx, self.vy = 0.0, 0.0

        # ⬅️ Теперь ВСЕГДА 4 HP — независимо от is_final
        self.max_hp = 4
        self.hp = self.max_hp

        self.hit_flash = 0.0
        self.is_final = is_final
        self.steal_timer = 0.0
        self.base_steal_cooldown = 4.0 if is_final else 5.0
        self.size = 22 if is_final else 18
        self.change_timer = 0.0

        # ⬅️ Множитель скорости — растёт с каждым попаданием
        self.speed_factor = 1.0

    @property
    def steal_cooldown(self):
        """Кулдаун кражи яблока уменьшается вместе с ускорением."""
        return self.base_steal_cooldown / self.speed_factor

    def take_hit(self):
        """Наносит урон боссу. Возвращает True, если босс побеждён."""
        self.hp -= 1
        self.hit_flash = 0.35
        # ⬅️ +35% к скорости за каждое попадание
        self.speed_factor = 1.0 + (self.max_hp - self.hp) * 0.35
        return self.hp <= 0

    def update(self, dt_ms, dt, snake, food):
        # ⬅️ Вращение ускоряется вместе с speed_factor
        self.angle += dt * 3 * self.speed_factor
        self.hit_flash = max(0.0, self.hit_flash - dt)
        self.steal_timer += dt
        self.change_timer += dt
        tgt_x = food[0]*CELL + CELL//2 + FIELD_X
        tgt_y = food[1]*CELL + CELL//2 + FIELD_Y
        cx = FIELD_X + FIELD_W//2
        cy = FIELD_Y + FIELD_H//2
        # Орбита чуть шире при высокой скорости
        orbit_r = (120 if self.is_final else 90) * (1.0 + (self.speed_factor - 1.0) * 0.5)
        bx = cx + math.cos(self.angle * 0.7) * orbit_r
        by = cy + math.sin(self.angle * 0.7) * orbit_r
        target_x = bx * 0.55 + tgt_x * 0.45
        target_y = by * 0.55 + tgt_y * 0.45
        # ⬅️ Скорость движения умножается на speed_factor
        base_speed = 2.0 * self.speed_factor
        self.vx = (target_x - self.x) * base_speed
        self.vy = (target_y - self.y) * base_speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def try_steal(self, food):
        if self.steal_timer >= self.steal_cooldown:
            self.steal_timer = 0.0
            return True
        return False

    def collides_with_head(self, head_pos):
        dx = self.x - head_pos[0]
        dy = self.y - head_pos[1]
        return (dx*dx + dy*dy) < (self.size + 8) ** 2

    def draw(self, s):
        cx, cy = int(self.x), int(self.y)
        size = self.size
        wing = int(size * 1.1)
        flap = math.sin(self.angle * 8) * 4

        # Тень
        shadow = pygame.Surface((size*4, size*2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0,0,0,80), (0, 0, size*3, size))
        s.blit(shadow, (cx - size*2, cy + size))

        # ⬅️ Красное свечение ярости при высокой скорости
        rage = max(0.0, self.speed_factor - 1.0) / 1.4
        if rage > 0:
            glow = pygame.Surface((size*6, size*6), pygame.SRCALPHA)
            for i in range(4, 0, -1):
                a = int(30 * rage * i / 4)
                pygame.draw.circle(glow, (255, 60, 60, a), (size*3, size*3), size*2*i//4)
            s.blit(glow, (cx - size*3, cy - size*3))

        # Крылья
        wcol = (60, 40, 80) if not self.hit_flash else (255, 200, 200)
        if rage > 0.3:
            wcol = (min(255, wcol[0] + int(100*rage)), wcol[1], wcol[2])
        pygame.draw.polygon(s, wcol, [
            (cx - 3, cy - 4), (cx - wing, cy - 12 + flap),
            (cx - wing + 4, cy + 6), (cx - 3, cy + 4)])
        pygame.draw.polygon(s, wcol, [
            (cx + 3, cy - 4), (cx + wing, cy - 12 - flap),
            (cx + wing - 4, cy + 6), (cx + 3, cy + 4)])

        # Тело — краснеет при ярости
        body_base = (30, 30, 50) if not self.hit_flash else (255, 150, 150)
        if rage > 0:
            body = (min(255, body_base[0] + int(150*rage)),
                    max(0, body_base[1] - int(20*rage)),
                    max(0, body_base[2] - int(20*rage)))
        else:
            body = body_base
        pygame.draw.ellipse(s, body, (cx - size//1.5, cy - size//1.2, size*1.3, size*1.6))
        pygame.draw.circle(s, body, (cx, cy - size//1.5), size//1.4)

        # Глаза — становятся ярко-красными
        eye_col = (255, int(60 - 40*rage), int(60 - 40*rage))
        pygame.draw.circle(s, eye_col, (cx - 3, cy - size//1.5), 2)
        pygame.draw.circle(s, eye_col, (cx + 3, cy - size//1.5), 2)

        # Клюв
        pygame.draw.polygon(s, (240, 160, 30), [
            (cx - 4, cy - size//1.5 + 3),
            (cx + 4, cy - size//1.5 + 3),
            (cx, cy - size//1.5 + 10)])

        # ⬅️ РОМБИКИ HP над головой (всегда 4)
        self._draw_hp_diamonds(s, cx, cy - size - 25)

    def _draw_hp_diamonds(self, s, cx, base_y):
        """Ромбики-индикаторы HP над головой босса."""
        spacing = 20
        total = (self.max_hp - 1) * spacing
        start_x = cx - total // 2
        for i in range(self.max_hp):
            dx = start_x + i * spacing
            dy = base_y
            pulse = 1 + 0.08 * math.sin(self.angle * 5 + i * 0.7)
            r = int(9 * pulse)
            if i < self.hp:
                # Живой ромбик — красный с бликом
                pts = [(dx, dy-r), (dx+r, dy), (dx, dy+r), (dx-r, dy)]
                pygame.draw.polygon(s, BOSS_HP_D, pts)
                pygame.draw.polygon(s, BOSS_HP_COL, pts, 3)
                pygame.draw.polygon(s, (255, 200, 200),
                                    [(dx, dy-r+2), (dx+r-2, dy), (dx, dy+2), (dx-r+2, dy)])
            else:
                # Пустой ромбик — тёмно-серый
                pts = [(dx, dy-r), (dx+r, dy), (dx, dy+r), (dx-r, dy)]
                pygame.draw.polygon(s, BOSS_HP_BG, pts)
                pygame.draw.polygon(s, (30, 20, 20), pts, 2)

# ==================== КНОПКА ====================
class Button:
    def __init__(self, rect, text, font, base=PANEL, border=PANEL_BORDER,
                 enabled=True, text_color=WHITE):
        self.rect = rect
        self.text = text
        self.font = font
        self.base = base
        self.border = border
        self.enabled = enabled
        self.text_color = text_color
        self.hovered = False
    def handle(self, event):
        if not self.enabled: return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    def draw(self, s):
        shadow = self.rect.move(0, 3)
        pygame.draw.rect(s, (0, 0, 0), shadow, border_radius=12)
        if self.enabled:
            fill = self._lighten(self.base) if self.hovered else self.base
            pygame.draw.rect(s, self.border, self.rect, border_radius=12)
            pygame.draw.rect(s, fill, self.rect.inflate(-4, -4), border_radius=10)
            hl = pygame.Rect(self.rect.x + 10, self.rect.y + 6, self.rect.w - 20, 8)
            pygame.draw.rect(s, PANEL_LIGHT, hl, border_radius=4)
            color = self.text_color; outline = self.border
        else:
            pygame.draw.rect(s, (90,90,90), self.rect, border_radius=12)
            pygame.draw.rect(s, (60,60,60), self.rect.inflate(-4,-4), border_radius=10)
            color = (150,150,150); outline = (40,40,40)
        if self.text:
            draw_text_outline(s, self.text, self.font, color, outline,
                              self.rect.center, outline_w=2, center=True)
    @staticmethod
    def _lighten(c, a=40):
        return (min(255, c[0]+a), min(255, c[1]+a), min(255, c[2]+a))

# ==================== ПРЕВЬЮ ЗМЕЙКИ ====================
def draw_snake_preview(surface, skin, cx, cy, total_size=110, segments=5, time_t=0.0):
    seg_size = total_size // segments
    head_r = seg_size // 2 + 2
    for i in range(segments):
        sx = cx - (segments - 1) * seg_size + i * seg_size
        sy = cy
        r = head_r if i == segments - 1 else head_r - 1
        main, light, dark, outline, alpha = get_skin_colors(skin, time_t, i)
        if alpha < 255:
            surf = pygame.Surface((head_r*3, head_r*3), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*outline, alpha), (head_r*3//2, head_r*3//2), r + 1)
            pygame.draw.circle(surf, (*main, alpha), (head_r*3//2, head_r*3//2), r)
            if i < segments - 1:
                pygame.draw.circle(surf, (*light, alpha),
                                   (head_r*3//2 - 2, head_r*3//2 - 3), max(2, r // 3))
            surface.blit(surf, (sx - head_r*3//2, sy - head_r*3//2))
        else:
            pygame.draw.circle(surface, outline, (sx, sy), r + 1)
            pygame.draw.circle(surface, main, (sx, sy), r)
            if i < segments - 1:
                pygame.draw.circle(surface, light, (sx - 2, sy - 3), max(2, r // 3))
    hx = cx + (segments - 1) * seg_size
    hy = cy
    main, light, dark, outline, alpha = get_skin_colors(skin, time_t, segments - 1)
    if alpha < 255:
        surf = pygame.Surface((head_r*3, head_r*3), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*outline, alpha), (head_r*3//2, head_r*3//2), head_r + 2)
        pygame.draw.circle(surf, (*main, alpha), (head_r*3//2, head_r*3//2), head_r + 1)
        pygame.draw.circle(surf, (*light, alpha), (head_r*3//2 - 4, head_r*3//2 - 4), max(3, head_r // 2))
        surface.blit(surf, (hx - head_r*3//2, hy - head_r*3//2))
    else:
        pygame.draw.circle(surface, outline, (hx, hy), head_r + 2)
        pygame.draw.circle(surface, main, (hx, hy), head_r + 1)
        pygame.draw.circle(surface, light, (hx - 4, hy - 4), max(3, head_r // 2))
    eye_r = max(3, head_r // 4)
    pupil_r = max(2, eye_r // 2)
    for dy in (-1, 1):
        ex = hx + 4
        ey = hy + dy * head_r // 2
        pygame.draw.circle(surface, (255, 255, 255), (ex, ey), eye_r)
        pygame.draw.circle(surface, DARK, (ex + 1, ey), pupil_r)

# ==================== ИГРА ====================
class SnakeGame:
    def __init__(self, level_id=1, skin_id="orange", endless=False):
        self.level_id = level_id
        self.level_cfg = LEVELS.get(level_id, LEVELS[1])
        self.skin = SKINS[skin_id]
        self.skin_id = skin_id
        self.endless = endless
        self.best = 0
        self.reset()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.prev_snake = list(self.snake)
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.coins_earned = 0

        self.rocks = []
        self.spikes = []
        self.golden = None
        self.golden_timer = 0.0
        self.apples_eaten = 0

        self.powerup = None
        self.powerup_timer = random.uniform(8, 12)
        self.shield_active = False
        self.slow_timer = 0.0
        self.magnet_timer = 0.0

        self.turns_since_apple = 0
        self.combo_x2 = False

        cfg = self.level_cfg
        if cfg.get("rocks", 0) > 0:
            self._place_rocks(cfg["rocks"])
        if cfg.get("spikes", 0) > 0:
            self._place_spikes(cfg["spikes"])

        self.food = self.spawn_food()

        self.boss = None
        if cfg.get("boss"):
            self.boss = Boss(FIELD_X + FIELD_W//2, FIELD_Y + 80,
                             is_final=cfg.get("final", False))
            play('boss')

        self.alive = True
        self.completed = False
        self.move_timer = 0
        self.time_alive = 0.0
        self.death_timer = 0.0
        self.death_particles = []
        self.trail_particles = []
        self.floating_texts = []
        self.death_flash = 0.0
        self.apple_pulse = 0.0
        self.eat_flash = 0.0
        self.move_speed = cfg.get("move_delay", 180)
        self.anim_t = 0.0

    def _place_rocks(self, count):
        occupied = set(self.snake)
        hx, hy = self.snake[0]
        tries = 0
        while len(self.rocks) < count and tries < 500:
            tries += 1
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) in occupied: continue
            if abs(x - hx) + abs(y - hy) < 5: continue
            self.rocks.append((x, y))
            occupied.add((x, y))

    def _place_spikes(self, count):
        occupied = set(self.snake)
        occupied.update(self.rocks)
        hx, hy = self.snake[0]
        placed = 0
        tries = 0
        while placed < count and tries < 300:
            tries += 1
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x, y = random.randint(0, COLS - 1), 0
                dx, dy = random.choice([-1, 1]), 0
            elif side == 'bottom':
                x, y = random.randint(0, COLS - 1), ROWS - 1
                dx, dy = random.choice([-1, 1]), 0
            elif side == 'left':
                x, y = 0, random.randint(0, ROWS - 1)
                dx, dy = 0, random.choice([-1, 1])
            else:
                x, y = COLS - 1, random.randint(0, ROWS - 1)
                dx, dy = 0, random.choice([-1, 1])
            if (x, y) in occupied: continue
            if abs(x - hx) + abs(y - hy) < 6: continue
            self.spikes.append(MovingSpike(x, y, dx, dy))
            occupied.add((x, y))
            placed += 1

    def spawn_food(self):
        occupied = set(self.snake)
        occupied.update(self.rocks)
        for sp in self.spikes: occupied.add(sp.cell())
        if self.golden: occupied.add(self.golden)
        if self.powerup: occupied.add(self.powerup.cell())
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in occupied]
        return random.choice(free) if free else (0, 0)

    def spawn_powerup(self):
        occupied = set(self.snake)
        occupied.update(self.rocks)
        for sp in self.spikes: occupied.add(sp.cell())
        if self.golden: occupied.add(self.golden)
        occupied.add(self.food)
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in occupied]
        if free:
            x, y = random.choice(free)
            kind = random.choice(PowerUp.KINDS)
            self.powerup = PowerUp(x, y, kind)

    def change_direction(self, d):
        if d[0] == -self.direction[0] and d[1] == -self.direction[1]:
            return
        if d != self.next_direction:
            self.next_direction = d
            self.turns_since_apple += 1
            if self.turns_since_apple > 0:
                self.combo_x2 = False
            play('turn')

    def step(self):
        self.prev_snake = list(self.snake)
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)

        wrapped = False

        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            if not self.shield_active:
                self.die(); return
            else:
                new_head = (new_head[0] % COLS, new_head[1] % ROWS)
                self.shield_active = False
                wrapped = True
                play('shield')
                self.floating_texts.append(FloatingText("ЩИТ!",
                    new_head[0]*CELL + FIELD_X + CELL//2,
                    new_head[1]*CELL + FIELD_Y, SHIELD_COL, 22))

        if new_head in self.snake[:-1]:
            if not self.shield_active:
                self.die(); return
            else:
                self.shield_active = False
                wrapped = True
                play('shield')

        if new_head in self.rocks:
            if not self.shield_active:
                self.die(); return
            else:
                self.shield_active = False
                wrapped = True
                play('shield')

        for sp in self.spikes:
            if sp.cell() == new_head:
                if not self.shield_active:
                    self.die(); return
                else:
                    self.shield_active = False
                    wrapped = True
                    play('shield')

        self.snake.insert(0, new_head)

        if wrapped:
            self.prev_snake = list(self.snake)

        if new_head == self.food:
            apples = 2 if self.combo_x2 else 1
            self.score += apples
            self.coins_earned += apples
            self.apples_eaten += 1
            self.eat_flash = 0.35
            play('eat')
            self.floating_texts.append(FloatingText(f"+{apples}",
                new_head[0]*CELL + FIELD_X + CELL//2,
                new_head[1]*CELL + FIELD_Y, GOLD_LIGHT, 22))
            if self.combo_x2:
                self.floating_texts.append(FloatingText("КОМБО СБРОШЕНО",
                    WIDTH//2, FIELD_Y + 40, GOLD_YELLOW, 20))
            self.turns_since_apple = 0
            self.combo_x2 = False
            self.food = self.spawn_food()
            if self.apples_eaten % 7 == 0:
                self.golden = self.spawn_food()
                self.golden_timer = 5.0
        elif self.golden is not None and new_head == self.golden:
            self.score += 5
            self.coins_earned += 5
            self.eat_flash = 0.5
            play('eat_gold')
            self.golden = None
            self.golden_timer = 0.0
        else:
            self.snake.pop()

        if self.turns_since_apple == 0 and self.apples_eaten > 0 and self.apples_eaten % 3 == 0:
            self.combo_x2 = True
            self.floating_texts.append(FloatingText("КОМБО ×2!",
                WIDTH//2, FIELD_Y + 30, GOLD_YELLOW, 28))
            play('powerup')

        if self.powerup and new_head == self.powerup.cell():
            kind = self.powerup.kind
            if kind == "shield":
                self.shield_active = True
                self.floating_texts.append(FloatingText("ЩИТ!",
                    new_head[0]*CELL + FIELD_X + CELL//2,
                    new_head[1]*CELL + FIELD_Y, SHIELD_COL, 22))
            elif kind == "slow":
                self.slow_timer = 5.0
                self.floating_texts.append(FloatingText("ЗАМЕДЛЕНИЕ",
                    new_head[0]*CELL + FIELD_X + CELL//2,
                    new_head[1]*CELL + FIELD_Y, SLOW_COL, 22))
            elif kind == "magnet":
                self.magnet_timer = 5.0
                self.floating_texts.append(FloatingText("МАГНИТ",
                    new_head[0]*CELL + FIELD_X + CELL//2,
                    new_head[1]*CELL + FIELD_Y, MAGNET_COL, 22))
            play('powerup')
            self.powerup = None

        length_factor = min(1.0, (len(self.snake) - 3) / 40.0)
        base = self.level_cfg.get("move_delay", 180)
        if self.endless:
            base = max(90, 190 - self.score * 2)
        speed = int(base * (1 - 0.30 * length_factor))
        if self.slow_timer > 0:
            speed = int(speed * 1.5)
        self.move_speed = max(60, speed)

    def die(self):
        self.alive = False
        self.death_timer = 0.0
        self.death_flash = 0.6
        play('death')
        for (x, y) in self.snake:
            cx = x * CELL + CELL // 2 + FIELD_X
            cy = y * CELL + CELL // 2 + FIELD_Y
            for _ in range(3):
                col = random.choice([self.skin["main"], self.skin["light"], self.skin["dark"]])
                self.death_particles.append(DeathParticle(cx, cy, col))

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.time_alive += dt
        self.anim_t += dt
        self.apple_pulse += dt * 3.5
        self.eat_flash = max(0.0, self.eat_flash - dt)

        if self.alive:
            self.move_timer += dt_ms
            if self.move_timer >= self.move_speed:
                self.move_timer = 0
                self.step()

            if self.snake:
                hx, hy = self.snake[0]
                px = hx*CELL + CELL//2 + FIELD_X + random.uniform(-4, 4)
                py = hy*CELL + CELL//2 + FIELD_Y + random.uniform(-4, 4)
                main, light, dark, outline, alpha = get_skin_colors(
                    self.skin, self.anim_t, 0)
                self.trail_particles.append(TrailParticle(px, py, light))

            if self.golden is not None:
                self.golden_timer -= dt
                if self.golden_timer <= 0:
                    self.golden = None
                    self.golden_timer = 0.0
            if self.slow_timer > 0:
                self.slow_timer = max(0.0, self.slow_timer - dt)
            if self.magnet_timer > 0:
                self.magnet_timer = max(0.0, self.magnet_timer - dt)

            if self.magnet_timer > 0:
                hx, hy = self.snake[0]
                fx, fy = self.food
                dx = hx - fx
                dy = hy - fy
                if abs(dx) + abs(dy) > 1:
                    if random.random() < 0.15:
                        nx = fx + (1 if dx > 0 else -1 if dx < 0 else 0)
                        ny = fy + (1 if dy > 0 else -1 if dy < 0 else 0)
                        if (nx, ny) not in self.rocks and (nx, ny) not in self.snake:
                            self.food = (nx, ny)

            self.powerup_timer -= dt
            if self.powerup_timer <= 0 and self.powerup is None:
                self.spawn_powerup()
                self.powerup_timer = random.uniform(10, 15)
            if self.powerup:
                self.powerup.update(dt)

            for sp in self.spikes:
                sp.update(dt_ms, dt)
                if sp.cell() == self.snake[0]:
                    if not self.shield_active:
                        self.die()
                        break
                    else:
                        self.shield_active = False
                        play('shield')

            # ⬅️ ОБНОВЛЁННЫЙ БЛОК: урон боссу через take_hit() + ускорение
            if self.boss:
                self.boss.update(dt_ms, dt, self.snake, self.food)
                hx = self.snake[0][0]*CELL + CELL//2 + FIELD_X
                hy = self.snake[0][1]*CELL + CELL//2 + FIELD_Y
                if self.boss.collides_with_head((hx, hy)):
                    killed = self.boss.take_hit()
                    # Отскок змейки
                    self.snake.pop(0)
                    self.snake.insert(0, self.prev_snake[0])
                    if killed:
                        play('complete')
                        self.floating_texts.append(FloatingText("БОСС ПОБЕЖДЁН!",
                            WIDTH//2, HEIGHT//2 - 100, GOLD_YELLOW, 40))
                        self.boss = None
                    else:
                        play('hit_boss')
                        # Всплывающий -1 над головой
                        self.floating_texts.append(FloatingText("-1",
                            hx, hy - 30, (255, 100, 100), 26))
                        # И сообщение БОСС ЗЛЕЕ
                        self.floating_texts.append(FloatingText("БОСС ЗЛЕЕ!",
                            WIDTH//2, FIELD_Y + 70, (255, 80, 80), 24))
                        play('boss')
                if self.boss and self.boss.try_steal(self.food):
                    self.food = self.spawn_food()
        else:
            self.death_timer += dt
            self.death_flash = max(0.0, self.death_flash - dt)

        for p in self.trail_particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.trail_particles.remove(p)

        for p in self.death_particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.death_particles.remove(p)

        for t in self.floating_texts[:]:
            t.update()
            if t.life <= 0:
                self.floating_texts.remove(t)

        if self.alive and not self.endless and not self.completed:
            if self.score >= self.level_cfg["target"]:
                if self.level_cfg.get("boss") and self.boss is not None:
                    pass
                else:
                    self.completed = True

    def get_positions(self):
        t = 0.0
        if self.alive:
            t = min(1.0, self.move_timer / self.move_speed)
        t = smoothstep(t)
        positions = []
        for i, (x, y) in enumerate(self.snake):
            px = x * CELL + CELL // 2 + FIELD_X
            py = y * CELL + CELL // 2 + FIELD_Y
            if self.alive and i < len(self.prev_snake):
                ppx_, ppy_ = self.prev_snake[i]
                ppx = ppx_ * CELL + CELL // 2 + FIELD_X
                ppy = ppy_ * CELL + CELL // 2 + FIELD_Y
                px = ppx + (px - ppx) * t
                py = ppy + (py - ppy) * t
            positions.append((px, py))
        return positions

    def draw(self, surface):
        surface.blit(get_bg(self.level_cfg["biome"]), (0, 0))
        for rx, ry in self.rocks:
            self._draw_rock(surface, rx, ry)
        if self.golden is not None:
            self._draw_apple(surface, *self.golden, golden=True, progress=self.golden_timer/5.0)
        self._draw_apple(surface, *self.food, golden=False)
        if self.powerup:
            self.powerup.draw(surface)

        for p in self.trail_particles:
            p.draw(surface)

        if self.eat_flash > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            a = int(70 * (self.eat_flash / 0.5))
            flash.fill((255, 255, 200, a))
            surface.blit(flash, (0, 0))

        if self.alive:
            self.draw_snake(surface, self.get_positions())

        for sp in self.spikes:
            self._draw_spike(surface, sp)

        if self.boss:
            self.boss.draw(surface)

        for p in self.death_particles:
            p.draw(surface)
        for t in self.floating_texts:
            t.draw(surface)

        if self.magnet_timer > 0:
            hx, hy = self.snake[0]
            px = hx*CELL + CELL//2 + FIELD_X
            py = hy*CELL + CELL//2 + FIELD_Y
            r = 90
            ring = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(ring, (*MAGNET_COL, 60), (r, r), r, 3)
            surface.blit(ring, (px - r, py - r))

        if self.death_flash > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            a = int(150 * (self.death_flash / 0.6))
            flash.fill((255, 30, 40, a))
            surface.blit(flash, (0, 0))

        self.draw_ui(surface)

    def _draw_rock(self, s, rx, ry):
        cx = rx * CELL + CELL // 2 + FIELD_X
        cy = ry * CELL + CELL // 2 + FIELD_Y
        size = CELL * 0.44
        rng = random.Random(rx * 1000 + ry)
        pts = []
        for i in range(8):
            a = i * math.tau / 8
            r = size * (0.75 + rng.random() * 0.35)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        pygame.draw.polygon(s, ROCK_BASE, pts)
        pygame.draw.polygon(s, ROCK_DARK, pts, 2)
        pygame.draw.circle(s, ROCK_LIGHT, (int(cx - size*0.3), int(cy - size*0.3)),
                           max(2, int(size*0.35)))

    def _draw_spike(self, s, sp):
        cx, cy = sp.pixel_center()
        r = CELL * 0.46
        pts = []
        for i in range(16):
            a = sp.angle + i * math.tau / 16
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        pygame.draw.polygon(s, SPIKE_BASE, pts)
        pygame.draw.polygon(s, SPIKE_DARK, pts, 2)
        pygame.draw.circle(s, SPIKE_LIGHT, (int(cx), int(cy)), max(3, int(r*0.45)))

    def _draw_apple(self, s, fx, fy, golden=False, progress=1.0):
        cx = fx * CELL + CELL // 2 + FIELD_X
        cy = fy * CELL + CELL // 2 + FIELD_Y
        pulse = 1 + 0.08 * math.sin(self.apple_pulse * 3 + (1 if golden else 0))
        r = int(CELL * 0.42 * pulse)
        if golden:
            bd, bm, bl = GOLD_DARK, GOLD_YELLOW, GOLD_LIGHT
        else:
            bd, bm, bl = APPLE_DARK, APPLE_RED, APPLE_LIGHT

        shadow = pygame.Surface((r*3, r*3), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 70), (r*3//2, r*3//2+3), r)
        s.blit(shadow, (cx - r*3//2, cy - r*3//2))

        if golden:
            glow = pygame.Surface((r*6, r*6), pygame.SRCALPHA)
            for i in range(6, 0, -1):
                rr = r*3 * i // 6
                a = 10 + i * 10
                pygame.draw.circle(glow, (*GOLD_YELLOW, a), (r*3, r*3), rr)
            s.blit(glow, (cx - r*3, cy - r*3))

        pygame.draw.circle(s, bd, (int(cx), int(cy)), r)
        pygame.draw.circle(s, bm, (int(cx), int(cy) - 1), r - 2)
        pygame.draw.circle(s, bl, (int(cx - r*0.35), int(cy - r*0.4)), max(2, r//4))
        pygame.draw.line(s, STEM, (cx, cy - r + 2), (cx + 2, cy - r - 6), 3)
        leaf_pts = [(cx+1, cy-r-5), (cx+9, cy-r-11), (cx+13, cy-r-3), (cx+5, cy-r+1)]
        pygame.draw.polygon(s, LEAF, leaf_pts)
        pygame.draw.polygon(s, LEAF_DARK, leaf_pts, 1)

        if golden and progress > 0:
            ring_r = r + 7
            visible = int(progress * 24)
            for i in range(visible):
                a = (i / 24) * math.tau - math.pi / 2
                x = cx + math.cos(a) * ring_r
                y = cy + math.sin(a) * ring_r
                pygame.draw.circle(s, GOLD_LIGHT, (int(x), int(y)), 2)

    def draw_snake(self, s, positions):
        n = len(positions)
        if n == 0: return

        MAX_CONNECT_DIST_SQ = (CELL * 2.5) ** 2

        for i in range(n):
            pos = positions[i]
            main, light, dark, outline, alpha = get_skin_colors(
                self.skin, self.anim_t, i)
            r = int(CELL * 0.48)
            if i == 0:
                r = int(CELL * 0.52)
            if alpha < 255:
                surf = pygame.Surface((r*3, r*3), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*outline, alpha), (r*3//2, r*3//2), r + 1)
                pygame.draw.circle(surf, (*main, alpha), (r*3//2, r*3//2), r)
                if i > 0:
                    pygame.draw.circle(surf, (*light, alpha), (r*3//2 - 2, r*3//2 - 3),
                                       max(2, int(CELL*0.13)))
                s.blit(surf, (pos[0] - r*3//2, pos[1] - r*3//2))
            else:
                pygame.draw.circle(s, outline, (int(pos[0]), int(pos[1])), r + 1)
                pygame.draw.circle(s, main, (int(pos[0]), int(pos[1])), r)
                if i > 0:
                    pygame.draw.circle(s, light, (int(pos[0] - 2), int(pos[1] - 3)),
                                       max(2, int(CELL*0.13)))

        for i in range(n - 1):
            p1 = positions[i]
            p2 = positions[i + 1]
            ddx = p1[0] - p2[0]
            ddy = p1[1] - p2[1]
            if ddx*ddx + ddy*ddy > MAX_CONNECT_DIST_SQ:
                continue

            main1, _, _, outline1, a1 = get_skin_colors(self.skin, self.anim_t, i)
            main2, _, _, outline2, a2 = get_skin_colors(self.skin, self.anim_t, i+1)
            mid_out = ((outline1[0]+outline2[0])//2,
                       (outline1[1]+outline2[1])//2,
                       (outline1[2]+outline2[2])//2)
            alpha = min(a1, a2)
            if alpha < 255:
                surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(surf, (*mid_out, alpha),
                                 p1, p2, int(CELL*0.95))
                s.blit(surf, (0, 0))
            else:
                pygame.draw.line(s, mid_out, p1, p2, int(CELL*0.95))

        hx, hy = positions[0]
        head_r = int(CELL * 0.52)
        main, light, dark, outline, alpha = get_skin_colors(self.skin, self.anim_t, 0)
        if alpha >= 255:
            pygame.draw.circle(s, outline, (int(hx), int(hy)), head_r + 1)
            pygame.draw.circle(s, main, (int(hx), int(hy)), head_r)
            pygame.draw.circle(s, light, (int(hx - head_r*0.4), int(hy - head_r*0.4)),
                               max(3, head_r // 3))

        dx, dy = self.direction
        px, py = -dy, dx
        eye_side = head_r * 0.55
        eye_fwd = head_r * 0.35
        e1 = (hx + px*eye_side + dx*eye_fwd, hy + py*eye_side + dy*eye_fwd)
        e2 = (hx - px*eye_side + dx*eye_fwd, hy - py*eye_side + dy*eye_fwd)
        eye_r = max(3, int(head_r * 0.32))
        pupil_r = max(2, int(eye_r * 0.55))
        for ex, ey in (e1, e2):
            pygame.draw.circle(s, DARK, (int(ex), int(ey)), eye_r + 1)
            pygame.draw.circle(s, WHITE, (int(ex), int(ey)), eye_r)
            pygame.draw.circle(s, DARK, (int(ex + dx*2), int(ey + dy*2)), pupil_r)

        mx = hx + dx * head_r * 0.55
        my = hy + dy * head_r * 0.55
        pygame.draw.circle(s, (180, 40, 40), (int(mx + px*3), int(my + py*3)), 2)
        pygame.draw.circle(s, (180, 40, 40), (int(mx - px*3), int(my - py*3)), 2)

        if self.shield_active:
            rr = head_r + 8
            ring = pygame.Surface((rr*2+4, rr*2+4), pygame.SRCALPHA)
            pygame.draw.circle(ring, (*SHIELD_COL, 180), (rr+2, rr+2), rr, 3)
            s.blit(ring, (hx - rr - 2, hy - rr - 2))

    def draw_ui(self, surface):
        score_rect = pygame.Rect(25, 18, 160, 55)
        draw_panel(surface, score_rect)
        if self.endless:
            txt = f"{self.score}"
        else:
            txt = f"{self.score}/{self.level_cfg['target']}"
        draw_text_outline(surface, txt, font_big, WHITE, PANEL_BORDER,
                          score_rect.center, outline_w=2, center=True)

        lvl_rect = pygame.Rect(200, 18, 220, 55)
        draw_panel(surface, lvl_rect)
        if self.endless:
            nm = "БЕСКОНЕЧНЫЙ"
        else:
            nm = f"Ур.{self.level_id} · {self.level_cfg['name']}"
        draw_text_outline(surface, nm, font_small, WHITE, PANEL_BORDER,
                          lvl_rect.center, outline_w=2, center=True)

        coins_rect = pygame.Rect(WIDTH - 25 - 175, 18, 130, 55)
        draw_panel(surface, coins_rect)
        cx = coins_rect.x + 28; cy = coins_rect.centery
        draw_coin_icon(surface, cx, cy, 15)
        t = font_mid.render(f"+{self.coins_earned}", True, WHITE)
        surface.blit(t, (cx + 22, cy - t.get_height()//2))

        if self.combo_x2:
            combo_t = font_mid.render("×2 КОМБО", True, GOLD_YELLOW)
            cr = combo_t.get_rect(center=(WIDTH // 2, 45))
            bg = cr.inflate(20, 8)
            sv = pygame.Surface((bg.w, bg.h), pygame.SRCALPHA)
            sv.fill((0, 0, 0, 150))
            surface.blit(sv, bg.topleft)
            pygame.draw.rect(surface, GOLD_YELLOW, bg, 2, border_radius=6)
            surface.blit(combo_t, cr)

        bonus_x = WIDTH // 2 + 220
        if self.shield_active:
            pygame.draw.circle(surface, SHIELD_COL, (bonus_x, 45), 14)
            t = font_tiny.render("ЩИТ", True, WHITE)
            surface.blit(t, (bonus_x - t.get_width()//2, 45 - t.get_height()//2))
        if self.slow_timer > 0:
            pygame.draw.circle(surface, SLOW_COL, (bonus_x + 32, 45), 14)
            t = font_tiny.render("ЗАМ", True, WHITE)
            surface.blit(t, (bonus_x + 32 - t.get_width()//2, 45 - t.get_height()//2))
        if self.magnet_timer > 0:
            pygame.draw.circle(surface, MAGNET_COL, (bonus_x + 64, 45), 14)
            t = font_tiny.render("МАГ", True, WHITE)
            surface.blit(t, (bonus_x + 64 - t.get_width()//2, 45 - t.get_height()//2))

        hint = font_tiny.render(
            "Стрелки / WASD — движение    P — пауза    ESC — меню    F11 — полный экран",
            True, WHITE)
        h = hint.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        bg_rect = h.inflate(20, 8)
        sv = pygame.Surface((bg_rect.w, bg_rect.h), pygame.SRCALPHA)
        sv.fill((0, 0, 0, 110))
        surface.blit(sv, bg_rect.topleft)
        surface.blit(hint, h)

# ==================== МЕНЮ ====================
def draw_menu_background(surface):
    surface.fill((24, 28, 48))
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(24*(1-t) + 10*t); g = int(28*(1-t) + 12*t); b = int(48*(1-t) + 26*t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
    rng = random.Random(7)
    for _ in range(120):
        x = rng.randint(0, WIDTH); y = rng.randint(0, HEIGHT)
        r = rng.choice([1, 1, 2])
        a = rng.randint(60, 200)
        s = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, a), (r+1, r+1), r)
        surface.blit(s, (x-r-1, y-r-1))

def draw_title(surface, text="ЗМЕЙКА DELUXE"):
    title = font_huge.render(text, True, WHITE)
    outline = font_huge.render(text, True, PANEL_BORDER)
    rect = title.get_rect(center=(WIDTH // 2, 60))
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx == 0 and dy == 0: continue
            surface.blit(outline, (rect.x + dx, rect.y + dy))
    surface.blit(title, rect)

def main_menu(save):
    bw, bh = 320, 62
    bx = WIDTH // 2 - bw // 2
    btns = {
        "play":     Button(pygame.Rect(bx, 140, bw, bh), "ИГРАТЬ",
                           font_big, base=(90,190,110), border=(30,100,50)),
        "endless":  Button(pygame.Rect(bx, 208, bw, bh), "БЕСКОНЕЧНЫЙ",
                           font_big, base=(100,150,220), border=(40,70,140)),
        "shop":     Button(pygame.Rect(bx, 276, bw, bh), "МАГАЗИН",
                           font_big, base=(200,120,200), border=(100,40,110)),
        "stats":    Button(pygame.Rect(bx, 344, bw, bh), "СТАТИСТИКА",
                           font_big, base=(180,180,90), border=(90,90,30)),
        "settings": Button(pygame.Rect(bx, 412, bw, bh), "НАСТРОЙКИ",
                           font_big, base=(120,200,200), border=(40,110,110)),
        "quit":     Button(pygame.Rect(bx, 480, bw, bh), "ВЫХОД",
                           font_big, base=(220,80,90), border=(120,30,40)),
    }
    t = 0.0
    daily_msg = "ЕЖЕДНЕВНЫЙ БОНУС +10!"
    daily_shown = False
    daily_timer = 0.0
    if try_daily_bonus(save):
        daily_shown = True
        daily_timer = 3.0
        play('achievement')

    while True:
        dt_ms = clock.tick(FPS)
        t += dt_ms / 1000.0
        if daily_timer > 0:
            daily_timer = max(0.0, daily_timer - dt_ms / 1000.0)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save)
                continue
            for k, b in btns.items():
                if b.handle(e):
                    play('click')
                    return k

        draw_menu_background(screen)
        draw_title(screen)
        draw_coins_display(screen, save["coins"])

        skin = SKINS[save["current_skin"]]
        seg_count = 10
        for i in range(seg_count):
            x = WIDTH // 2 - seg_count * 32 // 2 + i * 32
            y = 640 + math.sin(t * 3 + i * 0.5) * 12
            r = 13 - i // 2
            main, light, dark, outline, alpha = get_skin_colors(skin, t, seg_count - 1 - i)
            pygame.draw.circle(screen, outline, (x, y), r + 2)
            pygame.draw.circle(screen, main, (x, y), r)
        hx = WIDTH // 2 - seg_count * 32 // 2 + (seg_count - 1) * 32
        hy = 640 + math.sin(t * 3 + (seg_count - 1) * 0.5) * 12
        pygame.draw.circle(screen, WHITE, (hx + 5, hy - 4), 4)
        pygame.draw.circle(screen, WHITE, (hx + 5, hy + 4), 4)
        pygame.draw.circle(screen, DARK, (hx + 6, hy - 4), 2)
        pygame.draw.circle(screen, DARK, (hx + 6, hy + 4), 2)

        unlocked = len(save["unlocked_levels"])
        total_best = max([int(v) for v in save["best_scores"].values()], default=0)
        draw_text_outline(screen, f"Уровни: {unlocked}/{len(LEVELS)}    Рекорд: {total_best}    Достижений: {len(save['achievements'])}/{len(ACHIEVEMENTS)}    F11 — полный экран",
                          font_tiny, GOLD_LIGHT, PANEL_BORDER,
                          (WIDTH // 2, HEIGHT - 25), outline_w=2, center=True)

        for b in btns.values():
            b.draw(screen)

        if daily_shown and daily_timer > 0:
            a = int(255 * min(1.0, daily_timer))
            msg = font_big.render(daily_msg, True, GOLD_YELLOW)
            msg.set_alpha(a)
            mr = msg.get_rect(center=(WIDTH // 2, 110))
            screen.blit(msg, mr)

        pygame.display.flip()

def level_select(save):
    cards = []
    ids = sorted(LEVELS.keys())
    cols = 6
    cw, ch = 130, 200
    gap_x, gap_y = 15, 20
    for i, lid in enumerate(ids):
        row = i // cols
        col = i % cols
        row_items = ids[row*cols : (row+1)*cols]
        row_total = len(row_items) * cw + (len(row_items) - 1) * gap_x
        rx = (WIDTH - row_total) // 2
        r = pygame.Rect(rx + col * (cw + gap_x),
                        130 + row * (ch + gap_y),
                        cw, ch)
        cards.append((lid, r))

    back = Button(pygame.Rect(WIDTH//2 - 130, HEIGHT - 60, 260, 50),
                  "НАЗАД", font_mid, base=(200,200,220), border=(80,80,120))

    previews = {}
    for lid in LEVELS.keys():
        previews[lid] = get_preview(LEVELS[lid]["biome"], (110, 70))

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return None
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save)
                continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: return None
            if back.handle(e): play('click'); return None
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for lid, r in cards:
                    if r.collidepoint(e.pos) and lid in save["unlocked_levels"]:
                        play('click'); return lid

        draw_menu_background(screen)
        draw_coins_display(screen, save["coins"])
        draw_text_outline(screen, "ВЫБОР УРОВНЯ", font_mid,
                          WHITE, PANEL_BORDER, (WIDTH//2, 60),
                          outline_w=2, center=True)
        draw_text_outline(screen, "F11 — полный экран",
                          font_tiny, GOLD_LIGHT, PANEL_BORDER,
                          (WIDTH//2, HEIGHT - 25),
                          outline_w=1, center=True)

        mp = pygame.mouse.get_pos()
        for lid, r in cards:
            cfg = LEVELS[lid]
            unlocked = lid in save["unlocked_levels"]
            hovered = r.collidepoint(mp) and unlocked

            base_col = (60,70,110) if unlocked else (50,50,60)
            if hovered: base_col = (85,100,150)
            shadow = r.move(0, 4)
            pygame.draw.rect(screen, (0,0,0), shadow, border_radius=12)
            pygame.draw.rect(screen, base_col, r, border_radius=12)
            pygame.draw.rect(screen, (30,30,50), r, 3, border_radius=12)

            prev = previews[lid]
            screen.blit(prev, (r.x + 10, r.y + 10))
            pygame.draw.rect(screen, (30,30,50),
                             (r.x + 10, r.y + 10, 110, 70), 2, border_radius=4)

            num = font_big.render(str(lid), True, WHITE)
            nr = num.get_rect(center=(r.centerx, r.y + 105))
            pygame.draw.circle(screen, PANEL_DARK, (r.centerx, r.y + 105), 22)
            pygame.draw.circle(screen, PANEL, (r.centerx, r.y + 105), 18)
            screen.blit(num, nr)

            name = font_tiny.render(cfg["name"][:14], True, WHITE)
            nrect = name.get_rect(center=(r.centerx, r.y + 140))
            screen.blit(name, nrect)

            if cfg.get("boss"):
                bs = font_tiny.render("БОСС ×4", True, APPLE_LIGHT)
                br = bs.get_rect(center=(r.centerx, r.y + 158))
                screen.blit(bs, br)

            best = save["best_scores"].get(str(lid), 0)
            best_s = font_tiny.render(f"Рекорд {best}", True, (200,220,255))
            br = best_s.get_rect(center=(r.centerx, r.y + 175))
            screen.blit(best_s, br)

            tgt = font_tiny.render(f"Цель {cfg['target']}", True, GOLD_LIGHT)
            tr_ = tgt.get_rect(center=(r.centerx, r.y + 192))
            screen.blit(tgt, tr_)

            if not unlocked:
                ov = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                ov.fill((0,0,0,140))
                screen.blit(ov, r.topleft)
                lx, ly = r.centerx, r.centery
                pygame.draw.rect(screen, (220,200,80),
                                 (lx-14, ly-6, 28, 22), border_radius=4)
                pygame.draw.arc(screen, (220,200,80),
                                (lx-10, ly-22, 20, 20), 0, math.pi, 4)

        back.draw(screen)
        pygame.display.flip()

def shop_menu(save):
    skin_ids = list(SKINS.keys())
    cols = 4
    cw, ch = 190, 180
    gap_x, gap_y = 20, 20
    start_y = 200
    cards = []
    for i, sid in enumerate(skin_ids):
        row = i // cols; col = i % cols
        row_items = skin_ids[row*cols : (row+1)*cols]
        row_total = len(row_items) * cw + (len(row_items) - 1) * gap_x
        rx = (WIDTH - row_total) // 2
        r = pygame.Rect(rx + col * (cw + gap_x), start_y + row * (ch + gap_y), cw, ch)
        cards.append((sid, r))
    back = Button(pygame.Rect(WIDTH//2 - 130, HEIGHT - 80, 260, 55),
                  "НАЗАД", font_mid, base=(200,200,220), border=(80,80,120))
    t = 0.0; message = ""; message_timer = 0.0
    while True:
        dt_ms = clock.tick(FPS); t += dt_ms / 1000.0
        if message_timer > 0: message_timer = max(0.0, message_timer - dt_ms/1000.0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save); continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: return
            if back.handle(e): play('click'); return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for sid, r in cards:
                    if r.collidepoint(e.pos):
                        if sid in save["unlocked_skins"]:
                            save["current_skin"] = sid
                            save_data(save); play('click')
                            message = f"Выбрана: {SKINS[sid]['name']}"
                            message_timer = 1.5
                        else:
                            price = SKINS[sid]["price"]
                            if save["coins"] >= price:
                                save["coins"] -= price
                                save["unlocked_skins"].append(sid)
                                save["current_skin"] = sid
                                save_data(save); play('buy')
                                message = f"Куплено: {SKINS[sid]['name']}!"
                                message_timer = 1.5
                                check_achievements(save)
                            else:
                                need = price - save["coins"]
                                message = f"Не хватает {need} монет"
                                message_timer = 1.5
        draw_menu_background(screen)
        draw_coins_display(screen, save["coins"])
        draw_text_outline(screen, "МАГАЗИН СКИНОВ", font_big,
                          WHITE, PANEL_BORDER, (WIDTH//2, 80), outline_w=3, center=True)
        mp = pygame.mouse.get_pos()
        for sid, r in cards:
            skin = SKINS[sid]
            owned = sid in save["unlocked_skins"]
            active = sid == save["current_skin"]
            hovered = r.collidepoint(mp)
            if active: base_col = (100,200,130); border_col = (40,130,70)
            elif owned: base_col = (80,90,130) if not hovered else (105,120,165); border_col = (40,50,90)
            else: base_col = (60,60,80) if not hovered else (85,85,110); border_col = (30,30,45)
            shadow = r.move(0, 4)
            pygame.draw.rect(screen, (0,0,0), shadow, border_radius=14)
            pygame.draw.rect(screen, base_col, r, border_radius=14)
            pygame.draw.rect(screen, border_col, r, 3, border_radius=14)
            draw_snake_preview(screen, skin, r.centerx, r.y + 55, total_size=95, time_t=t)
            name = font_small.render(skin["name"], True, WHITE)
            nr = name.get_rect(center=(r.centerx, r.y + 120))
            screen.blit(name, nr)
            if active:
                st = font_tiny.render("ВЫБРАНО", True, (240,255,200))
                sr = st.get_rect(center=(r.centerx, r.y + 150))
                screen.blit(st, sr)
            elif owned:
                st = font_tiny.render("КУПЛЕНО", True, (200,220,255))
                sr = st.get_rect(center=(r.centerx, r.y + 150))
                screen.blit(st, sr)
            else:
                price = skin["price"]
                can = save["coins"] >= price
                coin_x = r.centerx - 25; coin_y = r.y + 150
                draw_coin_icon(screen, coin_x, coin_y, 10)
                col = GOLD_LIGHT if can else (200, 120, 120)
                price_t = font_small.render(str(price), True, col)
                screen.blit(price_t, (coin_x + 16, coin_y - price_t.get_height()//2))
                if not can:
                    ov = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                    ov.fill((0,0,0,80))
                    screen.blit(ov, r.topleft)
        if message_timer > 0:
            mt = font_mid.render(message, True, GOLD_LIGHT)
            mr = mt.get_rect(center=(WIDTH // 2, HEIGHT - 130))
            bg_r = mr.inflate(30, 16)
            sv = pygame.Surface((bg_r.w, bg_r.h), pygame.SRCALPHA)
            sv.fill((0,0,0,180))
            screen.blit(sv, bg_r.topleft)
            pygame.draw.rect(screen, PANEL_BORDER, bg_r, 2, border_radius=8)
            screen.blit(mt, mr)
        back.draw(screen)
        pygame.display.flip()

def stats_screen(save):
    back = Button(pygame.Rect(WIDTH//2 - 130, HEIGHT - 80, 260, 55),
                  "НАЗАД", font_mid, base=(200,200,220), border=(80,80,120))
    export_b = Button(pygame.Rect(WIDTH//2 - 320, HEIGHT - 80, 160, 55),
                      "ЭКСПОРТ", font_small, base=(120,180,240), border=(40,80,140))
    import_b = Button(pygame.Rect(WIDTH//2 + 160, HEIGHT - 80, 160, 55),
                      "ИМПОРТ", font_small, base=(240,180,120), border=(140,80,40))
    msg = ""; msg_timer = 0.0
    while True:
        dt_ms = clock.tick(FPS)
        if msg_timer > 0: msg_timer = max(0.0, msg_timer - dt_ms/1000.0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save); continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: return
            if back.handle(e): play('click'); return
            if export_b.handle(e):
                try:
                    shutil.copy(SAVE_FILE, BACKUP_FILE)
                    msg = "Сохранено в save_backup.json"
                except Exception as ex:
                    msg = f"Ошибка: {ex}"
                msg_timer = 2.5
            if import_b.handle(e):
                try:
                    if os.path.exists(BACKUP_FILE):
                        shutil.copy(BACKUP_FILE, SAVE_FILE)
                        msg = "Импортировано! Перезапусти игру"
                    else:
                        msg = "Файл бэкапа не найден"
                except Exception as ex:
                    msg = f"Ошибка: {ex}"
                msg_timer = 2.5
        draw_menu_background(screen)
        draw_coins_display(screen, save["coins"])
        draw_text_outline(screen, "СТАТИСТИКА И ДОСТИЖЕНИЯ", font_big,
                          WHITE, PANEL_BORDER, (WIDTH//2, 60), outline_w=3, center=True)
        st = save["stats"]
        lines = [
            f"Всего съедено яблок: {st['total_apples']}",
            f"Время в игре: {int(st['play_time'] // 60)} мин {int(st['play_time'] % 60)} сек",
            f"Монет: {save['coins']}",
            f"Открыто уровней: {len(save['unlocked_levels'])}/{len(LEVELS)}",
            f"Куплено скинов: {len(save['unlocked_skins'])}/{len(SKINS)}",
            f"Рекорд (бесконечный): {save.get('endless_best', 0)}",
        ]
        for i, line in enumerate(lines):
            draw_text_outline(screen, line, font_small, WHITE, PANEL_BORDER,
                              (WIDTH//2, 115 + i*24), outline_w=2, center=True)

        draw_text_outline(screen, "Достижения:", font_mid, GOLD_LIGHT, PANEL_BORDER,
                          (WIDTH//2, 265), outline_w=2, center=True)
        ach_list = list(ACHIEVEMENTS.keys())
        cols = 2
        cw = 400
        for i, key in enumerate(ach_list):
            row = i // cols; col = i % cols
            cx = WIDTH//2 - cw + col * cw + 20
            cy = 300 + row * 26
            have = key in save["achievements"]
            txt = f"{'✓' if have else '✗'}  {ACHIEVEMENTS[key]['name']}"
            col_ = (140, 240, 140) if have else (150, 150, 150)
            draw_text_outline(screen, txt, font_small, col_, PANEL_BORDER,
                              (cx, cy), outline_w=1)
            desc = ACHIEVEMENTS[key]['desc']
            draw_text_outline(screen, desc, font_tiny, (180, 180, 200), PANEL_BORDER,
                              (cx + 190, cy + 3), outline_w=1)

        draw_text_outline(screen, "Топ-5 рекордов:", font_mid, GOLD_LIGHT, PANEL_BORDER,
                          (WIDTH//2, 445), outline_w=2, center=True)
        for i, entry in enumerate(save["leaderboard"][:5]):
            line = f"{i+1}. {entry['score']} — {entry['level']} ({entry['date']})"
            draw_text_outline(screen, line, font_tiny, WHITE, PANEL_BORDER,
                              (WIDTH//2, 478 + i*22), outline_w=1, center=True)

        back.draw(screen)
        export_b.draw(screen)
        import_b.draw(screen)
        if msg_timer > 0:
            mt = font_mid.render(msg, True, GOLD_LIGHT)
            mr = mt.get_rect(center=(WIDTH // 2, HEIGHT - 130))
            bg = mr.inflate(30, 16)
            sv = pygame.Surface((bg.w, bg.h), pygame.SRCALPHA)
            sv.fill((0, 0, 0, 180))
            screen.blit(sv, bg.topleft)
            screen.blit(mt, mr)
        pygame.display.flip()

# ==================== НАСТРОЙКИ ====================
def settings_screen(save):
    sound_b = Button(pygame.Rect(WIDTH//2 - 200, 230, 400, 80),
                     "", font_big, base=(120, 220, 140), border=(40, 130, 70))
    music_b = Button(pygame.Rect(WIDTH//2 - 200, 360, 400, 80),
                     "", font_big, base=(120, 220, 140), border=(40, 130, 70))
    full_b = Button(pygame.Rect(WIDTH//2 - 200, 490, 400, 80),
                    "", font_big, base=(120, 220, 140), border=(40, 130, 70))
    back = Button(pygame.Rect(WIDTH//2 - 130, HEIGHT - 70, 260, 50),
                  "НАЗАД", font_mid, base=(200, 200, 220), border=(80, 80, 120))

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save); continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                save_data(save); return
            if back.handle(e):
                save_data(save); play('click'); return
            if sound_b.handle(e):
                save["sound_on"] = not save.get("sound_on", True)
                save_data(save)
                if save["sound_on"]:
                    play('click')
            if music_b.handle(e):
                save["music_on"] = not save.get("music_on", True)
                save_data(save)
                if save["music_on"]:
                    start_music()
                else:
                    stop_music()
                play('click')
            if full_b.handle(e):
                toggle_fullscreen(save)

        draw_menu_background(screen)
        draw_coins_display(screen, save["coins"])
        draw_text_outline(screen, "НАСТРОЙКИ", font_big, WHITE, PANEL_BORDER,
                          (WIDTH//2, 60), outline_w=3, center=True)

        sound_on = save.get("sound_on", True)
        sound_b.base = (120, 220, 140) if sound_on else (200, 100, 100)
        sound_b.border = (40, 130, 70) if sound_on else (120, 30, 30)
        sound_b.draw(screen)
        draw_text_outline(screen, "Звуковые эффекты", font_mid, WHITE, PANEL_BORDER,
                          (WIDTH//2, 270), outline_w=2, center=True)
        status = "ВКЛ" if sound_on else "ВЫКЛ"
        stat_col = (140, 255, 170) if sound_on else (255, 130, 130)
        draw_text_outline(screen, status, font_mid, stat_col, PANEL_BORDER,
                          (WIDTH//2 + 130, 270), outline_w=2, center=True)

        music_on = save.get("music_on", True)
        music_b.base = (120, 220, 140) if music_on else (200, 100, 100)
        music_b.border = (40, 130, 70) if music_on else (120, 30, 30)
        music_b.draw(screen)
        draw_text_outline(screen, "Фоновая музыка", font_mid, WHITE, PANEL_BORDER,
                          (WIDTH//2, 400), outline_w=2, center=True)
        status = "ВКЛ" if music_on else "ВЫКЛ"
        stat_col = (140, 255, 170) if music_on else (255, 130, 130)
        draw_text_outline(screen, status, font_mid, stat_col, PANEL_BORDER,
                          (WIDTH//2 + 130, 400), outline_w=2, center=True)

        fs_on = IS_FULLSCREEN[0]
        full_b.base = (120, 220, 140) if fs_on else (200, 100, 100)
        full_b.border = (40, 130, 70) if fs_on else (120, 30, 30)
        full_b.draw(screen)
        draw_text_outline(screen, "Полный экран (F11)", font_mid, WHITE, PANEL_BORDER,
                          (WIDTH//2, 530), outline_w=2, center=True)
        status = "ВКЛ" if fs_on else "ВЫКЛ"
        stat_col = (140, 255, 170) if fs_on else (255, 130, 130)
        draw_text_outline(screen, status, font_mid, stat_col, PANEL_BORDER,
                          (WIDTH//2 + 130, 530), outline_w=2, center=True)

        draw_text_outline(screen, "Кликни на панель, чтобы переключить",
                          font_tiny, GOLD_LIGHT, PANEL_BORDER,
                          (WIDTH//2, 600), outline_w=1, center=True)

        back.draw(screen)
        pygame.display.flip()

# ==================== ОВЕРЛЕИ ====================
def _draw_overlay_backdrop(screen):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        t = y / HEIGHT
        a = int(150 + 70 * t)
        pygame.draw.line(ov, (0, 0, 0, a), (0, y), (WIDTH, y))
    screen.blit(ov, (0, 0))

def _draw_center_panel(screen, pw, ph):
    px = (WIDTH - pw) // 2
    py = (HEIGHT - ph) // 2
    panel = pygame.Rect(px, py, pw, ph)

    panel_surf = pygame.Surface((pw, ph), pygame.SRCALPHA)
    for y in range(ph):
        t = y / ph
        r = int(45 * (1 - t) + 20 * t)
        g = int(35 * (1 - t) + 15 * t)
        b = int(80 * (1 - t) + 45 * t)
        pygame.draw.line(panel_surf, (r, g, b, 245), (0, y), (pw, y))
    screen.blit(panel_surf, (px, py))

    pygame.draw.rect(screen, (140, 65, 10), panel, 5, border_radius=20)
    pygame.draw.rect(screen, (245, 160, 55), panel.inflate(-10, -10), 2,
                     border_radius=15)
    return px, py, panel

def draw_game_over_panel(screen, score, coins,
                         title_text="ИГРА ОКОНЧЕНА",
                         hint_text="ПРОБЕЛ — заново    ESC — меню"):
    _draw_overlay_backdrop(screen)
    px, py, panel = _draw_center_panel(screen, 560, 360)

    draw_text_outline(screen, title_text, font_huge, APPLE_RED, PANEL_BORDER,
                      (WIDTH // 2, py + 70), outline_w=3, center=True)
    draw_text_outline(screen, f"Счёт: {score}", font_big, WHITE, PANEL_BORDER,
                      (WIDTH // 2, py + 155), outline_w=2, center=True)

    coin_x = WIDTH // 2 - 70
    coin_y = py + 225
    draw_coin_icon(screen, coin_x, coin_y, 18)
    coin_text = font_mid.render(f"+{coins}", True, GOLD_LIGHT)
    screen.blit(coin_text, (coin_x + 28, coin_y - coin_text.get_height() // 2))
    lbl = font_tiny.render("монет собрано", True, (200, 210, 240))
    screen.blit(lbl, (WIDTH // 2 + 40, coin_y - 8))

    draw_text_outline(screen, hint_text, font_small, WHITE, PANEL_BORDER,
                      (WIDTH // 2, py + 360 - 40), outline_w=2, center=True)

# ==================== ИГРОВОЙ ЭКРАН ====================
def play_level(save, level_id, endless=False):
    skin_id = save["current_skin"]
    best = save["best_scores"].get(str(level_id), 0)
    game = SnakeGame(level_id, skin_id, endless=endless)
    game.best = best
    paused = False
    saved = False

    session_start = time.time()

    while True:
        dt_ms = clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                _flush_stats(save, game, session_start)
                return ("quit",)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                toggle_fullscreen(save)
                continue
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if not saved:
                        _save_progress(save, game, level_id, best)
                        saved = True
                    _flush_stats(save, game, session_start)
                    return ("menu",)
                if e.key == pygame.K_p and game.alive:
                    paused = not paused
                if not paused and game.alive:
                    if e.key in (pygame.K_UP, pygame.K_w):
                        game.change_direction((0, -1))
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        game.change_direction((0, 1))
                    elif e.key in (pygame.K_LEFT, pygame.K_a):
                        game.change_direction((-1, 0))
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        game.change_direction((1, 0))

        if not paused:
            game.update(dt_ms)

        game.draw(screen)

        if paused:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 150))
            screen.blit(ov, (0, 0))
            draw_text_outline(screen, "ПАУЗА", font_huge, WHITE, PANEL_BORDER,
                              (WIDTH//2, HEIGHT//2), outline_w=3, center=True)
            draw_text_outline(screen, "P — продолжить,  ESC — меню",
                              font_small, WHITE, PANEL_BORDER,
                              (WIDTH//2, HEIGHT//2 + 60), outline_w=2, center=True)

        if game.completed and not saved:
            _save_progress(save, game, level_id, best)
            _flush_stats(save, game, session_start)
            saved = True
            next_id = level_id + 1 if level_id + 1 in LEVELS else None
            if next_id and next_id not in save["unlocked_levels"]:
                save["unlocked_levels"].append(next_id)
            save_data(save)
            play('complete')
            pygame.display.flip()
            waiting = True
            while waiting:
                clock.tick(FPS)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: return ("quit",)
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                        toggle_fullscreen(save); continue
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            waiting = False
                        if e.key == pygame.K_ESCAPE:
                            check_achievements(save)
                            return ("menu",)

                game.draw(screen)
                _draw_overlay_backdrop(screen)
                px, py, panel = _draw_center_panel(screen, 560, 380)

                draw_text_outline(screen, "УРОВЕНЬ ПРОЙДЕН!", font_big,
                                  GOLD_LIGHT, PANEL_BORDER,
                                  (WIDTH // 2, py + 70), outline_w=3, center=True)

                coin_x = WIDTH // 2 - 70
                coin_y = py + 145
                draw_coin_icon(screen, coin_x, coin_y, 18)
                coin_text = font_mid.render(f"+{game.coins_earned}", True, GOLD_LIGHT)
                screen.blit(coin_text,
                            (coin_x + 28, coin_y - coin_text.get_height() // 2))
                lbl = font_tiny.render("монет собрано", True, (200, 210, 240))
                screen.blit(lbl, (WIDTH // 2 + 40, coin_y - 8))

                if next_id:
                    msg = f"Открыт уровень {next_id}!"
                else:
                    msg = "Все 12 уровней пройдены! Ты — легенда!"
                draw_text_outline(screen, msg, font_mid, GOLD_YELLOW, PANEL_BORDER,
                                  (WIDTH // 2, py + 220), outline_w=2, center=True)

                draw_text_outline(screen, "ПРОБЕЛ — продолжить    ESC — меню",
                                  font_small, WHITE, PANEL_BORDER,
                                  (WIDTH // 2, py + 380 - 40), outline_w=2, center=True)
                pygame.display.flip()
            check_achievements(save)
            return ("level_select",)

        if game.alive and not game.endless and game.level_cfg.get("boss"):
            if game.score >= game.level_cfg["target"] and game.boss is None:
                game.completed = True

        if not game.alive and game.death_timer > 1.6 and not saved:
            _save_progress(save, game, level_id, best)
            _flush_stats(save, game, session_start)
            saved = True
            if game.endless:
                if game.score > save.get("endless_best", 0):
                    save["endless_best"] = game.score
            add_leaderboard(save, game.score,
                            "Бесконечный" if endless else LEVELS[level_id]["name"])
            save_data(save)
            check_achievements(save)
            pygame.display.flip()
            waiting = True
            result = None
            while waiting:
                clock.tick(FPS)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: return ("quit",)
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                        toggle_fullscreen(save); continue
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            waiting = False; result = "retry"
                        if e.key == pygame.K_ESCAPE:
                            waiting = False; result = "menu"
                game.draw(screen)
                draw_game_over_panel(screen, game.score, game.coins_earned)
                pygame.display.flip()
            if result == "retry":
                return ("retry", level_id)
            else:
                return ("menu",)

        pygame.display.flip()

def _save_progress(save, game, level_id, best):
    save["coins"] += game.coins_earned
    if not game.endless:
        if game.score > best:
            save["best_scores"][str(level_id)] = game.score
    save_data(save)

def _flush_stats(save, game, session_start):
    elapsed = time.time() - session_start
    st = save.setdefault("stats", {"total_apples": 0, "play_time": 0, "skin_uses": {}})
    st["play_time"] = st.get("play_time", 0) + elapsed
    st["total_apples"] = st.get("total_apples", 0) + game.apples_eaten
    sid = save["current_skin"]
    uses = st.setdefault("skin_uses", {})
    uses[sid] = uses.get(sid, 0) + 1
    save_data(save)
    check_achievements(save)

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
def main():
    global GLOBAL_SAVE, screen
    save = load_save()
    GLOBAL_SAVE = save
    state = "menu"
    current_level = 1
    endless_mode = False
    start_music()

    if save.get("fullscreen", False):
        IS_FULLSCREEN[0] = True
        pygame.display.quit()
        pygame.display.init()
        screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption("Змейка Deluxe 🐍")

    while True:
        if state == "menu":
            result = main_menu(save)
            if result == "play":
                state = "level_select"
            elif result == "endless":
                endless_mode = True
                current_level = 1
                state = "play"
            elif result == "shop":
                shop_menu(save)
                state = "menu"
            elif result == "stats":
                stats_screen(save)
                state = "menu"
            elif result == "settings":
                settings_screen(save)
                state = "menu"
            else:
                pygame.quit()
                sys.exit()

        elif state == "level_select":
            lid = level_select(save)
            if lid is None:
                state = "menu"
            else:
                current_level = lid
                endless_mode = False
                state = "play"

        elif state == "play":
            result = play_level(save, current_level, endless=endless_mode)
            if result[0] == "quit":
                pygame.quit()
                sys.exit()
            elif result[0] == "level_select":
                state = "level_select"
            elif result[0] == "menu":
                state = "menu"
            elif result[0] == "retry":
                current_level = result[1]
                state = "play"


if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        print("\n❌ Произошла ошибка! Подробности:")
        traceback.print_exc()
        input("\nНажми Enter, чтобы закрыть окно...")