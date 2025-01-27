%% parameters

g = 9.81; % gravitational constant

rho = 1.184; % air density

% Car parameters

width = 2.2; % car front area width
height = 1.6; % car front area height

AD = width*height; % car front area;

m_car = 500; % unloaded car mass
m_passenger = 80; % passenger mass
n_passenger = 2; % number of passengers

m_total = m_car + n_passenger*m_passenger; % loaded car mass

CD = 0.2; % car drag coefficient
Crr = 0.0025; % car rolling resistance

r_wheel = 0.550/2; % wheel radius

Fg = m_total*g;

p_battery = 25e3; % kWh battery capacity

motor_eff = 0.85;

% Route parameters

dist_tot = 3000; % km route total distance
n_day = 5; % number of days
dist_pd = dist_tot/n_day; % km avg. distance per day
t_day = 8; % hour driving per day

MAXMOTORPOWER = 20000 % 20kW

%% Avg. driving speed
% 
% v_avg = (dist_pd/t_day)*1000/3600;
% 
% phi_avg = deg2rad(0);
% 
% N_avg = Fg*cos(phi_avg);
% 
% Fd_avg = 1/2*rho*v_avg^2*CD*AD;
% 
% Fr_avg = N_avg*Crr;
% 
% T_avg = Fg*sin(phi_avg) + Fd_avg + Fr_avg;
% 
% P_avg = (T_avg*w_avg)/motor_eff; % power needed for cruising

%% Cruising speed
% 
% v_cruise = 90*1000/3600;
% 
% rpm_cruise = v_cruise/r_wheel
% phi_cruise = deg2rad(0);
% 
% N_cruise = Fg*cos(phi_cruise);
% 
% Fd_cruise = 1/2*rho*v_cruise^2*CD*AD;
% 
% Fr_cruise = N_cruise*Crr;
% 
% T_cruise = Fg*sin(phi_cruise) + Fd_cruise + Fr_cruise;
% 
% P_cruise = (T_cruise*w_cruise)/motor_eff % power needed for cruising

%% Cruising with acceleration
clc
vacc = 0:0.1:2

VELOCITY = 90 % [Km/h]
T_cruise = zeros(size(vacc))
P_cruise = zeros(size(vacc))
for i = 1:size(vacc,2)
acc_cruise = vacc(i); % [m/s^2] Desired acceleration @ v_cruise


v_cruise = VELOCITY*1000/3600 % [m/s]

w_cruise = v_cruise/r_wheel % frequency [Hz]

rpm_cruise = w_cruise * 60 %  Revolutions pr. minute


phi_cruise = deg2rad(0); % Tilt of the road with respect to gravity

N_cruise = Fg*cos(phi_cruise); % The cars normal force to the ground

Fd_cruise = 1/2*rho*v_cruise^2*CD*AD; % Drag force

Fr_cruise = N_cruise*Crr; % Force from rolling resistance Crr

Facc_cruise = acc_cruise*m_total; % Force from accelerating the car

F_tot_cruise = Fg*sin(phi_cruise) + Fd_cruise + Fr_cruise + Facc_cruise; % total road force

T_cruise(i) = F_tot_cruise * r_wheel; % total needed torque

P_cruise(i) = (T_cruise(i)*w_cruise)/motor_eff; % power needed for cruising

end

[~,i] = min(abs(P_cruise-MAXMOTORPOWER));
P_cruise(i) % 
disp(strcat("Torque requeired at ",num2str(VELOCITY),"km/h: ",num2str(T_cruise(i)),"Nm"))
disp(strcat("Torque requeired at ",num2str(VELOCITY),"km/h: ",num2str(T_cruise(i)),"Nm"))
vacc(i) % maximum possible acceleration at given power

%% City driving with acceleration:

clc;
vacc = 0:0.1:9;

VELOCITY = [40 90]; % [Km/h]
T_cruise = zeros(size(vacc));
P_cruise = zeros(size(vacc));
disp(strcat("From a motor power of: P = ",num2str(MAXMOTORPOWER),"W:"))
disp(" ")
for speed_cruise = VELOCITY

for i = 1:size(vacc,2)
acc_cruise = vacc(i); % [m/s^2] Desired acceleration @ v_cruise


v_cruise = speed_cruise*1000/3600; % [m/s]

w_cruise = v_cruise/r_wheel; % frequency [Hz]

rpm_cruise = w_cruise * 60; %  Revolutions pr. minute


phi_cruise = deg2rad(0); % Tilt of the road with respect to gravity

N_cruise = Fg*cos(phi_cruise); % The cars normal force to the ground

Fd_cruise = 1/2*rho*v_cruise^2*CD*AD; % Drag force

Fr_cruise = N_cruise*Crr; % Force from rolling resistance Crr

Facc_cruise = acc_cruise*m_total; % Force from accelerating the car

F_tot_cruise = Fg*sin(phi_cruise) + Fd_cruise + Fr_cruise + Facc_cruise; % total road force

T_cruise(i) = F_tot_cruise * r_wheel; % total needed torque

P_cruise(i) = (T_cruise(i)*w_cruise)/motor_eff; % power needed for cruising

end
P_cruise(1)
[~,i] = min(abs(P_cruise-MAXMOTORPOWER));
P_cruise(i); % 

disp(strcat("Torque requeired at ",num2str(speed_cruise),"km/h: T = ",num2str(T_cruise(i)),"Nm"))
disp(strcat("Resulting in an acceleration of: a = ",num2str(vacc(i)),"m/s^2"))
disp(" ")
vacc(i); % maximum possible acceleration at given power
end
%% Climbing
clc
v_climbing = 20*1000/3600;
rpm_climbing = v_climbing/r_wheel
phi_climbing = deg2rad(10);

N_climbing = Fg*cos(phi_climbing);

Fd_climbing = 1/2*rho*v_climbing^2*CD*AD;

Fr_climbing = N_climbing*Crr;

T_climbing = Fg*sin(phi_climbing) + Fd_climbing + Fr_climbing

P_climbing = (T_climbing*v_climbing)/motor_eff

%% Accelerating from stop

v_acc = 10*1000/3600;
a_acc = 3.5;

phi_acc = deg2rad(0);

N_acc = Fg*cos(phi_acc);

Fd_acc = 1/2*rho*v_acc^2*CD*AD;

Fr_acc = N_acc*Crr;

T_acc = m_total*a_acc + Fg*sin(phi_acc) + Fd_acc + Fr_acc;

P_acc = (T_acc*v_acc)/motor_eff % power needed for cruising










