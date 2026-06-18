close all;
clear all;
clc;

blocks=1; 
trials=1
;  
%دیتاب1س
baseDir = 'C:\Users\Home\Downloads\psychtool\AnimalDB\AnimalDB';
categories = {'Animall', 'NonAnimall'};
distances = {'Head', 'CloseBody', 'MediumBody', 'FarBody'};


stimList = [];
 
for c = 1:length(categories)
    for d = 1:length(distances)
        folderPath = fullfile(baseDir, categories{c}, distances{d});
        files = dir(fullfile(folderPath, '*.jpg'));  
        for f = 1:length(files)
            stimList(end+1).filepath = fullfile(folderPath, files(f).name);
            stimList(end).category = categories{c};
            stimList(end).distance = distances{d};
        end
    end
end

totalTrials = 5 * 120 ;
rng('shuffle');
randIdx = randperm(length(stimList), totalTrials);
selectedStimList = stimList(randIdx);

% تنظیمات اولیه
Screen('Preference', 'SkipSyncTests', 1);
[window, rect] = Screen('OpenWindow', 0, 128); 

% مرکز صفحه
[xCenter, yCenter] = RectCenter(rect);

fixTime = 0.5;     
stimTime = 0.0133;   
isiTime = 0.0133;   
maskTime = 0.08;   

screenWidth_cm = 53;
screenResX = 1920;
D = 57;
pix_per_cm = screenResX / screenWidth_cm;

fixSize_deg = 0.76;
fixSize_cm = 2 * D * tand(fixSize_deg / 2);
fixSize_px = round(fixSize_cm * pix_per_cm);

stimSize_deg = 7;                     
stimSize_cm = 2 * D * tand(stimSize_deg / 2); 
stimSize_px = round(stimSize_cm * pix_per_cm); 

barLength_deg = 12 ;  
barWidth_deg = 2.4;  

barLength_cm = 2 * D * tand(barLength_deg / 2);
barWidth_cm  = 2 * D * tand(barWidth_deg / 2);

barLength_px = round(barLength_cm * pix_per_cm);
barWidth_px  = round(barWidth_cm  * pix_per_cm);

numConfidenceLevels = 5; 
barSegmentHeight = barLength_px / numConfidenceLevels;


leftBarBase = [xCenter - 300 - barWidth_px, ...  
               yCenter - barLength_px/2, ...
               xCenter - 300, ...
               yCenter + barLength_px/2];

 
rightBarBase = [xCenter + 300, ...  
                yCenter - barLength_px/2, ...
                xCenter + 300 + barWidth_px, ...
                yCenter + barLength_px/2];

confidenceColors = [
    [255, 200, 200]; 
    [255, 150, 150];
    [200, 255, 200]; 
    [150, 255, 150]; 
    [100, 255, 100]; 
];


ShowCursor;

% تست ابتدایی
testImg = imread('C:\Users\Home\Downloads\psychtool\AnimalDB\AnimalDB\Animall\Head\H_N123022.jpg');
testImg = imresize(testImg, [stimSize_px stimSize_px]);
stimTex = Screen('MakeTexture', window, testImg);
maskImg = scrambleImage(testImg, 16);
maskTex = Screen('MakeTexture', window, maskImg);
stimRect = CenterRectOnPoint([0 0 stimSize_px stimSize_px], xCenter, yCenter);

% رسم علامت «+» با اندازه 0.76 درجه دید
Screen('DrawLine', window, 0, xCenter - fixSize_px/2, yCenter, xCenter + fixSize_px/2, yCenter, 2); % افقی
Screen('DrawLine', window, 0, xCenter, yCenter - fixSize_px/2, xCenter, yCenter + fixSize_px/2, 2); % عمودی
Screen('Flip', window);
WaitSecs(fixTime);

Screen('DrawTexture', window, stimTex, [], stimRect);
Screen('Flip', window); WaitSecs(stimTime);

Screen('FillRect', window, 128);
Screen('Flip', window); WaitSecs(isiTime);

Screen('DrawTexture', window, maskTex);
Screen('Flip', window); WaitSecs(maskTime);

