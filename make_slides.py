from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DARK_BG   = RGBColor(0x1E, 0x1E, 0x2E)
ACCENT    = RGBColor(0x89, 0xB4, 0xFA)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRY = RGBColor(0xCC, 0xCC, 0xDD)
GREEN     = RGBColor(0xA6, 0xE3, 0xA1)
YELLOW    = RGBColor(0xF9, 0xE2, 0xAF)
ORANGE    = RGBColor(0xFA, 0xB3, 0x87)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def bg(slide):
    s = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    s.fill.solid(); s.fill.fore_color.rgb = DARK_BG; s.line.fill.background()

def txt(slide, text, l, t, w, h, size=18, bold=False, colour=WHITE, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p  = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size = Pt(size); run.font.bold = bold; run.font.color.rgb = colour

def bar(slide, t=1.05):
    b = slide.shapes.add_shape(1, Inches(0.5), Inches(t), Inches(12.33), Inches(0.06))
    b.fill.solid(); b.fill.fore_color.rgb = ACCENT; b.line.fill.background()

def bullets(slide, items, l, t, size=16, colour=WHITE, gap=0.40):
    for i, item in enumerate(items):
        txt(slide, f"• {item}", l, t + i*gap, 12.3, 0.5, size=size, colour=colour)

def pill(slide, label, l, t, colour=ACCENT):
    box = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(2.4), Inches(0.52))
    box.fill.solid(); box.fill.fore_color.rgb = colour; box.line.fill.background()
    tb = box.text_frame; p = tb.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = label
    run.font.size = Pt(13); run.font.bold = True; run.font.color.rgb = DARK_BG

# ── SLIDE 1 — Title ──────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Explainable Failure Analysis in Time-Series Data",
    0.5, 1.5, 12.3, 1.1, size=34, bold=True, align=PP_ALIGN.CENTER)
txt(s, "Using SHAP — Master's Thesis Progress Update",
    0.5, 2.75, 12.3, 0.7, size=22, colour=ACCENT, align=PP_ALIGN.CENTER)
bar(s, t=3.7)
txt(s, "Abdul Karim Nasir Siddiqui  ·  Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU)",
    0.5, 4.0, 12.3, 0.5, size=15, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)
txt(s, "Supervisor: Prof. Dr.-Ing. habil. Philipp Beckerle  ·  July 2026",
    0.5, 4.5, 12.3, 0.5, size=15, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)

# ── SLIDE 2 — Thesis Overview ────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Thesis Overview", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Core Research Question", 0.5, 1.25, 12, 0.45, size=18, bold=True, colour=YELLOW)
txt(s, "Which sensor, at which exact timestep, caused the model to predict a robot failure?",
    0.5, 1.75, 12.3, 0.7, size=17, colour=WHITE)
txt(s, "Three SHAP Methods Compared", 0.5, 2.65, 12, 0.45, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "KernelSHAP  —  classical SHAP baseline  (Lundberg & Lee, NeurIPS 2017)",
    "TimeSHAP    —  extends KernelSHAP to recurrent models  (Bento et al., KDD 2021)",
    "WinIT       —  window-based temporal attribution, state of the art  (Leung et al., ICLR 2023)",
], 0.5, 3.15, size=16, gap=0.42)
txt(s, "Two Stages of Analysis", 0.5, 4.55, 12, 0.45, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "Stage 1 — CMAPSS (benchmark):  1 failure mode, binary label → validate SHAP methods on known data",
    "Stage 2 — Real robot data:  3 failure modes, multi-class → validate supervisor's failure mode design",
], 0.5, 5.0, size=15, gap=0.42)

# ── SLIDE 3 — 2-Week Progress ────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Progress — Last 2 Weeks", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Completed", 0.5, 1.15, 3, 0.4, size=17, bold=True, colour=GREEN)
bullets(s, [
    "GitHub repository set up — full project structure, CI, issue templates, supervisor guide",
    "Milestone timeline defined: July → December 2026",
    "NASA CMAPSS dataset acquired and loaded (FD001 — 100 engines, 15 active sensors)",
    "CMAPSSLoader — RUL computation, failure labels (threshold 30), constant sensor removal",
    "TimeSeriesPreprocessor — MinMax normalisation, sliding window (30 cycles, step 1)",
    "Notebook 03 — 8-section EDA: lifetimes, RUL curves, failure zone, heatmap, sensor trends",
    "MLP classifier trained — 99% accuracy, 75%+ recall on failure class",
    "KernelSHAP run — sensor importance, temporal importance, heatmap, single prediction explained",
], 0.5, 1.55, size=15, gap=0.36)

