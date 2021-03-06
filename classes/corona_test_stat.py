from time import time
from typing import List

from utils.binary import bin_len
from classes.corona_testing import CoronaTesting


class CoronaTestStat:
    # Unique identifiers for the methods to create sample ids for subjects.
    ASC = 0
    DEC = 1
    RANDOM = 2
    OPPOSITE = 3

    def __init__(self, num_of_subjects: int = 0b11111111, num_of_test_cases: int = 1000,
                 infection_percentage: float = 2, sample_id_types: List = None):
        self.num_of_subjects = num_of_subjects
        self.num_of_test_cases = num_of_test_cases
        self.infection_percentage = infection_percentage
        self.sample_id_types = sample_id_types if sample_id_types else [self.ASC]
        self.num_of_sample_ids = len(self.sample_id_types)
        self.all_corona_test_cases = []
        self.num_of_test_kits_in_case = bin_len(num_of_subjects) * self.num_of_sample_ids
        self.running_time = 0

        self.all_infected = []
        self.all_results = []
        self.avg_infected = 0
        self.avg_potential_positive = 0
        self.avg_num_of_groups = {}

    def run_all_test_cases(self):
        """
        Creating every test case with the same parameters,
        run all the methods in a chronological order and updates overall statistics.
        """
        running_time = time()
        num_of_infected = 0
        num_of_potential_positive = 0
        for idx in range(self.num_of_test_cases):
            # Creating the test object and initialize the subject's names.
            test = CoronaTesting(self.num_of_subjects, test_name=f'{idx}')
            test.generate_subjects_by_num()
            # Adding multiple sample ids to each subject.
            for sample_id_type in self.sample_id_types:
                if sample_id_type == self.ASC:
                    test.add_num_sample_id()
                if sample_id_type == self.DEC:
                    test.add_num_sample_id(reverse=True)
                if sample_id_type == self.RANDOM:
                    test.add_random_sample_id()
                if sample_id_type == self.OPPOSITE:
                    test.add_opposite_sample_id()
            # Create dictionary with all the sample ids of each subject.
            test.generate_subjects_dict()
            # Generates sick subject randomly.
            test.generate_infected(self.infection_percentage)
            # Calculates the result of the testing on all subjects,
            # having the generated infected subjects among them to make some of the test positive.
            test.generate_test_result()
            test.find_potential_positive()
            # Narrow down the possible options for groups of subjects that matches the results.
            test.find_groups_that_match_result(max_size_of_group=2)

            # Updating the stats
            self.all_corona_test_cases.append(test)
            self.all_infected.append(test.infected_subjects)
            self.all_results.append(test.tests_results)
            num_of_infected = num_of_infected + len(test.infected_subjects)
            num_of_potential_positive = num_of_potential_positive + len(test.potential_positive)

        self.avg_infected = num_of_infected / self.num_of_test_cases
        self.avg_potential_positive = num_of_potential_positive / self.num_of_test_cases
        self.running_time = time() - running_time

    def show_statistics(self):
        print(f'*Statistics of {self.num_of_test_cases} test cases in {round(self.running_time, 2)}s:*' )
        print(f'Number of subjects in tast case: {self.num_of_subjects}')
        print(f'Infection percentage in each case: {self.infection_percentage}%')
        print(f'Number of Covid-19 test kits used: {self.num_of_test_kits_in_case}')
        # Todo - change to names instead of numbers
        self.show_sample_id_types()
        print(f'Average real Covid-19 positive subjects in case: {self.avg_infected}')
        print(f'Average potential Covid-19 positive subjects found by the algorithm: {self.avg_potential_positive}')

        print(f'---')

    def show_sample_id_types(self):
        sample_id_types_names = []
        for sample_id_type in self.sample_id_types:
            if sample_id_type == self.ASC:
                sample_id_types_names.append('ASC')
            if sample_id_type == self.DEC:
                sample_id_types_names.append('DEC')
            if sample_id_type == self.RANDOM:
                sample_id_types_names.append('RANDOM')
            if sample_id_type == self.OPPOSITE:
                sample_id_types_names.append('OPPOSITE')
        print(f'Methods of creating sample ids: {sample_id_types_names}')
