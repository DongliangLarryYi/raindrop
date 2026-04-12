import flet as ft
import pygame
import threading
import os

pygame.mixer.init()
pygame.mixer.music.load("assets/rain.mp3")

def main(page: ft.Page):
    page.title = "RainDrop"
    page.bgcolor = "#1a1a2e"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    is_playing = False
    timer = None

    btn_text = ft.Text("▶ 播放", size=20, color="#ffffff")
    btn = ft.Container(
        content=btn_text,
        bgcolor="#2c5282",
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=40, vertical=16),
    )

    timer_text = ft.Text("", size=14, color="#a0aec0")

    def stop_music():
        nonlocal is_playing
        pygame.mixer.music.stop()
        is_playing = False
        btn_text.value = "▶ 播放"
        timer_text.value = ""
        page.update()

    def set_timer(minutes):
        nonlocal timer
        if timer:
            timer.cancel()
        timer = threading.Timer(minutes * 60, stop_music)
        timer.start()
        timer_text.value = f"⏱ 将在 {minutes} 分钟后停止"
        page.update()

    def toggle(e):
        nonlocal is_playing
        if is_playing:
            pygame.mixer.music.pause()
            btn_text.value = "▶ 播放"
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.unpause()
            btn_text.value = "⏸ 暂停"
        is_playing = not is_playing
        page.update()

    def on_disconnect(e):
        if timer:
            timer.cancel()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os._exit(0)

    page.on_disconnect = on_disconnect
    btn.on_click = toggle

    def make_timer_btn(label, minutes):
        return ft.Container(
            content=ft.Text(label, size=13, color="#ffffff"),
            bgcolor="#2d3748",
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            on_click=lambda e: set_timer(minutes),
        )

    page.add(
        ft.Text("🌧 RainDrop", size=32, color="#ffffff", weight=ft.FontWeight.BOLD),
        ft.Container(height=24),
        btn,
        ft.Container(height=24),
        ft.Text("定时关闭", size=13, color="#a0aec0"),
        ft.Container(height=8),
        ft.Row(
            controls=[
                make_timer_btn("15 分钟", 15),
                make_timer_btn("30 分钟", 30),
                make_timer_btn("60 分钟", 60),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        ft.Container(height=16),
        timer_text,
    )

ft.run(main)
