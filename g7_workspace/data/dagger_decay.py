import csv
import numpy as np
inputcsv='0_command.csv'
outputcsv='test_decay.csv'
def decay(diff,len,index,options):
    if options=='ex':
        sign=-1 if diff<0 else 1
        w=np.log(abs(int(diff)))/len
        return sign*np.exp(w*(index+1))
    elif options=='sigmoid':
        sign = -1 if diff < 0 else 1
        w=np.exp(abs(int(diff)))/len
        return np.log(w*(index+1))*sign
    elif options=='linear':
        sign = -1 if diff < 0 else 1
        w=abs(int(diff))/len
        return w*(index+1)*sign

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
        if len(command_queue)>40:
            adjust=command_queue[-1]["stage"]
            adjust_pre=command_queue[-2]["stage"]
            if adjust_pre=='0' and adjust=='1':
                change_number=command_queue[-1]["frame"]
                diff=int(command_queue[-1]["steering"])-int(command_queue[-2]["steering"])
                for index,command in enumerate(command_queue[:-1]):
                    print(command['steering'])
                    command['steering']=str(int(command['steering'])+int(decay(diff,len(command_queue),index+1,options='linear')))

            #   for i in command_queue:
            #     every i decay by little
            saving = command_queue.pop(0)
            csv_writer.writerow(saving)
