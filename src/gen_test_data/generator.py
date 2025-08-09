from __future__ import annotations

import importlib
import inspect
import json
import os
import pkgutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Type

from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory

from .config import DEFAULT_SETTINGS, Settings


@dataclass
class DiscoveredModel:
    qualified_name: str
    model_class: Type[BaseModel]


def _iter_modules(package_name: str) -> Iterable[str]:
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        return []

    if not hasattr(package, "__path__"):
        return [package_name]

    for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        yield module_info.name


def _is_pydantic_model(obj: object) -> bool:
    return inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel


def discover_models(settings: Settings = DEFAULT_SETTINGS) -> List[DiscoveredModel]:
    qualified_to_class: Dict[str, Type[BaseModel]] = {}
    for module_name in _iter_modules(settings.SCHEMAS_PACKAGE):
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        for name, obj in inspect.getmembers(module, _is_pydantic_model):
            qualified = f"{obj.__module__}.{obj.__name__}"
            if qualified in settings.EXCLUDE_MODELS:
                continue
            qualified_to_class[qualified] = obj

    return [DiscoveredModel(k, v) for k, v in sorted(qualified_to_class.items())]


def generate_instance(model_class: Type[BaseModel]) -> BaseModel:
    class _Factory(ModelFactory):
        __model__ = model_class

    return _Factory.build()


def _resolve_filename(dm: DiscoveredModel, settings: Settings) -> str:
    override = (settings.FILENAME_OVERRIDES or {}).get(dm.qualified_name)
    return override or dm.model_class.__name__


def generate_and_write(settings: Settings = DEFAULT_SETTINGS) -> List[Tuple[str, Path]]:
    Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    outputs: List[Tuple[str, Path]] = []
    for dm in discover_models(settings):
        instance = generate_instance(dm.model_class)
        data = json.loads(instance.model_dump_json(indent=2))

        base_name = _resolve_filename(dm, settings)
        for env in ("DEV", "QA", "PROD"):
            file_path = Path(settings.OUTPUT_DIR) / f"{env}_{base_name}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            outputs.append((env, file_path))

    return outputs