drawConfidenceBar(window, leftBarBase, rightBarBase, barSegmentHeight, confidenceColors, 0, 0);
DrawFormattedText(window, 'Left: NonAnimal', leftBarBase(1), leftBarBase(2)-30, [255, 255, 255]);
DrawFormattedText(window, 'Right.: Animal', rightBarBase(1), rightBarBase(2)-30, [255, 255, 255]);
Screen('Flip', window);
WaitSecs(2);

DrawFormattedText(window, 'Press any key to start!', 'center', 'center', 255);
Screen('Flip', window);
KbWait;

results = struct('file', {}, 'category', {}, 'distance', {}, 'block', {}, ...
                'trial', {}, 'response', {}, 'confidence', {}, 'responseTime', {}, ...
                'reactionTime', {}, 'correct', {});

% شروع
trialNum = 0;
for block = 1:blocks
    for trial = 1:trials
        trialNum = trialNum + 1;
        
        stimInfo = selectedStimList(trialNum);

        % رسم علامت «+» با اندازه 0.76 درجه دید
        Screen('DrawLine', window, 0, xCenter - fixSize_px/2, yCenter, xCenter + fixSize_px/2, yCenter, 2); % افقی
        Screen('DrawLine', window, 0, xCenter, yCenter - fixSize_px/2, xCenter, yCenter + fixSize_px/2, 2); % عمودی
        Screen('Flip', window);
        WaitSecs(fixTime);

        stimImg = imread(stimInfo.filepath);
        stimImg = imresize(stimImg, [stimSize_px stimSize_px]);
        stimTex = Screen('MakeTexture', window, stimImg);
        stimRect = CenterRectOnPoint([0 0 stimSize_px stimSize_px], xCenter, yCenter);

        % ساخت ماسک
        maskImg = scrambleImage(stimImg, 16);
        maskTex = Screen('MakeTexture', window, maskImg);

        stimOnsetTime = GetSecs;
        Screen('DrawTexture', window, stimTex, [], CenterRectOnPoint([0 0 stimSize_px stimSize_px], xCenter, yCenter));
        Screen('Flip', window); WaitSecs(stimTime);

        Screen('FillRect', window, 128);
        Screen('Flip', window); WaitSecs(isiTime);

        Screen('DrawTexture', window, maskTex);
        Screen('Flip', window); WaitSecs(maskTime);

        % مرحله پاسخ‌دهی
        responseGiven = false;
        responseStartTime = GetSecs;
        firstClickTime = [];  % For tracking reaction time
        
        while ~responseGiven
            [highlightLeft, highlightRight] = getMouseHighlight(leftBarBase, rightBarBase, barSegmentHeight, numConfidenceLevels);
            drawConfidenceBar(window, leftBarBase, rightBarBase, barSegmentHeight, confidenceColors, highlightLeft, highlightRight);
            
            DrawFormattedText(window, 'NonAnimal', leftBarBase(1), leftBarBase(2)-30, [255, 255, 255]);
            DrawFormattedText(window, 'Animal', rightBarBase(1), rightBarBase(2)-30, [255, 255, 255]);
            
            Screen('Flip', window);
            
            [x, y, buttons] = GetMouse;
            if any(buttons)
                if isempty(firstClickTime)
                    firstClickTime = GetSecs;
                end
                
                [response, confidence] = getMouseResponse(leftBarBase, rightBarBase, barSegmentHeight, numConfidenceLevels);
                if ~isempty(response)
                    responseGiven = true;
                    responseTime = GetSecs - responseStartTime;
                end
                
                while any(buttons)
                    [x, y, buttons] = GetMouse;
                    WaitSecs(0.001);
                end
            end
            
            WaitSecs(0.001); 
        end
        
        reactionTime = firstClickTime - stimOnsetTime;
        
        results(trialNum).file = stimInfo.filepath;
        results(trialNum).category = stimInfo.category;
        results(trialNum).distance = stimInfo.distance;
        results(trialNum).block = block;
        results(trialNum).trial = trial;
        results(trialNum).response = response;
        results(trialNum).confidence = confidence;
        results(trialNum).responseTime = responseTime;
        results(trialNum).reactionTime = reactionTime;  % NEW: Added reaction time
        results(trialNum).correct = strcmp(response, stimInfo.category);
        
        Screen('FillRect', window, 128);
        feedbackText = sprintf('Response: %s\nConfidence: %d/5\nReaction Time: %.3f s', response, confidence, reactionTime);
        DrawFormattedText(window, feedbackText, 'center', 'center', [255, 255, 255]);
        Screen('Flip', window);
        WaitSecs(0.5);
    end

    DrawFormattedText(window, sprintf('Block %d completed!\nPress any key to continue!', block), 'center', 'center', 255);
    Screen('Flip', window);
    KbWait;
