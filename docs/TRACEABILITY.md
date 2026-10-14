# Traceability

The live claim-to-evidence audit for this model is maintained in the
Project Z!B program workspace (`GITHUB_TRACEABILITY.md`) and re-run at
every design gate. It maps each model claim to referenceable
implementations (ArduPilot control laws, JSBSim 6-DOF, XFoil method, VLM
stability, level-flight equations) and marks our own numbers — propulsion
derate fit, hotel load, weight buildup, trim coefficients, our JSBSim
model — as Z!B-authored.

This file is the pointer, not the audit. Do not fork the audit here; the
workspace copy is the controlled truth and this repo's
`zb_model/data/assumptions.yaml` is its machine-readable companion.
