
clc;
clear all;
close all;

%%%%%%%%%%%%%%%     KRIGIING     %%%%%%%%%%%%%%%
% Get the location of the sensors
Sensor_loc = readtable("sensors_locations.csv");

% Separating the lat , long coordinates
lat=Sensor_loc.lat;
lon=Sensor_loc.lon;

% Single day rainfall data for all sensors (random sample)
Rainy_Day_Data = [3.36; 14.16; 21.84; 1.68; 0; 7.2; 0.96; ...
    5.52; 15.84; 14.4; 8.88; 21.6; 5.76];  

figure;
geobubble(lat,lon,Rainy_Day_Data);

% Load Rainy days data
rain_table=readtable('Rain_Comprehensive_All_15Aug2023.csv');
rain_mat=table2array(rain_table(:,2:14));

% Getting the number of days with rainfall data and the number of sensors
n_rain = size(rain_mat,1); %number of rainy days
n_points = size(rain_mat,2); % number of sensors

% Distance  matrix for calculating distance btw sensors
dist = zeros(n_points,n_points);
for i = 1:n_points
    for j = i+1:n_points
        d = pos2dist([lat(i), lon(i)],[lat(j), lon(j)]);
        dist(i,j) = d;
        dist(j,i) = d;
    end
end
%%
%create data for variations
var_mat = zeros(n_points,n_points);

% counting the number of days for each entry in variation matrix.
count=n_rain *ones(n_points,n_points);

% Calculating the variation matrix from the rainfall matrix
for n=1:n_rain
    for i = 1:n_points
        for j = i+1:n_points

            if (sum(ismissing([rain_mat(n,i),rain_mat(n,j)]))==0) && ...
                    (rain_mat(n,i)+rain_mat(n,j)~=0)
                var_mat(i,j) = var_mat(i,j)+((rain_mat(n,i)-rain_mat(n,j))^2);
                var_mat(j,i) = var_mat(i,j);
            else
                count(i,j)= count(i,j)-1;
                count(j,i)= count(i,j);
            end
        end
    end
end

% Dividing each Variation matrix entry by the number of days count for its calculaton
var_mat = 0.5*var_mat./count;

%%%%%%%%%%  Create Raw Variogram    %%%%%%%%%%%
var_func_raw = zeros(nchoosek(n_points,2),2); %first column for h second for gamma
k = 0;
for i = 1:n_points
    for j = i+1:n_points
        k = k+1;
        var_func_raw(k,1) = dist(i,j);
        var_func_raw(k,2) = var_mat(i,j);
    end
end
var_func_raw = sort(var_func_raw); %sort
h_raw = var_func_raw(:,1);
var_raw = var_func_raw(:,2);
figure;
scatter(h_raw,var_raw);

xlabel('$h$ - Distance in km','Interpreter','Latex');
ylabel('$\gamma(h)$','Interpreter','Latex');
title('Raw Variogram');

%%%%%%%%%%%%%   CREATE EXPERIMENTAL VARIOGRAM   %%%%%%%%%%%%%
var_exp = [];
h_exp = [];
n_obs_exp = [];
bin_size = 2;

% now perform binning here with distance of bin_size for one Bin size
for bb=0:bin_size:h_raw(end)
    ind = find(h_raw >= bb & h_raw < bb + bin_size);
    bin_dist = h_raw(ind);
    bin_value = var_raw(ind);
    bin_dist_avg = mean(bin_dist);
    bin_value_avg = mean(bin_value);
    var_exp = [var_exp;bin_value_avg];
    h_exp = [h_exp;bin_dist_avg];
    n_obs_exp = [n_obs_exp; length(ind)];
end
figure;
scatter(h_exp,var_exp);
xlabel('$h$ - Distance in km','Interpreter','Latex');
ylabel('$\gamma(h)$','Interpreter','Latex');
title('Experimental variogram');

%%%%%%%%%%%%%%% THEORETICAL VARIOGRAM   %%%%%%%%%%%%

%use provided function to get theoretical variogram
a0 = max(h_exp); % initial value: sill
c0 = max(var_exp); % initial value: range
%get parameters of variogram fit
%L and sig_s(sigma squarred) are the parameters of the model and nugg is
%the nugget

