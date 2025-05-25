from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
globals = lua.globals()

# Set a global variable
globals.secret = 42

# Define a Lua function that uses the global
func = lua.eval('function() return secret end')
print("First run:", func())  # Output: 42

# Now change the global
globals.secret = 99
print("After change:", func())  # Output: 99

# Now remove the global
globals.secret = None
try:
    print("After removal:", func())  # Error, since 'secret' is nil
except Exception as e:
    print("Error after removal:", e)
