import argparse
import logging
import time

from aoc2020.data import DataFactory
from aoc2020.solvers import PuzzleSolver, SolverFactory


logger = logging.getLogger("AoCRunner")


def run_solver(solver: PuzzleSolver, is_test: bool) -> None:
    correct = True
    a = time.time()
    solution_1 = solver.solve_1()
    b = time.time()
    if is_test:
        if solver.demo_result_1 is None:
            logger.warning(f"No demo result available for part one")
        elif solution_1 != solver.demo_result_1:
            logger.error(
                f"[Part one] Expected result {solver.demo_result_1}, "
                f"got {solution_1}."
            )
            correct = False
    else:
        logger.info(
            f"[Part one]: Solution is {solution_1} "
            f"(solved in {(b-a)*1000.:.2f}ms)"
        )

    a = time.time()
    solution_2 = solver.solve_2()
    b = time.time()
    if is_test:
        if solver.demo_result_2 is None:
            logger.warning(f"No demo result available for part two")
        elif solution_2 != solver.demo_result_2:
            logger.error(
                f"[Part two] Expected result {solver.demo_result_2}, "
                f"got {solution_2}."
            )
            correct = False
    else:
        logger.info(
            f"[Part two]: Solution is {solution_2} "
            f"(solved in {(b-a)*1000.:.2f}ms)"
        )

    if is_test and correct:
        logger.info(f"Congrats, both demo parts verified correctly!")


def run(day: int) -> None:
    demo_file = DataFactory.get_demo_file(day=day)
    demo_solver = SolverFactory.create_solver(day=day, input_file=demo_file)
    general_file = DataFactory.get_input_file(day=day)
    general_solver = SolverFactory.create_solver(day=day, input_file=general_file)

    # Run demo
    logger.info(f"Running demo")
    run_solver(solver=demo_solver, is_test=True)
    logger.info(f"")

    # Run actual solver
    logger.info(f"Running solver")
    run_solver(solver=general_solver, is_test=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Solve an advent of code puzzle"
    )
    parser.add_argument("day", type=int, help="Day of puzzle to solve")
    parser.add_argument(
        "-v", "--verbose", help="Output debug logging", action="store_true"
    )
    args = parser.parse_args()
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)
    run(day=args.day)


if __name__ == "__main__":
    main()
