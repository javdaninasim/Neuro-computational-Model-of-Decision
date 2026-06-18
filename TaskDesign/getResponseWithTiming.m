function [response, confidence, responseTime, reactionTime] = getResponseWithTiming(window, leftBarBase, rightBarBase, barSegmentHeight, confidenceColors, numConfidenceLevels)

    functionStartTime = GetSecs;  
    screenFlipTime = 0;          
    firstClickTime = 0;           
    
    response = '';
    confidence = 0;
    responseGiven = false;
    screenFlipped = false;
    
    while ~responseGiven
        [highlightLeft, highlightRight] = getMouseHighlight(leftBarBase, rightBarBase, barSegmentHeight, numConfidenceLevels);
        
        drawConfidenceBar(window, leftBarBase, rightBarBase, barSegmentHeight, confidenceColors, highlightLeft, highlightRight);
        
        DrawFormattedText(window, 'NonAnimal', leftBarBase(1), leftBarBase(2)-30, [255, 255, 255]);
        DrawFormattedText(window, 'Animal', rightBarBase(1), rightBarBase(2)-30, [255, 255, 255]);
        
        Screen('Flip', window);
        
        if ~screenFlipped
            screenFlipTime = GetSecs;
            screenFlipped = true;
        end
        
        [x, y, buttons] = GetMouse;
        if any(buttons)
            if firstClickTime == 0
                firstClickTime = GetSecs;
            end
            
            [tempResponse, tempConfidence] = getMouseResponse(leftBarBase, rightBarBase, barSegmentHeight, numConfidenceLevels);
            
            if ~isempty(tempResponse)
                response = tempResponse;
                confidence = tempConfidence;
                responseGiven = true;
            end
            
            while any(buttons)
                [x, y, buttons] = GetMouse;
                WaitSecs(0.001);
            end
        end
        
        WaitSecs(0.001); 
    end
    
    finalTime = GetSecs;
    responseTime = finalTime - functionStartTime;     
    reactionTime = firstClickTime - screenFlipTime;   
    
end


