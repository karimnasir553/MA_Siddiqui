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
RED       = RGBColor(0xF3, 0x8B, 0xA8)

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
        txt(slide, f"\u2022  {item}", l, t + i*gap, 12.3, 0.5, size=size, colour=colour)

def pill(slide, label, l, t, w=2.4, colour=ACCENT):
    box = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(0.52))
    box.fill.solid(); box.fill.fore_color.rgb = colour; box.line.fill.background()
    tb = box.text_frame; p = tb.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = label
    run.font.size = Pt(13); run.font.bold = True; run.font.color.rgb = DARK_BG

def card(slide, lx, ty, w, h, fill=RGBColor(0x2A, 0x2A, 0x3E)):
    box = slide.shapes.add_shape(1, Inches(lx), Inches(ty), Inches(w), Inches(h))
    box.fill.solid(); box.fill.fore_color.rgb = fill; box.line.fill.background()
    return box

# ── SLIDE 1 — Title ────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Explainable Failure Analysis in Time-Series Data",
    0.5, 1.3, 12.3, 1.1, size=34, bold=True, align=PP_ALIGN.CENTER)
txt(s, "Using SHAP — Master's Thesis Progress Update",
    0.5, 2.6, 12.3, 0.7, size=22, colour=ACCENT, align=PP_ALIGN.CENTER)
bar(s, t=3.55)
txt(s, "Abdul Karim Nasir Siddiqui  \u00b7  Friedrich-Alexander-Universit\u00e4t Erlangen-N\u00fcrnberg (FAU)",
    0.5, 3.85, 12.3, 0.5, size=15, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)
txt(s, "Supervisor: Prof. Dr.-Ing. habil. Philipp Beckerle  \u00b7  September 2026",
    0.5, 4.35, 12.3, 0.5, size=15, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)

# ── SLIDE 2 — Thesis Overview ──────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Thesis Overview", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Research Question", 0.5, 1.2, 12, 0.4, size=18, bold=True, colour=YELLOW)
txt(s, "Which sensor, at which exact timestep, caused the model to predict a robot failure — and does the method choice change the answer?",
    0.5, 1.65, 12.3, 0.55, size=16, colour=WHITE)

txt(s, "Three SHAP Methods Compared", 0.5, 2.45, 12, 0.4, size=18, bold=True, colour=YELLOW)
methods = [
    ("KernelSHAP", "Baseline — flattens sequence\ninto independent features.\nLundberg & Lee, NeurIPS 2017"),
    ("TimeSHAP",   "Keeps sequence structure.\nPrunes irrelevant timesteps.\nBento et al., KDD 2021"),
    ("WinIT",      "Masks windows of timesteps.\nMeasures prediction change directly.\nLeung et al., ICLR 2023"),
]
for i, (name, desc) in enumerate(methods):
    lx = 0.4 + i * 4.3
    card(s, lx, 3.0, 4.0, 2.2)
    txt(s, name, lx+0.15, 3.07, 3.7, 0.48, size=16, bold=True, colour=ACCENT)
    txt(s, desc, lx+0.15, 3.58, 3.7, 1.5,  size=13, colour=WHITE)

txt(s, "Two Stages", 0.5, 5.45, 12, 0.4, size=18, bold=True, colour=YELLOW)
card(s, 0.4, 5.9, 5.9, 0.95)
txt(s, "Stage 1 — NASA CMAPSS (benchmark)", 0.6, 5.95, 5.5, 0.35, size=14, bold=True, colour=ORANGE)
txt(s, "1 failure mode, binary label, 15 sensors  \u2192  validate methods on known data", 0.6, 6.3, 5.5, 0.35, size=13, colour=WHITE)
card(s, 6.95, 5.9, 5.9, 0.95)
txt(s, "Stage 2 — Real Robot Data (ASM lab)", 7.15, 5.95, 5.5, 0.35, size=14, bold=True, colour=GREEN)
txt(s, "3 failure modes, 4-class label, 62 sensors  \u2192  validate failure mode design", 7.15, 6.3, 5.5, 0.35, size=13, colour=WHITE)

# ── SLIDE 3 — Progress Since Last Meeting ─────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Progress Since Last Meeting", 0.5, 0.3, 12, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

