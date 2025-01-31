%% Transmitting a CAN message
%Defining the CAN message
message = canMessage(291,false,8);
% Data, any value other than zero will trigger an active request
load = 1;
charge = 0;
staging = 0;
% Compiling message
message.Data = ([0 0 0 0 0 staging charge load]);
% Selecting the CAN channel
canch = canChannel('PEAK-System','PCAN_USBBUS1');
start(canch)
transmit(canch,message)
stop(canch)

%% Receive staging request
rxCanCh = canChannel('PEAK-System','PCAN_USBBUS1');
% Filter to only listen for CAN ID 1
filterAllowOnly(rxCanCh, 1, "Standard");
start(rxCanCh)
rxmessage = receive(rxCanCh, Inf)
% Wait for staging request
% Variable i used as time-out functionality
i = 0;
% Flag for showing received staging request
stgFlag = 0;
while stgFlag ~= 1
    rxmessage = receive(rxCanCh, Inf);
    i = i + 1;
    % Active staging request
    if rxmessage.Data{5} ~= 0
        stgFlag = 1;
    % Time-out
    elseif i == 500
        break
    end
end
stop(rxCanCh)
if stgFlag == 1
    start(canch)
    staging = 1;
    message.Data = ([0 0 0 0 0 staging charge load])
    
    transmit(canch,message)
    staging = 0;
    stop(canch)
else
    disp('No good')
    load = 0;
end