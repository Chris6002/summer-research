import csv

inputcsv='0_command.csv'
outputcsv='test.csv'
with open(inputcsv) as csv_file, open(outputcsv, 'w') as out_file:
    csv_reader = csv.DictReader(csv_file)
    csv_writer = csv.DictWriter(out_file, csv_reader.fieldnames)
    csv_writer.writeheader()
    command_queue=[]
    for row in csv_reader:
        # print(row)
        command_queue.append(row)
        # for i in command_queue:
        #     print(i)
        if len(command_queue)>10:
            adjust=command_queue[-1]["stage"]
            adjust_pre=command_queue[-2]["stage"]
            if adjust_pre=='0' and adjust=='1':
                print(command_queue[-1]["frame"])
            # TODO:
            # for i in command_queue:
            #     every i decay by little
            saving = command_queue.pop(0)


                # csv_writer.writerow(saving)
