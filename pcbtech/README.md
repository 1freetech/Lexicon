# pcbtech shared lexicon

This folder is the shared terminology source for the `pcbtech` PCB construction game, engineering simulator, GUI tooltips, and technician-training modules.

## Design rules

- Every entry has a one-sentence definition.
- Stable `id` values are intended for future GUI, lesson, tooltip, and C++ integration.
- `implementation_status` prevents the Lexicon from presenting planned gameplay as already implemented: `current` means represented by the engineering core, `partial` means a limited implementation exists, and `planned` means required by the current roadmap or interaction rules but not yet a finished feature.
- `training_level` uses 1 for foundation, 2 for technician/intermediate, and 3 for advanced engineering concepts.
- `aliases` are semicolon-separated search terms.
- Unknown engineering data stays unknown; the vocabulary never implies that a visual asset, placement check, or unverified model proves electrical, thermal, manufacturing, or safety performance.

## Files

- `fundamentals.tsv` — PCB identity, part identity, packages, sources, tolerances, and mounting concepts.
- `symbols_connectivity.tsv` — schematic/board connection objects and typed pins.
- `components.tsv` — the component families and schematic component types used by the planned catalog.
- `layout_stackup.tsv` — board geometry, copper, stackup, impedance, return-path, and advanced routing concepts.
- `simulation_validation.tsv` — digital logic, SPICE, PDN, decoupling, accuracy tiers, and validation language.
- `manufacturing_instruments.tsv` — fabrication outputs, DFM/DFA/DFT, and technician instruments.
- `gameplay_training.tsv` — simplified GUI actions, views, guided mode, sandbox mode, and training features.

The TSV schema is `id`, `term`, `kind`, `implementation_status`, `training_level`, `aliases`, and `definition`, making the same data straightforward to load from Python now and from the C++ simulator later.
