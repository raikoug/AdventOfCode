from pathlib import Path
import sys

# get current absolute folder path : /path/to/this/file/main.pt
folder = Path(__file__).parent.absolute()
pythonclass = folder / Path('../../../../')
sys.path.append(str(pythonclass))

from pythonclass import AOC
CURRENT_YEAR = int(folder.parent.parent.parent.name)

