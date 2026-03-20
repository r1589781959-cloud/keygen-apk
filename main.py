import flet as ft
import hashlib


def main(page: ft.Page):
    # ================= 1. 手机屏幕基础设置 =================
    page.title = "藤原印钞机 (移动端)"
    page.window.width = 400
    page.window.height = 700
    page.window.resizable = False

    page.theme_mode = "dark"
    page.horizontal_alignment = "center"

    # ================= 2. 核心算法逻辑 =================
    def generate_key(e):
        mc = input_mc.value.strip()
        if not mc:
            error_snack = ft.SnackBar(content=ft.Text("老板，机器码不能为空哦！"), bgcolor="#D32F2F")
            page.overlay.append(error_snack)
            error_snack.open = True
            page.update()
            return

        # ⚠️ 【高度机密】照搬 V14.5 的底层算法
        s_part1 = "T!m3r"
        s_part2 = "Pr0"
        s_part3 = "V14_@uth"

        complex_raw = f"{s_part1}_{mc[::-1]}_{s_part2}_{mc}_{s_part3}"
        h = hashlib.sha256(complex_raw.encode()).hexdigest().upper()
        act_code = f"{h[3:7]}-{h[15:19]}-{h[27:31]}-{h[50:54]}"

        text_result.value = act_code
        text_result.color = "#66BB6A"

        success_snack = ft.SnackBar(content=ft.Text("⚡ 激活码生成成功！"), bgcolor="#388E3C")
        page.overlay.append(success_snack)
        success_snack.open = True
        page.update()

    def copy_to_clipboard(e):
        if text_result.value and text_result.value != "等待生成...":
            # 🚀 【终极修复】最新版 Flet 剪贴板唯一正确的语法：直接赋值
            page.set_clipboard(text_result.value)

            # 弹出一个酷炫的原生提示条
            copy_snack = ft.SnackBar(content=ft.Text("✅ 成功复制到剪贴板！快去微信发给客人吧~"), bgcolor="#1976D2")
            page.overlay.append(copy_snack)
            copy_snack.open = True
            page.update()

    # ================= 3. 绘制优美的手机 UI =================
    page.appbar = ft.AppBar(
        title=ft.Text("藤原专属印钞机", weight="bold"),
        center_title=True,
        bgcolor="#424242",
    )

    input_mc = ft.TextField(
        label="1. 粘贴客人的机器码",
        hint_text="例如: 7A8B-9C0D-1E2F-3A4B",
        text_align="center",
        width=320,
        border_radius=15
    )

    btn_generate = ft.Container(
        content=ft.Row(
            controls=[ft.Text("⚡ 验证并生成永久激活码", color="white", weight="bold", size=16)],
            alignment="center",
            vertical_alignment="center"
        ),
        width=320,
        height=50,
        bgcolor="#D32F2F",
        border_radius=15,
        on_click=generate_key,
        ink=True
    )

    text_result = ft.Text(
        value="等待生成...",
        size=24,
        weight="bold",
        color="#9E9E9E"
    )

    btn_copy = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("📋", size=18),
                ft.Text("一键复制激活码", color="white", weight="bold", size=14)
            ],
            alignment="center",
            vertical_alignment="center",
            spacing=8
        ),
        width=200,
        height=45,
        bgcolor="#1976D2",
        border_radius=15,
        on_click=copy_to_clipboard,
        ink=True
    )

    # ================= 4. 拼装到屏幕上 =================
    page.add(
        ft.Container(height=20),
        ft.Text("🛡️", size=80),
        ft.Container(height=10),
        input_mc,
        ft.Container(height=10),
        btn_generate,
        ft.Divider(height=40, color="#424242"),
        ft.Text("2. 请将以下【激活码】发送给客人:", size=14, color="#BDBDBD"),
        text_result,
        ft.Container(height=10),
        btn_copy
    )


if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)
