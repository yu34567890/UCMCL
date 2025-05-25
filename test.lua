

function set(args)
    local result = ""
    result = result .. "mov ax, " .. args[1][1] .. "\n"
    result = result .. "mov di, " .. vars[args[0][1]] .. "\n"
    result = result .. "mov word DS[di], ax\n"
    return result
end
