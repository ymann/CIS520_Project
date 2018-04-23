data = load("all_gun_data.csv"); 
data2 = data; 

%%
ncol = size(data, 2);
nrow = size(data, 1); 

%%
arr_missing = zeros(ncol, 1); 
arr_frac_missing = zeros(ncol, 1); 

%%
for c = 1: ncol 
    col = data(:, c); 
    avg_col = sum(col((col > -1), :))/nrow; 
    data2(col == -1, c) = avg_col; 
    
    n_missing = size(col(col == -1), 1); 
    arr_missing(c, 1) = n_missing; 
    arr_frac_missing(c, 1) = n_missing/nrow; 
end


