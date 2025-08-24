#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "altpe_sdk"


def unparse(node: ast.AST) -> str:
    return ast.unparse(node) if node is not None else ""


def is_enum_class(node: ast.ClassDef) -> bool:
    for b in node.bases:
        name = unparse(b)
        if name.endswith("Enum") or name == "Enum":
            return True
    return False


def is_model_class(node: ast.ClassDef) -> bool:
    for b in node.bases:
        name = unparse(b)
        if name.split(".")[-1] in {"BaseModel", "BaseApiModel", "PaginatedResponse"}:
            return True
    return False


def is_target_client_class(node: ast.ClassDef) -> bool:
    return node.name == "AlternativesPE"


def collect_enums(path: Path) -> Dict[str, List[str]]:
    tree = ast.parse(path.read_text())
    enums: Dict[str, List[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and is_enum_class(node):
            values: List[str] = []
            for stmt in node.body:
                if (
                    isinstance(stmt, ast.Assign)
                    and len(stmt.targets) == 1
                    and isinstance(stmt.targets[0], ast.Name)
                ):
                    key = stmt.targets[0].id
                    if key.startswith("_"):
                        continue
                    try:
                        val = ast.literal_eval(stmt.value)
                        values.append(str(val))
                    except Exception:
                        values.append(unparse(stmt.value))
            enums[node.name] = values
    return enums


def collect_models(path: Path) -> Dict[str, List[Tuple[str, str]]]:
    tree = ast.parse(path.read_text())
    models: Dict[str, List[Tuple[str, str]]] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and is_model_class(node):
            fields: List[Tuple[str, str]] = []
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(
                    stmt.target, ast.Name
                ):
                    name = stmt.target.id
                    typ = unparse(stmt.annotation)
                    alias = None
                    if stmt.value and isinstance(stmt.value, ast.Call):
                        if unparse(stmt.value.func).split(".")[-1] == "Field":
                            for kw in stmt.value.keywords or []:
                                if kw.arg == "alias":
                                    alias = ast.literal_eval(kw.value)
                    if alias:
                        typ = f"{typ} (alias={alias})"
                    fields.append((name, typ))
            models[node.name] = fields
    return models


def collect_client_methods(path: Path) -> List[Tuple[str, str, str]]:
    tree = ast.parse(path.read_text())
    methods: List[Tuple[str, str, str]] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and is_target_client_class(node):
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef):
                    name = stmt.name
                    if name.startswith("_") and name not in {
                        "__init__",
                        "__enter__",
                        "__exit__",
                    }:
                        continue
                    args = stmt.args
                    # Build parameters list
                    params: List[str] = []
                    pos_args = args.args[:]  # includes self
                    defaults = args.defaults[:] if args.defaults else []
                    # map defaults to last N positionals (excluding self)
                    positional = pos_args
                    default_offset = len(positional) - len(defaults)
                    for i, a in enumerate(positional):
                        pname = a.arg
                        if pname == "self":
                            continue
                        ann = unparse(a.annotation) if a.annotation else ""
                        dval: Optional[str] = None
                        if i >= default_offset and defaults:
                            d = defaults[i - default_offset]
                            dval = unparse(d)
                        if ann and dval is not None:
                            params.append(f"{pname}: {ann}={dval}")
                        elif ann:
                            params.append(f"{pname}: {ann}")
                        elif dval is not None:
                            params.append(f"{pname}={dval}")
                        else:
                            params.append(pname)
                    # kwonly args
                    if args.kwonlyargs:
                        for j, a in enumerate(args.kwonlyargs):
                            pname = a.arg
                            ann = unparse(a.annotation) if a.annotation else ""
                            dval = None
                            if args.kw_defaults and args.kw_defaults[j] is not None:
                                dval = unparse(args.kw_defaults[j])
                            if ann and dval is not None:
                                params.append(f"{pname}: {ann}={dval}")
                            elif ann:
                                params.append(f"{pname}: {ann}")
                            elif dval is not None:
                                params.append(f"{pname}={dval}")
                            else:
                                params.append(pname)
                    ret = unparse(stmt.returns) if stmt.returns else ""
                    methods.append((name, ", ".join(params), ret))
    return methods


def collect_mapping_samples(path: Path) -> Dict[str, List[Tuple[Any, Any]]]:
    tree = ast.parse(path.read_text())
    samples: Dict[str, List[Tuple[Any, Any]]] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "EntityMappings":
            for stmt in node.body:
                if (
                    isinstance(stmt, ast.Assign)
                    and len(stmt.targets) == 1
                    and isinstance(stmt.targets[0], ast.Name)
                ):
                    name = stmt.targets[0].id
                    if isinstance(stmt.value, ast.Dict):
                        pairs: List[Tuple[Any, Any]] = []
                        for k, v in zip(stmt.value.keys, stmt.value.values):
                            try:
                                kk = ast.literal_eval(k)
                            except Exception:
                                kk = unparse(k)
                            try:
                                vv = ast.literal_eval(v)
                            except Exception:
                                vv = unparse(v)
                            pairs.append((kk, vv))
                        # first 5 ordered by key if comparable
                        try:
                            pairs.sort(key=lambda x: x[0])
                        except Exception:
                            pass
                        samples[name] = pairs[:5]
    return samples


def emit_llms(enums, models, methods, mapping_samples) -> str:
    out: List[str] = []
    out.append("[altpe_sdk.enums]")
    for ename, vals in enums.items():
        vals_fmt = ", ".join(str(v) for v in vals)
        out.append(f"{ename} = {{ {vals_fmt} }}")
    out.append("")

    out.append("[altpe_sdk.models]")
    out.append("BaseApiModel")
    for mname, fields in models.items():
        if not fields:
            out.append(f"{mname}")
            continue
        inner = ", ".join(f"{n}: {t}" for n, t in fields)
        out.append(f"{mname}: {{ {inner} }}")
    out.append("")

    out.append("[altpe_sdk._sync_client.AlternativesPE]")
    for name, params, ret in methods:
        sig = f"{name}({params})"
        if ret:
            sig += f" -> {ret}"
        out.append(sig)
    out.append("")

    out.append("[altpe_sdk.mappings]")

    def fmt_sample(tag: str):
        if tag in mapping_samples:
            pairs = mapping_samples[tag]
            kv = ", ".join(
                f'{k}: "{v}"' if isinstance(v, str) else f"{k}: {v}" for k, v in pairs
            )
            out.append(f"{tag} (sample): {{ {kv} }}")

    fmt_sample("SECTORS")
    fmt_sample("THEMES")
    fmt_sample("LOCATIONS")
    fmt_sample("FUND_TYPES")
    out.append(
        "Full list via: from altpe_sdk.mappings import mappings; mappings.get_sector_choices(); mappings.get_theme_choices(); mappings.get_location_choices(); mappings.get_fund_type_choices()"
    )
    out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    enums = collect_enums(PKG / "enums.py")
    models = collect_models(PKG / "models.py")
    methods = collect_client_methods(PKG / "_sync_client.py")
    mapping_samples = collect_mapping_samples(PKG / "mappings.py")
    text = emit_llms(enums, models, methods, mapping_samples)
    (ROOT / "llms.txt").write_text(text)


if __name__ == "__main__":
    main()
