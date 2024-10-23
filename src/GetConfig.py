import os
import platform
import settings


def is_gui_available():
    """
    Return whether the current environment support GUI(Graphical User Interface).
    :return: bool, return True if supported, False if not support
    """
    system = platform.system()
    # Check for Windows (GUI always available)
    if system == 'Windows':
        return True
    # Check for macOS (GUI always available)
    if system == 'Darwin':
        return True
    # Check for Linux-based systems
    if system == 'Linux':
        # Check for X11 (X Window System)
        if os.environ.get('DISPLAY'):
            return True
        # Check for Wayland
        if os.environ.get('WAYLAND_DISPLAY'):
            return True
        # Check for Mir (specific to Ubuntu Unity)
        if os.environ.get('MIR_SERVER_NAME'):
            return True

        # Check for specific desktop environments on Linux
        desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if desktop_environment in ['kde', 'plasma']:
            return True
        if desktop_environment == 'gnome' and os.environ.get('GNOME_SHELL_SESSION_MODE') == 'wayland':
            return True
    return False


def get_config():
    '''
    Get the config and settings, including target DBMS, tables and files that want to import into the database.
    :return: dbms,selected_table_set, file_form
    '''
    table_set = {
        'RXNCONSO', 'RXNSAT', 'RXNSTY', 'RXNREL', 'RXNCUICHANGES'
    }
    dbms_set = {'mysql', 'postgresql'}

    # %% Check GUI and get config
    from GetConfig import is_gui_available
    from SelectFilesModules import SelectFiles
    if is_gui_available():
        # %% GUI: Select Target DBMS
        from SelectDBMSModules import SelectedDBMS
        dbs = SelectedDBMS(default_dbms=settings.DBMS)
        dbms = dbs.get_target_dbms()
        import SelectTablesModules
        selected_table_set = SelectTablesModules.get_selected_table_set(list(table_set))
        file_form = SelectFiles().get_target_files_with_gui()
    else:
        dbms = settings.DBMS
        selected_table_set = settings.TABLE
        file_form = SelectFiles().get_target_files_without_gui()
    # Check if config is legal
    if dbms not in dbms_set:
        raise IOError("Selected DBMS not in {'mysql','postgresql'}")
    if not selected_table_set.issubset(table_set):
        raise IOError("Selected tables not fully in {'RXNCONSO','RXNSAT','RXNSTY','RXNREL','RXNCUICHANGES'}")
    return dbms, selected_table_set, file_form


if __name__ == "__main__":
    if is_gui_available():
        print("GUI is available in this environment.")
    else:
        print("GUI is not available in this environment.")
