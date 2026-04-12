import flet as ft
import pygame

pygame.mixer.init()
pygame.mixer.music.load("assets/rain.mp3")

def main(page: ft.Page):
    page.title = "RainDrop"
    page.bgcolor = "#1a1a2e"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    is_playing = False

    btn_text = ft.Text("▶ 播放", size=20, color="#ffffff")

    btn = ft.Container(
        content=btn_text,
        bgcolor="#2c5282",
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=40, vertical=16),
    )

    def toggle(e):
        nonlocal is_playing
        if is_playing:
            pygame.mixer.music.pause()
            btn_text.value = "▶ 播放"
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # -1 表示无限循环
            else:
                pygame.mixer.music.unpause()
            btn_text.value = "⏸ 暂停"
        is_playing = not is_playing
        page.update()

    btn.on_click = toggle

    page.add(
        ft.Text("🌧 RainDrop", size=32, color="#ffffff", weight=ft.FontWeight.BOLD),
        ft.Container(height=30),
        btn,
    )

ft.run(main)
