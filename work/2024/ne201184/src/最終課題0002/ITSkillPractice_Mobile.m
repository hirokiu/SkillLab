% ITSkillPractice_Mobile.m

% Enable sensors
m = mobiledev;
m.AccelerationSensorEnabled = 1;
m.PositionSensorEnabled = 1;

% Start logging data
m.Logging = 1;
disp('Logging started.');

% Use tic and toc to simulate a 10-second pause
startTime = tic;  % Start timer
duration = 10;    % Set duration to 10 seconds

% Keep collecting data for the specified duration
while toc(startTime) < duration
    % No explicit pause; just a loop to let time pass
end

% Stop logging
m.Logging = 0;
disp('Logging stopped.');

% Retrieve data
[accelData, timeAccel] = accellog(m);
[lat, lon, alt, timePos] = poslog(m);

% Save data to MATLAB Drive (as CSV)
csvwrite('acceleration_data_mobile.csv', [timeAccel, accelData]);
csvwrite('position_data_mobile.csv', [timePos, lat, lon]);

disp('Data saved to MATLAB Drive.');

