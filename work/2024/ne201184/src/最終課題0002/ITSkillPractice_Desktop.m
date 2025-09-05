% ITSkillPractice_Desktop.m

% 1. Load the data from MATLAB Drive
accelData = readmatrix('acceleration_data_mobile.csv');  % Accelerometer data
positionData = readmatrix('position_data_mobile.csv');   % GPS data (latitude and longitude)

% Separate the data into variables
timeAccel = accelData(:,1);
accelX = accelData(:,2);  % Assuming X-axis acceleration for step counting
lat = positionData(:, 2);  % Latitude
lon = positionData(:, 3);  % Longitude

% 2. Step counting (simple threshold-based detection)
threshold = 1.0;  % Threshold for detecting steps
numSteps = sum(accelX > threshold);  % Count steps based on acceleration

% Calculate distance walked (using average step length)
stepLength = 0.78;  % Average step length in meters
distanceWalked = numSteps * stepLength;  % Total distance in meters
distanceKm = distanceWalked / 1000;  % Convert distance to kilometers

% Display results
fprintf('Total Steps: %d\n', numSteps);
fprintf('Total Distance Walked: %.2f meters (%.2f km)\n', distanceWalked, distanceKm);

% Calculate calories burned
userWeight = 60;  % Example weight in kg
caloriesPerKmPerKg = 0.8;  % Calories burned per kilometer per kilogram
caloriesBurned = distanceKm * userWeight * caloriesPerKmPerKg;
fprintf('Total Calories Burned: %.2f kcal\n', caloriesBurned);

% 3. Plot GPS data on a map using MATLAB's geoplot function
if ~isempty(lat) && ~isempty(lon)
    figure;
    geoplot(lat, lon, '-o');
    title('GPS Path');  % Add only the title
else
    disp('No GPS data available.');
end

% 4. Use Python (Folium) to display GPS data on an interactive map
if ~isempty(lat) && ~isempty(lon)
    % Prepare the GPS data for use in Python (Folium)
    pyrun("import folium", ...
          "m = folium.Map(location=[35.7056232, 139.751919], tiles='cartodbpositron', zoom_start=14)", ...
          sprintf("folium.PolyLine([%s], color='blue', weight=2.5).add_to(m)", ...
                  strjoin(arrayfun(@(i) sprintf('[%.6f, %.6f]', lat(i), lon(i)), 1:length(lat), 'UniformOutput', false), ',')), ...
          "m.save('map.html')")
    % Open the saved map in a web browser
    web('map.html', '-browser');
else
    disp('No GPS data available.');
end