end


sca;

for j = 1:length(results)
    fprintf('Trial %d:\n', j);
    fprintf('  File: %s\n', results(j).file);
    fprintf('  Category: %s\n', results(j).category);
    fprintf('  Distance: %s\n', results(j).distance);
    fprintf('  Block: %d\n', results(j).block);
    fprintf('  Trial in Block: %d\n', results(j).trial);
    fprintf('  Response: %s\n', results(j).response);
    fprintf('  Confidence: %d\n', results(j).confidence);
    fprintf('  Response Time: %.3f s\n', results(j).responseTime);
    fprintf('  Reaction Time: %.3f s\n', results(j).reactionTime);  % NEW
    fprintf('  Correct: %d\n', results(j).correct);
    fprintf('-----------------------------\n');
end

save('results.mat', 'results');
T = struct2table(results);
writetable(T, 'results.csv');

fprintf('\n========== DETAILED PERFORMANCE ANALYSIS ==========\n\n');

categories = {'Animall', 'NonAnimall'};
distances = {'Head', 'CloseBody', 'MediumBody', 'FarBody'};

totalTrials = length(results);
totalCorrect = sum([results.correct]);
overallAccuracy = (totalCorrect / totalTrials) * 100;
avgReactionTime = mean([results.reactionTime]);  % NEW

fprintf('OVERALL PERFORMANCE:\n');
fprintf('Total Trials: %d\n', totalTrials);
fprintf('Total Correct: %d\n', totalCorrect);
fprintf('Overall Accuracy: %.1f%%\n', overallAccuracy);
fprintf('Average Reaction Time: %.3f seconds\n\n', avgReactionTime);  % NEW

fprintf('DETAILED BREAKDOWN:\n');
fprintf('===================\n\n');

for c = 1:length(categories)
    for d = 1:length(distances)
        categoryMask = strcmp({results.category}, categories{c});
        distanceMask = strcmp({results.distance}, distances{d});
        combinedMask = categoryMask & distanceMask;
        
        if sum(combinedMask) > 0
            categoryResults = results(combinedMask);
            
            numTrials = length(categoryResults);
            numCorrect = sum([categoryResults.correct]);
            accuracy = (numCorrect / numTrials) * 100;
            avgConfidence = mean([categoryResults.confidence]);
            avgResponseTime = mean([categoryResults.responseTime]);
            avgReactionTime = mean([categoryResults.reactionTime]);  % NEW
            
            confidenceCounts = histcounts([categoryResults.confidence], 1:6);
            
            fprintf('%s - %s:\n', categories{c}, distances{d});
            fprintf('  Trials: %d\n', numTrials);
            fprintf('  Correct: %d\n', numCorrect);
            fprintf('  Accuracy: %.1f%%\n', accuracy);
            fprintf('  Average Confidence: %.1f/5\n', avgConfidence);
            fprintf('  Average Response Time: %.2f seconds\n', avgResponseTime);
            fprintf('  Average Reaction Time: %.3f seconds\n', avgReactionTime);  % NEW
            fprintf('  Confidence Distribution:\n');
            for conf = 1:5
                percentage = (confidenceCounts(conf) / numTrials) * 100;
                fprintf('    Level %d: %d trials (%.1f%%)\n', conf, confidenceCounts(conf), percentage);
            end
            fprintf('\n');
        end
    end
end

fprintf('CATEGORY SUMMARY:\n');
fprintf('=================\n\n');

for c = 1:length(categories)
    categoryMask = strcmp({results.category}, categories{c});
    categoryResults = results(categoryMask);
    
    if length(categoryResults) > 0
        numTrials = length(categoryResults);
        numCorrect = sum([categoryResults.correct]);
        accuracy = (numCorrect / numTrials) * 100;
        avgConfidence = mean([categoryResults.confidence]);
        avgResponseTime = mean([categoryResults.responseTime]);
        avgReactionTime = mean([categoryResults.reactionTime]);  % NEW
        
        fprintf('%s (All distances):\n', categories{c});
        fprintf('  Trials: %d\n', numTrials);
        fprintf('  Correct: %d\n', numCorrect);
        fprintf('  Accuracy: %.1f%%\n', accuracy);
        fprintf('  Average Confidence: %.1f/5\n', avgConfidence);
        fprintf('  Average Response Time: %.2f seconds\n', avgResponseTime);
        fprintf('  Average Reaction Time: %.3f seconds\n\n', avgReactionTime);  % NEW
    end