# ── SLIDE 4 — Numbers ────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Key Numbers", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

stats = [
    ("17,731", "training windows"),
    ("10,196", "test windows"),
    ("15",     "active sensors"),
    ("30",     "window size (cycles)"),
    ("82 / 18", "normal / failure split (%)"),
    ("99%",    "overall model accuracy"),
    ("75%+",   "failure class recall"),
    ("50",     "predictions explained by SHAP"),
]
for i, (val, label) in enumerate(stats):
    col = i % 4
    row = i // 4
    lx = 0.4 + col * 3.2
    ty = 1.5 + row * 2.2
    box = s.shapes.add_shape(1, Inches(lx), Inches(ty), Inches(3.0), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E)
    box.line.fill.background()
    txt(s, val,   lx+0.15, ty+0.15, 2.7, 0.8, size=28, bold=True, colour=ACCENT, align=PP_ALIGN.CENTER)
    txt(s, label, lx+0.1,  ty+0.85, 2.8, 0.5, size=13, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)

# ── SLIDE 5 — CMAPSS Dataset ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "NASA CMAPSS — Dataset Overview", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "What is it?", 0.5, 1.2, 6, 0.4, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "NASA simulation of jet turbofan engines degrading until failure",
    "100 engines run cycle-by-cycle, sensors recorded at every step",
    "Failure mode: High Pressure Compressor (HPC) degradation",
    "Ground truth RUL provided — used to create binary failure label",
    "Standard benchmark — used in every predictive maintenance paper",
], 0.5, 1.65, size=15, gap=0.40)
txt(s, "Key numbers", 7.2, 1.2, 5.5, 0.4, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "Subset       :  FD001",
    "Engines      :  100",
    "Total sensors:  21  →  15 after cleaning",
    "Window size  :  30 cycles",
    "Threshold    :  RUL ≤ 30  =  failure",
    "Final X shape:  (n, 30, 15)",
], 7.2, 1.65, size=15, colour=ACCENT, gap=0.40)
txt(s, "Important limitation: CMAPSS has only ONE failure mode (HPC degradation) — binary label only (failure / normal).",
    0.5, 5.2, 12.3, 0.5, size=14, colour=ORANGE)
txt(s, "Role in thesis: methods validation benchmark only. Real multi-class failure analysis happens on robot data.",
    0.5, 5.65, 12.3, 0.5, size=14, colour=LIGHT_GRY)

# ── SLIDE 6 — Pipeline ───────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Implemented Pipeline", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
steps = [
    ("1  Raw Data",    "train_FD001.txt  /  robot SQL  /  ROS2 bags",                          ACCENT, True),
    ("2  Load & Label","CMAPSSLoader — RUL → binary label (threshold 30)",                      ACCENT, True),
    ("3  Clean",       "Drop 6 constant sensors  →  15 active sensors",                         ACCENT, True),
    ("4  Normalise",   "MinMaxScaler fitted on train, applied to test",                          ACCENT, True),
    ("5  Window",      "Sliding window 30 cycles, step 1  →  X (n, 30, 15)",                    ACCENT, True),
    ("6  Model",       "MLP trained — 99% accuracy, 75%+ recall on failure class  ✓",           GREEN,  True),
    ("7  SHAP",        "KernelSHAP done ✓   TimeSHAP + WinIT next",                            GREEN,  True),
]
for i, (title, desc, col, done) in enumerate(steps):
    t = 1.25 + i * 0.72
    pill(s, title, 0.4, t, colour=col)
    txt(s, desc, 3.05, t+0.06, 9.9, 0.5, size=14, colour=WHITE if done else LIGHT_GRY)

# ── SLIDE 7 — What is SHAP ───────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "What is SHAP?", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "The Core Idea", 0.5, 1.2, 12, 0.4, size=18, bold=True, colour=YELLOW)
txt(s, "SHAP assigns every input feature a score: how much did this feature push the prediction toward failure?",
    0.5, 1.65, 12.3, 0.6, size=16, colour=WHITE)
txt(s, "Three Methods — Each Handles Time Differently", 0.5, 2.5, 12, 0.4, size=18, bold=True, colour=YELLOW)

