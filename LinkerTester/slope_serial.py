import numpy as np
from os.path import abspath

def main(inputPath, outputPath):
	input_file = open(inputPath, 'r')
	ncols = input_file.readline().split()[1]
	nrows = input_file.readline().split()[1]
	xllcorner = input_file.readline().split()[1]
	yllcorner = input_file.readline().split()[1]
	cellsize = float(input_file.readline().split()[1])
	NODATA = int(input_file.readline().split()[1])

        # read data in as n by m list of numpy floats
        # NOTE: Don't skip any lines here, the file pointer has already advanced
        # past the header to the data.
	data = np.loadtxt(input_file)
        input_file.close()
  
	slope_data = calc_slope(data, cellsize, NODATA)

        #set up header
        header_str = ("ncols %s\n"
                  "nrows %s\n"
                  "xllcorner %s\n"
                  "yllcorner %s\n"
                  "cellsize %f\n"
                  "NODATA_value %d"
                  % (ncols, nrows, xllcorner, yllcorner, cellsize, NODATA)
                 )

	#print slope_data
	np.savetxt(outputPath, slope_data, fmt='%5.2f', header=header_str, comments='')

def calc_slope(grid, cellsize, NODATA):
	slope_grid = np.zeros_like(grid)
	for row in range(len(grid)):
		for col in range((len(grid[0]))):
			slope_grid[row][col] = cell_slope(grid, row, col, cellsize, NODATA)

	return slope_grid

def cell_slope(grid, row, col, cellsize, NODATA):
	if grid[row][col] == NODATA:
		return NODATA
	
  #First, grab values for cells used in calculation
	nbhd = []
	for i in range(-1,2):
		for j in range(-1,2):
		#If out of bounds, log NODATA, these will be changed later.
			if row+i<=0 or row+i>=len(grid) or col+j<=0 or col+j>=len(grid[0]) or grid[row + i][col +j] == NODATA:
				nbhd.append(NODATA)
			else:
				nbhd.append(grid[row+i][col+j])

	dz_dx = (nbhd[2] + 2*nbhd[5] + nbhd[8] - (nbhd[0] + 2*nbhd[3] + nbhd[6])) \
				/ (8*cellsize)
	dz_dy = (nbhd[6] + 2*nbhd[7] + nbhd[8] - (nbhd[0] + 2*nbhd[1] + nbhd[2])) \
				/ (8*cellsize)

	slope = np.arctan(np.sqrt(np.square(dz_dx) + np.square(dz_dy)))

	return slope
	
if __name__ == '__main__':
	main()