done = [
    "CMAPSS pipeline complete: load, clean, window, MLP + LSTM + KernelSHAP + TimeSHAP",
    "Robot data loaded: 81,450 rows \u00d7 62 active sensors, 4-class labels (diagnostic model.xlsx)",
    "Solved class imbalance: Normal 39 k vs Failure-2 only 4.8 k \u2192 inverse-frequency class weights in CrossEntropyLoss",
    "LSTM trained on robot data: 128 hidden, 2 layers, 40 epochs, temporal 80/20 split",
    "KernelSHAP run on robot data: flatten (30,62)\u21921860, l1_reg=0 (OLS), 4 classes explained",
    "WinIT implemented from scratch (no pip package): suffix-masking + finite-difference attribution",
    "Notebook 08 ready to run: WinIT temporal + feature importance + heatmap per failure class",
]
in_prog = [
    "Re-run LSTM on robot data with class weights (kernel was restarted after code update)",
    "Run WinIT on robot data and compare top sensors vs KernelSHAP per failure class",
    "Identify failure mode semantics (Class 1 meaning unclear \u2014 to confirm with supervisor)",
]

txt(s, "Completed", 0.5, 1.18, 5, 0.38, size=16, bold=True, colour=GREEN)
for i, item in enumerate(done):
    txt(s, f"\u2713  {item}", 0.5, 1.58 + i*0.36, 12.3, 0.35, size=12, colour=WHITE)

txt(s, "In Progress", 0.5, 4.2, 5, 0.38, size=16, bold=True, colour=YELLOW)
for i, item in enumerate(in_prog):
    txt(s, f"\u25cb  {item}", 0.5, 4.6 + i*0.38, 12.3, 0.35, size=13, colour=YELLOW)

# ── SLIDE 4 — CMAPSS Stage Done ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Stage 1 Complete — CMAPSS Benchmark", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

card(s, 0.4, 1.15, 5.9, 2.45)
txt(s, "Dataset", 0.6, 1.22, 5.5, 0.38, size=15, bold=True, colour=YELLOW)
bullets(s, [
    "NASA FD001: 100 jet engines, 21 sensors \u2192 15 active",
    "Window: 30 cycles, step 1 \u2192 17,731 train / 10,196 test",
    "Label: RUL \u2264 30 = failure (binary)",
    "Single failure mode: HPC degradation",
], 0.6, 1.62, size=13, gap=0.36)

card(s, 6.95, 1.15, 5.9, 2.45)
txt(s, "Models + SHAP", 7.15, 1.22, 5.5, 0.38, size=15, bold=True, colour=YELLOW)
bullets(s, [
    "MLP (450\u2192128\u219264\u21922): 99% acc, 75%+ failure recall",
    "LSTM (30,15): sequence-aware predictions",
    "KernelSHAP: top sensors Ps30, NRf, phi",
    "TimeSHAP: W31 + Nf surface as temporal trends visible",
], 7.15, 1.62, size=13, gap=0.36)

txt(s, "Key Finding — Method Comparison", 0.5, 3.8, 12, 0.4, size=17, bold=True, colour=YELLOW)
card(s, 0.4, 4.25, 5.9, 1.65, fill=RGBColor(0x1A, 0x3A, 0x1A))
txt(s, "KernelSHAP vs TimeSHAP — 3/5 sensors agree:", 0.6, 4.32, 5.5, 0.38, size=14, bold=True, colour=GREEN)
bullets(s, [
    "NRf (sensor_13), Ps30 (sensor_11), phi (sensor_12)",
    "Consistent signal \u2192 physically real HPC degradation",
], 0.6, 4.72, size=12, colour=WHITE, gap=0.36)

card(s, 6.95, 4.25, 5.9, 1.65, fill=RGBColor(0x3A, 0x2A, 0x1A))
txt(s, "TimeSHAP sees additionally:", 7.15, 4.32, 5.5, 0.38, size=14, bold=True, colour=ORANGE)
bullets(s, [
    "W31 (HPT coolant bleed) + Nf (fan speed)",
    "Only visible as trends over 30 cycles \u2192 temporal context matters",
], 7.15, 4.72, size=12, colour=WHITE, gap=0.36)

txt(s, "Conclusion: method choice changes 2/5 top sensors even on the same data \u2192 WinIT on robot data will be the decisive comparison.",
    0.5, 6.1, 12.3, 0.5, size=13, colour=ORANGE)