methods = [
    ("KernelSHAP", "Treats each (sensor, timestep) cell independently.\nIgnores the fact that data is a sequence.\nBaseline — Lundberg & Lee, NeurIPS 2017"),
    ("TimeSHAP",   "Extends KernelSHAP to recurrent models.\nUses pruning to focus on the most recent timesteps.\nBento et al., KDD 2021"),
    ("WinIT",      "Masks whole windows of timesteps and measures prediction change.\nState of the art for temporal attribution.\nLeung et al., ICLR 2023"),
]
for i, (name, desc) in enumerate(methods):
    lx = 0.4 + i * 4.3
    box = s.shapes.add_shape(1, Inches(lx), Inches(3.1), Inches(4.0), Inches(2.8))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); box.line.fill.background()
    txt(s, name, lx+0.15, 3.15, 3.7, 0.5, size=16, bold=True, colour=ACCENT)
    txt(s, desc, lx+0.15, 3.65, 3.7, 2.0, size=13, colour=WHITE)

txt(s, "We run all three on the same dataset and compare: faithfulness, stability, compute time.",
    0.5, 6.2, 12.3, 0.5, size=14, colour=LIGHT_GRY)

# ── SLIDE 8 — KernelSHAP Results ─────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "KernelSHAP Results — CMAPSS FD001", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Model", 0.5, 1.2, 3, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "MLP  (450 inputs → 128 → 64 → 2 outputs)",
    "17,731 training windows  ·  10,196 test",
    "99% overall accuracy",
    "75%+ recall on failure class",
], 0.5, 1.62, size=14, gap=0.36)

txt(s, "What SHAP Found", 4.8, 1.2, 4, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "Top sensors: T30, Ps30, NRc",
    "These are HPC degradation signatures",
    "Last 5–10 of 30 timesteps matter most",
    "Physically consistent with fault mode",
], 4.8, 1.62, size=14, gap=0.36)

txt(s, "4 Plots Produced", 9.0, 1.2, 4, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "Bar chart — sensor ranking",
    "Line chart — temporal importance",
    "Heatmap — sensor × timestep",
    "Single prediction explained",
], 9.0, 1.62, size=14, colour=ACCENT, gap=0.36)

txt(s, "What This Means", 0.5, 3.5, 12, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "The model is not a black box anymore — we can see exactly which sensor at which moment triggered the failure alert",
    "T30 (HPC outlet temperature) rising in the last 8 cycles is the strongest signal — physically this makes sense",
    "This is the baseline. TimeSHAP and WinIT will give different timestep attributions — that difference is the thesis contribution",
    "Same pipeline will run on real robot data to validate the supervisor's designed failure modes",
], 0.5, 3.95, size=15, gap=0.42)

# ── SLIDE 9 — MLP vs LSTM ────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "MLP vs LSTM — Why the Model Choice Matters for SHAP", 0.5, 0.3, 12.3, 0.7, size=26, bold=True, colour=ACCENT)
bar(s)

# MLP box
mlp_box = s.shapes.add_shape(1, Inches(0.4), Inches(1.15), Inches(5.9), Inches(4.8))
mlp_box.fill.solid(); mlp_box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); mlp_box.line.fill.background()
txt(s, "MLP  (Notebook 04 — Baseline)", 0.6, 1.2, 5.5, 0.5, size=16, bold=True, colour=YELLOW)
bullets(s, [
    "Input: (n, 450) — sequence flattened into one vector",
    "Each (sensor, timestep) cell treated independently",
    "No memory — timestep 1 and timestep 30 equally weighted",
    "SHAP: importance per flattened cell, no temporal ordering",
    "Accuracy: 99%  ·  Failure recall: 75%+",
], 0.6, 1.72, size=13, gap=0.38)
txt(s, "Limitation", 0.6, 3.65, 5.4, 0.35, size=14, bold=True, colour=ORANGE)
txt(s, "MLP does not know time exists. It sees 450 independent\nfeatures, not a 30-step sequence. SHAP values may\nhighlight artifacts of flattening, not real temporal patterns.",
    0.6, 4.0, 5.4, 0.9, size=12, colour=LIGHT_GRY)

# arrow
txt(s, "→", 6.45, 3.2, 0.5, 0.6, size=28, bold=True, colour=ACCENT, align=PP_ALIGN.CENTER)

