import pandas as pd


class ResultsSerializer():
    input_type = ''
    is_male_competition = True
    competiton_data: pd.DataFrame

    def __init__(
        self, input_type: str, is_male_competition: bool = True
    ) -> None:
        self.input_type = input_type
        self.is_male_competition = is_male_competition

    def main(self) -> None:
        self.get_data()
        self.calculate_results()

    def get_data(self, path: str = 'Decathlon.csv') -> None:

        # mens and womans competition have different events and order
        if self.input_type == 'csv':
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

            self.competiton_data = pd.read_csv(
                path, delimiter=';', names=header_names
            )

    def validate_data(self) -> None:
        pass

    def calculate_results(self) -> None:
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

        self.competiton_data['points'] = 0
        some = self.competiton_data['1500_metres']

        # and adding total points for all other events
        for event_name in self.competiton_data.keys():
            event_vars = POINTS_SYSTEM.get(event_name)

            # skip non event columns
            if not event_vars:
                continue

            # use track event formula to calculate points
            if event_vars['event'] == 'track':
                # some events results have to be converted to s
                event_results = self.competiton_data[event_name] * 100 \
                    if event_vars['convert_units'] \
                    else self.competiton_data[event_name]

                self.competiton_data['points'] += (
                    event_vars['A'] *
                    (event_vars['B'] - event_results) **
                    event_vars['C']
                ).astype(int)
            # use field event formula to calculate points
            elif event_vars['event'] == 'field':
                # some events results have to be converted to cm
                event_results = self.competiton_data[event_name] * 100 \
                    if event_vars['convert_units'] \
                    else self.competiton_data[event_name]

                self.competiton_data['points'] += (
                    event_vars['A'] *
                    (event_results - event_vars['B']) **
                    event_vars['C']
                ).astype(int)

            print(self.competiton_data)

    def order_results(self) -> None:
        pass

    def export_results(self) -> None:
        pass


if __name__ == '__main__':
    ResultsSerializer(input_type='csv').main()