# ── SLIDE 5 — Robot Data Overview ─────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Stage 2 — Robot Data Overview", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

stats = [
    ("81,450", "total rows"),
    ("62",     "active sensors"),
    ("30",     "window size"),
    ("4",      "classes (1 normal + 3 failure)"),
    ("39,240", "Normal rows (48%)"),
    ("33,597", "Failure-1 rows (41%)"),
    ("4,783",  "Failure-2 rows (6%)"),
    ("3,830",  "Failure-3 rows (5%)"),
]
for i, (val, label) in enumerate(stats):
    col_ = i % 4
    row_ = i // 4
    lx = 0.4 + col_ * 3.2
    ty = 1.25 + row_ * 2.05
    card(s, lx, ty, 3.0, 1.75)
    c = ORANGE if i >= 4 and i < 6 else (RED if i >= 6 else ACCENT)
    txt(s, val,   lx+0.15, ty+0.12, 2.7, 0.75, size=26, bold=True, colour=c, align=PP_ALIGN.CENTER)
    txt(s, label, lx+0.1,  ty+0.85, 2.8, 0.6,  size=12, colour=LIGHT_GRY, align=PP_ALIGN.CENTER)

txt(s, "Source: diagnostic model.xlsx (single file with sensor readings + Outcome labels, no missing values)",
    0.5, 5.55, 12.3, 0.4, size=13, colour=LIGHT_GRY)
txt(s, "Challenge: severe class imbalance \u2014 Normal + Failure-1 dominate (89%), Failure-2 and Failure-3 rare (11%)",
    0.5, 5.95, 12.3, 0.4, size=14, colour=ORANGE)
txt(s, "Fix: inverse-frequency class weights in CrossEntropyLoss \u2014 model forced to learn all 4 classes equally",
    0.5, 6.4, 12.3, 0.4, size=14, colour=GREEN)

# ── SLIDE 6 — Failure Mode Identification ─────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Failure Mode Identification from Sensor Data", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "No documentation in data file \u2014 failure mode semantics inferred from per-class sensor means",
    0.5, 1.15, 12.3, 0.38, size=14, colour=LIGHT_GRY)

