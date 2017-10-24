# For the uninitiated, Python multithreading uses threads to do parallel processing.
# This is the most common way to do parallel work in many programming languages.
# But CPython has the Global Interpreter Lock (GIL),
# which means that no two Python statements (bytecodes, strictly speaking)
# can execute at the same time. So this form of parallelization is only helpful
# if most of your threads are either not actively doing anything (for example, waiting for input),
# or doing something that happens outside the GIL (for example launching a subprocess or doing a numpy calculation).
# Using threads is very lightweight, for example, the threads share memory space.
#
# Python multiprocessing, on the other hand, uses multiple system level processes,
# that is, it starts up multiple instances of the Python interpreter.
# This gets around the GIL limitation, but obviously has more overhead.
# In addition, communicating between processes is not as easy as reading and writing shared memory.



import requests
from multiprocessing import Process
import os
import time
import csv
import datetime
import inspect





def gen_chunks(reader, chunksize=100):
    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk

def SplitCsvFile(path, inputfile):
    with open(path + inputfile, "r") as task_data_csv:
        csvreader = csv.reader(task_data_csv)
        header = next(csvreader)
        print("Breaking list into smaller chunks")
        chunks = gen_chunks(csvreader, chunksize=5000)
        print("Saving to CSV Files")
        it = 0
        for chunk in chunks:
            it += 1
            if it > 1000: #it's not going to create 1000 processes....
                print("File too large")
                break

            with open(path + str(it) + ".csv", "w") as output_file:
                csvwriter = csv.writer(output_file, lineterminator='\n')
                #csvwriter.writerow(header)
                for line in chunk:
                    csvwriter.writerow(line)

            print("Finished Saving Chunk " + str(it))
            output_file.close()
    task_data_csv.close()
    return it #return number of files which will be used for number of processes later..


def ApiCall(vin,country='CA'):
    r = requests.get('http://residualapi1.algprod1.wc.truecarcorp.com:40018/residual-services/services/vinSearch/trims?' + \
                    '&vin=' + str(vin) + '&country=' + str(country))
    data = r.json()
    return data

def Worker(path,chunkFileName):
    todayDate = datetime.date.today()
    with open(path + str(chunkFileName)+'.csv', 'r') as reader:
        csvreader = csv.reader(reader)
        # header = next(csvreader)
        with open(path + str(chunkFileName) + '_.csv', 'w') as writer:
            csvwriter = csv.writer(writer, delimiter=',', lineterminator='\n')
            #csvwriter.writerow(header)
            for row in csvreader:
                try:
                    originalData = ','.join(row[:6])
                    jsonData = ApiCall(row[0])
                except TypeError:
                    continue
                except:
                    print(row[0] +' is not able to match.\n')
                    writer.write(','.join([originalData,
                                        'N/A', #country
                                        'N/A', #VinModelYear
                                        'N/A', #VinAlgCode
                                        'N/A', #DateAdded
                                        ])+'\n')

                finally:
                    print(row[0] + ' is matched.\n')
                    for data in jsonData:
                        writer.write(','.join([originalData,
                                            'CA',
                                            str(data['modelYear']),
                                            str(data['algCode']),
                                            str(todayDate),
                                            ])+'\n')
        writer.close()
    reader.close()


def MergeAllChunks(path, inputfile, chunk):
    #Get header from original file first
    with open(path + inputfile,'r') as reader:
        csvreader = csv.reader(reader)
        header = next(csvreader)
        header+=(['Country','VinModelYear','VinAlgCode','DateAdded'])
    with open(path + 'Output.csv', 'w') as writer:
        writer.write(','.join(header) + '\n')
        for i in range(chunk):
            print('Merging File ' + str(i+1))
            with open(path + str(i+1) +'_.csv','r') as reader:
                for row in reader:
                    writer.write(row)

def CleanUp(path, chunk):
    for i in range(chunk):
        os.remove(path + str(i+1) + '.csv')
        os.remove(path + str(i+1) +'_.csv')


if __name__ == '__main__':
    start_time = time.time()
    pyFileName = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(pyFileName)) + '/'
    for csvfilename in os.listdir(path):
        if (csvfilename).endswith('.csv'):
            print(csvfilename)
            numberOfFiles = SplitCsvFile(path, csvfilename)
            start_time = time.time()
            jobs = []
            for i in range(numberOfFiles):
                p = Process(target=Worker, args=(path,str(i + 1),))
                jobs.append(p)
                p.start()
            for j in jobs:
                j.join()  # wait for all child processes to end first
            MergeAllChunks(path, csvfilename, numberOfFiles)
            CleanUp(path,numberOfFiles)

    print('Runtime: ' + str(time.time() - start_time))
    input('Press Enter to End.')


        #path = 'C:/Users/nnguyen/Desktop/_DecoderBrian/InputTest.csv'