# LSTM box
lstm_box = s.shapes.add_shape(1, Inches(7.0), Inches(1.15), Inches(5.9), Inches(4.8))
lstm_box.fill.solid(); lstm_box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); lstm_box.line.fill.background()
txt(s, "LSTM  (Notebook 05 — Current)", 7.2, 1.2, 5.5, 0.5, size=16, bold=True, colour=GREEN)
bullets(s, [
    "Input: (n, 30, 15) — sequence preserved",
    "Hidden state carries information across timesteps",
    "Model learns which earlier cycles matter for prediction",
    "KernelSHAP explains both — but predictions differ",
    "LSTM predictions already encode temporal patterns",
    "Better suited for: failure detection in sequences",
], 7.2, 1.72, size=13, gap=0.38)
txt(s, "Advantage", 7.2, 3.65, 5.4, 0.35, size=14, bold=True, colour=GREEN)
txt(s, "Both use KernelSHAP on flat (450,) input.\nLSTM's hidden state already learned temporal trends,\nso its predictions — and SHAP attributions — reflect sequence.\nMLP has no such memory.",
    7.2, 4.0, 5.4, 0.9, size=12, colour=LIGHT_GRY)

txt(s, "Key Question: do MLP and LSTM SHAP values agree on the top sensors?  If yes → signal is robust.  If no → model architecture changes the explanation.",
    0.5, 6.2, 12.3, 0.5, size=13, colour=ORANGE)

# ── SLIDE 10 — SHAP Results Comparison: MLP vs LSTM ─────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "SHAP Results — MLP vs LSTM (KernelSHAP, CMAPSS FD001)", 0.5, 0.3, 12.3, 0.7, size=26, bold=True, colour=ACCENT)
bar(s)

# MLP column
mlp_box = s.shapes.add_shape(1, Inches(0.4), Inches(1.15), Inches(5.9), Inches(3.6))
mlp_box.fill.solid(); mlp_box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); mlp_box.line.fill.background()
txt(s, "MLP — Top Sensors (Notebook 04)", 0.6, 1.2, 5.5, 0.45, size=15, bold=True, colour=YELLOW)

mlp_sensors = [
    ("#1  sensor_11", "Ps30  — Static pressure HPC outlet"),
    ("#2  sensor_9 ", "Nc    — Physical core speed"),
    ("#3  sensor_12", "phi   — Fuel flow / Ps30 ratio"),
    ("#4  sensor_4 ", "T50   — Temperature at LPT outlet"),
    ("#5  sensor_2 ", "T24   — Temperature at LPC outlet"),
]
for i, (rank, name) in enumerate(mlp_sensors):
    ty = 1.72 + i * 0.46
    txt(s, rank, 0.6,  ty, 2.2, 0.4, size=13, bold=True, colour=ACCENT)
    txt(s, name, 2.85, ty, 3.3, 0.4, size=13, colour=WHITE)

# LSTM column
lstm_box = s.shapes.add_shape(1, Inches(7.0), Inches(1.15), Inches(5.9), Inches(3.6))
lstm_box.fill.solid(); lstm_box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); lstm_box.line.fill.background()
txt(s, "LSTM — Top Sensors (Notebook 05)", 7.2, 1.2, 5.5, 0.45, size=15, bold=True, colour=GREEN)

lstm_sensors = [
    ("#1  sensor_13", "NRf   — Corrected fan speed     ← NEW"),
    ("#2  sensor_11", "Ps30  — Static pressure HPC outlet"),
    ("#3  sensor_12", "phi   — Fuel flow / Ps30 ratio"),
    ("#4  sensor_2 ", "T24   — Temperature at LPC outlet"),
    ("#5  sensor_7 ", "P30   — Total pressure HPC outlet ← NEW"),
]
for i, (rank, name) in enumerate(lstm_sensors):
    ty = 1.72 + i * 0.46
    is_new = "← NEW" in name
    txt(s, rank, 7.2,  ty, 2.2, 0.4, size=13, bold=True, colour=GREEN if is_new else ACCENT)
    txt(s, name, 9.45, ty, 3.3, 0.4, size=13, colour=GREEN if is_new else WHITE)

# Agreement / difference section
txt(s, "What This Tells Us", 0.5, 4.95, 12, 0.4, size=17, bold=True, colour=YELLOW)

agree_box = s.shapes.add_shape(1, Inches(0.4), Inches(5.4), Inches(5.9), Inches(1.7))
agree_box.fill.solid(); agree_box.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x1A); agree_box.line.fill.background()
txt(s, "Both agree on:", 0.6, 5.45, 5.5, 0.35, size=13, bold=True, colour=GREEN)
bullets(s, [
    "Ps30 (sensor_11) + phi (sensor_12) — strong HPC degradation signal",
    "Consistent across architectures → physically real signal",
], 0.6, 5.82, size=12, colour=WHITE, gap=0.38)

