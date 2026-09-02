// Static scoping / shadowing demo: assignment inside a function is local
set x = 100

def hide()
    set x = 7
    return x
end

print x
print hide()
print x
