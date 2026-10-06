"""The Lexicon - Version 63 (2026-10-06 daily update)

Lexicon63 preserves the accumulated terminology from Lexicon61 + Lexicon62,
adds the deduplicated 2026-10-06 terminology batch, and refreshes the Tkinter
GUI without adding unrelated features.
"""

import ast
import difflib
import re
import tkinter as tk
from pathlib import Path
from tkinter import ttk

BASE_LEXICON = "Lexicon61.py"
PREVIOUS_EXTENSION = "Lexicon62.py"

LEXICON_63_TERMS = {
    "rail kit": "A rail kit is the matched mechanical hardware used to mount and support a rack server or other device inside a standard equipment rack. Correct installation requires compatible left and right rails at the same rack-unit height, fully engaged with the rack posts and chassis so the equipment can be inserted, retained, and serviced safely.",
    "blanking panel": "A blanking panel is a solid panel installed in unused rack-unit openings to prevent supply air from bypassing equipment or mixing with hot exhaust. In hot-aisle/cold-aisle data centers, blanking panels help preserve front-to-back airflow and reduce recirculation into server inlets.",
    "cable management arm": "A cable management arm is a hinged or sliding rack accessory that organizes power, network, and management cables while allowing a rail-mounted server to extend for service. Proper slack and routing prevent connectors from being pulled, pinched, heated, or blocked by fans and serviceable components.",
    "joint-space planning": "Joint-space planning generates robot motion directly in joint coordinates, such as individual joint angles or displacements, between a start and goal configuration. It makes joint limits straightforward to evaluate, but a simple path in joint space does not generally produce a straight end-effector path in Cartesian space.",
    "time scaling (robotics)": "Time scaling in robotics maps elapsed time to progress along a geometric path, commonly with a path parameter s(t) that advances from 0 to 1. It lets engineers change velocity and acceleration profiles without changing the underlying path geometry.",
    "via point (robotics)": "A via point is an intermediate robot configuration or pose used to shape a trajectory around fixtures, align a tool before contact, or enforce process geometry. Adjacent trajectory segments should meet with sufficient continuity so the robot does not require impossible instantaneous changes in velocity or acceleration.",
    "minority-carrier injection": "Minority-carrier injection is the increase of minority charge carriers on the opposite side of a forward-biased PN junction as carriers cross the reduced junction barrier. Their diffusion and recombination in the quasi-neutral regions are central to the forward-current behavior of an ideal PN-junction diode.",
    "Shockley diode equation": "The Shockley diode equation models the idealized current-voltage relationship of a PN-junction diode as I = Is[exp(Vd/(nVt)) - 1]. It links diode current to junction voltage, saturation current, thermal voltage, and ideality factor and explains the approximately exponential rise of forward current.",
    "ideality factor": "The ideality factor is the dimensionless n term in the diode exponential equation that modifies the slope of the current-voltage characteristic. Values near 1 are associated with diffusion-dominated behavior, while larger values can indicate recombination or other non-ideal transport mechanisms.",
    "diffusion capacitance": "Diffusion capacitance is the incremental capacitance associated with stored minority-carrier charge in a forward-biased semiconductor junction. It becomes important at substantial forward current and helps explain diode switching delay and reverse-recovery behavior.",
    "mass flow controller (MFC)": "A mass flow controller (MFC) is an integrated device that measures gas mass flow and adjusts an internal control valve to make actual flow follow a commanded setpoint. Semiconductor process tools use MFCs for repeatable gas dosing because film growth, etch rate, plasma chemistry, and chamber conditioning can depend on precise flow ratios.",
    "valve manifold box (VMB)": "A valve manifold box (VMB) is an enclosed distribution assembly in a semiconductor gas-delivery system that contains valves and related components used to route, isolate, and distribute process gases from facility supply lines toward tools. Its design supports controlled branching, maintenance isolation, containment, and interlocked operation.",
    "purge sequence (semiconductor gas)": "A purge sequence is the prescribed order of valve operations and inert-gas flow used to clear hazardous or contaminating process gas from lines, manifolds, and components before maintenance, source changes, or operating transitions. The sequence must be followed as designed because incorrect valve states can create exposure, contamination, ignition, or reaction hazards.",
    "ANSI device number": "An ANSI device number is a standardized numerical function code used on power-system protection and control drawings to identify equipment or relay functions independently of vendor naming. Examples include 50 for instantaneous overcurrent, 51 for time overcurrent, 52 for an AC circuit breaker, and 87 for differential protection.",
    "CT saturation": "Current-transformer (CT) saturation occurs when a CT core is driven beyond the range in which secondary current accurately reproduces primary current. The resulting waveform distortion or reduced secondary magnitude can cause protective relays to misjudge fault conditions, so CT ratio, burden, core capability, and expected fault current matter in protection design.",
    "active parameters (AI)": "Active parameters are the subset of a model's total learned parameters that participate in computation for a particular token or inference step. In sparse mixture-of-experts models, the active-parameter count can be far smaller than the total parameter count because a router sends each token through only selected expert blocks.",
    "linear redriver": "A linear redriver is a signal-conditioning device that amplifies and reshapes a high-speed electrical signal to compensate for channel loss without fully retiming the data as a retimer does. In short-reach data-center links, redrivers can extend direct-attach copper reach with relatively low power and implementation complexity.",
    "scale-across connectivity": "Scale-across connectivity links distributed compute infrastructure across larger physical domains such as rows, buildings, campuses, or regions rather than only within one rack or cluster. In AI infrastructure it describes the networking layer that connects pools of compute across distance while preserving high aggregate bandwidth and manageable operational complexity.",
}