diff_box = s.shapes.add_shape(1, Inches(7.0), Inches(5.4), Inches(5.9), Inches(1.7))
diff_box.fill.solid(); diff_box.fill.fore_color.rgb = RGBColor(0x3A, 0x2A, 0x1A); diff_box.line.fill.background()
txt(s, "LSTM sees differently:", 7.2, 5.45, 5.5, 0.35, size=13, bold=True, colour=ORANGE)
bullets(s, [
    "NRf (corrected fan speed) rises to #1 — only visible as a trend over 30 cycles",
    "Nc (core speed) drops out — LSTM prefers corrected over raw speed",
], 7.2, 5.82, size=12, colour=WHITE, gap=0.38)

txt(s, "Finding: model architecture changes SHAP rankings — validating the need to compare MLP and LSTM attributions.",
    0.5, 7.15, 12.3, 0.35, size=12, colour=LIGHT_GRY)

# ── SLIDE 11 — TimeSHAP ──────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "TimeSHAP — Sequence-Aware SHAP on LSTM", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

# Problem with KernelSHAP
kbox = s.shapes.add_shape(1, Inches(0.4), Inches(1.15), Inches(5.9), Inches(2.5))
kbox.fill.solid(); kbox.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); kbox.line.fill.background()
txt(s, "Problem with KernelSHAP on LSTM", 0.6, 1.2, 5.6, 0.45, size=15, bold=True, colour=ORANGE)
bullets(s, [
    "KernelSHAP flattens (30, 15) → 450 features",
    "Loses all temporal structure before explaining",
    "SHAP sees 450 independent numbers, not a sequence",
    "Cannot detect trends that span multiple timesteps",
], 0.6, 1.68, size=13, colour=WHITE, gap=0.38)

txt(s, "→", 6.45, 2.2, 0.5, 0.6, size=28, bold=True, colour=ACCENT, align=PP_ALIGN.CENTER)

# TimeSHAP solution
tbox = s.shapes.add_shape(1, Inches(7.0), Inches(1.15), Inches(5.9), Inches(2.5))
tbox.fill.solid(); tbox.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); tbox.line.fill.background()
txt(s, "How TimeSHAP Fixes This", 7.2, 1.2, 5.6, 0.45, size=15, bold=True, colour=GREEN)
bullets(s, [
    "Keeps input as (30, 15) — sequence never flattened",
    "Runs backwards from last timestep (most recent first)",
    "Pruning: stops when earlier timesteps stop contributing",
    "Gives importance per timestep AND per sensor separately",
], 7.2, 1.68, size=13, colour=WHITE, gap=0.38)

# 3-step flow
txt(s, "How TimeSHAP Works — 3 Steps", 0.5, 3.85, 12, 0.4, size=17, bold=True, colour=YELLOW)
steps_ts = [
    ("Step 1\nPruning", "Starts at timestep 30, works backwards.\nStops when removing older timesteps\nno longer changes the prediction.", ACCENT),
    ("Step 2\nEvent SHAP", "Assigns a SHAP score to each timestep.\nAnswers: which of the 30 cycles\nmattered most for this prediction?", GREEN),
    ("Step 3\nFeature SHAP", "Assigns a SHAP score to each sensor.\nAnswers: which of the 15 sensors\ndrove the prediction?", YELLOW),
]
for i, (title, desc, col) in enumerate(steps_ts):
    bx = 0.4 + i * 4.3
    box = s.shapes.add_shape(1, Inches(bx), Inches(4.35), Inches(4.0), Inches(2.4))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); box.line.fill.background()
    txt(s, title, bx+0.15, 4.4,  3.7, 0.55, size=14, bold=True, colour=col, align=PP_ALIGN.CENTER)
    txt(s, desc,  bx+0.15, 4.98, 3.7, 1.6,  size=12, colour=WHITE)

txt(s, "Paper: Bento et al. (KDD 2021) — arxiv.org/abs/2012.00073  |  Notebook: 06_timeshap.ipynb",
    0.5, 7.1, 12.3, 0.35, size=11, colour=LIGHT_GRY)

# ── SLIDE 12 — KernelSHAP vs TimeSHAP Results ───────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "KernelSHAP vs TimeSHAP — Sensor Rankings Compared", 0.5, 0.3, 12.3, 0.7, size=26, bold=True, colour=ACCENT)
bar(s)

