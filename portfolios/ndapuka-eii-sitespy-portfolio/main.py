import flet as ft

BG = '#07101E'
SURFACE = '#101B2D'
TEXT = '#F8FBFF'
MUTED = '#A8B6CC'
ACCENT = '#25C7F7'
GOLD = '#D8A73E'
SUCCESS = '#49D28F'
BORDER = '#273A5D'


def chip(text, color=ACCENT):
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=12, vertical=7),
        border_radius=18,
        bgcolor=color,
        content=ft.Text(text, size=12, weight=ft.FontWeight.BOLD, color=BG),
    )


def tile(title, children, accent=GOLD):
    return ft.Container(
        padding=22,
        border_radius=8,
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        content=ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.W_900, color=TEXT),
            ft.Container(width=54, height=3, bgcolor=accent, border_radius=4),
            *children,
        ], spacing=10),
    )


def main(page: ft.Page):
    page.title = "Emilly Ndapuka - SiteSpy Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    hero = ft.Container(
        padding=ft.padding.symmetric(horizontal=28, vertical=34),
        bgcolor=BG,
        content=ft.Column([
            ft.Image(src='assets/sitespy-wordmark.svg', width=190, fit=ft.ImageFit.CONTAIN),
            ft.Row([chip("Mining"), chip("Frontend", GOLD)], wrap=True, spacing=10),
            ft.Text("Emilly Ndapuka", size=34, weight=ft.FontWeight.W_900, color=TEXT),
            ft.Text("GitHub: emilly20-06 | Email: emillyndapuka@gmail.com", color=MUTED, selectable=True),
            ft.Text("Project creation and manual estimate forms.", size=16, color=TEXT),
            ft.Text("GitHub profile: https://github.com/emilly20-06", color=GOLD, selectable=True),
        ], spacing=13),
    )

    page.add(
        hero,
        ft.Container(
            padding=28,
            content=ft.ResponsiveRow([
                ft.Container(tile('Profile', [
                    ft.Text("Department: Mining", color=TEXT),
                    ft.Text("Suggested role/area: Frontend", color=MUTED),
                    ft.Text("Match status: MATCHED", color=SUCCESS),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Contribution Area', [
                    ft.Text("Project creation and manual estimate forms.", color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Files / Validation Area', [
                    ft.Text('- src/screens/NewProjectScreen.js', color=MUTED, size=13),
                    ft.Text('- src/screens/ManualEstimateScreen.js', color=MUTED, size=13),
                    ft.Text('- src/components/AppInput.js', color=MUTED, size=13),
                    ft.Text('- src/utils/validators.js', color=MUTED, size=13),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Local Git Setup', [
                    ft.Text("git config user.name \"Emilly Ndapuka\"\ngit config user.email \"emillyndapuka@gmail.com\"\ngit config --get user.name\ngit config --get user.email", color=TEXT, selectable=True),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Clone, Commit, Push', [
                    ft.Text("git clone \"Replace with your own fork URL after creating the fork.\"\ncd \"Replace with your cloned repository folder\"\ngit status\ngit checkout -b portfolio/ndapuka-eii-sitespy-portfolio\ngit add README.md index.html main.py\ngit commit -m \"Update Emilly Ndapuka SiteSpy portfolio\"\ngit push -u origin portfolio/ndapuka-eii-sitespy-portfolio", color=TEXT, selectable=True),
                ], SUCCESS), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Evidence', [
                    ft.Text('Add screenshots, code notes, terminal output, testing evidence, or review notes for work personally verified by the student.', color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Individual Video', [
                    ft.Text('Manual link required. Maximum duration: 1 minute 30 seconds.', color=GOLD, weight=ft.FontWeight.BOLD),
                ], SUCCESS), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Handover Note', [
                    ft.Text('Use your own fork or portfolio repository. Do not claim commits or authorship that are not personally yours.', color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
            ], spacing=16, run_spacing=16),
        ),
    )


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