LEXICON_63_METADATA = {
    "rail kit": {"source_title": "OSDCTC.004: Server Rack-and-Stack — Rail Kits, U Positions, Airflow, Power, Network, and Verification", "source_url": "https://bitcoinversus.tech/2026/10/06/osdctc-004-server-rack-and-stack-rail-kits-u-positions-airflow-power-network-verification/", "why_it_matters": "Foundational mechanical vocabulary for safe rack-and-stack work and serviceability."},
    "blanking panel": {"source_title": "OSDCTC.004: Server Rack-and-Stack — Rail Kits, U Positions, Airflow, Power, Network, and Verification", "source_url": "https://bitcoinversus.tech/2026/10/06/osdctc-004-server-rack-and-stack-rail-kits-u-positions-airflow-power-network-verification/", "why_it_matters": "Connects rack installation quality directly to cooling efficiency and inlet-air control."},
    "cable management arm": {"source_title": "OSDCTC.004: Server Rack-and-Stack — Rail Kits, U Positions, Airflow, Power, Network, and Verification", "source_url": "https://bitcoinversus.tech/2026/10/06/osdctc-004-server-rack-and-stack-rail-kits-u-positions-airflow-power-network-verification/", "why_it_matters": "Explains how rack cabling remains connected and serviceable when sliding servers are extended."},
    "joint-space planning": {"source_title": "OSREC.004: Robot Trajectory Planning — Joint Space, Cartesian Paths, Time Scaling, Velocity, Acceleration, and Jerk", "source_url": "https://bitcoinversus.tech/2026/10/06/osrec-004-robot-trajectory-planning-joint-space-cartesian-paths-time-scaling-velocity-acceleration-jerk/", "why_it_matters": "Separates robot motion planned in actuator coordinates from motion constrained by tool geometry."},
    "time scaling (robotics)": {"source_title": "OSREC.004: Robot Trajectory Planning — Joint Space, Cartesian Paths, Time Scaling, Velocity, Acceleration, and Jerk", "source_url": "https://bitcoinversus.tech/2026/10/06/osrec-004-robot-trajectory-planning-joint-space-cartesian-paths-time-scaling-velocity-acceleration-jerk/", "why_it_matters": "Provides the mathematical bridge between a geometric robot path and executable motion over time."},
    "via point (robotics)": {"source_title": "OSREC.004: Robot Trajectory Planning — Joint Space, Cartesian Paths, Time Scaling, Velocity, Acceleration, and Jerk", "source_url": "https://bitcoinversus.tech/2026/10/06/osrec-004-robot-trajectory-planning-joint-space-cartesian-paths-time-scaling-velocity-acceleration-jerk/", "why_it_matters": "Useful for shaping practical robot motion around fixtures and process constraints without unnecessary stops."},
    "minority-carrier injection": {"source_title": "OSSEC.004: Diode Current–Voltage Physics — Minority-Carrier Injection, Shockley Equation, Ideality Factor, and Temperature", "source_url": "https://bitcoinversus.tech/2026/10/06/ossec-004-diode-current-voltage-physics-minority-carrier-injection-shockley-equation-ideality-factor-temperature/", "why_it_matters": "Connects PN-junction electrostatics to the carrier transport that actually produces forward diode current."},
    "Shockley diode equation": {"source_title": "OSSEC.004: Diode Current–Voltage Physics — Minority-Carrier Injection, Shockley Equation, Ideality Factor, and Temperature", "source_url": "https://bitcoinversus.tech/2026/10/06/ossec-004-diode-current-voltage-physics-minority-carrier-injection-shockley-equation-ideality-factor-temperature/", "why_it_matters": "Core equation for understanding and approximating PN-junction diode current-voltage behavior."},
    "ideality factor": {"source_title": "OSSEC.004: Diode Current–Voltage Physics — Minority-Carrier Injection, Shockley Equation, Ideality Factor, and Temperature", "source_url": "https://bitcoinversus.tech/2026/10/06/ossec-004-diode-current-voltage-physics-minority-carrier-injection-shockley-equation-ideality-factor-temperature/", "why_it_matters": "Helps interpret why measured diode behavior departs from the simplest diffusion-current model."},
    "diffusion capacitance": {"source_title": "OSSEC.004: Diode Current–Voltage Physics — Minority-Carrier Injection, Shockley Equation, Ideality Factor, and Temperature", "source_url": "https://bitcoinversus.tech/2026/10/06/ossec-004-diode-current-voltage-physics-minority-carrier-injection-shockley-equation-ideality-factor-temperature/", "why_it_matters": "Links forward-bias charge storage to diode switching and small-signal behavior."},
    "mass flow controller (MFC)": {"source_title": "OSSTC.004: Semiconductor Gas Delivery Systems — MFCs, Regulators, Valves, Purge, and Interlocks", "source_url": "https://bitcoinversus.tech/2026/10/06/osstc-004-semiconductor-gas-delivery-systems-mfc-regulators-valves-purge-interlocks/", "why_it_matters": "Essential semiconductor-fab component for precise, repeatable process-gas dosing."},
    "valve manifold box (VMB)": {"source_title": "OSSTC.004: Semiconductor Gas Delivery Systems — MFCs, Regulators, Valves, Purge, and Interlocks", "source_url": "https://bitcoinversus.tech/2026/10/06/osstc-004-semiconductor-gas-delivery-systems-mfc-regulators-valves-purge-interlocks/", "why_it_matters": "Identifies a key gas-distribution and isolation component between facility supply and process tools."},
    "purge sequence (semiconductor gas)": {"source_title": "OSSTC.004: Semiconductor Gas Delivery Systems — MFCs, Regulators, Valves, Purge, and Interlocks", "source_url": "https://bitcoinversus.tech/2026/10/06/osstc-004-semiconductor-gas-delivery-systems-mfc-regulators-valves-purge-interlocks/", "why_it_matters": "Critical safety concept for clearing hazardous or contaminating gases before service and source changes."},
    "ANSI device number": {"source_title": "OSEEC.013: Protective Relaying Fundamentals — CTs, VTs, ANSI Device Numbers, Zones, and Trip Logic", "source_url": "https://bitcoinversus.tech/2026/10/06/oseec-013-protective-relaying-fundamentals-cts-vts-ansi-device-numbers-zones-trip-logic/", "why_it_matters": "Provides a vendor-independent shorthand for protection and control functions on electrical drawings."},
    "CT saturation": {"source_title": "OSEEC.013: Protective Relaying Fundamentals — CTs, VTs, ANSI Device Numbers, Zones, and Trip Logic", "source_url": "https://bitcoinversus.tech/2026/10/06/oseec-013-protective-relaying-fundamentals-cts-vts-ansi-device-numbers-zones-trip-logic/", "why_it_matters": "A protection-critical failure mode because distorted CT secondary current can change relay decisions during faults."},
    "active parameters (AI)": {"source_title": "Artificial Intelligence: Reflection AI’s Beam Puts 501B Parameters Behind a 23B-Active Open Model", "source_url": "https://bitcoinversus.tech/2026/10/06/artificial-intelligence-reflection-ai-beam-501b-23b-active-open-weight-model/", "why_it_matters": "Clarifies how sparse AI models can expose far more total capacity than they compute for each token."},
    "linear redriver": {"source_title": "Networking: Ciena Targets 200T AI Interconnects With 6.4T Optics and Up to 70% Lower Power", "source_url": "https://bitcoinversus.tech/2026/10/06/networking-ciena-6-4t-optics-200t-ai-interconnect-70-percent-lower-power/", "why_it_matters": "Useful data-center interconnect vocabulary for extending high-speed copper links without a full retimer."},
    "scale-across connectivity": {"source_title": "Networking: Ciena Targets 200T AI Interconnects With 6.4T Optics and Up to 70% Lower Power", "source_url": "https://bitcoinversus.tech/2026/10/06/networking-ciena-6-4t-optics-200t-ai-interconnect-70-percent-lower-power/", "why_it_matters": "Names the networking layer that links distributed AI compute across larger physical domains."},
}


