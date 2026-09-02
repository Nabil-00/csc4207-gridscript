// GridScript example: a quest for treasure
set gold = 0
set steps = 0
set found_treasure = false

def find_treasure(distance)
    while distance > 0 do
        step_forward()
        set distance = distance - 1
    end
    turn_left()
    return 1
end

find_treasure(3)
set gold = gold + 10
print "gold: " + "10"

while steps < 2 do
    set steps = steps + 1
end

print found_treasure
print "done"
