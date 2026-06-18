function drawConfidenceBar(window, leftBarBase, rightBarBase, barSegmentHeight, confidenceColors, highlightLeft, highlightRight)
    numLevels = size(confidenceColors, 1);
    
    for level = 1:numLevels
        segmentRect = [leftBarBase(1), ...
                       leftBarBase(4) - level * barSegmentHeight, ...
                       leftBarBase(3), ...
                       leftBarBase(4) - (level-1) * barSegmentHeight];
        
        if highlightLeft == level
            Screen('FillRect', window, [255, 255, 255], segmentRect); % سفید برای هایلایت
            Screen('FrameRect', window, [0, 0, 0], segmentRect, 4); % حاشیه ضخیم‌تر
        else
            Screen('FillRect', window, confidenceColors(level, :), segmentRect);
            Screen('FrameRect', window, [0, 0, 0], segmentRect, 2); % حاشیه ضخیم‌تر
        end
    end
    
    for level = 1:numLevels
        segmentRect = [rightBarBase(1), ...
                       rightBarBase(4) - level * barSegmentHeight, ...
                       rightBarBase(3), ...
                       rightBarBase(4) - (level-1) * barSegmentHeight];
        
        if highlightRight == level
            Screen('FillRect', window, [255, 255, 255], segmentRect); % سفید برای هایلایت
            Screen('FrameRect', window, [0, 0, 0], segmentRect, 4); % حاشیه ضخیم‌تر
        else
            Screen('FillRect', window, confidenceColors(level, :), segmentRect);
            Screen('FrameRect', window, [0, 0, 0], segmentRect, 2); % حاشیه ضخیم‌تر
        end
    end
end