def _literal_assignment(path, variable_name):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return ast.literal_eval(node.value)
    raise RuntimeError(f"Could not find {variable_name} in {path.name}")


_here = Path(__file__).resolve().parent
_base_terms = _literal_assignment(_here / BASE_LEXICON, "BitcoinTerminology")
_previous_terms = _literal_assignment(_here / PREVIOUS_EXTENSION, "LEXICON_62_TERMS")

_existing_terms = set(_base_terms) | set(_previous_terms)
_duplicates = sorted(_existing_terms.intersection(LEXICON_63_TERMS))
if _duplicates:
    raise RuntimeError("Lexicon63 contains existing terms: " + ", ".join(_duplicates))

BitcoinTerminology = dict(_base_terms)
BitcoinTerminology.update(_previous_terms)
BitcoinTerminology.update(LEXICON_63_TERMS)


def normalize(text):
    return re.sub(r"[^\w\s]", "", text.casefold()).strip()


def extract_aliases(term):
    aliases = [term]
    aliases.extend(re.findall(r"\((.*?)\)", term))
    return aliases


# Precompute normalized aliases once instead of rebuilding them on every keypress.
SEARCH_INDEX = []
NORMALIZED_LOOKUP = {}
for _term in BitcoinTerminology:
    if not _term.strip():
        continue
    _aliases = tuple(filter(None, (normalize(alias) for alias in extract_aliases(_term))))
    SEARCH_INDEX.append((_term, _aliases))
    NORMALIZED_LOOKUP.setdefault(normalize(_term), _term)

