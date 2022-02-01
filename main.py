import csv
import json


class ResultsSerializer():
    """Gets competition data and serializes it to JSON file"""
    input_type = ''
    is_male_competition = True
    competiton_data = {}

    def __init__(
        self, input_type: str, is_male_competition: bool = True
    ) -> None:
        self.input_type = input_type
        self.is_male_competition = is_male_competition

    def defaultCSV(self) -> None:
        """
        the process for taking the default file in the same folder as project
        and exporting to results.json
        """
        self.get_data('Decathlon.csv')
        self.calculate_results()
        self.order_and_evaluate_results()
        self.export_to_json()

    def get_data(self, path: str) -> None:
        """Get's the data from the source"""
        if self.input_type == 'csv':
            # mens and womans competition have different events and order
            header_names = (
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

            with open(path, mode='r') as file:
                reader = csv.DictReader(
                    file, fieldnames=header_names, delimiter=';'
                )

                self.competiton_data = [row for row in reader]

    def calculate_results(self) -> None:
        """
        Calculate how many points competitors have won and add it to 
        competiton_data dictionary
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
        for contestant in self.competiton_data:
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
        competiton_data dictionary
        """
        self.competiton_data.sort(key=lambda x: x.get('points'), reverse=True)

        # a list or ordered results
        list_of_points = list(map(lambda x: x['points'], self.competiton_data))

        # evaluate won positions
        for index, competitor in enumerate(self.competiton_data):

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

    def export_to_json(self) -> None:
        """Exports data to json file"""
        json_results = json.dumps(self.competiton_data, indent=4)

        with open('results.json', 'w') as file:
            file.write(json_results)


if __name__ == '__main__':
    ResultsSerializer(input_type='csv').defaultCSV()
