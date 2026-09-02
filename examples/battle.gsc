// GridScript example: actor battle — loops, conditionals, and the potion
set hp = 30
set potions = 1
set round = 0

while hp > 0 do
    set round = round + 1
    print "round " + "1"
    if hp < 25 then
        use_potion()
        set hp = 100
        print "potions: " + "0"
    end
    set hp = hp - 40
end

print "defeated"
