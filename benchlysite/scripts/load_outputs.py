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
                        f_ha=row[2],
                        atmos_co2=row[3],
                        ocean_co2=row[4],
                        ocean_ph=row[5],
                        t_C = row[6],
                        t_F = row[7],
                        t_anomaly = row[8],
                        albedo = row[9],
                        f_oa = row[10],
                        f_la = row[11],
                        tot_ha = row[12]
)
            clim_outputs.save()

            # new_team = Team(
            # nickname = team_name,
            # employee_id = employee_id,
            # department_id = Department.objects.get(password = password, department_name = department_name)
