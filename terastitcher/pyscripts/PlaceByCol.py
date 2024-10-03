# Hsuan Lee @ LCT
# Modified on 01/2022


import os
import numpy as np
import sys

def find_parameter(line, string):
    index_string = line.find(string)
    parameter_start = line.find('"', index_string)
    parameter_end = line.find('"', parameter_start+1)
    
    return line[parameter_start+1:parameter_end]



# read the col and row from filename
def read_row_col(filename):
    with open(filename) as file:
        lines = file.readlines()
        Lines = [line.rstrip() for line in lines]

    for line in Lines:

        if 'stack_rows="' in line:
            row = int(find_parameter(line, 'stack_rows='))
            col = int(find_parameter(line, 'stack_columns='))

    return row, col

# read the xml file into arrays
def read_xml(filename,abs_disp,cal_disp):
    with open(filename) as file:
        lines = file.readlines()
        Lines = [line.rstrip() for line in lines]

    for line in Lines:

        if 'ROW=' in line:
            row = int(find_parameter(line, 'ROW='))
            col = int(find_parameter(line, 'COL='))
            abs_disp[row][col][0] = int(find_parameter(line, 'ABS_V='))
            abs_disp[row][col][1] = int(find_parameter(line, 'ABS_H='))

        if 'NORTH' in line:
            direction = 0
        elif 'EAST' in line:
            direction = 1
        elif 'SOUTH' in line:
            direction = 2
        elif 'WEST' in line:
            direction = 3

        if 'V displ=' in line:
            cal_disp[row][col][direction][0][0] = int(find_parameter(line, 'V displ='))
            cal_disp[row][col][direction][0][1] = float(find_parameter(line, 'reliability='))
            cal_disp[row][col][direction][0][2] = float(find_parameter(line, 'nccPeak='))
            cal_disp[row][col][direction][0][3] = float(find_parameter(line, 'nccWidth='))
            cal_disp[row][col][direction][0][4] = float(find_parameter(line, 'nccWRangeThr='))
            cal_disp[row][col][direction][0][5] = float(find_parameter(line, 'nccInvWidth='))
            cal_disp[row][col][direction][0][6] = float(find_parameter(line, 'delay='))
        elif 'H displ=' in line:
            cal_disp[row][col][direction][1][0] = int(find_parameter(line, 'H displ='))
            cal_disp[row][col][direction][1][1] = float(find_parameter(line, 'reliability='))
            cal_disp[row][col][direction][1][2] = float(find_parameter(line, 'nccPeak='))
            cal_disp[row][col][direction][1][3] = float(find_parameter(line, 'nccWidth='))
            cal_disp[row][col][direction][1][4] = float(find_parameter(line, 'nccWRangeThr='))
            cal_disp[row][col][direction][1][5] = float(find_parameter(line, 'nccInvWidth='))
            cal_disp[row][col][direction][1][6] = float(find_parameter(line, 'delay='))

    #print(abs_disp)
    #print(cal_disp)
    
    return abs_disp, cal_disp
    

