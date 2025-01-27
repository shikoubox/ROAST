%% Initialization:
clc
clear

%% Route parameters:

% TRAVLE_HOURS = [9, 9.5, 9.5, 9.5, 9.5, 4]; % [Hours]

time.day.start = [10 8  8  8  8  8];
time.day.end   = [17 17 17 17 17 14];
time.day.break = [1  1  1  1  1  1] + [0.5 0.5 0.5 0.5 0.5 0.5]; % Probably increase to two Hours as drivers need breaks outside the ordenary ones.
time.day.travle = time.day.end - time.day.start - time.day.break;
time.total = sum(time.day.travle);
time.day.available = [1 1 1 1 1 8/12]
disp(time.day.travle)


%%
% TRAVLE_HOURS = [9, 9.5, 9.5, 9.5, 9.5, 4]; % [Hours]
% t_tot = sum(TRAVLE_HOURS); % [Hours] The total number of hours we have to drive the route
    % TRAVLE_TIME = TRAVLE_TIMES(1) % maximum travle time in [s]
    % SIMTIMES = TRAVLE_TIMES + 3600;
    % SIM_TIME = TRAVLE_TIME + 3600; % Allowed travle time + One hour
    % STEP_SIZE = 10;
location.start = 0;
location.tennant_creek = 986;
location.Coober_Pedy = 2178;
location.Adelaide = 3020;
location.overNight1 = mean([location.tennant_creek,location.start]);
location.overNight2 = mean([location.Coober_Pedy,location.tennant_creek]);
location.overNight3 = mean([location.Adelaide,location.Coober_Pedy]);

p.dist = [location.overNight1 - location.start ,...
          location.tennant_creek - location.overNight1,...
          location.overNight2 - location.tennant_creek,...
          location.Coober_Pedy - location.overNight2,...
          location.overNight3 - location.Coober_Pedy,...
          location.Adelaide - location.overNight3]
% p.dist = [588, 986-588, 1493-986, ...
%                     2178-1493, 2720-2178, ...
%                     3020-2720].*1000; % Travle distance in [m]
    % TRAVLE_DISTANCE = TRAVLE_DISTANCES(1);
    % SIM_TIME_VECTOR = 0:STEP_SIZE:SIM_TIME;
%% Solar Power:
panels.area = 5; %[m^2]
energy.days = 7.5*ones(1,6);
panels.eff = 0.22;
energy.power = panels.area .* panels.eff .* energy.days .* time.day.available;
energy.solar.total = sum(energy.power);
%% Charging Power:
%% Energy from charging [kWh]
disp(" ")
% % % % P_sun_and_charge = 70 % [kWh] Total input power, minus the initial power from the battery 
% % % % P_batreq  =    % Required initial battery power to complete the race
time.stage_location.charge = [3.5, 3.5];
time.stage_location.name   = ["Tennant Creek", "Coober Pedy"];
time.stage_location.total = sum(time.stage_location.charge);
t_staging_locations = 2*3.5; %[Hours] Total time available to charge externally at the two staging locaitons.
% We can charge from sundown 19:30 or 19:00 depending on their definition
% of sundown, until 23:00. This results in a charging time of 2*3.5Hours =
% 7 hours.

I_SL = [6, 30];               % [A] possible range of charging currents
V_SL = [216.2 , 253];         % [Vrms] possible range of charging voltages
P_SL = V_SL.'*I_SL;           % [W] The range of Watts we can charge at staging locations
P_SLmax = max(P_SL,[],'all'); % [W] maximum amount of Watts per hour we can charge at staging locations
P_SLmean = mean(mean(P_SL));
E_from_charging = P_SLmax * time.stage_location.total;
disp(strcat("The energy we expect to get from the Staging Locations is:"))
disp(strcat("    E_from_charging = ",num2str(E_from_charging*1e-3),"kWh"))

%%
p.velocity.target = (p.dist)./time.day.travle
p.velocity.ms = p.velocity.target/3.6
p.velocity.mean = mean(p.velocity.ms);
disp(p.velocity.mean); % This is one of the parameters we should minimize
p.velocity.set = 22;
%% Energy consumption by things other than the motor:
Power.other = 150 % [W]
%% Car Parameters
battery.cell.power_density  = 0.127; % kWh/kg 
% battery.cell.power_density  = 0.500; % kWh/kg 
battery.capacity            = 25; %kWh
car.mass.battery            = battery.capacity / battery.cell.power_density
car.mass.shell              = 150;
car.mass.chassis            = 250;
monocoque = false
if monocoque
    car.mass.shell              = 150;
    car.mass.chassis            = 100;
