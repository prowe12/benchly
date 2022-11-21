import csv
from benchly.models import ClimOutputs, ClimInputs


def run():
    with open('templates/climate_model_outputs.txt') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        ClimOutputs.objects.all().delete()

        for row in reader:
            print(row)

            # scenario id, year, atmospheric co2, oceanic co2
            clim_outputs = ClimOutputs(scenario=ClimInputs.objects.get(scenario=int(row[0])),
                        year=row[1],
                        atmos_co2=row[2],
                        ocean_co2=row[3])
            clim_outputs.save()

            # new_team = Team(
            # nickname = team_name,
            # employee_id = employee_id,
            # department_id = Department.objects.get(password = password, department_name = department_name)
