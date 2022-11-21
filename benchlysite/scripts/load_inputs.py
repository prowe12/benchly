import csv
from benchly.models import ClimInputs


def run():
    with open('templates/climate_model_inputs.txt') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        ClimInputs.objects.all().delete()

        for row in reader:
            print(row)

            clim_inputs = ClimInputs(scenario=row[0],
                        start_year=row[1],
                        final_emiss=row[2])
            clim_inputs.save()
