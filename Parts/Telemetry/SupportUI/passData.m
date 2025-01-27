function [speed, SOH, SOC, cap, sol, usage, range] = passData()
% passData function for sending data to the BMSapp

% Dummy data for testing purposes
speed = 20.5;   % Speed in m/s
SOH = 0.9;      % State of health
SOC = 1;        % State of charge
cap = 40000;    % Capacity of battery - Find mulighed for at trække data fra app
sol = 4944.2;   % See Energy_budget_2020_05_07
usage = 14200;  % Usage of power

time = ((cap*SOH*SOC)+sol)/usage*3600;
range = speed*time;
end