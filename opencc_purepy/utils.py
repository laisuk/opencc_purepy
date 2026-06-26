from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal, Optional, Tuple

from .dict_slot import DictSlot, DictSlotLike
from .dictionary_lib import PathLike, SlotPathMap

CustomDictMode = Literal["append", "override"]

@dataclass(frozen=True)
class CustomDictSpec:
    slot: DictSlot
    mode: CustomDictMode
    path: PathLike

def parse_custom_dict_spec(spec: str) -> CustomDictSpec:
    """Parse one --custom-dict value in slot:mode:path format."""
    parts = spec.split(":", 2)
    if len(parts) != 3:
        raise ValueError(
            "Invalid --custom-dict spec {!r}. Expected slot:mode:path".format(spec)
        )

    slot, mode, path = (p.strip() for p in parts)

    if not slot:
        raise ValueError(
            "Invalid --custom-dict spec {!r}: slot is empty".format(spec)
        )

    mode = mode.lower()
    if mode not in ("append", "override"):
        raise ValueError(
            "Invalid --custom-dict mode {!r}. Expected append or override".format(mode)
        )

    if not path:
        raise ValueError(
            "Invalid --custom-dict spec {!r}: path is empty".format(spec)
        )

    return CustomDictSpec(
        slot=normalize_dict_slot(slot),
        mode=mode,
        path=path,
    )

def parse_custom_dict_specs(
        specs: Optional[Iterable[str]],
) -> Tuple[SlotPathMap, SlotPathMap]:
    """Parse --custom-dict values into override/appends maps."""
    overrides: SlotPathMap = {}
    appends: SlotPathMap = {}

    for spec in specs or ():
        slot, mode, path = parse_custom_dict_spec(spec)

        if not Path(path).is_file():
            raise ValueError("Custom dictionary file not found: {}".format(path))

        if mode == "override":
            overrides[slot] = path
        else:
            appends[slot] = path

    return overrides, appends


def normalize_dict_slot(slot: DictSlotLike) -> DictSlot:
    """
    Normalize a user-supplied dictionary slot to a DictSlot.

    Accepts:
        HKPhrasesRev
        hkphrasesrev
        hk_phrases_rev
        DictSlot.HKPhrasesRev
    """
    if isinstance(slot, DictSlot):
        return slot

    key = slot.strip().lower().replace("_", "")

    for member in DictSlot:
        if member.name.lower() == key:
            return member

        if member.value.replace("_", "").lower() == key:
            return member

    raise ValueError("Unknown dictionary slot: {}".format(slot))