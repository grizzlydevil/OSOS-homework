import csv
import json


class CompetitionDataReceiver():
    """
    Get's competition data and creates a list of competor dicts with it
    """
    is_male_competition = True
    competition_data = []

    def __init__(self, is_male_competition: bool) -> None:
        self.is_male_competition = is_male_competition

    def _get_competition_headers(self) -> tuple:
        """mens and womans competition have different events and order"""
        return (
                'full_name',
                '100_metres',
                'long_jump',
                'shot_put',
                'high_jump',
                '400_metres',
                '110_metres_hurdles',
                'discus_throw',
                'pole_vault',
                'javelin_throw',
                '1500_metres'
            ) if self.is_male_competition else (
                'full_name',
                '100_metres',
                'discus_throw',
                'pole_vault',
                'javelin_throw',
                '400_metres',
                '100_metres_hurdles',
                'long_jump',
                'shot_put',
                'high_jump',
                '1500_metres'
            )

    def set_csv_data(self, path: str) -> None:
        """Sets the competition data from the source"""
        header_names = self._get_competition_headers()
        with open(path, mode='r') as file:
            reader = csv.DictReader(
                file, fieldnames=header_names, delimiter=';'
            )

            self.competition_data = [row for row in reader]

    def get_data(self) -> list:
        """returns loaded data as dictionary"""
        return self.competition_data


class ResultsProcessor():
    """Calculates and Orders competition data"""
    competition_data = []

    def __init__(self, competition_data: list) -> None:
        self.competition_data = competition_data

    def calculate_results(self) -> None:
        """
        Calculate how many points competitors have won and add it to
        athletes dictionary
        """
        POINTS_SYSTEM = {
            '100_metres': {'A': 25.4347, 'B': 18, 'C': 1.81, 'event': 'track',
                           'convert_units': False},
            'long_jump': {'A': 0.14354, 'B': 220, 'C': 1.4, 'event': 'field',
                          'convert_units': True},
            'shot_put': {'A': 51.39, 'B': 1.5, 'C': 1.05, 'event': 'field',
                         'convert_units': False},
            'high_jump': {'A': 0.8465, 'B': 75, 'C': 1.42, 'event': 'field',
                          'convert_units': True},
            '400_metres': {'A': 1.53775, 'B': 82, 'C': 1.81, 'event': 'track',
                           'convert_units': False},
            '110_metres_hurdles': {'A': 5.74352, 'B': 28.5, 'C': 1.92,
                                   'event': 'track', 'convert_units': False},
            '100_metres_hurdles': {'A': 5.74352, 'B': 28.5, 'C': 1.92,
                                   'event': 'track', 'convert_units': False},
            'discus_throw': {'A': 12.91, 'B': 4, 'C': 1.1, 'event': 'field',
                             'convert_units': False},
            'pole_vault': {'A': 0.2797, 'B': 100, 'C': 1.35, 'event': 'field',
                           'convert_units': True},
            'javelin_throw': {'A': 10.14, 'B': 7, 'C': 1.08, 'event': 'field',
                              'convert_units': False},
            '1500_metres': {'A': 0.03768, 'B': 480, 'C': 1.85,
                            'event': 'track', 'convert_units': True}
        }

        # loop over contestants
        for contestant in self.competition_data:
            contestant['points'] = 0

            # loop over events
            for event_name in contestant.keys():
                event_vars = POINTS_SYSTEM.get(event_name)

                # skip non event columns
                if not event_vars:
                    continue

                # skip this event if the result is 0 or empty
                if not contestant[event_name]:
                    continue

                # use track event formula to calculate points
                if event_vars['event'] == 'track':

                    # 1500_metres results have to be converted to seconds
                    if event_name == '1500_metres':
                        first_dot = contestant[event_name].find('.')
                        event_result = \
                            float(contestant[event_name][0:first_dot]) * 60 +\
                            float(contestant[event_name][first_dot + 1:])
                    else:
                        event_result = float(contestant[event_name])

                    # track event formula
                    contestant['points'] += int(
                        event_vars['A'] *
                        (event_vars['B'] - event_result) ** event_vars['C']
                    )

                # use field event formula to calculate points
                elif event_vars['event'] == 'field':

                    # some events results have to be converted to cm
                    event_result = float(contestant[event_name]) * 100 \
                        if event_vars['convert_units'] \
                        else float(contestant[event_name])

                    # field event formula
                    contestant['points'] += int(
                        event_vars['A'] *
                        (event_result - event_vars['B']) **
                        event_vars['C']
                    )

    def order_and_evaluate_results(self) -> None:
        """
        Orders the cometitors by place taken and adds won place to
        athletes dictionary
        """
        self.competition_data.sort(key=lambda x: x.get('points'), reverse=True)

        # a list or ordered results
        list_of_points = list(
            map(lambda x: x['points'], self.competition_data)
        )

        # evaluate won positions
        for index, competitor in enumerate(self.competition_data):

            # only one competitor takes this place
            if list_of_points.count(competitor['points']) == 1:
                competitor['position'] = str(index + 1)

            # assign multiple positions to competitors with same results
            else:
                # first index who has same amount of points
                first_same_points = list_of_points.index(competitor["points"])

                # last index place who has same amount of points
                last_same_points = len(list_of_points) -\
                    list_of_points[::-1].index(competitor['points'])

                competitor['position'] = f'{first_same_points + 1}-' +\
                    f'{last_same_points}'

    def get_processed_results(self) -> list:
        self.calculate_results()
        self.order_and_evaluate_results()

        return self.competition_data


class ResultsSerializer():
    """Serializes and exports data"""
    results = []

    def __init__(self, results) -> None:
        self.results = results

    def export_to_json_file(self, file_name: str) -> None:
        """Exports data to json file"""
        json_results = json.dumps(self.results, indent=4)

        with open(file_name, 'w') as file:
            file.write(json_results)


def export_file_to_json(file: str, exported_file_name: str):
    competition_data_receiver = CompetitionDataReceiver(True)
    competition_data_receiver.set_csv_data(file)
    competition_data = competition_data_receiver.get_data()

    results_processor = ResultsProcessor(competition_data)
    processed_results = results_processor.get_processed_results()

    results_serializer = ResultsSerializer(processed_results)
    results_serializer.export_to_json_file(exported_file_name)


if __name__ == '__main__':
    export_file_to_json('Decathlon.csv', 'res.json')
