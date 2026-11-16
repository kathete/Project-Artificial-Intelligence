#Import of the class 'GUI_Control' to start the GUI.
from marketing_department_tool_gui_control import GUI_Control

#Calling the class 'GUI_Controll' and its function 'start_menu' to display the GUI.
call_start_menu = GUI_Control()
call_start_menu.start_menu()

#Keeps the windows open - important for the GUI exe
call_start_menu.window.mainloop()

