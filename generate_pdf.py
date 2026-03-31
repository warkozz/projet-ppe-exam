"""
Generation PDFs PPE Foot5 -- style epure (inspire RESTRUCTURE_FINAL)
Polices TTF Windows : Arial (Unicode) + Consolas (mono)
"""
import re
import math
from pathlib import Path
from fpdf import FPDF, XPos, YPos

# ── Polices systeme Windows ───────────────────────────────────────────────
_FD = Path(r"C:\Windows\Fonts")
ARIAL     = str(_FD / "arial.ttf")
ARIALB    = str(_FD / "arialbd.ttf")
ARIALI    = str(_FD / "ariali.ttf")
ARIALBI   = str(_FD / "arialbi.ttf")
CONSOLAS  = str(_FD / "consola.ttf")

# ── Palette ───────────────────────────────────────────────────────────────
GREEN_DARK   = ( 25,  75,  35)   # couverture, DOC-badge, footer-line
GREEN_MAIN   = ( 42, 122,  50)   # barre H1, H2 texte, separ, table header
GREEN_LIGHT  = ( 76, 175,  80)   # accents fins, bullet num
GREEN_PALE   = (240, 248, 240)   # fond blockquote
DARK_TEXT    = ( 26,  26,  26)   # texte principal
GREY_TEXT    = (110, 110, 110)   # footer/description
GREY_LINE    = (210, 220, 210)   # lignes separatrices
CODE_BG      = (246, 248, 245)   # fond code (clair)
CODE_FG      = ( 30,  30,  30)   # texte code
TABLE_HDR    = ( 45,  85,  50)   # fond en-tete tableau
TABLE_ALT    = (249, 253, 249)   # lignes paires tableau
WHITE        = (255, 255, 255)
BLACK        = ( 26,  26,  26)

# ── Descripteurs documents ────────────────────────────────────────────────
DOCUMENTS = [
    dict(
        num="01", out="01_Tableau_Synthese.pdf",
        title="Tableau de Synthese Comparative",
        desc="Comparaison des deux applications, technologies, fonctionnalites, roles utilisateurs.",
        file="01_Tableau_Synthese.md",
    ),
    dict(
        num="02", out="02_Dossier_Principal_Commun.pdf",
        title="Dossier Principal -- Partie Commune",
        desc="Contexte M2L, base de donnees partagee (MCD/MLD/SQL), architecture globale.",
        file="02_Dossier_Principal_Commun.md",
    ),
    dict(
        num="03", out="03_Application_Legere_Web.pdf",
        title="Application Legere -- Web Client",
        desc="Interface React + FastAPI, parcours reservation, authentification JWT, tests.",
        file="03_Application_Legere_Web.md",
    ),
    dict(
        num="04", out="04_Application_Lourde_Admin.pdf",
        title="Application Lourde -- Admin Desktop",
        desc="App admin PySide6, architecture MVC, RBAC, bcrypt, calendrier, tests 87%.",
        file="04_Application_Lourde_Admin.md",
    ),
    dict(
        num="05", out="05_Sources_Code.pdf",
        title="Code Source -- Liens GitHub",
        desc="Depots GitHub, structures des projets, metriques de code, guide de demarrage.",
        file="05_Sources_Code.md",
    ),
]


