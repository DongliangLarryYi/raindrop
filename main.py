import sys
import flet as ft
import threading
import os

IS_ANDROID = sys.platform == "android"

if not IS_ANDROID:
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load("assets/rain.mp3")
else:
    import flet_audio as fa

def main(page: ft.Page):
    page.title = "RainDrop"
    page.bgcolor = "#0f1923"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    if not IS_ANDROID:
        page.window.width = 360
        page.window.height = 580

    timer = None
    timer_btns = {}
    is_playing = False

    # Android音频控件
    if IS_ANDROID:
        audio = fa.Audio(
            src="assets/rain.mp3",
            autoplay=False,
            volume=1.0,
            release_mode=fa.ReleaseMode.LOOP,
        )
        page.overlay.append(audio)
        page.update()

    btn_text = ft.Text("▶  播放", size=18, color="#ffffff", weight=ft.FontWeight.W_500)
    btn = ft.Container(
        content=btn_text,
        bgcolor="#2c5282",
        border_radius=50,
        width=160,
        height=56,
        alignment=ft.Alignment(0, 0),
    )

    timer_text = ft.Text("", size=13, color="#718096")

    def stop_music():
        nonlocal is_playing
        if IS_ANDROID:
            audio.pause()
        else:
            pygame.mixer.music.stop()
        is_playing = False
        btn_text.value = "▶  播放"
        btn.bgcolor = "#2c5282"
        timer_text.value = ""
        for b in timer_btns.values():
            b.bgcolor = "#1e2d3d"
        page.update()

    def set_timer(minutes):
        nonlocal timer
        if timer:
            timer.cancel()
        timer = threading.Timer(minutes * 60, stop_music)
        timer.start()
        timer_text.value = f"⏱  将在 {minutes} 分钟后停止"
        for m, b in timer_btns.items():
            b.bgcolor = "#2c5282" if m == minutes else "#1e2d3d"
        page.update()

    async def toggle(e):
        nonlocal is_playing
        if is_playing:
            if IS_ANDROID:
                await audio.pause()
            else:
                pygame.mixer.music.pause()
            btn_text.value = "▶  播放"
            btn.bgcolor = "#2c5282"
        else:
            if IS_ANDROID:
                await audio.play()
            else:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.unpause()
            btn_text.value = "⏸  暂停"
            btn.bgcolor = "#1a4a7a"
        is_playing = not is_playing
        page.update()

    btn.on_click = toggle

    if not IS_ANDROID:
        page.window.on_event = lambda e: os._exit(0) if e.data == "close" else None

    def make_timer_btn(label, minutes):
        b = ft.Container(
            content=ft.Text(label, size=13, color="#ffffff"),
            bgcolor="#1e2d3d",
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=18, vertical=10),
            on_click=lambda e, m=minutes: set_timer(m),
        )
        timer_btns[minutes] = b
        return b

    page.add(
        ft.Text("🌧", size=64),
        ft.Container(height=8),
        ft.Text("RainDrop", size=28, color="#ffffff", weight=ft.FontWeight.BOLD),
        ft.Text("专注 · 入睡 · 放松", size=13, color="#4a6580"),
        ft.Container(height=40),
        btn,
        ft.Container(height=40),
        ft.Text("定时关闭", size=12, color="#4a6580"),
        ft.Container(height=10),
        ft.Row(
            controls=[
                make_timer_btn("15 分钟", 15),
                make_timer_btn("30 分钟", 30),
                make_timer_btn("60 分钟", 60),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        ft.Container(height=20),
        timer_text,
    )

ft.run(main)
