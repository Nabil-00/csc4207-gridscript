// The actor patrols, taking damage each step, until health runs out.
set health = 100
set damage = 25

while health > 0 do
    step_forward()
    set health = health - damage
    if health < 50 then
        print "low health"
    end
end
print "patrol complete"