# =========================================================================
#  CLASSE PDF PRINCIPALE
# =========================================================================
class FootPDF(FPDF):
    """PDF propre avec polices TTF, header/footer discrets."""
    # fpdf2 >=2.8: marqueurs par defaut sont ITALIC=__ et UNDERLINE=--
    # On desactive italic/underline pour eviter les conflits avec -- et __
    MARKDOWN_BOLD_MARKER      = "**"
    MARKDOWN_ITALICS_MARKER   = "\x00"  # desactive
    MARKDOWN_UNDERLINE_MARKER = "\x01"  # desactive

    def __init__(self, doc_title="Foot5", doc_num=""):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.doc_title = doc_title
        self.doc_num   = doc_num
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(left=20, top=15, right=20)
        self._load_fonts()

    def _load_fonts(self):
        self.add_font("Arial",    style="",   fname=ARIAL)
        self.add_font("Arial",    style="B",  fname=ARIALB)
        self.add_font("Arial",    style="I",  fname=ARIALI)
        self.add_font("Arial",    style="BI", fname=ARIALBI)
        self.add_font("Consolas", style="",   fname=CONSOLAS)

    # ── Header ────────────────────────────────────────────────────────────
    def header(self):
        if self.page_no() == 1:
            return
        # Ligne verte fine en haut
        self.set_fill_color(*GREEN_MAIN)
        self.rect(0, 0, 210, 1.8, style="F")
        # Carre vert coin droit (decoration)
        self.rect(194, 0, 16, 5, style="F")
        self.set_y(self.t_margin + 3)

    # ── Footer ────────────────────────────────────────────────────────────
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        # Filet separateur
        self.set_draw_color(*GREY_LINE)
        self.set_line_width(0.25)
        self.line(20, self.get_y(), 190, self.get_y())
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.set_y(self.get_y() + 2)
        self.set_font("Arial", "", 7)
        self.set_text_color(*GREY_TEXT)
        self.set_x(20)
        self.cell(85, 5, "Foot5  --  PPE BTS SIO SLAM  --  Hakim Rayane", align="L")
        lbl = (f"DOC {self.doc_num}  |  Page {self.page_no()}"
               if self.doc_num else f"Page {self.page_no()}")
        self.cell(85, 5, lbl, align="R")
        self.set_text_color(*BLACK)

    # ── Utilitaires ───────────────────────────────────────────────────────
    def _clean(self, text):
        """Supprime syntaxe Markdown inline, remplace emojis."""
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*',     r'\1', text)
        text = re.sub(r'`(.+?)`',       r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Supprimer seulement les tirets et puces de debut de ligne
        text = re.sub(r'^\s*[-\u2022\u00b7]\s*', '', text)
        emoji_map = {
            '\u2705': '[OK]', '\u274c': '[X]', '\u26a0': '[!]',
            '\U0001f7e1': '[?]', '\U0001f7e2': '[V]', '\U0001f534': '[X]',
            '\U0001f4c1': '[D]', '\U0001f3af': '[>]', '\U0001f4e6': '[P]',
        }
        for e, r in emoji_map.items():
            text = text.replace(e, r)
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        text = re.sub(r'[\u2600-\u27BF]', '', text)
        return text.strip()

    def _safe(self, text):
        """Remplace box-drawing et fleches et symbols non supportes."""
        reps = {
            '\u2014': '--',  '\u2013': '-',
            '\u2018': "'",   '\u2019': "'",
            '\u201c': '"',   '\u201d': '"',
            '\u2026': '...',
            '\u25ba': '>',   '\u25b6': '>',   '\u25c0': '<',
            '\u25bc': 'v',   '\u25b2': '^',   '\u25bd': 'v',  '\u25b3': '^',
            '\u2022': '*',   '\u25aa': '*',   '\u25ab': '*',
            # Box-drawing
            '\u2502': '|',   '\u2514': '+',   '\u251c': '+',  '\u2500': '-',
            '\u252c': '+',   '\u2510': '+',   '\u250c': '+',  '\u2518': '+',
            '\u2524': '+',   '\u253c': '+',   '\u2550': '=',  '\u2551': '|',
            '\u2554': '+',   '\u2557': '+',   '\u255a': '+',  '\u255d': '+',
            '\u2560': '+',   '\u2563': '+',   '\u2566': '+',  '\u2569': '+',
            '\u256c': '+',
        }
        for ch, r in reps.items():
            text = text.replace(ch, r)
        return text

    def _w(self):
        return self.w - self.l_margin - self.r_margin


# =========================================================================
#  PAGE DE GARDE
# =========================================================================
def add_cover_page(pdf: FootPDF, doc_num: str, title: str, desc: str):
    """Page de garde propre : bande sombre + badge DOC + grand titre + desc."""
    pdf.add_page()
    w = pdf.w - pdf.l_margin - pdf.r_margin

    # Bande verte sombre en haut (14mm)
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(0, 0, 210, 14, style="F")

    # Badge "DOC XX"
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(pdf.l_margin, 22, 24, 10, style="F")
    pdf.set_xy(pdf.l_margin, 22)
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(*WHITE)
    pdf.cell(24, 10, f"DOC {doc_num}", align="C")
    pdf.set_text_color(*BLACK)

    # Titre principal avec barre gauche verte
    pdf.set_y(42)
    y0 = pdf.get_y()
    bar_h = max(18, 10 * (1 + len(title) // 38))
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(pdf.l_margin, y0, 4.5, bar_h, style="F")
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(*DARK_TEXT)
    pdf.set_xy(pdf.l_margin + 8, y0 + 1)
    pdf.multi_cell(w - 8, 10, title)
    new_y = max(pdf.get_y(), y0 + bar_h)

    # Ligne separatrice verte
    pdf.set_draw_color(*GREEN_LIGHT)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, new_y + 3, pdf.l_margin + w, new_y + 3)
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_y(new_y + 8)

    # Description
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(*GREY_TEXT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 6, desc)
    pdf.set_text_color(*BLACK)

    # Phrase cle en encadre style blockquote
    pdf.set_y(max(pdf.get_y() + 8, 110))
    y_bq = pdf.get_y()
    bq_h = 28
    pdf.set_fill_color(*GREEN_PALE)
    pdf.rect(pdf.l_margin, y_bq, w, bq_h, style="F")
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(pdf.l_margin, y_bq, 3, bq_h, style="F")
    pdf.set_font("Arial", "I", 9.5)
    pdf.set_text_color(50, 100, 55)
    pdf.set_xy(pdf.l_margin + 7, y_bq + 4)
    pdf.multi_cell(w - 9, 5.5,
        "\"Le projet Foot5 repose sur une architecture composee de deux applications "
        "complementaires : une application web destinee aux clients et une application "
        "lourde destinee a l'administration, partageant une base de donnees commune.\""
    )
    pdf.set_text_color(*BLACK)

    # Pied de page couverture (desactiver auto-break pour eviter page fantome)
    pdf.set_auto_page_break(False)
    pdf.set_y(258)
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(0, 257, 210, 40, style="F")
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(pdf.l_margin, 263)
    pdf.cell(w / 2, 6, "Hakim Rayane")
    pdf.set_xy(pdf.l_margin, 270)
    pdf.set_font("Arial", "", 9)
    pdf.cell(w / 2, 5, "BTS SIO SLAM  --  Mars 2026")

    pdf.set_font("Arial", "", 8.5)
    pdf.set_xy(pdf.l_margin + w / 2, 263)
    pdf.cell(w / 2, 5, "App legere  : github.com/warkozz/projet-ppe-foot5-web", align="R")
    pdf.set_xy(pdf.l_margin + w / 2, 269)
    pdf.cell(w / 2, 5, "App lourde  : github.com/warkozz/projet-ppe-exam", align="R")
    pdf.set_xy(pdf.l_margin + w / 2, 275)
    pdf.cell(w / 2, 5, "Base de donnees  : MySQL 'foot5'  --  XAMPP", align="R")
    pdf.set_text_color(*BLACK)
    # Reeactiver auto-break pour les pages suivantes
    pdf.set_auto_page_break(True, margin=22)


# =========================================================================
#  PAGE DE GARDE DOSSIER COMPLET (style RESTRUCTURE)
# =========================================================================
def add_master_cover(pdf: FootPDF):
    """Couverture sobre fond blanc, accents verts, tout centre."""
    pdf.add_page()

    # Fond blanc
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, 210, 297, style="F")

    # Bande verte fine en haut (6mm)
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(0, 0, 210, 6, style="F")

    # Bande verte fine en bas (6mm)
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(0, 291, 210, 6, style="F")

    # Accent vert clair (bande decorative sous la bande du haut)
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(0, 6, 210, 2, style="F")
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(0, 289, 210, 2, style="F")

    # "FOOT5" grand titre centre
    pdf.set_font("Arial", "B", 80)
    pdf.set_text_color(*GREEN_DARK)
    pdf.set_xy(0, 88)
    pdf.cell(210, 36, "FOOT5", align="C")

    # Sous-titre lettre-espacee
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*GREEN_MAIN)
    pdf.set_xy(0, 130)
    pdf.cell(210, 7, "DOSSIER TECHNIQUE COMPLET", align="C")

    # Ligne fine verte centree
    pdf.set_draw_color(*GREEN_LIGHT)
    pdf.set_line_width(0.5)
    pdf.line(60, 143, 150, 143)
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)

    # Bloc infos centre
    pdf.set_xy(0, 196)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(*DARK_TEXT)
    pdf.cell(210, 8, "Maison des Ligues de Lorraine", align="C")

    pdf.set_xy(0, 207)
    pdf.set_font("Arial", "", 9.5)
    pdf.set_text_color(*GREY_TEXT)
    pdf.cell(210, 6, "Projet de Soutenance -- BTS SIO SLAM", align="C")

    # Ligne fine grise
    pdf.set_draw_color(*GREY_LINE)
    pdf.set_line_width(0.3)
    pdf.line(75, 218, 135, 218)
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)

    pdf.set_xy(0, 222)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(*GREEN_DARK)
    pdf.cell(210, 9, "HAKIM RAYANE", align="C")

    pdf.set_xy(0, 233)
    pdf.set_font("Arial", "", 9.5)
    pdf.set_text_color(*GREY_TEXT)
    pdf.cell(210, 6, "Mars 2026", align="C")

    pdf.set_text_color(*BLACK)