[L,sig_s,nugg] = variogramfit(h_exp,var_exp,a0,c0,n_obs_exp,...
    'solver','fminsearchbnd','nugget',0,'model','gaussian',...
    'weightfun','none','plotit',false);
h_th = 0:0.1:h_exp(end);
%Gaussian variogram function
var_th = nugg + sig_s*(1-exp(-(h_th.^2)/(L^2)));
figure;
plot(h_th,var_th);
xlabel('$h$ - Distance in km','Interpreter','Latex');
ylabel('$\gamma(h)$','Interpreter','Latex');
title('Theoretical Variogram');

%%   **RAINFALL AT THE UNOBSERVED LOCATIONS**   %%

%load lake data
Namal_WS = kml2struct('Namal_WS_boundaryline.kml'); %load KML file
wb_lon = Namal_WS.Lon;
wb_lat = Namal_WS.Lat;

[Lon1_i,Lat1_i]=meshgrid(min(wb_lon):0.001:max(wb_lon),min(wb_lat):0.001:max(wb_lat));
%Remove the extra area than lake contributary
mask = ~inpolygon(Lon1_i,Lat1_i,wb_lon,wb_lat);

n= length(Rainy_Day_Data);
%% A*x=b %%
A=zeros(n+1,n+1);
for i = 1:n
    A(n+1,i)=1;
    A(i,n+1)=1;
    for j = i+1:n
        h=dist(i,j);
        a = -(nugg + sig_s*(1-exp(-(h^2)/(L^2))));
        A(i,j) = a;
        A(j,i) = a;
    end
end


AverageRain = zeros(length(rain_mat(:,1)),1);
for rainyday = 1:length(rain_mat(:,1))
    Rainy_Day_Data = rain_mat(rainyday,:)'
    indices = find(isnan(Rainy_Day_Data) == 1);
    indices = sort(indices, 'descend');
    Z_hat=zeros(size(Lon1_i));
    b = zeros(n+1,1);
    for i = 1:size(Lon1_i,1)
        for j=1:size(Lon1_i,2)
            copyA = A;
            for k = 1:n
                xi=[Lat1_i(i,j),Lon1_i(i,j)];
                x0=[lat(k),lon(k)];
                h0=pos2dist(xi,x0);
                b(k)= -(nugg + sig_s*(1-exp(-(h0^2)/(L^2))));
            end
            b(n+1)=1;
            copyB = b;
            copyRD = Rainy_Day_Data;
            for a = 1:length(indices)
                copyB(indices(a))=[];
                copyA(indices(a),:)=[];
                copyA(:,indices(a))=[];
                copyRD(indices(a))=[];
            end
            newN = length(copyRD);
            lambda=copyA\copyB;
            Z_hat(i,j)=lambda(1:newN)'*copyRD;
            %Z_var(i,j)=-b'*lambda;
        end
    end
    Z_hat(mask) = NaN;
    % Calculate the mean of total rainfal in namal contributary
    AverageRain(rainyday,1) = mean(Z_hat(~isnan(Z_hat)));
end
AverageRain=array2table(AverageRain);
finalMatrix = [rain_table, AverageRain];
writetable(finalMatrix, "Rain_ComprehensiveWithAverage.csv");
figure;
fv = surf2patch(Lon1_i,Lat1_i,zeros(size(Z_hat)),Z_hat);
patch(fv,'FaceColor','interp','EdgeColor','none')
hold on;
%%%%% Remove lat, long of missing data units %%%%%%%
for i=1:length(indices)
    lon(indices(i))=[];
    lat(indices(i))=[];
end
%plot only units having data available
s=scatter(lon,lat,'*r');
s.SizeData = 80;
p1 = plot(NaN,NaN,'*r');

% hold off;
% hold on;
% p2=plot(watershed_boundary_long,watershed_boundary_lat,'-k')

%hold off;
hc = colorbar;
legend('Rainfall data','Sensors Locations');
title(hc,'(mm)');
title('kriging predictions')
xlabel('Longitude')
ylabel('Latitude')