end

fprintf('DISTANCE SUMMARY:\n');
fprintf('=================\n\n');

for d = 1:length(distances)
    distanceMask = strcmp({results.distance}, distances{d});
    distanceResults = results(distanceMask);
    
    if length(distanceResults) > 0
        numTrials = length(distanceResults);
        numCorrect = sum([distanceResults.correct]);
        accuracy = (numCorrect / numTrials) * 100;
        avgConfidence = mean([distanceResults.confidence]);
        avgResponseTime = mean([distanceResults.responseTime]);
        avgReactionTime = mean([distanceResults.reactionTime]);  % NEW
        
        fprintf('%s (All categories):\n', distances{d});
        fprintf('  Trials: %d\n', numTrials);
        fprintf('  Correct: %d\n', numCorrect);
        fprintf('  Accuracy: %.1f%%\n', accuracy);
        fprintf('  Average Confidence: %.1f/5\n', avgConfidence);
        fprintf('  Average Response Time: %.2f seconds\n', avgResponseTime);
        fprintf('  Average Reaction Time: %.3f seconds\n\n', avgReactionTime);  % NEW
    end
end

fprintf('CONFIDENCE vs ACCURACY ANALYSIS:\n');
fprintf('================================\n\n');

for conf = 1:5
    confidenceMask = [results.confidence] == conf;
    confidenceResults = results(confidenceMask);
    
    if length(confidenceResults) > 0
        numTrials = length(confidenceResults);
        numCorrect = sum([confidenceResults.correct]);
        accuracy = (numCorrect / numTrials) * 100;
        avgReactionTime = mean([confidenceResults.reactionTime]);  % NEW
        
        fprintf('Confidence Level %d:\n', conf);
        fprintf('  Trials: %d\n', numTrials);
        fprintf('  Correct: %d\n', numCorrect);
        fprintf('  Accuracy: %.1f%%\n', accuracy);
        fprintf('  Average Reaction Time: %.3f seconds\n\n', avgReactionTime);  % NEW
    end
end

fprintf('REACTION TIME ANALYSIS:\n');
fprintf('=======================\n\n');
reactionTimes = [results.reactionTime];
fprintf('Minimum Reaction Time: %.3f seconds\n', min(reactionTimes));
fprintf('Maximum Reaction Time: %.3f seconds\n', max(reactionTimes));
fprintf('Median Reaction Time: %.3f seconds\n', median(reactionTimes));
fprintf('Standard Deviation: %.3f seconds\n\n', std(reactionTimes));

fprintf('========== SUMMARY MESSAGE ==========\n');
fprintf('You completed %d trials with %.1f%% overall accuracy.\n', totalTrials, overallAccuracy);
fprintf('Your average reaction time was %.3f seconds.\n', avgReactionTime);

bestAccuracy = 0;
worstAccuracy = 100;
bestCategory = '';
worstCategory = '';

for c = 1:length(categories)
    for d = 1:length(distances)
        categoryMask = strcmp({results.category}, categories{c});
        distanceMask = strcmp({results.distance}, distances{d});
        combinedMask = categoryMask & distanceMask;
        
        if sum(combinedMask) > 0
            categoryResults = results(combinedMask);
            accuracy = (sum([categoryResults.correct]) / length(categoryResults)) * 100;
            avgConf = mean([categoryResults.confidence]);
            
            categoryName = sprintf('%s %s', categories{c}, distances{d});
            
            if accuracy > bestAccuracy
                bestAccuracy = accuracy;
                bestCategory = sprintf('%s with %.1f%% accuracy and %.1f average confidence', categoryName, accuracy, avgConf);
            end
            
            if accuracy < worstAccuracy
                worstAccuracy = accuracy;
                worstCategory = sprintf('%s with %.1f%% accuracy and %.1f average confidence', categoryName, accuracy, avgConf);
            end
        end
    end
end