# =========================================================================
#  PAGE DE FIN
# =========================================================================
def add_final_page(pdf: FootPDF):
    """Page de cloture sobre en bas du dossier."""
    pdf.add_page()
    w = pdf.w - pdf.l_margin - pdf.r_margin

    # Grand espace vide (respiration)
    pdf.set_y(80)

    # Ligne decorative
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(pdf.l_margin, pdf.get_y(), w, 1.5, style="F")
    pdf.ln(12)

    # Texte central
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(50, 100, 55)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w, 12, "Fin du Dossier Technique", align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*GREY_TEXT)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w, 7, "Projet PPE -- BTS SIO SLAM", align="C")
    pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w, 7, "Hakim Rayane  --  Mars 2026", align="C")
    pdf.ln(12)

    # Ligne decorative basse
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(pdf.l_margin, pdf.get_y(), w, 1.5, style="F")
    pdf.ln(14)

    # Liens GitHub
    pdf.set_font("Arial", "I", 8.5)
    pdf.set_text_color(*GREY_TEXT)
    for label, url in [
        ("App legere (Web)    :", "github.com/warkozz/projet-ppe-foot5-web"),
        ("App lourde (Admin)  :", "github.com/warkozz/projet-ppe-exam"),
    ]:
        pdf.set_x(pdf.l_margin)
        pdf.cell(w / 2, 6, label, align="R")
        pdf.set_font("Arial", "", 8.5)
        pdf.cell(w / 2, 6, f"  {url}")
        pdf.set_font("Arial", "I", 8.5)
        pdf.ln(6)

    pdf.set_text_color(*BLACK)


