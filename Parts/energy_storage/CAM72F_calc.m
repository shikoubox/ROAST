% battery CALB CAM 72 

v = 120;
c = 17e3;

v_cell = 3.2;

n_series = ceil(v/v_cell);

v_pack = v_cell*n_series;

ih_cell = 72;
c_series = v_pack*ih_cell; 

n_parallel = ceil(c/c_series);

n_cell = n_series*n_parallel;

m_cell = 1.9;
m_pack = n_cell*m_cell;

width_cell = 29e-3;
height_cell = 222e-3;
length_cell = 135e-3;

width = width_cell*n_series;
depth = length_cell*n_parallel;
height = height_cell;

volume = width*depth*height;

cell_price = 67; % EUR
pack_price = cell_price*n_cell*7.5; % DKK


