%% Receiving a CAN message
% Setup CAN channel
rxCh = canChannel('PEAK-System','PCAN_USBBUS1');
% Start listening on the CAN bus
start(rxCh)
% Receive data on CAN bus in a time table
rxMsg = receive(rxCh, Inf, 'OutputFormat', 'timetable')
% Stop listening on the CAN bus
stop(rxCh)

% Create an array with CAN IDs to hold values
IDarray = {1, [];200, []; 201, []; 202, []; 203, []; 204, []; 205, []; 
    206, []; 207, []};

% Search through received CAN IDs for matches with ID array
for i = 1:1:height(rxMsg)
    for j = 1:1:height(IDarray)
        % In case of ID match, the data from the message is copied into 
        % the IDarray data
        if rxMsg{i,1} == IDarray{j,1}
           IDarray{i,2} = rxMsg{i,4};
        end 
    end
end
