'The Lexicon - Version 62 (2026-10-05 daily update)'

# Lexicon62 is a versioned extension of Lexicon61. It preserves the complete
# Lexicon61 application and injects the deduplicated 2026-10-05 terminology
# before the existing UI code runs.
import ast
from pathlib import Path

BASE_LEXICON = "Lexicon61.py"

LEXICON_62_TERMS = {'AI-native backend': 'An AI-native backend is application infrastructure designed from the outset to be configured, queried, or operated through AI agents and natural-language workflows as well as conventional APIs and consoles. The design typically exposes bounded, machine-readable capabilities so agents can make useful changes without receiving unrestricted system access.',
 'LiveOps': 'LiveOps is the continuing operation of a live game or online service after release through events, configuration changes, messaging, offers, analytics, moderation, maintenance, and player-management systems. It turns a shipped product into an actively operated service whose behavior can evolve without a full client release.',
 'bounded agent surface': 'A bounded agent surface is the deliberately limited set of tools, resources, parameters, and actions exposed to an AI agent. Constraining the surface reduces the blast radius of mistakes and makes authorization, validation, logging, and human approval easier to enforce.',
 'logical radix': 'Logical radix is the number of usable network interfaces or endpoints a switch can present after accounting for supported breakout modes, rather than counting only physical front-panel cages. It is useful for comparing high-capacity AI and data-center switches whose single high-speed ports can fan out into multiple lower-speed links.',
 'port breakout': 'Port breakout is the practice of dividing one high-speed physical Ethernet port into multiple lower-speed logical interfaces, such as splitting an 800 Gb/s port into several 100 Gb/s or 200 Gb/s links when the hardware and optics support it. Breakout increases usable endpoint count without adding more physical switch cages.',
 'interface density': 'Interface density is the number of usable network interfaces available within a given chassis, rack-unit count, or physical footprint. High interface density matters in accelerator clusters because it determines how many servers, GPUs, switches, or optical links can be connected without expanding rack space.',
 'JTAG': 'JTAG is a standardized boundary-scan and hardware-debug interface commonly associated with IEEE 1149.1. It can provide test access to digital devices and, on supported processors, enables operations such as halting execution, inspecting registers and memory, setting breakpoints, and programming devices.',
 'SWD': "Serial Wire Debug (SWD) is Arm's compact two-wire debug interface, typically using SWDIO for bidirectional data and SWCLK for the clock. It provides processor-debug capabilities similar to JTAG while using fewer pins, which makes it common on microcontrollers and embedded boards.",
 'OpenOCD': 'OpenOCD, or Open On-Chip Debugger, is an open-source tool that connects supported debug probes to embedded targets and can expose services such as a GDB server. It translates debugger requests into low-level JTAG or SWD operations used to inspect, halt, reset, and program hardware.',
 'hardware breakpoint': 'A hardware breakpoint is a processor-supported breakpoint implemented with dedicated debug resources rather than by modifying the program instruction in memory. It is especially useful when code executes from read-only flash or when changing instructions would be unsafe or impractical.',
 'watchpoint': 'A watchpoint is a debug trigger that stops or reports execution when a selected memory address or data access condition occurs. Watchpoints are valuable for finding unexpected writes, reads, state corruption, and timing-sensitive changes that are difficult to catch with ordinary line breakpoints.',
 'connect-under-reset': 'Connect-under-reset is a debugging technique in which a probe establishes control while the target is held in reset or during the reset sequence. It can recover access to firmware that crashes immediately, reconfigures debug pins, enters low-power states, or activates a watchdog before a normal debugger connection completes.',
 'Heisenbug': 'A Heisenbug is a software defect whose behavior changes or disappears when the system is observed, instrumented, or debugged. In real-time and embedded systems, breakpoints, logging, timing changes, cache effects, and debugger halts can alter the conditions that originally produced the failure.',
 'behind-the-meter (BTM)': "Behind-the-meter (BTM) generation or storage is located on the customer's side of the utility revenue meter and primarily serves the customer's own load. A BTM system can reduce grid purchases, support resilience, or supply large facilities such as data centers directly from on-site energy assets.",
 'prime power': 'Prime power is electrical generation intended to carry sustained operational load for extended periods rather than operate only during emergencies. Prime-power plants require fuel, maintenance, controls, emissions planning, and reliability practices suitable for routine service.',
 'island mode': 'Island mode is the operating state in which a microgrid or facility electrical system disconnects from the larger utility grid and continues supplying local loads independently. Successful islanding requires coordinated generation, storage, protection, frequency and voltage control, and a safe reconnection strategy.',
 'megawatt-hour (MWh)': 'A megawatt-hour (MWh) is a unit of energy equal to one megawatt of power delivered or consumed continuously for one hour. It measures an amount of energy, while megawatts (MW) measure the instantaneous rate of power delivery or consumption.',
 'storage duration': 'Storage duration is the approximate time an energy-storage system can operate at its rated power before exhausting its usable stored energy. It is commonly estimated as energy capacity divided by power rating, so a 400 MWh system rated at 100 MW has about four hours of nominal duration.',
 'agentic engineering assistant': 'An agentic engineering assistant is an AI system that can inspect engineering context, invoke approved tools, execute supported actions, and follow multi-step workflows rather than only generate text answers. In hardware and embedded development it can connect design intent with build, analysis, debug, and documentation tools under defined controls.',
 'agent skill': 'An agent skill is a reusable, structured procedure that teaches an AI agent how to perform a specific class of work, including instructions, tool-use patterns, interpretation rules, and expected outputs. Skills turn repeatable engineering knowledge into workflows that can be invoked consistently across tasks.',
 'Rayleigh backscatter': 'Rayleigh backscatter is the small fraction of light scattered back toward the source by microscopic refractive-index variations in optical fiber. OTDR instruments analyze this returned light over time to estimate distance-dependent loss and construct much of the fiber trace.',
 'OTDR dead zone': 'An OTDR dead zone is the distance after a strong reflective or loss event over which the instrument cannot accurately resolve another nearby event. Dead zones depend on factors such as pulse width, receiver recovery, event reflectance, and instrument design, and they are a major reason launch and receive fibers are used.',
 'launch fiber': "A launch fiber is a known length of fiber placed between an OTDR and the link under test so the instrument can settle before measuring the link's first connector or event. It moves the near-end connection outside the OTDR dead zone and improves characterization of the link entrance.",
 'Coolant Distribution Unit (CDU)': 'A Coolant Distribution Unit (CDU) manages the transfer of heat between an IT liquid-cooling loop and a facility cooling loop. A CDU commonly contains pumps, a heat exchanger, filtration, controls, sensors, and pressure or flow management needed to deliver conditioned coolant to racks or cold plates.',
 'direct-to-chip cooling': 'Direct-to-chip cooling is a liquid-cooling architecture that places cold plates directly on processors, GPUs, memory, or other major heat-producing components. Coolant removes heat close to the source, allowing higher rack power density and reducing the amount of heat that must be carried away by room air.',
 'psychrometrics': 'Psychrometrics is the engineering study of the thermodynamic properties of moist air, including dry-bulb temperature, wet-bulb temperature, relative humidity, dew point, humidity ratio, and enthalpy. In data centers it supports humidity control, condensation avoidance, economizer decisions, and cooling-system analysis.',
 'economization (free cooling)': 'Economization, often called free cooling, uses favorable outdoor air or water conditions to reject heat while reducing or avoiding mechanical refrigeration. Air-side and water-side economizers can lower cooling energy when environmental conditions remain within equipment and humidity limits.',
 'thermal ΔT': 'Thermal ΔT is the temperature difference between the entering and leaving fluid or air streams across equipment, a rack, or a cooling loop. It is a basic indicator of how much heat is being carried for a given flow rate and is central to airflow, hydronic, and liquid-cooling calculations.'}