end
car.mass.motor              = 21;
car.mass.motor_driver       = 10;
car.mass.other_stuff        = 100;
car.mass.wheels             = 14*4
car.mass.passenger          = 80;
car.passengers              = 2;
car.mass.no_passengers      = car.mass.battery + ...
                              car.mass.shell + ...
                              car.mass.chassis + ...
                              car.mass.motor + ...
                              car.mass.motor_driver + ...
                              car.mass.other_stuff + ...
                              car.mass.wheels;
car.mass.total              = car.mass.no_passengers + car.mass.passenger * car.passengers;
car.r_wheel                 = 0.62/2;
car.Crr                     = 0.0035;
car.CdA                     = 0.45; % Skulle meget gerne blive mindre :) Målet er 0.15 #NEMT
double_krum = false;
if double_krum
    car.CdA                 = 0.2;
end
car.efficiency.motor        = 0.91;
car.efficiency.drive_train  = 0.82;
car.efficiency.driver       = 0.99;
car.efficiency.battery      = 0.99;
car.efficiency.mppt         = 0.97;
car.efficiency.solar_panels = 0.99;

nat.g = 9.81;
nat.rho = 1.2754;%1.184; % air density
road.slope = 0;
road.acceleration = 0;

Force.drag         = 1/2 * nat.rho * p.velocity.set^2 * car.CdA;
Force.g            = car.mass.total * nat.g;
Force.roll         = Force.g * cos(road.slope) * car.Crr;
Force.climb        = Force.g * sin(road.slope);
Force.acceleration = road.acceleration * car.mass.total;
Power.drag         = Force.drag         * p.velocity.set; % [W]
Power.roll         = Force.roll         * p.velocity.set; % [W]
Power.climb        = Force.climb        * p.velocity.set; % [W] 
Power.acceleration = Force.acceleration * p.velocity.set; % [W]
Power.total        = Power.drag + Power.roll + Power.climb + Power.acceleration + Power.other
% p.reldist          = p.dist/location.Adelaide
Power.kWh          = Power.total*1e-3 * time.day.travle; % 

Power.kWhp100km    = Power.kWh * 100 ./ (p.dist)
disp(Power.kWhp100km)
% Tal vi gerne vil have:
% kWh/100km
%% Simplified Power Loss Calculation


%% Choice of Target Speed
Route_elevation = ones(1,3200); % [m] Elevation above sea height in meters
Route_tilt = movmean(Route_elevation,10);
dist_tot = 3020; %[km] route total distance
n_days = 5.5; %[Days] number of days available to finish the race
% dist_pd = dist_tot/time.total; %[avg km/day] km avg. distance per day required travle
req_drv_spd = dist_tot/(time.total); %[avg km/h] required average driving speed
disp(strcat("Required average driving speed:"))
disp(strcat("    ",num2str(req_drv_spd),"km/h = ",num2str(req_drv_spd/3.6),"m/s"))

guess_req_drv_spd = 21; % [m/s] Use google maps to correct this value for 
% intersections on the road

disp(" ")
disp(strcat("The estimated required speed needed to be"))
disp(       "driven on the highway to compensate for")
disp(       "slowdowns in cities and at intersections")
disp(strcat("is therefore assumed to be: "))
disp(strcat("    ",num2str(guess_req_drv_spd*3.6),"km/h = ",num2str(guess_req_drv_spd),"m/s"))
% ,num2str(guess_req_drv_spd),"m/s"))
disp("This velocity value will be used")
disp("for all further calculaitons")
%% Energy from the sun [kWh]
disp(" ")
P_solar = 6.8; %7; %[(kWh/day)/m^2] solar power per day per m^2 in Australia
A_solar = 5;%5; %[m^2] area of solar panels on car
eta_solar = 0.24; %[] efficiency of solar panels from SUNPOWER (Swedish company)
Sun_angle_rms = (0.89/sqrt(2)); %[radians] RMS-angle of sun in Australia, calculated as: Top-angle of sun in Australia in October divided by sqrt(2) to get Root-mean-square
E_from_sun = P_solar * A_solar * eta_solar * cos(Sun_angle_rms) * n_days;
disp(strcat("The energy we expect to get from the sun is:"))
disp(strcat("    E_from_sun = ",num2str(E_from_sun),"kWh"))
%% Energy from charging [kWh]
disp(" ")
% % % % P_sun_and_charge = 70 % [kWh] Total input power, minus the initial power from the battery 
% % % % P_batreq  =    % Required initial battery power to complete the race


