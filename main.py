import csv
with open('in.csv', 'r') as rfile:
    with open('out.csv', 'w', newline='') as wfile:
        csv_reader = csv.reader(rfile)
        csv_writer = csv.writer(wfile)
        flag = 0
        for row in csv_reader:
            print(row)
            i = 0
            line = []
            for column in row:
                if i == 1 and len(column) > 1:
                    if column[1] > '4':
                        flag = 1
                        print(flag, column[1])
                        n_column = column[:-1] + '1'
                        line.append(n_column)
                    else:
                        line.append(column)
                else:
                    line.append(column)
                i += 1
            if len(line) > 1:
                csv_writer.writerow(line)
                print("wrote:", line)