LEXICON_62_METADATA = {'AI-native backend': {'source_title': 'Gaming: Hive Axyl Lets Codex Wire Game Backends With Natural-Language Prompts', 'source_url': 'https://bitcoinversus.tech/2026/10/05/gaming-hive-axyl-codex-game-backends-natural-language/', 'why_it_matters': 'Shows how application infrastructure is being redesigned so coding agents can interact with production services safely.'},
 'LiveOps': {'source_title': 'Gaming: Hive Axyl Lets Codex Wire Game Backends With Natural-Language Prompts', 'source_url': 'https://bitcoinversus.tech/2026/10/05/gaming-hive-axyl-codex-game-backends-natural-language/', 'why_it_matters': 'Explains the operational layer behind continuously updated games and online services.'},
 'bounded agent surface': {'source_title': 'Gaming: Hive Axyl Lets Codex Wire Game Backends With Natural-Language Prompts', 'source_url': 'https://bitcoinversus.tech/2026/10/05/gaming-hive-axyl-codex-game-backends-natural-language/', 'why_it_matters': 'Provides a useful security and architecture concept for limiting what autonomous agents can change.'},
 'logical radix': {'source_title': 'Networking: The 3 Largest Switches by Port Count — Arista Leads With 4,608 100G Interfaces', 'source_url': 'https://bitcoinversus.tech/2026/10/05/networking-largest-switches-port-count-arista-cisco-juniper/', 'why_it_matters': 'Makes modern switch capacity comparable when breakout creates far more logical links than physical cages.'},
 'port breakout': {'source_title': 'Networking: The 3 Largest Switches by Port Count — Arista Leads With 4,608 100G Interfaces', 'source_url': 'https://bitcoinversus.tech/2026/10/05/networking-largest-switches-port-count-arista-cisco-juniper/', 'why_it_matters': 'Explains how high-speed Ethernet ports are converted into multiple accelerator- or server-facing links.'},
 'interface density': {'source_title': 'Networking: The 3 Largest Switches by Port Count — Arista Leads With 4,608 100G Interfaces', 'source_url': 'https://bitcoinversus.tech/2026/10/05/networking-largest-switches-port-count-arista-cisco-juniper/', 'why_it_matters': 'Connects switch design to rack space, cable count, and the scale of AI fabrics.'},
 'JTAG': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Foundational interface for board test, firmware bring-up, and processor debugging.'},
 'SWD': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Common low-pin-count debug interface on Arm microcontrollers and embedded systems.'},
 'OpenOCD': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Key open-source bridge between hardware debug probes and software debuggers such as GDB.'},
 'hardware breakpoint': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Essential when debugging code in flash or other memory that should not be modified.'},
 'watchpoint': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Helps locate memory corruption and unexpected state changes that line breakpoints miss.'},
 'connect-under-reset': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Provides a recovery path when bad firmware prevents a normal debugger connection.'},
 'Heisenbug': {'source_title': 'OSFEC.003: Hardware Debugging with JTAG, SWD, OpenOCD, and GDB', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfec-003-hardware-debugging-jtag-swd-openocd-gdb/', 'why_it_matters': 'Names a major class of timing-sensitive failures whose behavior changes under observation.'},
 'behind-the-meter (BTM)': {'source_title': 'Energy: Behind-the-Meter Power Explained — Why Data Centers Are Building Electricity On-Site', 'source_url': 'https://bitcoinversus.tech/2026/10/05/energy-behind-the-meter-power-explained-data-centers-onsite-generation/', 'why_it_matters': 'Core vocabulary for data centers and industrial loads building generation on-site.'},
 'prime power': {'source_title': 'Energy: Behind-the-Meter Power Explained — Why Data Centers Are Building Electricity On-Site', 'source_url': 'https://bitcoinversus.tech/2026/10/05/energy-behind-the-meter-power-explained-data-centers-onsite-generation/', 'why_it_matters': 'Separates sustained generation assets from conventional emergency-only backup systems.'},
 'island mode': {'source_title': 'Energy: Behind-the-Meter Power Explained — Why Data Centers Are Building Electricity On-Site', 'source_url': 'https://bitcoinversus.tech/2026/10/05/energy-behind-the-meter-power-explained-data-centers-onsite-generation/', 'why_it_matters': 'Describes whether a microgrid can continue operating when the utility grid is unavailable.'},
 'megawatt-hour (MWh)': {'source_title': 'Energy: MW vs. MWh Explained — The Easy Guide to Power vs. Energy', 'source_url': 'https://bitcoinversus.tech/2026/10/05/energy-mw-vs-mwh-explained-power-vs-energy-easy-guide/', 'why_it_matters': 'Prevents the common mistake of confusing power capacity in MW with energy quantity in MWh.'},
 'storage duration': {'source_title': 'Energy: MW vs. MWh Explained — The Easy Guide to Power vs. Energy', 'source_url': 'https://bitcoinversus.tech/2026/10/05/energy-mw-vs-mwh-explained-power-vs-energy-easy-guide/', 'why_it_matters': 'Turns MW and MWh battery ratings into an intuitive operating-time metric.'},
 'agentic engineering assistant': {'source_title': 'Semiconductors: AMD Ross Brings Agentic AI Into FPGA and Embedded-System Design', 'source_url': 'https://bitcoinversus.tech/2026/10/05/semiconductors-amd-ross-agentic-ai-fpga-embedded-design/', 'why_it_matters': 'Captures the shift from AI chat tools to systems that can operate engineering toolchains.'},
 'agent skill': {'source_title': 'Semiconductors: AMD Ross Brings Agentic AI Into FPGA and Embedded-System Design', 'source_url': 'https://bitcoinversus.tech/2026/10/05/semiconductors-amd-ross-agentic-ai-fpga-embedded-design/', 'why_it_matters': 'Describes reusable procedural knowledge that makes agent workflows repeatable and auditable.'},
 'Rayleigh backscatter': {'source_title': 'OSFOTC.003: OTDR Field Testing — Launch/Receive Fibers, Range, Pulse Width, Events, Dead Zones, and Fault Location', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfotc-003-otdr-field-testing-launch-receive-fibers-range-pulse-width-events-dead-zones-fault-location/', 'why_it_matters': 'Explains the physical signal that lets an OTDR build a distance-resolved fiber trace.'},
 'OTDR dead zone': {'source_title': 'OSFOTC.003: OTDR Field Testing — Launch/Receive Fibers, Range, Pulse Width, Events, Dead Zones, and Fault Location', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfotc-003-otdr-field-testing-launch-receive-fibers-range-pulse-width-events-dead-zones-fault-location/', 'why_it_matters': 'Determines whether closely spaced fiber events can actually be distinguished in field testing.'},
 'launch fiber': {'source_title': 'OSFOTC.003: OTDR Field Testing — Launch/Receive Fibers, Range, Pulse Width, Events, Dead Zones, and Fault Location', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osfotc-003-otdr-field-testing-launch-receive-fibers-range-pulse-width-events-dead-zones-fault-location/', 'why_it_matters': 'Explains a standard test setup needed to measure the first connector of an optical link accurately.'},
 'Coolant Distribution Unit (CDU)': {'source_title': 'OSDCEC.003: Data Center Cooling Engineering — Airflow, ΔT, Containment, Psychrometrics, Economization, and Liquid Cooling', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osdcec-003-data-center-cooling-engineering-airflow-deltat-containment-psychrometrics-economization-liquid-cooling/', 'why_it_matters': 'CDUs are becoming standard infrastructure as AI racks move to liquid cooling.'},
 'direct-to-chip cooling': {'source_title': 'OSDCEC.003: Data Center Cooling Engineering — Airflow, ΔT, Containment, Psychrometrics, Economization, and Liquid Cooling', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osdcec-003-data-center-cooling-engineering-airflow-deltat-containment-psychrometrics-economization-liquid-cooling/', 'why_it_matters': 'Enables power densities that conventional room-air cooling increasingly struggles to support.'},
 'psychrometrics': {'source_title': 'OSDCEC.003: Data Center Cooling Engineering — Airflow, ΔT, Containment, Psychrometrics, Economization, and Liquid Cooling', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osdcec-003-data-center-cooling-engineering-airflow-deltat-containment-psychrometrics-economization-liquid-cooling/', 'why_it_matters': 'Connects humidity, dew point, economization, and condensation risk in data-center cooling.'},
 'economization (free cooling)': {'source_title': 'OSDCEC.003: Data Center Cooling Engineering — Airflow, ΔT, Containment, Psychrometrics, Economization, and Liquid Cooling', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osdcec-003-data-center-cooling-engineering-airflow-deltat-containment-psychrometrics-economization-liquid-cooling/', 'why_it_matters': 'Explains how facilities reduce chiller energy by using favorable outdoor conditions.'},
 'thermal ΔT': {'source_title': 'OSDCEC.003: Data Center Cooling Engineering — Airflow, ΔT, Containment, Psychrometrics, Economization, and Liquid Cooling', 'source_url': 'https://bitcoinversus.tech/2026/10/05/osdcec-003-data-center-cooling-engineering-airflow-deltat-containment-psychrometrics-economization-liquid-cooling/', 'why_it_matters': 'Links temperature rise to heat transport and is a basic diagnostic and sizing metric for cooling systems.'}}

def _load_base_lexicon_source():
    base_path = Path(__file__).with_name(BASE_LEXICON)
    source = base_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(base_path))

    assignment = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "BitcoinTerminology":
                    assignment = node
                    break
        if assignment is not None:
            break

    if assignment is None:
        raise RuntimeError(f"Could not find BitcoinTerminology in {BASE_LEXICON}")

    base_terms = ast.literal_eval(assignment.value)
    duplicates = sorted(set(base_terms).intersection(LEXICON_62_TERMS))
    if duplicates:
        raise RuntimeError(
            "Lexicon62 contains terms already present in Lexicon61: "
            + ", ".join(duplicates)
        )

    lines = source.splitlines(keepends=True)
    prelude = "".join(lines[: assignment.lineno - 1])
    tail = "".join(lines[assignment.end_lineno :])
    return base_path, prelude, tail, base_terms


_base_path, _prelude, _tail, _base_terms = _load_base_lexicon_source()

# Reuse the original imports and any pre-dictionary setup.
exec(compile(_prelude, str(_base_path), "exec"), globals(), globals())

BitcoinTerminology = dict(_base_terms)
BitcoinTerminology.update(LEXICON_62_TERMS)

# Preserve the complete Lexicon61 application behavior with the updated dictionary.
exec(compile(_tail, str(_base_path), "exec"), globals(), globals())
