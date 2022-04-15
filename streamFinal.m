function [t, dataActual] = streamFinal(runTime, plotFlag)
    totalTime = runTime; % seconds MUST EXCEED CALIBRATION TIME
    inputBufferSize = 1000; % 0.05s to fill buffer
    calibrationTime = 10; % Seconds
    portNumber = '/dev/tty.usbserial-DJ00DV99'; % Port number depends on MAC or PC
    delete(instrfindall) % Close all unwanted connections
    s = InitializePortInput(inputBufferSize, portNumber); % Initialize data stream
    Fs = 10000; % Sampling Rate Hz
    
    % Setup Plotting Window
    figure('color', 'w')
    xlabel('Time (s)')
    
    % Create array to store streamed data
    dataActual = [];
    
    % Calculate number of buffer loops for entire streaming time
    totalLoops = 20000/s.InputBufferSize*totalTime; % Conversion factor of 20 0000 = 1 second
    bufferFillTime = s.InputBufferSize/20000; % Time (s) to fill a single buffer for a given input buffer size
    
    % Caluclate number of buffer loops for calibration
    calibrationLoops = calibrationTime/bufferFillTime;
    calibrationArray = [];

    for i = 1:totalLoops
        dataIn = fread(s)';
        dataTemp = process_data(dataIn); % Data from the current buffer/loop
        dataNorm = dataTemp;
        % FFT HIGH PASS filter
        N = size(dataNorm, 1);
        dF = Fs/N;
        f = (-Fs/2:dF:Fs/2-dF)';
        lowerFreqCutoff = 1;
        HP_filter = (abs(f) > lowerFreqCutoff);
        spectrum = fftshift(fft(dataNorm))/N;
        spectrum = HP_filter.*spectrum;
        fftFiltered = ifft(ifftshift(spectrum), 'symmetric')*N;
        % BUTTERWORTH LOW PASS FILTER
        cutoff = 6; %Hz
        order = 5;
        [b,a] = butter(order, cutoff/(Fs/2));
        filteredSignal = (filtfilt(b,a,double(fftFiltered))); % Zero-Phase double filter
        
        if i <= calibrationLoops % CALIBRATION PHASE
            calibrationArray = [filteredSignal, calibrationArray]; % Append new data to start of the array
            calibrationT = i*s.InputBufferSize/20000*linspace(0,1,length(calibrationArray));
            if plotFlag == true % PLOT CALIBRATION PHASE
                drawnow;
                plot(calibrationT, calibrationArray);
                xlabel('time (s)')
                xlim([0, calibrationTime])
            end
                
        else
            % STREAMING PHASE
            if i == (calibrationLoops + 1)
                noise = mean(calibrationArray); % Calculate baseline for subtraction
            end
            filteredSignal = filteredSignal - noise; % Subtract baseline
            dataActual = [filteredSignal, dataActual]; % Save to array
            t = i*s.InputBufferSize/20000*linspace(0,1,length(dataActual)); 
           % DISPLAY RAW DATA 
            disp(dataActual(1:4)) % Display most recent measurements
            if plotFlag == true
                drawnow;
                plot(t, dataActual)
                xlabel('time (s)')
                xlim([0 calibrationTime])
            end
        end
    end
end