# KernelSHAP column
kb = s.shapes.add_shape(1, Inches(0.4), Inches(1.15), Inches(5.9), Inches(3.4))
kb.fill.solid(); kb.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); kb.line.fill.background()
txt(s, "KernelSHAP — Top 5 Sensors", 0.6, 1.2, 5.5, 0.45, size=15, bold=True, colour=YELLOW)
ks = [("#1  sensor_13", "NRf   — Corrected fan speed"),
      ("#2  sensor_11", "Ps30  — Static pressure HPC outlet"),
      ("#3  sensor_12", "phi   — Fuel flow / Ps30 ratio"),
      ("#4  sensor_2 ", "T24   — Temperature LPC outlet"),
      ("#5  sensor_7 ", "P30   — Total pressure HPC outlet"),]
for i, (r, n) in enumerate(ks):
    ty = 1.72 + i * 0.44
    txt(s, r, 0.6,  ty, 2.2, 0.38, size=13, bold=True, colour=ACCENT)
    txt(s, n, 2.85, ty, 3.3, 0.38, size=13, colour=WHITE)

# TimeSHAP column
tb = s.shapes.add_shape(1, Inches(7.0), Inches(1.15), Inches(5.9), Inches(3.4))
tb.fill.solid(); tb.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); tb.line.fill.background()
txt(s, "TimeSHAP — Top 5 Sensors", 7.2, 1.2, 5.5, 0.45, size=15, bold=True, colour=GREEN)
ts = [("#1  sensor_13", "NRf   — Corrected fan speed",        False),
      ("#2  sensor_20", "W31   — HPT coolant bleed   ← NEW",  True),
      ("#3  sensor_8 ", "Nf    — Physical fan speed  ← NEW",  True),
      ("#4  sensor_12", "phi   — Fuel flow / Ps30 ratio",     False),
      ("#5  sensor_11", "Ps30  — Static pressure HPC outlet", False),]
for i, (r, n, new) in enumerate(ts):
    ty = 1.72 + i * 0.44
    col = GREEN if new else ACCENT
    txt(s, r, 7.2,  ty, 2.2, 0.38, size=13, bold=True, colour=col)
    txt(s, n, 9.45, ty, 3.3, 0.38, size=13, colour=GREEN if new else WHITE)

# Agreement box
ab = s.shapes.add_shape(1, Inches(0.4), Inches(4.75), Inches(5.9), Inches(1.85))
ab.fill.solid(); ab.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x1A); ab.line.fill.background()
txt(s, "Both agree on (3/5 sensors):", 0.6, 4.82, 5.5, 0.38, size=14, bold=True, colour=GREEN)
bullets(s, [
    "sensor_13 (NRf)  — top sensor in both methods",
    "sensor_11 (Ps30) — HPC pressure, consistent",
    "sensor_12 (phi)  — fuel-pressure ratio, consistent",
], 0.6, 5.22, size=12, colour=WHITE, gap=0.35)

# Difference box
db = s.shapes.add_shape(1, Inches(7.0), Inches(4.75), Inches(5.9), Inches(1.85))
db.fill.solid(); db.fill.fore_color.rgb = RGBColor(0x3A, 0x2A, 0x1A); db.line.fill.background()
txt(s, "TimeSHAP sees differently:", 7.2, 4.82, 5.5, 0.38, size=14, bold=True, colour=ORANGE)
bullets(s, [
    "W31 (HPT coolant bleed) — temporal trend hidden from KernelSHAP",
    "Nf (fan speed) surfaces — sequence-aware attribution finds it",
    "T24 and P30 drop out — less important when time is respected",
], 7.2, 5.22, size=12, colour=WHITE, gap=0.35)

txt(s, "Finding: 3/5 sensors agree → HPC pressure/speed signal is robust. 2 new sensors from TimeSHAP → temporal context reveals additional failure signatures.",
    0.5, 6.78, 12.3, 0.4, size=12, colour=ORANGE)

# ── SLIDE 13 — Federated Learning ─────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Federated Learning — 3 Real Robots, Not Simulation", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Setup: 3 physical lab robots, each with the same 3 failure modes physically implemented by the supervisor.",
    0.5, 1.15, 12.3, 0.45, size=15, colour=WHITE)