def stitch_col_first(abs_disp,cal_disp, V_pixel, H_pixel,good_row_method):
    # stitch individual columns
    for col in range(abs_disp.shape[1]):

        # stitch row x+1 to row x
        for row in range(abs_disp.shape[0]-1):

            #change by NORTH displacement
            abs_disp[row+1][col][0] = int(abs_disp[row][col][0] - cal_disp[row+1][col][0][0][0])
            abs_disp[row+1][col][1] = int(abs_disp[row][col][1] - cal_disp[row+1][col][0][1][0])
            abs_disp = abs_disp.astype(int)
    
    # calculate columns shift 
    column_shift_V = []
    column_shift_H = []
    
    #sum_over_row_average = np.sum(abs_disp,0)/num_row
    sum_over_row_average_V = []
    sum_over_row_average_H = []
      
    
    # scan over row, and choose the most reliable rows
    good_row = []
    
    
    if good_row_method == 'threshold':
        print("Determine good row:")
        for row in range(abs_disp.shape[0]):
            print(cal_disp[row,1:,3,0,1])
            print(cal_disp[row,1:,3,0,2])
            print(cal_disp[row,1:,3,0,3])
            print("")
            if sum(cal_disp[row,1:,3,0,1]>0.75) == (abs_disp.shape[1] - 1):
                good_row.append(row)

        # if the list is empty, choose the top three reliable rows
        if not good_row:
            a = np.argsort(np.mean(cal_disp[:,1:,3,0,1],1)) 
            good_row = a[-3:]
    else:
        print(abs_disp.shape[0])
        if abs_disp.shape[0] == 1: # only one row
            good_row = [0]        
        elif isinstance((abs_disp.shape[0]/2),int): # even rows
            good_row = [int(abs_disp.shape[0]/2-0.5),int(abs_disp.shape[0]/2+0.5)]
        else: # odd rows
            good_row = [int(abs_disp.shape[0]/2-1), int(abs_disp.shape[0]/2), int(abs_disp.shape[0]/2+1)]
    
    
    print("Good row:", good_row)
            
    # average column positions from the good_row
    for col in range(abs_disp.shape[1]):
        sum_over_row_average_V.append(np.mean(abs_disp[good_row,col,0]))
        sum_over_row_average_H.append(np.mean(abs_disp[good_row,col,1]))


    print('average V over row:', sum_over_row_average_V)
    print('average H over row:', sum_over_row_average_H)
        
    
    for col in range(abs_disp.shape[1]-1):
        shift_V_weight = 0
        V_weight = 0
        previous_V_shift = 0

        shift_H_weight = 0
        H_weight = 0
        previous_H_shift = -H_pixel # set as H_pixel
        
        # average all the rows (disp*reliability)
        for row in range(abs_disp.shape[0]):
            if cal_disp[row][col+1][3][0][1] * cal_disp[row][col+1][3][1][1]> 0.64:
                shift_V_weight = shift_V_weight + cal_disp[row][col+1][3][0][0]*cal_disp[row][col+1][3][0][1]
                V_weight = V_weight + cal_disp[row][col+1][3][0][1]

                shift_H_weight = shift_H_weight + cal_disp[row][col+1][3][1][0]*cal_disp[row][col+1][3][1][1]
                H_weight = H_weight + cal_disp[row][col+1][3][1][1]
                
        #column_shift_V.append(shift_V_weight/V_weight + (sum_over_row_average[col+1][0] - sum_over_row_average[col][0]))
        #column_shift_H.append(shift_H_weight/H_weight + (sum_over_row_average[col+1][1] - sum_over_row_average[col][1]))  

        try:
            column_shift_V.append(shift_V_weight/V_weight + (sum_over_row_average_V[col+1] - sum_over_row_average_V[col]))
            column_shift_H.append(shift_H_weight/H_weight + (sum_over_row_average_H[col+1] - sum_over_row_average_H[col]))
            previous_V_shift = shift_V_weight/V_weight
            previous_H_shift = shift_H_weight/H_weight

        # if all of the columns are not reliable, use the shift from previous column
        except ZeroDivisionError:
            column_shift_V.append(previous_V_shift + (sum_over_row_average_V[col+1] - sum_over_row_average_V[col]))
            column_shift_H.append(previous_H_shift + (sum_over_row_average_H[col+1] - sum_over_row_average_H[col]))

        print(previous_V_shift, previous_H_shift)
        print(sum_over_row_average_H[col+1], sum_over_row_average_H[col])
    
    print('')
    print('Before moving by column:')
    print(abs_disp)


        
    # shift whole columns (accumulated over columns)
    accumulate_shift_V = 0
    accumulate_shift_H = 0
    
    
    
    
    
    for col in range(abs_disp.shape[1]-1):

        # stitch row x+1 to row x
        accumulate_shift_V = accumulate_shift_V + column_shift_V[col]
        accumulate_shift_H = accumulate_shift_H + column_shift_H[col]

        for row in range(abs_disp.shape[0]):

            #change by WEST displacement            
            abs_disp[row][col+1][0] = int(abs_disp[row][col+1][0] - accumulate_shift_V)
            abs_disp[row][col+1][1] = int(abs_disp[row][col+1][1] - accumulate_shift_H)
            
    abs_disp = abs_disp.astype(int)

    return abs_disp, cal_disp

def generate_merging_xml(filename, abs_disp, cal_disp):
    with open(filename) as file:
        lines = file.readlines()
        Lines = [line.rstrip() for line in lines]

    file1 = open('xml_merging.xml','w')
        
    for line in Lines:

        if 'ROW=' in line:
            
            row = int(find_parameter(line, 'ROW='))
            col = int(find_parameter(line, 'COL='))
            try:
                file1.write(line[:line.find('ABS_V=')] + 'ABS_V="' + str(abs_disp[row][col][0]) + '" ABS_H="' + str(abs_disp[row][col][1]) + '" '+ line[line.find('ABS_D='):]+ '\n')                
            except IndexError:
                print(row,col)
                print((abs_disp[row][col][0]))
        
        else:
            file1.write(line + '\n')



if __name__ == '__main__' :
    #xml_displthres = r'F:\stitching_bad_ones\20211204_19_21_33_HTBatch12_9_Autofluor_NeuN_cFos_destriped_DONE\Ex_647_Em_690_MIP_Middle\xml_displthres.xml'
    filename = sys.argv[1] 

    print(filename)
    os.chdir(filename[:filename.rindex("xml_displthres")])
    num_row, num_col= read_row_col(filename)


    #row, col, V/H displacenment
    abs_disp = np.zeros((num_row,num_col,2)) 

    #row, col, NESW, V/H, displ/reliability/nccPeak/nccWidth/nccRangeThr/nccInvWidth/delay
    cal_disp = np.zeros((abs_disp.shape[0], abs_disp.shape[1], 4, 2, 7) )





    abs_disp, cal_disp = read_xml(filename,abs_disp,cal_disp)

    abs_disp, cal_disp = stitch_col_first(abs_disp,cal_disp, 1440, 1800, 'None')

    generate_merging_xml(filename, abs_disp, cal_disp)
