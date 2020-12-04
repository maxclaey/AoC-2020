import argparse
import logging
import pkg_resources
from pathlib import Path

import mako.exceptions
import mako.template

logger = logging.getLogger("InitSolver")


def init_solution(data_folder: Path, solver_folder: Path, day: int):
    # Check if data folder is valid
    demo_data_folder = data_folder / "demo_files"
    input_data_folder = data_folder / "input_files"
    if not demo_data_folder.is_dir() or not input_data_folder.is_dir():
        logger.error(f"'{str(data_folder)}' is not a valid data folder")
        return

    # Check if data files are not existing yet
    demo_file = demo_data_folder / f"day{day}.txt"
    input_file = input_data_folder / f"day{day}.txt"
    if demo_file.is_file() or input_file.is_file():
        logger.error(f"Data file(s) already exist")
        return

    # Check if solver folder is valid
    impl_folder = solver_folder / "implementations"
    if not impl_folder.is_dir():
        logger.error(f"'{str(solver_folder)}' is not a valid solver folder")
        return

    # Check if script file is not existing yet
    script_file = impl_folder / f"day{day}.py"
    if script_file.is_file():
        logger.error(f"The solver file '{str(script_file)}' already exists")
        return

    template_path = pkg_resources.resource_filename(__package__, "dayx.mako")
    # Load the template
    try:
        t = mako.template.Template(filename=template_path)
    except mako.exceptions.SyntaxException:
        logger.error(f"Template {template_path} contains a syntax error")
        return
    except FileNotFoundError:
        logger.error(f"Template {template_path} not found")
        return

    # Render the template and save
    rendered = t.render(day=day)
    with script_file.open(mode="w") as f:
        f.write(rendered)

    # Create empty data files
    with demo_file.open(mode="w"):
        pass
    with input_file.open(mode="w"):
        pass
    logger.info(f"Script file and data files created")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Create placeholders for a new solver"
    )
    parser.add_argument("day", type=int, help="Day of puzzle to solve")
    parser.add_argument(
        "-d", "--data_folder", help="Data folder", required=True
    )
    parser.add_argument(
        "-s", "--solver_folder", help="Solver folder", required=True
    )
    args = parser.parse_args()

    init_solution(
        data_folder=Path(args.data_folder),
        solver_folder=Path(args.solver_folder),
        day=args.day,
    )


if __name__ == "__main__":
    main()