# Flow diagram — 3 robots → local train → local SHAP → server
flow = [
    ("Robot 1", "trains locally\nruns SHAP locally"),
    ("Robot 2", "trains locally\nruns SHAP locally"),
    ("Robot 3", "trains locally\nruns SHAP locally"),
]
for i, (name, sub) in enumerate(flow):
    bx = 0.5 + i * 4.1
    box = s.shapes.add_shape(1, Inches(bx), Inches(1.75), Inches(3.5), Inches(1.1))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); box.line.fill.background()
    txt(s, name, bx+0.1, 1.8, 3.3, 0.4, size=15, bold=True, colour=ACCENT, align=PP_ALIGN.CENTER)
    txt(s, sub,  bx+0.1, 2.2, 3.3, 0.55, size=12, colour=WHITE, align=PP_ALIGN.CENTER)
    txt(s, "↓ SHAP values only\n(no raw data)", bx+0.9, 2.9, 2.0, 0.55, size=11, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)

box = s.shapes.add_shape(1, Inches(4.4), Inches(3.65), Inches(4.5), Inches(0.75))
box.fill.solid(); box.fill.fore_color.rgb = GREEN; box.line.fill.background()
txt(s, "Central Server — aggregates SHAP values from all 3 robots", 4.55, 3.72, 4.2, 0.6, size=13, bold=True, colour=DARK_BG, align=PP_ALIGN.CENTER)

txt(s, "What the Server Checks", 0.5, 4.6, 12, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "Do all 3 robots agree on which sensors cause failure mode 1? mode 2? mode 3?",
    "Are the temporal patterns (which timesteps matter) consistent across robots?",
    "If YES → failure modes are physically consistent and correctly designed across all 3 robots",
    "If NO → disagreement reveals hardware variation, sensor placement differences, or inconsistent failure implementation",
], 0.5, 5.05, size=15, gap=0.38)

txt(s, "Why this is novel: federating SHAP explanations (not just model weights) as a cross-robot design validation tool.",
    0.5, 6.75, 12.3, 0.4, size=13, colour=ORANGE)
txt(s, "McMahan et al. (2017) — Communication-Efficient Learning of Deep Networks from Decentralized Data",
    0.5, 7.15, 12.3, 0.3, size=11, colour=LIGHT_GRY)

# ── SLIDE 10 — Benchmarks ────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Existing SHAP Benchmarks — Where We Stand", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "What Already Exists", 0.5, 1.2, 12, 0.4, size=18, bold=True, colour=YELLOW)

bench = [
    (
        "WinIT  —  Leung et al. (ICLR 2023)",
        "arxiv.org/abs/2210.01622",
        "WinIT vs TimeSHAP vs FIT vs LIME\non MIMIC-III (ICU) + synthetic data",
        "Medical / synthetic only — no industrial data"
    ),
    (
        "Theissler et al. (Neural Networks 2022)",
        "doi.org/10.1016/j.neunet.2022.06.041",
        "Survey of 30+ XAI methods across\nmultiple time-series classification tasks",
        "No robot or industrial sensor data"
    ),
    (
        "Ismail Fawaz et al. (DSS 2020)",
        "arxiv.org/abs/1905.04755",
        "Saliency / gradient methods on\nUCR archive (128 datasets)",
        "Not SHAP-specific — no temporal attribution"
    ),
]
for i, (paper, link, what, gap_) in enumerate(bench):
    lx = 0.4 + i * 4.3
    box = s.shapes.add_shape(1, Inches(lx), Inches(1.75), Inches(4.0), Inches(2.6))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); box.line.fill.background()
    txt(s, paper, lx+0.12, 1.82, 3.75, 0.55, size=13, bold=True, colour=ACCENT)
    txt(s, link,  lx+0.12, 2.38, 3.75, 0.35, size=11, colour=YELLOW)
    txt(s, what,  lx+0.12, 2.75, 3.75, 0.75, size=12, colour=WHITE)
    txt(s, f"Gap: {gap_}", lx+0.12, 3.52, 3.75, 0.45, size=11, colour=ORANGE)

txt(s, "The Gap — and Our Contribution", 0.5, 4.15, 12, 0.4, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "No existing benchmark uses real robot failure data with physically designed failure modes",
    "All benchmarks use medical or synthetic data — not industrial sensor data from hardware",
    "We replicate the WinIT benchmark setup and extend it to ASM robot data",
    "Key question: do TimeSHAP / WinIT rankings from medical data hold up on robot sensor data?",
    "If not → our contribution is showing SHAP method choice is domain-dependent",
], 0.5, 4.6, size=15, gap=0.38)