classes = [
    ("Class 0 — Normal", "V=15.2V  Cap=90%+  Temp=30\u00b0C\nvel_L=2.1  vel_R=2.1  (balanced, normal speed)", "Healthy operation baseline", ACCENT, False),
    ("Class 1 — Failure-1", "V=15.1V  Cap=64%  Temp=32\u00b0C\nvel_L=2.0  vel_R=2.1  (still normal speed)", "Battery partially discharged?\nMeaning unclear \u2014 to confirm with supervisor", YELLOW, True),
    ("Class 2 — Failure-2", "V=14.8V  Cap=52%  Temp=35\u00b0C\nvel_L=4.1  vel_R=4.2  (2\u00d7 higher speed!)", "Motor / wheel anomaly\nHigh wheel speed distinguishes this class", ORANGE, False),
    ("Class 3 — Failure-3", "V=13.8V  Cap=7%   Temp=40\u00b0C\nvel_L=1.9  vel_R=1.9  (slow, battery dying)", "Battery failure\nVoltage below 14V, near-zero capacity", RED, False),
]
for i, (title, sensors, meaning, col, question) in enumerate(classes):
    lx = 0.4 + (i % 2) * 6.45
    ty = 1.65 + (i // 2) * 2.55
    card(s, lx, ty, 6.1, 2.35)
    txt(s, title,   lx+0.15, ty+0.1,  5.8, 0.42, size=14, bold=True, colour=col)
    txt(s, sensors, lx+0.15, ty+0.58, 5.8, 0.65, size=12, colour=WHITE)
    c_m = ORANGE if question else GREEN
    txt(s, meaning, lx+0.15, ty+1.28, 5.8, 0.85, size=12, colour=c_m, bold=True)

txt(s, "Battery threshold (from supervisor's instruction): normal = V \u2265 14V, Cap \u2265 90%, Temp \u2264 36\u00b0C",
    0.5, 6.95, 12.3, 0.35, size=12, colour=LIGHT_GRY)

# ── SLIDE 7 — LSTM + Class Weights ────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "LSTM Training on Robot Data — Solving Class Imbalance", 0.5, 0.3, 12.3, 0.7, size=26, bold=True, colour=ACCENT)
bar(s)

card(s, 0.4, 1.15, 5.9, 3.05)
txt(s, "Model Architecture", 0.6, 1.22, 5.5, 0.4, size=15, bold=True, colour=YELLOW)
bullets(s, [
    "Input: (n, 30, 62)  \u2014  30 timesteps, 62 sensors",
    "LSTM: hidden=128, layers=2, dropout=0.3",
    "Output: 4-class softmax",
    "Epochs: 40  \u00b7  Batch: 256  \u00b7  lr=0.001",
    "Temporal split: first 80% train, last 20% test",
], 0.6, 1.65, size=13, gap=0.36)

card(s, 6.95, 1.15, 5.9, 3.05)
txt(s, "Class Weights (inverse frequency)", 7.15, 1.22, 5.5, 0.4, size=15, bold=True, colour=YELLOW)
wt_data = [
    ("Normal (39,240 rows)",   "0.52\u00d7",  ACCENT),
    ("Failure-1 (33,597 rows)","0.61\u00d7",  ACCENT),
    ("Failure-2 (4,783 rows)", "4.26\u00d7",  ORANGE),
    ("Failure-3 (3,830 rows)", "5.32\u00d7",  RED),
]
for i, (lbl, wt, col) in enumerate(wt_data):
    ty = 1.65 + i*0.54
    txt(s, lbl, 7.15, ty, 3.8, 0.4, size=13, colour=WHITE)
    txt(s, wt,  10.5, ty, 1.2, 0.4, size=14, bold=True, colour=col, align=PP_ALIGN.RIGHT)
txt(s, "Rare failure classes up-weighted \u2192 loss penalises misclassifying Failure-2/3 more heavily",
    7.15, 3.7, 5.5, 0.42, size=11, colour=LIGHT_GRY)

txt(s, "Design Decisions", 0.5, 4.4, 12, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "Temporal split (not random shuffle): test window is chronologically later \u2014 realistic deployment scenario",
    "Test set has no Failure-2 (last 20% of recording has none) \u2192 KernelSHAP uses training samples for that class",
    "l1_reg=0 for KernelSHAP: 1860 features > 50 samples \u2192 Lasso fails; switch to OLS",
], 0.5, 4.85, size=14, gap=0.42)

# ── SLIDE 8 — KernelSHAP on Robot Data ────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "KernelSHAP on Robot Data \u2014 4-Class Attribution", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

txt(s, "How KernelSHAP Works on (30, 62) Robot Sequences", 0.5, 1.18, 12, 0.4, size=17, bold=True, colour=YELLOW)
bullets(s, [
    "Flatten each sample: (30, 62) \u2192 1860 independent features",
    "KernelSHAP fits a weighted linear model on perturbed predictions",
    "Output: (4 classes, 40 samples, 1860) SHAP values",
    "Reshape back: per sensor + per timestep \u2014 which (sensor, time) cell drove each failure class?",
], 0.5, 1.58, size=14, gap=0.38)

txt(s, "Early Results (biased model \u2014 to be re-run with class weights)", 0.5, 3.35, 12, 0.4, size=17, bold=True, colour=ORANGE)