t_staging_locations = 2*3.5; %[Hours] Total time available to charge externally at the two staging locaitons.
% We can charge from sundown 19:30 or 19:00 depending on their definition
% of sundown, until 23:00. This results in a charging time of 2*3.5Hours =
% 7 hours.

I_SL = [6, 30];               % [A] possible range of charging currents
V_SL = [216.2 , 253];         % [Vrms] possible range of charging voltages
P_SL = V_SL.'*I_SL;           %[W] The range of Watts we can charge at staging locations
P_SLmax = max(P_SL,[],'all'); %[W] maximum amount of Watts per hour we can charge at staging locations
P_SLmean = mean(mean(P_SL));
E_from_charging = P_SLmax * t_staging_locations;
disp(strcat("The energy we expect to get from the Staging Locations is:"))
disp(strcat("    E_from_charging = ",num2str(E_from_charging*1e-3),"kWh"))
%% Total external Energy input to the system minus the initial energy in the battery:
disp(" ")
P_tot_minus_battery = E_from_charging*1e-3 + E_from_sun;

disp(       "The total energy we expect to get")
disp(       "  from the Staging Locations and")
disp(       "  the sun is therefore:")
disp(strcat("    P_tot_minus_battery = ",num2str(P_tot_minus_battery),"kWh"))
%% Car parameters:
disp(" ")

g = 9.81; % gravitational constant

rho = 1.2754;%1.184; % air density

% Car parameters

width  = 1.910; %[m] car front area width  (max 2.2m)
height = 1.185; %[m] car front area height (max 1.6m)

% AD = width*height; %[m^2] car front area;
AD = 1.9; %real present value: 2.05; %[m^2] car front area;

% Car mass:
m_chassis = 200;%270; % Real Chassis weight: 250; 70 kg if carbon fiber
m_shell = 133;% 184; % kg; steel: 184kg, carbon fiber: 133kg;
m_battery = 50;%300;
m_motor = 40;
m_other_electronics = 60;
m_car = m_chassis + m_shell + m_battery + m_motor + m_other_electronics;
m_passenger = 80; % passenger mass
n_passenger = 2; % number of passengers
m_total = m_car + n_passenger*m_passenger; % loaded car mass

P_batPcell = 500 ;%[Wh] %for prismatic cells(present solution): 72*3.2[Wh]; 
%Lithium-Sulfur: 500[Wh]
m_batterycell = 1;%[kg] for prismatic cells(present solution): 1.9; % 
E_bat = m_battery*P_batPcell/m_batterycell; %[Wh]

CD =  0.21;% probably the real value: 0.2; %[] car drag coefficient

Crr = 0.0035;% probably the real value: 0.006; %[] car rolling resistance

r_wheel = 0.7/2; % [m] wheel radius

Fg = m_total*g; %[N]
% p_battery = 25e3; % kWh battery capacity (unused parameter)
motor_eff = 0.91*(1 - 0.18); %[]


run_old_code = false;
if run_old_code
% %% Optimization & simulation
% % acc = 0.1:0.1:1
% t1 = STEP_SIZE*10:STEP_SIZE*10:TRAVLE_TIME/2;
% % Possible accelerations:
% a = -TRAVLE_DISTANCE./(-t1.^2 - t1.*(TRAVLE_TIME - 2.*t1));
% 
% road_tilt = deg2rad(0)
% 
% %% Simulation:
% mysim = sim('Power_consumption_simulation')
% 
% % t1 = STEP_SIZE*10*zeros(size(Allowed_travle_times)):STEP_SIZE*10:Allowed_travle_times;
% 
% %% 
% figure
% subplot(3,1,1)
% plot(mysim.E_tot)
% grid on
% 
% subplot(3,1,2)
% plot(mysim.P_tot)
% grid on
% 
% subplot(3,1,3)
% plot(mysim.v)
% grid on
% 
% %% Constant power consumption parts:
% % Peripherals
% %   Lights:
% P_lights = 50 % [W]
% P_peripherals = P_lights % [W]
% 
% % Audio
% %   A 100W amplifier will be used to support a 50W speaker
% P_audio = 100 % [W]



