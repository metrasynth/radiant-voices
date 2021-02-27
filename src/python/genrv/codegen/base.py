from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jinja2 import Environment

log = getLogger(__name__)


@dataclass
class CodeGenerator(ABC):
    spec_base: Union[Path, str]
    dest_base: Union[Path, str]
    fileformat: Dict[Any, Any] = field(init=False, repr=False)

    def __post_init__(self):
        self.spec_base = Path(self.spec_base)
        self.dest_base = Path(self.dest_base)
        fileformat_path = self.spec_base / "fileformat.yaml"
        with fileformat_path.open() as f:
            self.fileformat = yaml.safe_load(f)

    @abstractmethod
    def run(self, env: Environment):
        pass

    def write_file(self, path: Path, content: str):
        log.info("Writing %s", path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
