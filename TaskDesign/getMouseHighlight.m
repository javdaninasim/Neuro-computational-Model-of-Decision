
function [highlightLeft, highlightRight] = getMouseHighlight(leftBarBase, rightBarBase, barSegmentHeight, numLevels)
    highlightLeft = 0;
    highlightRight = 0;
    
    [x, y, ~] = GetMouse;
    
    % بررسی موقعیت در نوار چپ
    if x >= leftBarBase(1) && x <= leftBarBase(3) && y >= leftBarBase(2) && y <= leftBarBase(4)
        relativeY = y - leftBarBase(2);
        highlightLeft = numLevels - floor(relativeY / barSegmentHeight);
        highlightLeft = max(1, min(numLevels, highlightLeft));
    end
    
    % بررسی موقعیت در نوار راست
    if x >= rightBarBase(1) && x <= rightBarBase(3) && y >= rightBarBase(2) && y <= rightBarBase(4)
        relativeY = y - rightBarBase(2);
        highlightRight = numLevels - floor(relativeY / barSegmentHeight);
        highlightRight = max(1, min(numLevels, highlightRight));
    end
end