% %% Power consumption at cruising(cr) velocity:
% Notes:
%   Motor torque:
%       The motor is only most efficient (92%) when it experiences a torque
%       above 35Nm. 
%           30Nm => 91% efficiency
%           25Nm => 90% efficiency
%           20Nm => 87% efficiency
%           15Nm => 83% efficiency
%           10Nm => 75% efficiency
%            5Nm => 57% efficiency
end
%% Calculaiton of Expected power loss from driving the route.
guess_req_drv_spd = 21;
v_cr = guess_req_drv_spd; % [m/s]

acc_cr = 1.5; % [m/s^2]

w_cr = v_cr/r_wheel; % Frequency [Hz]

rpm_cr = w_cr * 60; %  Revolutions pr. minute

phi_cr = deg2rad(0); % Tilt of the road with respect to gravity [degrees]

N_cr = Fg*cos(phi_cr); % The cars normal force to the ground [N]

Fd_cr = 1/2*rho*v_cr^2*CD*AD; % Drag force [N]

Fr_cr = N_cr*Crr; % Force from rolling resistance Crr [N]
% Fr_cr = 1;
Facc_cr = acc_cr*m_total; % Force from accelerating the car [N]

F_tot_cr = Fg*sin(phi_cr) + Fd_cr + Fr_cr + Facc_cr; % total road force [N]

T_cr = F_tot_cr * r_wheel; % total needed torque [Nm]

P_c = (Fg*sin(phi_cr) * v_cr)/motor_eff; %[w] Climbing power loss

P_d = (Fd_cr * v_cr)/motor_eff; %[w] Drag power loss

P_r = (Fr_cr * v_cr)/motor_eff; %[w] Rolling resistance power loss

P_a = (Facc_cr * v_cr)/motor_eff; %[w] Acceleration power loss

P_cr = (T_cr*w_cr)/motor_eff; % power needed for cruising [W]

P_req_tot = (P_cr + P_other)/1000*sum(TRAVLE_HOURS); % Total required power to complete the race [kWh]

% Printing of calculations:
disp("Requirements for Cruising at:")
disp("Car stats:")
disp(strcat("Car mass w. passengers = ",num2str(m_total),"kg"))
disp(strcat("Velocity  = ",num2str(v_cr)," m/s = ",num2str(v_cr*3.6)," km/h"))
disp(strcat("Car cross sectional areal = ",num2str(AD),"m^2"))
disp(" ")
disp(strcat("Torque    = ",num2str(T_cr),"Nm"))
disp("Power loss:")
disp(strcat("    Climbing           = ",num2str(P_c),"W"))
disp(strcat("    Drag               = ",num2str(P_d),"W"))
disp(strcat("    Rolling resistance = ",num2str(P_r),"W"))
disp(strcat("    Acceleration       = ",num2str(P_a),"W"))
disp(" ")
disp(strcat("Power_car = ",num2str(P_cr),"W"))
disp(strcat("w         = ",num2str(w_cr),"Hz = ",num2str(round(w_cr*60)),"rpm")) % angular velocity
disp(" ")
disp(       "Power requirement to complete the race is therefore:")
disp(       "    P_req_tot = Power_car[W]/1000[1/k]*(TRAVLE_TIMES[s]/3600[h/s]) [kWh]")
disp(strcat("    P_req_tot = ",num2str(P_req_tot),"kWh"))
disp(strcat("P_sun_and_charge = ",num2str(P_tot_minus_battery),"kWh"))
disp(strcat(" <=> "))
disp(       "P_bat = P_req_tot - P_sun_and_charge")
disp(strcat("P_bat = ",num2str(P_req_tot - P_tot_minus_battery),"kWh"))
disp(" ")
disp("Expected energy in battery given allowed mass:")
disp(strcat("m_bat = ",num2str(m_battery),"kg"))
disp(strcat("E_bat = ",num2str(E_bat/1000),"kWh"))
disp("efficiency rating: kWh/km")
disp(strcat(num2str(P_req_tot/dist_tot)))
%% Nomial power consumption
P_nom = P_cr + P_other;
disp(strcat("Nominal Power consumption: ",num2str(P_nom),"W"))

%% END