# ── SLIDE 9 — Real Robot Data ─────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Real Robot Data — ASM Lab Update", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Key Difference vs CMAPSS", 0.5, 1.2, 12, 0.4, size=18, bold=True, colour=YELLOW)
box_diff = s.shapes.add_shape(1, Inches(0.4), Inches(1.65), Inches(12.4), Inches(1.0))
box_diff.fill.solid(); box_diff.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x3E); box_diff.line.fill.background()
txt(s, "CMAPSS:  1 failure mode  →  binary label (normal / failure)", 0.7, 1.72, 5.8, 0.45, size=14, colour=ORANGE)
txt(s, "Robot data:  3 failure modes  →  multi-class (normal / mode 1 / mode 2 / mode 3)", 6.7, 1.72, 6.1, 0.45, size=14, colour=GREEN)
txt(s, "SHAP output shape changes: (n, features, 2)  →  (n, features, 4)  — one attribution set per class", 0.7, 2.2, 12.0, 0.35, size=12, colour=LIGHT_GRY)

txt(s, "Dataset Update from Supervisor", 0.5, 2.8, 12, 0.4, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "Supervisor collected robot failure dataset — February 2026",
    "3 failure modes physically designed and implemented on lab robot",
    "Data already exists — Milestone 3 potentially achieved ahead of schedule",
], 0.5, 3.25, size=16, gap=0.42)
txt(s, "How Multi-Class SHAP Validates the Design", 0.5, 4.6, 12, 0.4, size=18, bold=True, colour=YELLOW)
bullets(s, [
    "Train LSTM/GRU: 4-class output (normal + 3 failure modes)",
    "SHAP per class: which sensor at which timestep distinguishes mode 2 from mode 1?",
    "If SHAP highlights physically correct sensors for each mode → design is validated",
    "If SHAP highlights wrong sensors → failure modes are not separable in the sensor data",
], 0.5, 5.05, size=15, gap=0.38)
txt(s, "Next action: obtain database credentials / ROS2 bag files to start real data pipeline.",
    0.5, 6.9, 12.3, 0.4, size=13, colour=LIGHT_GRY)

# ── SLIDE 10 — Timeline ───────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Project Timeline", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
milestones = [
    ("M1 — July 2026",      "Literature review, repo setup, CMAPSS pipeline + KernelSHAP baseline", True),
    ("M2 — August 2026",    "SQL data processed, LSTM/GRU trained, TimeSHAP + WinIT implemented",   False),
    ("M3 — September 2026", "ROS2 / real robot data pipeline, all failure modes analysed",           False),
    ("M4 — October 2026",   "Full SHAP comparison complete, all figures generated",                  False),
    ("M5 — December 2026",  "Thesis written and submitted",                                          False),
]
for i, (title, desc, done) in enumerate(milestones):
    t = 1.35 + i * 1.0
    col = GREEN if done else LIGHT_GRY
    dot = s.shapes.add_shape(1, Inches(0.4), Inches(t+0.1), Inches(0.3), Inches(0.5))
    dot.fill.solid(); dot.fill.fore_color.rgb = col; dot.line.fill.background()
    txt(s, title, 0.9, t, 3.8, 0.4, size=16, bold=True, colour=col)
    txt(s, desc,  0.9, t+0.38, 11.5, 0.4, size=14, colour=WHITE)
txt(s, "Green = completed / in progress", 0.5, 6.55, 5, 0.4, size=12, colour=GREEN)

# ── SLIDE 11 — Next Steps ─────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Next Steps", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
bullets(s, [
    "Obtain access to ASM SQL database / ROS2 bag files from supervisor",
    "Implement LSTM and GRU classifiers — replace MLP baseline  (src/models/)",
    "Implement TimeSHAP wrapper and run on CMAPSS  (src/explainability/timeshap_explainer.py)",
    "Implement WinIT wrapper and run on CMAPSS  (src/explainability/winit_explainer.py)",
    "Compare all three SHAP methods: faithfulness, stability, compute time",
    "Apply full pipeline to real robot data — validate supervisor's failure mode design",
    "Discuss federated learning extension with supervisor",
], 0.5, 1.4, size=18, gap=0.62)

# ── Save ─────────────────────────────────────────────────────────────────────
out = r"MA_Siddiqui_Progress.pptx"
prs.save(out)
print(f"Saved: {out}")
