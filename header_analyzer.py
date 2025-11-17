import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import time

import requests

pygame.mixer.music.load("song.ogg") #Eric Matyas
pygame.mixer.music.play(-1)

level=-2
message=""
target="https://127.0.0.1"
count=0

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

def draw():
    global level, target,message,count
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
        count=0
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Page-Header to analyze (e.g. https://example.com):", center=(400, 330), fontsize=24, color=(25, 0, 55))
        screen.draw.text(target, center=(400, 480), fontsize=24, color=(55, 55, 0))
    elif level==2:
        screen.blit("back",(0,0))
        screen.draw.text(message, center=(400, 280), fontsize=24, color=(55, 55, 0))

def analyze_headers(url: str):
    global message,level,count
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        message+=f"Fehler beim Abrufen von {url}: {e}\n"
        print(f"Fehler beim Abrufen von {url}: {e}\n")
        return

    message+=f"\nHTTP Header Analyse for: {url}\n"
    print(f"\nHTTP Header Analyse for: {url}\n")
    headers = response.headers

    for header in SECURITY_HEADERS:
        if header in headers:
            message+=f"[✔] {header}: {headers[header]}\n"
            print(f"[✔] {header}: {headers[header]}\n")
        else:
            message+=f"[✘] {header} missing!\n"
            print(f"[✘] {header} missing!\n")
        if header=="Permissions-Policy":
            wait_mouse()
            count+=1
        if count==2:
            level=-1

def wait_mouse():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  

def on_key_down(key, unicode=None):
    global level, target
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "127.0.0.1"
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        target += unicode

def update():
    global level
    global target
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    elif keyboard.space and level==2:
        level=-1
    if level==2:
        analyze_headers(target)

pgzrun.go()
