from pathlib import Path
from typing import Any, Dict, List, NewType, Set, Tuple, Union

Schema = NewType("Schema", Dict[str, Any])
PathLike = Union[Path, str]

Query = NewType("Query", List[Tuple[str, str]])  # To use in HTTP client
Body = NewType("Body", Dict[str, Any])
PathParameters = NewType("PathParameters", Dict[str, Any])
Headers = NewType("Headers", Dict[str, Any])

# A filter for endpoint / method
Filter = Union[str, List[str], Tuple[str], Set[str]]