cls_data = [
    ("Normal",    ["velocity_right (negative)", "integrated_x (negative)", "Current (A)"]),
    ("Failure-1", ["Current (A)", "velocity_right", "integrated_x"]),
    ("Failure-2", ["Poss Y (unique)", "Current (A)", "velocity_right"]),
    ("Failure-3", ["Current (A)", "velocity_right", "integrated_x"]),
]
for i, (cls, feats) in enumerate(cls_data):
    lx = 0.4 + (i % 2) * 6.45
    ty = 3.85 + (i // 2) * 1.5
    col = [ACCENT, YELLOW, ORANGE, RED][i]
    card(s, lx, ty, 6.1, 1.35)
    txt(s, cls, lx+0.15, ty+0.1, 5.8, 0.38, size=14, bold=True, colour=col)
    txt(s, "Top sensors: " + "  \u00b7  ".join(feats), lx+0.15, ty+0.55, 5.8, 0.6, size=13, colour=WHITE)

txt(s, "Shared across all failure classes: Current (A), velocity_right, integrated_x",
    0.5, 7.05, 12.3, 0.35, size=13, colour=LIGHT_GRY)

# ── SLIDE 9 — WinIT Method ────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "WinIT \u2014 Window-Based Importance (ICLR 2023)", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)
txt(s, "Leung et al., \u201cExplaining Time Series Predictions via Window-based Importance\u201d, ICLR 2023  \u00b7  No pip package \u2014 implemented from scratch",
    0.5, 1.12, 12.3, 0.38, size=13, colour=LIGHT_GRY)

card(s, 0.4, 1.6, 12.4, 1.35)
txt(s, "Core Idea: suffix masking with finite difference", 0.6, 1.68, 12.0, 0.4, size=15, bold=True, colour=YELLOW)
txt(s, "For each timestep t:  mask the suffix [t, T) with training-set mean baseline  \u2192  measure how much prediction changes",
    0.6, 2.1, 11.8, 0.45, size=14, colour=WHITE)

txt(s, "Mathematics", 0.5, 3.15, 12, 0.38, size=16, bold=True, colour=YELLOW)
txt(s, "raw(t)  =  f(x)  \u2212  f(x\u0303\u209c\u208d\u209c\u208e)      where x\u0303\u209c\u208d\u209c\u208e = x with timesteps [t, T) replaced by baseline",
    0.5, 3.58, 12.3, 0.45, size=14, colour=WHITE)
txt(s, "raw(T)  =  0   (nothing masked)     importance(t)  =  raw(t) \u2212 raw(t+1)  =  marginal contribution of timestep t",
    0.5, 4.05, 12.3, 0.45, size=14, colour=ACCENT)

txt(s, "Why WinIT Is Better Than KernelSHAP for Time Series", 0.5, 4.65, 12, 0.38, size=16, bold=True, colour=YELLOW)
cols_w = [
    ("KernelSHAP", "Flattens (30,62)\u21921860\nTreats each cell independently\nLoses temporal structure\n1860 features \u2192 OLS needed", ORANGE),
    ("WinIT",      "Works on native (30,62)\nCaptures when and where\nMeasures prediction change directly\nNo approximation overhead", GREEN),
    ("Output",     "KernelSHAP: (1860,) per class\nWinIT: (30,) temporal + (62,) feature\nWinIT tells you both WHICH sensor\nand at WHICH timestep", ACCENT),
]
for i, (title, desc, col) in enumerate(cols_w):
    lx = 0.4 + i * 4.3
    card(s, lx, 5.1, 4.0, 2.1)
    txt(s, title, lx+0.15, 5.18, 3.7, 0.42, size=15, bold=True, colour=col)
    txt(s, desc,  lx+0.15, 5.65, 3.7, 1.4,  size=12, colour=WHITE)

# ── SLIDE 10 — WinIT Pipeline ────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "WinIT Pipeline \u2014 Notebook 08", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

steps_w = [
    ("Step 1\nData + Model", "Load robot data, train LSTM with class weights\n(same setup as notebook 07, self-contained)", ACCENT),
    ("Step 2\nBaseline", "Compute training-set mean per feature\nBaseline shape: (30, 62)", ACCENT),
    ("Step 3\nSuffix Mask", "For each sample, for each timestep t:\nmask x[t:] with baseline, get prediction", YELLOW),
    ("Step 4\nFinite Diff", "importance(t) = raw(t) \u2212 raw(t+1)\nOutput: (30, 4) per sample", YELLOW),
    ("Step 5\nFeature Level", "At important timesteps: leave-one-feature-out\nWhich sensor matters at that moment?", ORANGE),
    ("Step 6\nHeatmap", "Temporal \u00d7 Feature heatmap per class\nCompare top sensors vs KernelSHAP", GREEN),
]
for i, (title, desc, col) in enumerate(steps_w):
    lx = 0.4 + (i % 3) * 4.3
    ty = 1.2 + (i // 3) * 2.55
    card(s, lx, ty, 4.05, 2.25)
    txt(s, title, lx+0.15, ty+0.1,  3.8, 0.55, size=14, bold=True, colour=col, align=PP_ALIGN.CENTER)
    txt(s, desc,  lx+0.15, ty+0.7,  3.8, 1.3,  size=12, colour=WHITE)

txt(s, "Outputs: winit_temporal_importance.png  \u00b7  winit_feature_importance.png  \u00b7  winit_heatmap.png  \u00b7  winit_scores.npy",
    0.5, 6.85, 12.3, 0.45, size=13, colour=LIGHT_GRY)

# ── SLIDE 11 — Comparison Plan ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "KernelSHAP vs WinIT \u2014 Comparison Plan", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

header_items = ["Property", "KernelSHAP", "WinIT"]
col_x = [0.4, 3.65, 8.7]
col_w = [3.0, 4.8, 4.5]

txt(s, "Property",    col_x[0]+0.1, 1.15, col_w[0], 0.4, size=14, bold=True, colour=YELLOW)
txt(s, "KernelSHAP",  col_x[1]+0.1, 1.15, col_w[1], 0.4, size=14, bold=True, colour=YELLOW)
txt(s, "WinIT",       col_x[2]+0.1, 1.15, col_w[2], 0.4, size=14, bold=True, colour=YELLOW)
b_hdr = s.shapes.add_shape(1, Inches(0.4), Inches(1.55), Inches(12.4), Inches(0.04))
b_hdr.fill.solid(); b_hdr.fill.fore_color.rgb = ACCENT; b_hdr.line.fill.background()

rows = [
    ("Input format",    "(n, 1860) flattened",                      "(n, 30, 62) native sequence"),
    ("Temporal info",   "Lost \u2014 each cell independent",                "Preserved \u2014 suffix masking"),
    ("Output",          "1860 SHAP values \u2192 reshape back",             "(30,) time + (62,) feature separately"),
    ("Baseline",        "All-zero or mean (same)",                   "Training-set mean per feature"),
    ("Approx. needed",  "OLS (l1_reg=0) for 1860 features",          "None \u2014 direct prediction difference"),
    ("Speed (robot)",   "Fast per sample, many samples needed",      "30 passes per sample (slower)"),
    ("Class support",   "SHAP per class (output dim)",               "Importance per class channel"),
    ("Novel use",       "Established baseline",                      "First use on industrial robot data"),
]
for i, (prop, ks, wi) in enumerate(rows):
    ty = 1.65 + i*0.62
    bg_col = RGBColor(0x2A, 0x2A, 0x3E) if i % 2 == 0 else RGBColor(0x24, 0x24, 0x38)
    card(s, 0.4, ty, 12.4, 0.58, fill=bg_col)
    txt(s, prop, col_x[0]+0.1, ty+0.1, col_w[0], 0.4, size=12, bold=True, colour=LIGHT_GRY)
    txt(s, ks,   col_x[1]+0.1, ty+0.1, col_w[1], 0.4, size=12, colour=WHITE)
    txt(s, wi,   col_x[2]+0.1, ty+0.1, col_w[2], 0.4, size=12, colour=GREEN)

txt(s, "Thesis contribution: first systematic comparison of KernelSHAP vs WinIT on real robot failure data with 3 physically designed failure modes",
    0.5, 6.67, 12.3, 0.5, size=13, colour=ORANGE)

# ── SLIDE 12 — Open Questions ────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Open Questions for Supervisor", 0.5, 0.3, 12.3, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

questions = [
    ("Q1", "What is Failure-1 physically?",
     "From sensor analysis: Failure-1 has healthy battery (V=15.1V, Cap=64%) and normal wheel speed.\n"
     "It looks like a partial battery discharge but no other clear signal. Not a motor fault, not a battery failure.\n"
     "What was physically implemented on the robot for Failure-1?"),
    ("Q2", "Is the temporal distribution expected?",
     "The last 20% of the recording (test set) has zero Failure-2 events.\n"
     "Was Failure-2 only induced early in the experiment? Does the robot recover from it?\n"
     "This affects how we evaluate the model on Failure-2."),
    ("Q3", "Which data from the other 2 robots is available?",
     "Current data: 1 robot, 1 recording session.\n"
     "For federated learning extension: do we have equivalent recordings from Robot 2 and Robot 3?\n"
     "Are the same 3 failure modes implemented on all 3?"),
]
for i, (num, title, detail) in enumerate(questions):
    ty = 1.25 + i * 1.85
    card(s, 0.4, ty, 12.4, 1.7)
    txt(s, f"{num}  {title}", 0.65, ty+0.1, 11.8, 0.45, size=16, bold=True, colour=YELLOW)
    txt(s, detail, 0.65, ty+0.6, 11.8, 0.95, size=13, colour=WHITE)

# ── SLIDE 13 — Updated Timeline ──────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Updated Project Timeline", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

milestones = [
    ("M1 \u2014 July 2026",      "Literature review, repo, CMAPSS pipeline, MLP + KernelSHAP baseline",          "DONE",        GREEN),
    ("M2 \u2014 August 2026",    "LSTM + TimeSHAP on CMAPSS done. Robot data loaded, LSTM trained, KernelSHAP done. WinIT implemented.",
                                                                                                                  "NEARLY DONE", YELLOW),
    ("M3 \u2014 September 2026", "WinIT results on robot data. Full KernelSHAP vs WinIT comparison per failure class. Failure mode validation.", "IN PROGRESS", ORANGE),
    ("M4 \u2014 October 2026",   "Federated SHAP aggregation (3 robots). Final figures + tables generated.",      "UPCOMING",    LIGHT_GRY),
    ("M5 \u2014 December 2026",  "Thesis written and submitted.",                                                 "UPCOMING",    LIGHT_GRY),
]
for i, (title, desc, status, col) in enumerate(milestones):
    ty = 1.25 + i * 1.1
    dot = s.shapes.add_shape(1, Inches(0.4), Inches(ty+0.1), Inches(0.3), Inches(0.5))
    dot.fill.solid(); dot.fill.fore_color.rgb = col; dot.line.fill.background()
    txt(s, title, 0.9, ty, 3.4, 0.4, size=15, bold=True, colour=col)
    pill(s, status, 4.5, ty-0.02, w=1.8, colour=col)
    txt(s, desc, 6.55, ty, 6.5, 0.5, size=12, colour=WHITE)
    b_sep = s.shapes.add_shape(1, Inches(0.4), Inches(ty+0.9), Inches(12.4), Inches(0.02))
    b_sep.fill.solid(); b_sep.fill.fore_color.rgb = RGBColor(0x40, 0x40, 0x55); b_sep.line.fill.background()

txt(s, "On track for December 2026 submission. Robot data analysis is the current focus.",
    0.5, 7.05, 12.3, 0.35, size=13, colour=LIGHT_GRY)

# ── SLIDE 14 — Next Steps ─────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK); bg(s)
txt(s, "Next Steps", 0.5, 0.3, 10, 0.7, size=28, bold=True, colour=ACCENT)
bar(s)

immediate = [
    "Re-run notebook 07 from cell 1 (kernel restarted) \u2014 retrain LSTM with class weights",
    "Run notebook 08 (WinIT) end-to-end \u2014 get temporal + feature importance per failure class",
    "Compare WinIT vs KernelSHAP top sensors per class \u2014 do they agree?",
    "Confirm failure mode semantics with supervisor (especially Failure-1)",
]
next_sprint = [
    "Implement TimeSHAP on robot data (notebook 09) \u2014 complete the 3-method comparison",
    "Generate final comparison figures: sensor rankings, temporal patterns, heatmaps per method",
    "Write SHAP comparison section of thesis (Methods + Results chapters)",
    "Plan federated aggregation experiment if Robot 2 + 3 data is available",
]

txt(s, "This Week", 0.5, 1.18, 12, 0.38, size=17, bold=True, colour=GREEN)
for i, item in enumerate(immediate):
    txt(s, f"\u25b6  {item}", 0.5, 1.6 + i*0.44, 12.3, 0.4, size=14, colour=WHITE)

txt(s, "Next Sprint", 0.5, 3.55, 12, 0.38, size=17, bold=True, colour=ACCENT)
for i, item in enumerate(next_sprint):
    txt(s, f"\u25b6  {item}", 0.5, 3.98 + i*0.44, 12.3, 0.4, size=14, colour=LIGHT_GRY)

txt(s, "End Goal: three SHAP methods, two datasets, one honest comparison \u2014 which method best explains failure in real robot data?",
    0.5, 6.45, 12.3, 0.5, size=14, bold=True, colour=ORANGE, align=PP_ALIGN.CENTER)

# ── Save ──────────────────────────────────────────────────────────────────────
out = r"MA_Siddiqui_Progress.pptx"
prs.save(out)
print(f"Saved: {out}  ({len(prs.slides)} slides)")