# =========================================================================
#  PARSER MARKDOWN -> PDF
# =========================================================================
class MarkdownToPDF:
    def __init__(self, pdf: FootPDF):
        self.pdf = pdf
        self.in_code  = False
        self.code_acc = []
        self.in_table       = False
        self.table_headers  = []
        self.table_rows     = []

    # ── Bloc de code ──────────────────────────────────────────────────────
    def _flush_code(self):
        if not self.code_acc:
            return
        pdf   = self.pdf
        lh    = 4.6
        pad   = 5
        x0    = pdf.l_margin
        lines = list(self.code_acc)
        self.code_acc = []

        remaining  = lines
        first_chunk = True
        while remaining:
            y_start = pdf.get_y()
            space   = pdf.h - 22 - y_start
            if space < lh * 2 + pad * 2:
                pdf.add_page()
                y_start = pdf.get_y()
                space   = pdf.h - 22 - y_start

            max_lines = max(1, int((space - pad * 2) / lh))
            batch     = remaining[:max_lines]
            remaining = remaining[max_lines:]
            is_last   = len(remaining) == 0

            batch_h = lh * len(batch) + pad * (2 if first_chunk else 1) + (pad if is_last else 0)
            y0 = pdf.get_y()

            # Fond clair
            pdf.set_fill_color(*CODE_BG)
            pdf.rect(x0, y0, pdf._w(), batch_h, style="F")
            # Barre gauche verte
            pdf.set_fill_color(*GREEN_MAIN)
            pdf.rect(x0, y0, 3, batch_h, style="F")

            # Texte
            pdf.set_font("Consolas", "", 7.8)
            pdf.set_text_color(*CODE_FG)
            pdf.set_xy(x0 + 6, y0 + (pad if first_chunk else 2))
            for line in batch:
                clean = pdf._safe(line[:118])
                pdf.set_x(x0 + 6)
                pdf.cell(pdf._w() - 8, lh, clean,
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_y(y0 + batch_h)
            pdf.set_text_color(*BLACK)
            first_chunk = False
            if remaining:
                pdf.add_page()

        pdf.ln(4)

    # ── Tableau (cellules multi-lignes, pas de troncature) ─────────────────
    def _flush_table(self):
        if not self.table_rows:
            self._reset_table()
            return
        pdf     = self.pdf
        headers = self.table_headers
        rows    = self.table_rows
        ncols   = max(len(headers), max((len(r) for r in rows), default=0))
        if ncols == 0:
            self._reset_table()
            return

        col_w = pdf._w() / ncols
        lh    = 5.2   # hauteur d'une ligne de texte
        vpad  = 2.0   # padding vertical haut/bas

        def _prep(text):
            t = text.strip()
            # Conserver les marqueurs **gras** pour rendu markdown
            t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)   # liens -> texte
            t = re.sub(r'`(.+?)`',               r'\1', t)    # code inline -> texte
            t = re.sub(r'^\s*[-\u2022\u00b7]\s*', '', t)      # puce debut de ligne
            for e, r in [('\u2705','[OK]'), ('\u274c','[X]'), ('\u26a0','[!]'),
                         ('\U0001f7e1','[?]'), ('\U0001f7e2','[V]'), ('\U0001f534','[X]'),
                         ('\U0001f4c1','[D]'), ('\U0001f3af','[>]'), ('\U0001f4e6','[P]')]:
                t = t.replace(e, r)
            t = re.sub(r'[\U00010000-\U0010ffff]', '', t)
            t = re.sub(r'[\u2600-\u27BF]', '', t)
            return pdf._safe(t).strip()

        def _est_h(text, bold=False):
            pdf.set_font("Arial", "B" if bold else "", 8.5)
            if not text:
                return lh + vpad * 2
            w_avail = col_w - 4
            if w_avail <= 0:
                return lh + vpad * 2
            # Retirer les marqueurs markdown pour le calcul de largeur
            clean_w = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            clean_w = re.sub(r'\*(.+?)\*',     r'\1', clean_w)
            sw = pdf.get_string_width(clean_w)
            lines = max(1, math.ceil(sw / w_avail * 1.2))
            return lines * lh + vpad * 2

        def _row_h(cells, bold=False):
            return max((_est_h(t, bold) for t in cells), default=lh + vpad * 2)

        def _draw_row(y0, cells, rh, fill_color, text_color, bold=False):
            style = "B" if bold else ""
            pdf.set_fill_color(*fill_color)
            pdf.set_text_color(*text_color)
            pdf.set_draw_color(*GREY_LINE)
            pdf.set_line_width(0.2)
            for ci, text in enumerate(cells):
                pdf.set_font("Arial", style, 8.5)  # reset avant chaque cellule
                x = pdf.l_margin + ci * col_w
                pdf.rect(x, y0, col_w, rh, style="FD")
                if text:
                    pdf.set_xy(x + 2, y0 + vpad)
                    pdf.multi_cell(col_w - 4, lh, text, align="L",
                                   markdown=(not bold),
                                   new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_y(y0 + rh)

        # Prepare
        hdr_cells  = [_prep(h) for h in (headers[:ncols] + [''] * max(0, ncols - len(headers)))]
        data_cells = [[_prep(rows[ri][ci] if ci < len(rows[ri]) else '') for ci in range(ncols)]
                      for ri in range(len(rows))]
        hdr_h   = _row_h(hdr_cells, bold=True)
        rows_hs = [_row_h(r) for r in data_cells]
        total_h = hdr_h + sum(rows_hs) + 4

        if pdf.get_y() + total_h > pdf.h - 25:
            if total_h < pdf.h - 35:
                pdf.add_page()

        # En-tete
        _draw_row(pdf.get_y(), hdr_cells, hdr_h, TABLE_HDR, WHITE, bold=True)

        # Lignes de donnees
        for ri, (cells, rh) in enumerate(zip(data_cells, rows_hs)):
            y = pdf.get_y()
            if y + rh > pdf.h - 22:
                pdf.add_page()
                y = pdf.get_y()
            fill = TABLE_ALT if ri % 2 == 0 else WHITE
            _draw_row(y, cells, rh, fill, BLACK)

        pdf.set_draw_color(0, 0, 0)
        pdf.set_text_color(*BLACK)
        pdf.ln(3)
        self._reset_table()

    def _reset_table(self):
        self.in_table      = False
        self.table_headers = []
        self.table_rows    = []

    # ── Rendu d'une ligne Markdown ────────────────────────────────────────
    def render_line(self, line: str):
        pdf = self.pdf

        # Image inline : syntaxe ![alt](chemin) ou marqueur special ![IMAGE](chemin)
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
        if img_match and not self.in_code:
            if self.in_table:
                self._flush_table()
            img_path = img_match.group(2).strip()
            alt_text = img_match.group(1).strip()
            # Chemin relatif a la racine du projet
            base = Path(__file__).parent
            full_path = base / img_path if not Path(img_path).is_absolute() else Path(img_path)
            if full_path.exists():
                from PIL import Image as PILImage
                try:
                    with PILImage.open(str(full_path)) as im:
                        iw, ih = im.size
                    max_w  = pdf._w()
                    max_disp_w = max_w * 0.70  # 70 % de la largeur imprimable
                    scale  = min(1.0, max_disp_w / (iw * 0.352778))  # px -> mm (96dpi)
                    disp_w = iw * 0.352778 * scale
                    disp_h = ih * 0.352778 * scale
                    if pdf.get_y() + disp_h > pdf.h - 25:
                        pdf.add_page()
                    x = pdf.l_margin + (max_w - disp_w) / 2
                    pdf.image(str(full_path), x=x, y=pdf.get_y(), w=disp_w)
                    pdf.set_y(pdf.get_y() + disp_h + 3)
                    if alt_text:
                        pdf.set_font("Arial", "I", 8)
                        pdf.set_text_color(*GREY_TEXT)
                        pdf.set_x(pdf.l_margin)
                        pdf.cell(pdf._w(), 5, alt_text, align="C")
                        pdf.ln(5)
                        pdf.set_text_color(*BLACK)
                except Exception:
                    pdf.set_font("Arial", "I", 8.5)
                    pdf.set_text_color(*GREY_TEXT)
                    pdf.set_x(pdf.l_margin)
                    pdf.cell(pdf._w(), 6, f"[Image : {alt_text or img_path}]", align="C")
                    pdf.ln(6)
                    pdf.set_text_color(*BLACK)
            else:
                pdf.set_font("Arial", "I", 8.5)
                pdf.set_text_color(*GREY_TEXT)
                pdf.set_x(pdf.l_margin)
                pdf.cell(pdf._w(), 6, f"[Image introuvable : {img_path}]", align="C")
                pdf.ln(6)
                pdf.set_text_color(*BLACK)
            return

        # Bloc code
        if line.strip().startswith("```"):
            if self.in_table:
                self._flush_table()
            if not self.in_code:
                self.in_code  = True
                self.code_acc = []
            else:
                self.in_code = False
                self._flush_code()
            return
        if self.in_code:
            self.code_acc.append(line.rstrip())
            return

        # Tableau
        if '|' in line and line.strip().startswith('|'):
            stripped = line.strip()
            if re.match(r'^\|[\s\-|:]+\|$', stripped):
                return
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not self.in_table:
                self.in_table = True
                self.table_headers = cells
                self.table_rows    = []
            else:
                self.table_rows.append(cells)
            return
        else:
            if self.in_table:
                self._flush_table()

        # Blockquote
        if line.strip().startswith('>'):
            content = line.strip().lstrip('> ').strip()
            if content:
                clean    = pdf._safe(pdf._clean(content))
                est_h    = max(1, (len(clean) // 65) + 1) * 5.5 + 10
                if pdf.get_y() + est_h > pdf.h - 25:
                    pdf.add_page()
                x0, y0 = pdf.l_margin, pdf.get_y()
                pdf.set_fill_color(*GREEN_PALE)
                pdf.rect(x0, y0, pdf._w(), est_h, style="F")
                pdf.set_fill_color(*GREEN_MAIN)
                pdf.rect(x0, y0, 3.5, est_h, style="F")
                pdf.set_font("Arial", "I", 9.5)
                pdf.set_text_color(50, 100, 55)
                pdf.set_xy(x0 + 8, y0 + 4)
                pdf.multi_cell(pdf._w() - 10, 5.5, clean)
                pdf.set_text_color(*BLACK)
                if pdf.get_y() < y0 + est_h:
                    pdf.set_y(y0 + est_h)
                pdf.ln(4)
            return

        # Titres
        h1 = re.match(r'^#\s+(.+)$',    line)
        h2 = re.match(r'^##\s+(.+)$',   line)
        h3 = re.match(r'^###\s+(.+)$',  line)
        h4 = re.match(r'^####\s+(.+)$', line)

        if h1:
            title = pdf._safe(pdf._clean(h1.group(1)))
            pdf.ln(6)
            if pdf.get_y() + 28 > pdf.h - 25:
                pdf.add_page()
            y0 = pdf.get_y()
            # Barre laterale gauche
            pdf.set_fill_color(*GREEN_MAIN)
            pdf.rect(pdf.l_margin, y0, 4.5, 17, style="F")
            # Texte titre
            pdf.set_font("Arial", "B", 20)
            pdf.set_text_color(*DARK_TEXT)
            pdf.set_xy(pdf.l_margin + 8, y0 + 1)
            pdf.multi_cell(pdf._w() - 8, 9, title)
            new_y = max(pdf.get_y(), y0 + 17)
            # Filet sous le titre
            pdf.set_draw_color(*GREEN_LIGHT)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, new_y + 2, pdf.l_margin + pdf._w(), new_y + 2)
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_text_color(*BLACK)
            pdf.set_y(new_y + 7)
            return

        if h2:
            title = pdf._safe(pdf._clean(h2.group(1)))
            pdf.ln(5)
            if pdf.get_y() + 20 > pdf.h - 25:
                pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.set_text_color(*GREEN_MAIN)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf._w(), 7, title)
            new_y = pdf.get_y()
            # Filet vert leger
            pdf.set_draw_color(*GREEN_LIGHT)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, new_y + 1, pdf.l_margin + pdf._w(), new_y + 1)
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_text_color(*BLACK)
            pdf.set_y(new_y + 5)
            return

        if h3:
            title = pdf._safe(pdf._clean(h3.group(1)))
            pdf.ln(4)
            if pdf.get_y() + 14 > pdf.h - 25:
                pdf.add_page()
            pdf.set_font("Arial", "B", 11.5)
            pdf.set_text_color(*GREEN_DARK)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf._w(), 6, title)
            pdf.set_text_color(*BLACK)
            pdf.ln(2)
            return

        if h4:
            title = pdf._safe(pdf._clean(h4.group(1)))
            pdf.ln(3)
            if pdf.get_y() + 11 > pdf.h - 25:
                pdf.add_page()
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(*DARK_TEXT)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf._w(), 5.5, title)
            pdf.set_text_color(*BLACK)
            pdf.ln(1.5)
            return

        # Ligne horizontale ---
        if re.match(r'^[-*_]{3,}$', line.strip()):
            pdf.ln(2)
            pdf.set_draw_color(*GREY_LINE)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, pdf.get_y(),
                     pdf.l_margin + pdf._w(), pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            return

        # Listes (puces et numerotees)
        bullet_match = re.match(r'^(\s*)([-*+\u2022]|\d+\.)\s+(.+)$', line)
        if bullet_match:
            indent  = len(bullet_match.group(1))
            marker  = bullet_match.group(2)
            content = bullet_match.group(3)
            clean   = pdf._safe(pdf._clean(content))
            x_off   = pdf.l_margin + 3 + (indent // 2) * 5
            y_bul   = pdf.get_y()
            if y_bul + 5.5 > pdf.h - 22:
                pdf.add_page()
                y_bul = pdf.get_y()
            b = marker if re.match(r'\d+\.', marker) else "\u2022"
            pdf.set_font("Arial", "", 9.5)
            pdf.set_text_color(*BLACK)
            pdf.set_xy(x_off, y_bul)
            pdf.cell(6, 5.5, b)
            pdf.set_xy(x_off + 6, y_bul)
            pdf.multi_cell(pdf._w() - (x_off - pdf.l_margin) - 8, 5.5, clean)
            return

        # Ligne vide
        if not line.strip():
            pdf.ln(2.5)
            return

        # Texte normal
        clean = pdf._safe(pdf._clean(line))
        if not clean:
            return
        pdf.set_font("Arial", "", 9.5)
        pdf.set_text_color(*BLACK)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf._w(), 5.5, clean)
        pdf.ln(0.5)

    def render_file(self, md_path: Path):
        lines = md_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            self.render_line(line)
        if self.in_code:
            self._flush_code()
        if self.in_table:
            self._flush_table()