NORMALIZED_KEYS = tuple(NORMALIZED_LOOKUP)

# -----------------------------------------------------------------------------
# WINDOW + THEME
# -----------------------------------------------------------------------------
root = tk.Tk()
root.title("The Lexicon")
root.geometry("760x620")
root.minsize(620, 480)
root.configure(bg="#0b0b0b")

BG = "#0b0b0b"
PANEL = "#141414"
FIELD = "#1b1b1b"
TEXT = "#eeeeee"
MUTED = "#8f8f8f"
GREEN = "#39ff14"
BORDER = "#2a2a2a"

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Lexicon.TEntry",
    fieldbackground=FIELD,
    foreground=TEXT,
    insertcolor=GREEN,
    bordercolor=BORDER,
    lightcolor=BORDER,
    darkcolor=BORDER,
    padding=(12, 10),
    font=("Helvetica", 14),
)
style.map("Lexicon.TEntry", bordercolor=[("focus", GREEN)])

entry_var = tk.StringVar()
suggestions = tk.StringVar(value=[])
status_var = tk.StringVar(value="Type a term, acronym, or alias")
term_title_var = tk.StringVar(value="Definition")

# -----------------------------------------------------------------------------
# SEARCH + DEFINITION LOGIC
# -----------------------------------------------------------------------------
def set_definition(term=None, message=None):
    definition_box.config(state="normal")
    definition_box.delete("1.0", tk.END)
    if term and term in BitcoinTerminology:
        term_title_var.set(term)
        definition_box.insert("1.0", BitcoinTerminology[term])
    else:
        term_title_var.set("Definition")
        definition_box.insert("1.0", message or "Select a result to read its definition.")
    definition_box.config(state="disabled")
    definition_box.yview_moveto(0)


