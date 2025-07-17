import sys
import traceback
from datetime import datetime

def detailed_exception_info(extra_info: str = "") -> str:
    """Get detailed exception information as a formatted string"""
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_type is None:
        return "No exception currently being handled"

    # Build the detailed info string directly
    timestamp = datetime.now().isoformat()
    exception_name = exc_type.__name__
    exception_message = str(exc_value)
    full_traceback = traceback.format_exc()

    # Get additional context information
    frame_info = ""
    if exc_traceback:
        tb_frame = exc_traceback.tb_frame
        filename = tb_frame.f_code.co_filename
        line_number = exc_traceback.tb_lineno
        function_name = tb_frame.f_code.co_name

        frame_info = f"""
extra_info: {extra_info}
Location Details:
  File: {filename}
  Function: {function_name}
  Line: {line_number}"""

    # Get local variables from the exception frame (if available)
    local_vars = ""
    if exc_traceback and exc_traceback.tb_frame.f_locals:
        locals_dict = exc_traceback.tb_frame.f_locals
        # Filter out built-ins and large objects for cleaner output
        filtered_locals = {
            k: str(v)[:100] + "..." if len(str(v)) > 100 else v
            for k, v in locals_dict.items()
            if not k.startswith('__') and not callable(v)
        }

        if filtered_locals:
            local_vars = "\nLocal Variables:\n"
            for var_name, var_value in filtered_locals.items():
                local_vars += f"  {var_name} = {repr(var_value)}\n"

    # Construct the final detailed error message
    detailed_info = f"""{'=' * 60}
EXCEPTION DETAILS
{'=' * 60}
Timestamp: {timestamp}
Exception Type: {exception_name}
Exception Message: {exception_message}{frame_info}{local_vars}

Full Traceback:
{'-' * 40}
{full_traceback}{'=' * 60}"""

    return detailed_info
