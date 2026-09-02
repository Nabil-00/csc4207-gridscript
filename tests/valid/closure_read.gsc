// Functions with no return fall through to 0; global read-only from inside a function
set bonus = 10

def add_bonus(value)
    return value + bonus
end

print add_bonus(5)