def ranked_matches(search):
    ranked = []
    for term, aliases in SEARCH_INDEX:
        best = None
        for alias in aliases:
            if search == alias:
                best = 0
                break
            if alias.startswith(search):
                best = 1 if best is None else min(best, 1)
            elif any(word.startswith(search) for word in alias.split()):
                best = 2 if best is None else min(best, 2)
            elif search in alias:
                best = 3 if best is None else min(best, 3)
        if best is not None:
            ranked.append((best, len(normalize(term)), term.casefold(), term))
    ranked.sort()
    return [item[3] for item in ranked]


def update_suggestions(*_args):
    raw = entry_var.get().strip()
    search = normalize(raw)

    if not search:
        suggestions.set([])
        status_var.set("Type a term, acronym, or alias")
        set_definition(message="Select a result to read its definition.")
        return

    if raw.startswith('"') and raw.endswith('"'):
        exact = normalize(raw.strip('"'))
        term = NORMALIZED_LOOKUP.get(exact)
        results = [term] if term else []
    else:
        results = ranked_matches(search)

    if not results:
        close = difflib.get_close_matches(search, NORMALIZED_KEYS, n=8, cutoff=0.35)
        results = [NORMALIZED_LOOKUP[key] for key in close]

    if results:
        visible = results[:40]
        suggestions.set(visible)
        if len(results) > len(visible):
            status_var.set(f"Showing {len(visible)} of {len(results)} matches")
        else:
            status_var.set(f"{len(results)} match{'es' if len(results) != 1 else ''}")

        exact_term = NORMALIZED_LOOKUP.get(search)
        if exact_term:
            set_definition(term=exact_term)
    else:
        suggestions.set(["No matches found"])
        status_var.set("No matches found")
        set_definition(message="No definition matched that search.")


def choose_term(term):
    if not term or term == "No matches found":
        return
    entry_var.set(term)
    set_definition(term=term)
    status_var.set("Exact term")


def on_select(_event=None):
    selection = listbox.curselection()
    if selection:
        choose_term(listbox.get(selection[0]))
    return "break"


def on_enter(_event=None):
    selection = listbox.curselection()
    if selection:
        choose_term(listbox.get(selection[0]))
    elif listbox.size() > 0:
        choose_term(listbox.get(0))
    else:
        exact_term = NORMALIZED_LOOKUP.get(normalize(entry_var.get()))
        if exact_term:
            choose_term(exact_term)
    return "break"


def focus_listbox(_event=None):
    if listbox.size() > 0 and listbox.get(0) != "No matches found":
        listbox.focus_set()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(0)
        listbox.activate(0)
        set_definition(term=listbox.get(0))
    return "break"


def clear_suggestions(_event=None):
    suggestions.set([])
    status_var.set("Suggestions hidden — keep typing or press Ctrl+L")
    return "break"

# -----------------------------------------------------------------------------
# LAYOUT
# -----------------------------------------------------------------------------
main = tk.Frame(root, bg=BG, padx=24, pady=22)
main.pack(fill=tk.BOTH, expand=True)
main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(4, weight=1)

header = tk.Frame(main, bg=BG)
header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
header.grid_columnconfigure(0, weight=1)

