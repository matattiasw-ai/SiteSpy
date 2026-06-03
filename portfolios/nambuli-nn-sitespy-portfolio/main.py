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
        border_radius=22,
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        content=ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.W_900, color=TEXT),
            ft.Container(width=54, height=3, bgcolor=accent, border_radius=4),
            *children,
        ], spacing=10),
    )


def main(page: ft.Page):
    page.title = 'NAMBULI, NN - SiteSpy Portfolio'
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    hero = ft.Container(
        padding=ft.padding.symmetric(horizontal=28, vertical=34),
        bgcolor=BG,
        content=ft.Column([
            ft.Image(src='assets/sitespy-wordmark.svg', width=190, fit=ft.ImageFit.CONTAIN),
            ft.Row([chip('Frontend and UX'), chip('SiteSpy final showcase', GOLD)], wrap=True, spacing=10),
            ft.Text('NAMBULI, NN', size=34, weight=ft.FontWeight.W_900, color=TEXT),
            ft.Text('Student number: 224078798 | Team: frontend', color=MUTED),
            ft.Text('Dashboard UI cards, sections, and theme consistency.', size=16, color=TEXT),
            ft.Text('Repository: https://github.com/matattiasw-ai/SiteSpy', color=GOLD, selectable=True),
        ], spacing=13),
    )

    page.add(
        hero,
        ft.Container(
            padding=28,
            content=ft.ResponsiveRow([
                ft.Container(tile('Home / About', [
                    ft.Text('This portfolio presents my assigned SiteSpy contribution area and the evidence I must add for final validation.', color=TEXT),
                    ft.Text('Final app branding: deep navy interface, cyan actions, gold measurement accents, and mobile-first Expo Android screens.', color=MUTED),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Contribution', [
                    ft.Text('Assigned branch: frontend/nambuli-nn-dashboard-ui', color=SUCCESS, selectable=True),
                    ft.Text('Mobile UI polish, screen validation, responsive layout, user experience, and visual evidence.', color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Screen Evidence', [
                    ft.Text('Add phone screenshots for the owned screens and note layout behavior on Android portrait.', color=TEXT),
                    ft.Text('Visual focus: dark navy surfaces, cyan actions, gold measurement accents, readable forms.', color=MUTED),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Evidence of My Work', [
                    ft.Text('Add screenshots of final dark navy/cyan/gold mobile screens, before/after UI notes, responsive checks, and owned screen code references.', color=TEXT),
                    ft.Text('Work evidence to be added by the student before portfolio submission.', color=GOLD),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Blog: My SiteSpy Contribution', [
                    ft.Text('Reflection: explain the exact responsibility and how it supports the full SiteSpy app.', color=TEXT),
                    ft.Text('Responsibility: Dashboard UI cards, sections, and theme consistency.', color=MUTED),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Blog: Evidence of My Work', [
                    ft.Text('Add screenshots, code snippets, design notes, terminal output, or Firebase evidence for the files below.', color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Blog: Challenges and Lessons Learned', [
                    ft.Text('Balancing a polished mobile-first interface with readable forms, navigation, spacing, and Expo web/Android behavior.', color=TEXT),
                    ft.Text('I learned how shared React Native components, theme tokens, and validation states shape a consistent field app experience.', color=MUTED),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Blog: Individual Contribution Video', [
                    ft.Text('Video link placeholder: paste the final individual contribution video link here.', color=TEXT, selectable=True),
                    ft.Text('Maximum duration: 1 minute 30 seconds.', color=GOLD, weight=ft.FontWeight.BOLD),
                ], SUCCESS), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Challenges', [
                    ft.Text('Balancing a polished mobile-first interface with readable forms, navigation, spacing, and Expo web/Android behavior.', color=TEXT),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('What I Learned', [
                    ft.Text('I learned how shared React Native components, theme tokens, and validation states shape a consistent field app experience.', color=TEXT),
                ], ACCENT), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Files Owned / Validation', [
                    ft.Text('- src/screens/DashboardScreen.js', color=MUTED, size=13),
                    ft.Text('- src/components/AppCard.js', color=MUTED, size=13),
                    ft.Text('- src/components/SectionHeader.js', color=MUTED, size=13),
                    ft.Text('- src/theme/', color=MUTED, size=13),
                    ft.Text('Final validation: run checks, collect evidence, and commit only from the student own account.', color=GOLD),
                ]), col={'xs': 12, 'md': 6}),
                ft.Container(tile('Final Delivery Notes', [
                    ft.Text('- Validate final dark navy/cyan/gold dashboard UI system.', color=TEXT, size=13),
                    ft.Text('- Prepare personal Flet portfolio repository.', color=TEXT, size=13),
                    ft.Text('Submission reminder: Sunday, 14 June 2026, 23:59.', color=GOLD, weight=ft.FontWeight.BOLD),
                    ft.Text('The student must personally verify, edit if needed, commit, and push these changes from their own account.', color=MUTED),
                ], SUCCESS), col={'xs': 12}),
            ], spacing=16, run_spacing=16),
        ),
    )


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
