def do_calculation(number1, number2):
    return number1 + number2

def compare_csv(csv_input,correct_csv):
    error_count = 0
    total_count = 0
    ind = 0

    for line in csv_input:
        line2 = correct_csv[ind]
        ind = ind + 1
        total_count = total_count + 1
        #print("Original")
        #print(line)
        #print("Original2")
        #print("Total Count : " +str(total_count))
        #print(line2)
        if line != line2:
            error_count = error_count + 1
            #print("Error Count : "+str(error_count))
    accuracy = (total_count - error_count) / total_count * 100
    return accuracy