# =========================================================================
#  CONSTRUCTION DES PDFs
# =========================================================================
def build_pdf_doc(doc_info: dict, src_dir: Path, out_dir: Path):
    src = src_dir / doc_info["file"]
    if not src.exists():
        print(f"  [SKIP] {src} introuvable")
        return None

    pdf = FootPDF(doc_title=doc_info["title"], doc_num=doc_info["num"])
    add_cover_page(pdf, doc_info["num"], doc_info["title"], doc_info["desc"])
    pdf.add_page()
    MarkdownToPDF(pdf).render_file(src)
    add_final_page(pdf)

    out = out_dir / doc_info["out"]
    pdf.output(str(out))
    return out


def build_complete_pdf(src_dir: Path, out_dir: Path):
    pdf = FootPDF(doc_title="Foot5 -- Dossier Complet", doc_num="")
    add_master_cover(pdf)

    # Page sommaire
    pdf.add_page()
    w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_y(32)
    y0 = pdf.get_y()
    pdf.set_fill_color(*GREEN_MAIN)
    pdf.rect(pdf.l_margin, y0, 5, 22, style="F")
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(*DARK_TEXT)
    pdf.set_xy(pdf.l_margin + 10, y0 + 2)
    pdf.cell(w - 10, 20, "SOMMAIRE")
    new_y = y0 + 22
    pdf.set_draw_color(*GREEN_LIGHT)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, new_y + 3, pdf.l_margin + w, new_y + 3)
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(*BLACK)
    pdf.set_y(new_y + 18)

    sommaire_page = pdf.page_no()
    sommaire_ypos  = {}
    link_ids = {doc['num']: pdf.add_link() for doc in DOCUMENTS}

    for doc in DOCUMENTS:
        sommaire_ypos[doc['num']] = pdf.get_y()
        lnk = link_ids[doc['num']]
        # Badge DOC XX (cliquable)
        pdf.set_fill_color(*GREEN_MAIN)
        pdf.rect(pdf.l_margin, pdf.get_y(), 20, 10, style="F")
        pdf.set_xy(pdf.l_margin, pdf.get_y())
        pdf.set_font("Arial", "B", 9)
        pdf.set_text_color(*WHITE)
        pdf.cell(20, 10, f"DOC {doc['num']}", align="C", link=lnk)
        # Titre (cliquable)
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(*DARK_TEXT)
        pdf.cell(w - 36, 10, f"   {doc['title']}", link=lnk)
        pdf.ln(20)
    pdf.set_text_color(*BLACK)

    # Contenu de chaque document -- suivi des pages de depart
    doc_start_pages = {}
    for doc_info in DOCUMENTS:
        src = src_dir / doc_info["file"]
        if not src.exists():
            continue
        pdf.add_page()
        doc_start_pages[doc_info['num']] = pdf.page_no()
        # Badge DOC XX en haut (avant tout contenu)
        pdf.set_fill_color(*GREEN_MAIN)
        pdf.rect(pdf.l_margin, 18, 24, 10, style="F")
        pdf.set_xy(pdf.l_margin, 18)
        pdf.set_font("Arial", "B", 9)
        pdf.set_text_color(*WHITE)
        pdf.cell(24, 10, f"DOC {doc_info['num']}", align="C")
        pdf.set_text_color(*BLACK)
        pdf.set_y(32)
        MarkdownToPDF(pdf).render_file(src)

    # Retour sur la page sommaire pour inserer les numeros de pages reels
    # + definir les destinations des liens
    for doc in DOCUMENTS:
        num = doc['num']
        if num in doc_start_pages and num in link_ids:
            pdf.set_link(link_ids[num], page=doc_start_pages[num])

    active_page = pdf.page_no()
    pdf.page = sommaire_page
    for doc in DOCUMENTS:
        num = doc['num']
        if num not in sommaire_ypos or num not in doc_start_pages:
            continue
        y  = sommaire_ypos[num]
        pg = doc_start_pages[num]
        # Ligne de points (leaders) - apres badge(20) + espace(3) + titre
        pdf.set_font("Arial", "B", 13)
        title_w = pdf.get_string_width(f"   {doc['title']}")
        x_dots  = pdf.l_margin + 20 + 3 + title_w
        x_end   = pdf.l_margin + w - 16
        if x_end > x_dots + 3:
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(*GREY_LINE)
            dot_w  = pdf.get_string_width(".")
            n_dots = max(0, int((x_end - x_dots) / dot_w) - 1)
            pdf.set_xy(x_dots, y + 2)
            pdf.cell(x_end - x_dots, 7, "." * n_dots)
        # Numero de page
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(*GREEN_MAIN)
        pdf.set_xy(pdf.l_margin + w - 16, y)
        pdf.cell(16, 10, str(pg), align="R")
    pdf.page = active_page
    pdf.set_text_color(*BLACK)

    add_final_page(pdf)

    out = out_dir / "00_DOSSIER_COMPLET_PPE_FOOT5.pdf"
    pdf.output(str(out))
    return out


# =========================================================================
#  MAIN
# =========================================================================
if __name__ == "__main__":
    base = Path(__file__).parent
    src  = base / "PPE-DOCS.md"
    out  = base / "PPE-DOCS-PDF"
    out.mkdir(exist_ok=True)

    print("=" * 57)
    print("  Generation PDFs -- PPE Foot5  (style epure)")
    print("=" * 57)

    print("\nDocuments individuels :")
    for doc in DOCUMENTS:
        path = build_pdf_doc(doc, src, out)
        if path:
            size = path.stat().st_size // 1024
            print(f"  [OK] {doc['out']}  ({size} Ko)")

    print("\nDossier complet :")
    path = build_complete_pdf(src, out)
    if path:
        size = path.stat().st_size // 1024
        print(f"  [OK] {path.name}  ({size} Ko)")

    print("\n" + "=" * 57)
    print(f"  PDFs generes dans : {out.resolve()}")
    for f in sorted(out.glob("*.pdf")):
        print(f"    {f.name:<48}  {f.stat().st_size // 1024:>4} Ko")
    print("=" * 57)
