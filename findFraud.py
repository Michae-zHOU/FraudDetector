# Complete the function below.

def findViolations(datafeed):
    start_contractorList = {}
    completed_list = []
    fraud_list = []
    i = 0
    for line in datafeed:
        i+=1
        job_info = line.split(";")
        if job_info[1] == "START":
            if job_info[0] not in start_contractorList:
                start_contractorList[job_info[0]] = []
                start_contractorList[job_info[0]].append(i)
            else:
                start_contractorList[job_info[0]].append(i)
        else:
            contractor_name = job_info[0]
            invoice_list = job_info[1].split(',')
            fraud = ""
            if len(invoice_list) == 1:
                fraud = checkShortened(start_contractorList,completed_list,contractor_name,invoice_list[0],i)
                if fraud != "":
                    fraud_list.append(fraud)
            else:
                batch_shortened_list = batchCheckShortened(start_contractorList,completed_list,contractor_name,invoice_list,i)
                fraud_list.extend(batch_shortened_list)
                fraud = checkSuspicious(start_contractorList,completed_list,contractor_name,invoice_list,i)
                if fraud != "":
                    fraud_list.append(fraud)
    return fraud_list

def batchCheckShortened(start_contractorList,completed_job_list,contractor_name,invoice_list,end_time):
    pass_list = []
    fraud_list = []
    for start_time in start_contractorList[contractor_name]:
        i = 0
        for invoice in invoice_list:
            if checkBatchShortenedJob(completed_job_list,invoice,start_time):
                pass_list.append(start_time)
                break
    for start_time in start_contractorList[contractor_name]:
        if start_time not in pass_list:
            fraud_list.append(str(start_time)+";"+contractor_name+";SHORTENED_JOB")
    return fraud_list

def checkShortened(start_contractorList,completed_job_list,contractor_name,invoice,end_time):
    start_time = start_contractorList[contractor_name][0]
    if len(completed_job_list) == 0:
        return updateContractorList(start_contractorList,completed_job_list,contractor_name,invoice,start_time,end_time)
    for completed_job in completed_job_list:
        if completed_job[3] > int(invoice) and completed_job[1] < start_time:
            start_contractorList[contractor_name].pop(0)
            return str(start_time)+";"+contractor_name+";SHORTENED_JOB"
    return updateContractorList(start_contractorList,completed_job_list,contractor_name,invoice,start_time,end_time)

def checkBatchSuspicious(start_contractorList,start_time_list,completed_list,contractor_name,invoice_list,end_time):
    if len(invoice_list) == 1 and len(start_time_list) == 1:
        if checkBatchShortenedJob(completed_list,invoice,start_time_list[0]):
            updateContractorList(start_contractorList,completed_list,contractor_name,invoice_list[0],start_time_list[0],end_time)
            return True
        else:
            return False
    else:
        for start_time in start_time_list:
            for invoice in invoice_list:
                new_start_time_list = list(start_time_list)
                new_start_time_list.remove(start_time)
                new_inovoice_list = list(invoice_list)
                new_inovoice_list.remove(invoice)
                if checkBatchShortenedJob(completed_list,invoice,start_time) and checkBatchSuspicious(start_contractorList,new_start_time_list,completed_list,contractor_name,inovice_list,end_time,fraud_list):
                    updateContractorList(start_contractorList,completed_list,contractor_name,invoice,start_time,end_time)
                    return True
        return False

def checkSuspicious(start_contractorList,completed_list,contractor_name,invoice_list,end_time):
    start_time_list = start_contractorList[contractor_name]
    if not checkBatchSuspicious(start_contractorList,start_time_list,completed_list,contractor_name,invoice_list,end_time):
        return str(end_time)+";"+contractor_name+";SUSPICIOUS_BATCH"
    return ""

def checkBatchShortenedJob(completed_job_list,invoice,start_time):
    for completed_job in completed_job_list:
        if completed_job[3] > invoice and completed_job[1] < start_time:
            return False
    return True

def updateContractorList(start_contractorList,completed_list,contractor_name,invoice,start_time,end_time):
    start_contractorList[contractor_name].remove(start_time)
    completed_list.append([start_time,end_time,contractor_name,int(invoice)])
    return ""
