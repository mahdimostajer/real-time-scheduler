from main import schedule


def part_one(overrun_prob):
    number_of_aperiodic_jobs = 40
    schedule(overrun_probability=overrun_prob, number_of_processors=2, sum_util=0.5 * 2,
             number_of_aperiodic_jobs=number_of_aperiodic_jobs)
    schedule(overrun_probability=overrun_prob, number_of_processors=4, sum_util=0.5 * 4,
             number_of_aperiodic_jobs=number_of_aperiodic_jobs)
    schedule(overrun_probability=overrun_prob, number_of_processors=8, sum_util=0.5 * 8,
             number_of_aperiodic_jobs=number_of_aperiodic_jobs)
    schedule(overrun_probability=overrun_prob, number_of_processors=16, sum_util=0.5 * 16,
             number_of_aperiodic_jobs=number_of_aperiodic_jobs)


def part_two(overrun_prob):
    number_of_processors = 8
    schedule(overrun_probability=overrun_prob, number_of_processors=number_of_processors,
             sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=40)
    schedule(overrun_probability=overrun_prob, number_of_processors=number_of_processors,
             sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=80)
    schedule(overrun_probability=overrun_prob, number_of_processors=number_of_processors,
             sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=120)
    schedule(overrun_probability=overrun_prob, number_of_processors=number_of_processors,
             sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=160)


def section_two(number_of_processors):
    for i in range(100):
        schedule(overrun_probability=0.2, number_of_processors=number_of_processors,
                 sum_util=0.25 * number_of_processors, number_of_aperiodic_jobs=0)

    for i in range(100):
        schedule(overrun_probability=0.2, number_of_processors=number_of_processors,
                 sum_util=0.5 * number_of_processors, number_of_aperiodic_jobs=0)

    for i in range(100):
        schedule(overrun_probability=0.2, number_of_processors=number_of_processors,
                 sum_util=0.6 * number_of_processors, number_of_aperiodic_jobs=0)

    for i in range(100):
        schedule(overrun_probability=0.2, number_of_processors=number_of_processors,
                 sum_util=0.75 * number_of_processors, number_of_aperiodic_jobs=0)


def run_scenarios():
    # section 1

    part_one(overrun_prob=0.2)
    part_one(overrun_prob=0.1)
    part_one(overrun_prob=0.01)

    part_two(overrun_prob=0.2)
    part_two(overrun_prob=0.1)
    part_two(overrun_prob=0.01)

    schedule(overrun_probability=0.2, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)
    schedule(overrun_probability=0.1, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)
    schedule(overrun_probability=0.01, number_of_processors=8, sum_util=0.5 * 8, number_of_aperiodic_jobs=0,
             should_print=True)

    # section 2

    section_two(number_of_processors=2)
    section_two(number_of_processors=4)
    section_two(number_of_processors=8)
    section_two(number_of_processors=16)


if __name__ == "__main__":
    run_scenarios()