tk.Label(
    header,
    text="THE LEXICON",
    bg=BG,
    fg=GREEN,
    font=("Helvetica", 24, "bold"),
    anchor="w",
).grid(row=0, column=0, sticky="w")

tk.Label(
    header,
    text=f"Technical reference  •  {len(BitcoinTerminology):,} terms",
    bg=BG,
    fg=MUTED,
    font=("Helvetica", 10),
    anchor="w",
).grid(row=1, column=0, sticky="w", pady=(4, 0))

search_header = tk.Frame(main, bg=BG)
search_header.grid(row=1, column=0, sticky="ew")
search_header.grid_columnconfigure(0, weight=1)

tk.Label(
    search_header,
    text="SEARCH",
    bg=BG,
    fg=TEXT,
    font=("Helvetica", 10, "bold"),
).grid(row=0, column=0, sticky="w")

tk.Label(
    search_header,
    textvariable=status_var,
    bg=BG,
    fg=MUTED,
    font=("Helvetica", 9),
).grid(row=0, column=1, sticky="e")

entry = ttk.Entry(main, textvariable=entry_var, style="Lexicon.TEntry")
entry.grid(row=2, column=0, sticky="ew", pady=(7, 10))

results_panel = tk.Frame(main, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
results_panel.grid(row=3, column=0, sticky="ew", pady=(0, 14))
results_panel.grid_columnconfigure(0, weight=1)

results_scroll = tk.Scrollbar(results_panel, orient=tk.VERTICAL)
results_scroll.grid(row=0, column=1, sticky="ns")

listbox = tk.Listbox(
    results_panel,
    listvariable=suggestions,
    height=7,
    bg=PANEL,
    fg=TEXT,
    selectbackground="#244d20",
    selectforeground=GREEN,
    activestyle="none",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
    font=("Helvetica", 12),
    yscrollcommand=results_scroll.set,
    exportselection=False,
)
listbox.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
results_scroll.config(command=listbox.yview)

definition_panel = tk.Frame(main, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
definition_panel.grid(row=4, column=0, sticky="nsew")
definition_panel.grid_columnconfigure(0, weight=1)
definition_panel.grid_rowconfigure(1, weight=1)

tk.Label(
    definition_panel,
    textvariable=term_title_var,
    bg=PANEL,
    fg=GREEN,
    font=("Helvetica", 15, "bold"),
    anchor="w",
).grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

definition_scroll = tk.Scrollbar(definition_panel, orient=tk.VERTICAL)
definition_scroll.grid(row=1, column=1, sticky="ns", pady=(0, 12))

definition_box = tk.Text(
    definition_panel,
    wrap=tk.WORD,
    bg=PANEL,
    fg=TEXT,
    insertbackground=GREEN,
    yscrollcommand=definition_scroll.set,
    font=("Helvetica", 13),
    padx=16,
    pady=8,
    spacing1=2,
    spacing3=5,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
)
definition_box.grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=(0, 12))
definition_scroll.config(command=definition_box.yview)
definition_box.config(state="disabled")

footer = tk.Label(
    main,
    text="Enter opens a result  •  ↓ moves to matches  •  Ctrl+L focuses search  •  Ctrl+Q quits",
    bg=BG,
    fg=MUTED,
    font=("Helvetica", 9),
    anchor="w",
)
footer.grid(row=5, column=0, sticky="ew", pady=(10, 0))

entry.bind("<Return>", on_enter)
entry.bind("<Down>", focus_listbox)
entry.bind("<Escape>", clear_suggestions)
listbox.bind("<<ListboxSelect>>", on_select)
listbox.bind("<Return>", on_select)
listbox.bind("<Escape>", lambda _e: entry.focus_set())
root.bind("<Control-l>", lambda _e: (entry.focus_set(), entry.select_range(0, tk.END)))
root.bind("<Control-q>", lambda _e: root.destroy())
entry_var.trace_add("write", update_suggestions)

set_definition(message="Select a result to read its definition.")
entry.focus_set()
root.mainloop()
