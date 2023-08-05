import sys, json, datetime, os, time
from PyQt5 import QtCore, QtWidgets
from core.utils import center, background, Worker, find_consec, find_keys, raise_window, \
    cancel_window, Communicate
from core.settings import Settings_Window
from core.smtpSettings import SmtpSettings, AddExpter, add_Expter
from core.klusta_functions import klusta, check_klusta_ready
from core.klusta_utils import folder_ready
from core.ChooseDirectory import chooseDirectory, new_directory
from core.addSessions import RepeatAddSessions
from core.utils import print_msg
from core.defaultParameters import defaultAppend

_author_ = "Geoffrey Barrett"  # defines myself as the author


class Window(QtWidgets.QWidget):  # defines the window class (main window)

    def __init__(self):  # initializes the main window
        super(Window, self).__init__()

        background(self)  # acquires some features from the background function we defined earlier
        self.setWindowTitle("BatchTINT - Main Window")  # sets the title of the window

        self.numCores = str(os.cpu_count())  # initializing the number of cores the users CPU has

        self.settingsWindow = None

        self.RepeatAddSessionsThread = QtCore.QThread(self)
        self.BatchTintThread = QtCore.QThread()
        self.reset_add_thread = False
        self.repeat_thread_active = False
        self.append_changed = False

        self.current_session = ''
        self.current_subdirectory = ''
        self.LogAppend = Communicate()
        self.LogAppend.myGUI_signal_str.connect(self.AppendLog)

        self.LogError = Communicate()
        self.LogError.myGUI_signal_str.connect(self.raiseError)

        self.RemoveQueueItem = Communicate()
        self.RemoveQueueItem.myGUI_signal_str.connect(self.takeTopLevel)

        self.RemoveSessionItem = Communicate()
        self.RemoveSessionItem.myGUI_signal_str.connect(self.takeChild)

        self.RemoveSessionData = Communicate()
        self.RemoveSessionData.myGUI_signal_str.connect(self.takeChildData)

        self.RemoveChildItem = Communicate()
        self.RemoveChildItem.myGUI_signal_QTreeWidgetItem.connect(self.removeChild)

        self.adding_session = True
        self.reordering_queue = False
        self.modifying_list = False

        self.choice = None
        self.home()  # runs the home function

    def home(self):  # defines the home function (the main window)

        try:  # attempts to open previous directory catches error if file not found
            # No saved directory's need to create file
            with open(self.directory_settings, 'r+') as filename:  # opens the defined file
                directory_data = json.load(filename)  # loads the directory data from file
                if os.path.exists(directory_data['directory']):
                    current_directory_name = directory_data['directory']  # defines the data
                else:
                    current_directory_name = 'No Directory Currently Chosen!'  # states that no directory was chosen

        except FileNotFoundError:  # runs if file not found
            with open(self.directory_settings, 'w') as filename:  # opens a file
                current_directory_name = 'No Directory Currently Chosen!'  # states that no directory was chosen
                directory_data = {'directory': current_directory_name}  # creates a dictionary
                json.dump(directory_data, filename)  # writes the dictionary to the file

        # ------buttons ------------------------------------------
        quitbtn = QtWidgets.QPushButton('Quit', self)  # making a quit button
        quitbtn.clicked.connect(self.close_app)  # defining the quit button functionality (once pressed)
        quitbtn.setShortcut("Ctrl+Q")  # creates shortcut for the quit button
        quitbtn.setToolTip('Click to quit Batch-Tint!')

        self.setbtn = QtWidgets.QPushButton('Klusta Settings')  # Creates the settings pushbutton
        self.setbtn.setToolTip('Define the settings that KlustaKwik will use.')

        self.klustabtn = QtWidgets.QPushButton('Run', self)  # creates the batch-klusta pushbutton
        self.klustabtn.setToolTip('Click to perform batch analysis via Tint and KlustaKwik!')

        self.smtpbtn = QtWidgets.QPushButton('SMTP Settings', self)
        self.smtpbtn.setToolTip("Click to change the SMTP settings for e-mail notifications.")

        self.choose_dir = QtWidgets.QPushButton('Choose Directory', self)  # creates the choose directory pushbutton

        self.current_directory = QtWidgets.QLineEdit()  # creates a line edit to display the chosen directory (current)
        self.current_directory.textChanged.connect(self.change_directory)
        self.current_directory.setText(current_directory_name)  # sets the text to the current directory
        self.current_directory.setAlignment(QtCore.Qt.AlignHCenter)  # centers the text
        self.current_directory.setToolTip('The current directory that Batch-Tint will analyze.')

        # defines an attribute to exchange info between classes/modules
        self.current_directory_name = current_directory_name

        # defines the button functionality once pressed
        self.klustabtn.clicked.connect(lambda: self.run(self.current_directory_name))

        # ------------------------------------ check box  ------------------------------------------------
        self.nonbatch_check = QtWidgets.QCheckBox('Non-Batch?')
        self.nonbatch_check.setToolTip("Check this if you don't want to run batch. This means you will choose\n"
                                       "the folder that directly contains all the session files (.set, .pos, .N, etc.).")

        self.silent_cb = QtWidgets.QCheckBox('Run Silently')
        self.silent_cb.setToolTip("Check if you want Tint to run in the background.")

        # ---------------- queue widgets --------------------------------------------------
        self.directory_queue = QtWidgets.QTreeWidget()
        self.directory_queue.headerItem().setText(0, "Axona Sessions:")
        self.directory_queue.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        directory_queue_label = QtWidgets.QLabel('Queue: ')

        self.up_btn = QtWidgets.QPushButton("Move Up", self)
        self.up_btn.setToolTip("Clcik this button to move selected directories up on the queue!")
        self.up_btn.clicked.connect(lambda: self.moveQueue('up'))

        self.down_btn = QtWidgets.QPushButton("Move Down", self)
        self.down_btn.setToolTip("Clcik this button to move selected directories down on the queue!")
        self.down_btn.clicked.connect(lambda: self.moveQueue('down'))

        queue_btn_layout = QtWidgets.QVBoxLayout()
        queue_btn_layout.addWidget(self.up_btn)
        queue_btn_layout.addWidget(self.down_btn)

        queue_layout = QtWidgets.QVBoxLayout()
        queue_layout.addWidget(directory_queue_label)
        queue_layout.addWidget(self.directory_queue)

        queue_and_btn_layout = QtWidgets.QHBoxLayout()
        queue_and_btn_layout.addLayout(queue_layout)
        queue_and_btn_layout.addLayout(queue_btn_layout)

        # ------------------------ multithreading widgets -------------------------------------

        Multithread_l = QtWidgets.QLabel('Simultaneous Tetrodes (#):')
        Multithread_l.setToolTip('Input the number of tetrodes you want to analyze simultaneously')

        self.numThreads = QtWidgets.QLineEdit()

        Multi_layout = QtWidgets.QHBoxLayout()

        # for order in [self.multithread_cb, core_num_l, self.core_num, Multithread_l, self.numThreads]:
        for order in [Multithread_l, self.numThreads]:
            if 'Layout' in order.__str__():
                Multi_layout.addLayout(order)
            else:
                Multi_layout.addWidget(order, 0, QtCore.Qt.AlignCenter)

        # ----- append cut --------------------
        append_cut_label = QtWidgets.QLabel("Append Cut:")
        self.append_cut = QtWidgets.QLineEdit()
        self.append_cut.setText(defaultAppend)
        self.append_cut.textChanged.connect(self.change_append)

        append_cut_layout = QtWidgets.QHBoxLayout()
        append_cut_layout.addWidget(append_cut_label)
        append_cut_layout.addWidget(self.append_cut)

        parameter_layout = QtWidgets.QHBoxLayout()
        parameter_layout.addStretch(1)
        parameter_layout.addWidget(self.nonbatch_check)
        parameter_layout.addStretch(1)
        parameter_layout.addWidget(self.silent_cb)
        parameter_layout.addStretch(1)
        parameter_layout.addLayout(Multi_layout)
        parameter_layout.addStretch(1)
        parameter_layout.addLayout(append_cut_layout)
        parameter_layout.addStretch(1)

        try:
            with open(self.settings_fname, 'r+') as filename:
                settings = json.load(filename)
                self.numThreads.setText(str(settings['NumThreads']))
                if settings['Silent'] == 1:
                    self.silent_cb.toggle()
                if settings['nonbatch'] == 1:
                    self.nonbatch_check.toggle()

        except FileNotFoundError:
            self.silent_cb.toggle()
            self.numThreads.setText('1')

        self.get_non_batch()

        # ------------- Log Box -------------------------
        self.Log = QtWidgets.QTextEdit()
        log_label = QtWidgets.QLabel('Log: ')

        log_lay = QtWidgets.QVBoxLayout()
        log_lay.addWidget(log_label, 0, QtCore.Qt.AlignTop)
        log_lay.addWidget(self.Log)

        # ------------------------------------ version information -------------------------------------------------

        # creates a label with that information
        vers_label = QtWidgets.QLabel("BatchTINT V3.1.0")

        # ------------------- page layout ----------------------------------------
        layout = QtWidgets.QVBoxLayout()  # setting the layout

        layout1 = QtWidgets.QHBoxLayout()  # setting layout for the directory options
        layout1.addWidget(self.choose_dir)  # adding widgets to the first tab
        layout1.addWidget(self.current_directory)

        btn_order = [self.klustabtn, self.setbtn, self.smtpbtn, quitbtn]  # defining button order (left to right)
        btn_layout = QtWidgets.QHBoxLayout()  # creating a widget to align the buttons
        for butn in btn_order:  # adds the buttons in the proper order
            btn_layout.addWidget(butn)

        layout_order = [layout1, parameter_layout, queue_and_btn_layout, log_lay, btn_layout]

        layout.addStretch(1)  # adds the widgets/layouts according to the order
        for order in layout_order:
            if 'Layout' in order.__str__():
                layout.addLayout(order)
                layout.addStretch(1)
            else:
                layout.addWidget(order, 0, QtCore.Qt.AlignCenter)
                layout.addStretch(1)

        layout.addStretch(1)  # adds stretch to put the version info at the bottom
        layout.addWidget(vers_label)  # adds the date modification/version number
        self.setLayout(layout)  # sets the widget to the one we defined

        center(self)  # centers the widget on the screen

        # if self.current_directory_name != 'No Directory Currently Chosen!':
        # starting adding any existing sessions in a different thread
        # self.RepeatAddSessionsThread = QtCore.QThread(self)
        self.RepeatAddSessionsThread.start()
        self.RepeatAddSessionsWorker = Worker(RepeatAddSessions, self)
        self.RepeatAddSessionsWorker.moveToThread(self.RepeatAddSessionsThread)
        self.RepeatAddSessionsWorker.start.emit("start")

        self.show()  # shows the widget

    def run(self, directory):  # function that runs klustakwik

        """This method runs when the Batch-TINT button is pressed on the GUI,
        and commences the analysis"""
        self.batch_tint = True
        self.klustabtn.setText('Stop')
        self.klustabtn.setToolTip('Click to stop Batch-Tint.')  # defining the tool tip for the start button
        self.klustabtn.clicked.disconnect()
        self.klustabtn.clicked.connect(self.stopBatch)

        # self.BatchTintThread = QtCore.QThread()
        self.BatchTintThread.start()

        self.BatchTintWorker = Worker(runGUI, self, self.settingsWindow, directory)
        self.BatchTintWorker.moveToThread(self.BatchTintThread)
        self.BatchTintWorker.start.emit("start")

    def close_app(self):
        # pop up window that asks if you really want to exit the app ------------------------------------------------

        choice = QtWidgets.QMessageBox.question(self, "Quitting BatchTINT",
                                                "Do you really want to exit?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()  # tells the app to quit
        else:
            pass

    def raiseError(self, error_val):
        """raises an error window given certain errors from an emitted signal"""

        if 'ManyFet' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "No Chosen Directory: BatchTINT",
                                                         "You have chosen more than four features,\n"
                                                         "clustering will take a long time.\n"
                                                         "Do you realy want to continue?",
                                                         QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        elif 'NoDir' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "No Chosen Directory: BatchTINT",
                                                         "You have not chosen a directory,\n"
                                                         "please choose one to continue!",
                                                         QtWidgets.QMessageBox.Ok)

        elif 'GoogleDir' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "Google Drive Directory: BatchTINT",
                                                         "You have not chosen a directory within Google Drive,\n"
                                                         "be aware that during testing we have experienced\n"
                                                         "permissions errors while using Google Drive directories\n"
                                                         "that would result in BatchTINTV3 not being able to move\n"
                                                         "the files to the Processed folder (and stopping the GUI),\n"
                                                         "do you want to continue?",
                                                         QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        elif 'NoSet' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "No .Set Files!",
                                                         "You have chosen a directory that has no .Set files!\n"
                                                         "Please choose a different directory!",
                                                         QtWidgets.QMessageBox.Ok)

        elif 'InvDirBatch' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "Invalid Directory!",
                                                         "In 'Batch Mode' you need to choose a directory\n"
                                                         "with subdirectories that contain all your Tint\n"
                                                         "files. Press Abort and choose new file, or if you\n"
                                                         "plan on adding folders to the chosen directory press\n"
                                                         "continue.",
                                                         QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Ok)
        elif 'InvDirNonBatch' in error_val:
            self.choice = QtWidgets.QMessageBox.question(self, "Invalid Directory!",
                                                         "In 'Non-Batch Mode' you need to choose a directory\n"
                                                         "that contain all your Tint files.\n",
                                                         QtWidgets.QMessageBox.Ok)

    def AppendLog(self, message):
        """
        A function that will append the Log field of the main window (mainly
        used as a slot for a custom pyqt signal)
        """
        if '#' in message:
            message = message.split('#')
            color = message[-1].lower()
            message = message[0]
            message = '<span style="color:%s">%s</span>' % (color, message)

        self.Log.append(message)

    def stopBatch(self):

        enableParameters(self)

        self.klustabtn.clicked.connect(lambda: self.run(self.current_directory_name))
        self.BatchTintThread.terminate()

        self.LogAppend.myGUI_signal_str.emit(
            '[%s %s]: BatchTint stopped!' % (str(datetime.datetime.now().date()),
                                             str(datetime.datetime.now().time())[
                                             :8]))

        self.batch_tint = False
        self.klustabtn.setText('Run')
        self.klustabtn.setToolTip(
            'Click to perform batch analysis via Tint and KlustaKwik!')  # defining the tool tip for the start button

    def change_directory(self):
        """
        Whenever directory is changed, clear the directory queue
        """
        self.current_directory_name = self.current_directory.text()

        try:
            self.directory_queue.clear()
        except AttributeError:
            pass

        self.restart_add_sessions_thread()

    def change_append(self):

        self.change_append_time = time.time()
        self.append_changed = True

    def restart_add_sessions_thread(self):

        self.reset_add_thread = True

        if not hasattr(self, 'repeat_thread_active'):
            return

        while self.repeat_thread_active:
            time.sleep(0.1)

        self.RepeatAddSessionsThread.setTerminationEnabled(True)
        self.RepeatAddSessionsThread.start()

        self.RepeatAddSessionsWorker = Worker(RepeatAddSessions, self)
        self.RepeatAddSessionsWorker.moveToThread(self.RepeatAddSessionsThread)
        self.RepeatAddSessionsWorker.start.emit("start")

    def moveQueue(self, direction):
        # get all the queue items

        while self.adding_session:
            time.sleep(0.1)
            if self.reordering_queue:
                self.reordering_queue = False

        self.reordering_queue = True

        item_count = self.directory_queue.topLevelItemCount()
        queue_items = {}
        for item_index in range(item_count):
            queue_items[item_index] = self.directory_queue.topLevelItem(item_index)

        # get selected options and their locations
        selected_items = self.directory_queue.selectedItems()
        selected_items_copy = []
        [selected_items_copy.append(item.clone()) for item in selected_items]

        add_to_new_queue = list(queue_items.values())

        if not selected_items:
            # skips when there are no items selected
            return

        new_queue_order = {}

        # find if consecutive indices from 0 on are selected as these won't move any further up

        indices = find_keys(queue_items, selected_items)
        consecutive_indices = find_consec(indices)
        # this will spit a list of lists, these nested lists will have consecutive indices within them
        # i.e. if indices 0, 1 and 3 were chosen it would have [[0, 1], [3]]

        if 'up' in direction:
            # first add the selected items to their new spots
            for consecutive in consecutive_indices:
                if 0 in consecutive:
                    # these items can't move up any further
                    for index in consecutive:
                        new_item = queue_items[index].clone()
                        new_queue_order[index] = new_item

                else:
                    for index in consecutive:
                        # move these up the list (decrease in index value since 0 is the top of the list)
                        new_item = queue_items[index].clone()
                        new_queue_order[index - 1] = new_item

            for key, val in new_queue_order.items():
                for index, item in enumerate(add_to_new_queue):
                    if val.data(0, 0) == item.data(0, 0):
                        add_to_new_queue.remove(item)  # remove item from the list
                        break

            _ = list(new_queue_order.keys())  # a list of already moved items

            not_in_reordered = False
            # place the unplaced items that aren't moving
            for static_index, static_value in queue_items.items():
                # print(static_value.data(0,0))
                # place the unplaced items
                if static_index in _:
                    continue

                for queue_item in new_queue_order.values():
                    not_in_reordered = True
                    if static_value.data(0, 0) == queue_item.data(0, 0):
                        # don't re-add the one that is going to be moved
                        not_in_reordered = False
                        break

                if not_in_reordered:
                    for value in add_to_new_queue:
                        if static_value.data(0, 0) == value.data(0, 0):
                            add_to_new_queue.remove(value)  # remove item from the list
                            break

                    new_queue_order[static_index] = static_value.clone()

        elif 'down' in direction:
            # first add the selected items to their new spots
            for consecutive in consecutive_indices:
                if (item_count - 1) in consecutive:
                    # these items can't move down any further
                    for index in consecutive:
                        new_item = queue_items[index].clone()
                        # new_item.setSelected(True)
                        new_queue_order[index] = new_item
                else:
                    for index in consecutive:
                        # move these down the list (increase in index value since 0 is the top of the list)
                        new_item = queue_items[index].clone()
                        # new_item.setSelected(True)
                        new_queue_order[index + 1] = new_item

            for key, val in new_queue_order.items():
                for index, item in enumerate(add_to_new_queue):
                    if val.data(0, 0) == item.data(0, 0):
                        add_to_new_queue.remove(item)
                        break

            _ = list(new_queue_order.keys())  # a list of already moved items

            not_in_reordered = False
            # place the unplaced items that aren't moving
            for static_index, static_value in queue_items.items():
                if static_index in _:
                    continue

                for queue_item in new_queue_order.values():
                    not_in_reordered = True
                    if static_value.data(0, 0) == queue_item.data(0, 0):
                        # don't re-add the one that is going to be moved
                        not_in_reordered = False
                        break

                if not_in_reordered:
                    for value in add_to_new_queue:
                        if static_value.data(0, 0) == value.data(0, 0):
                            add_to_new_queue.remove(value)  # remove item from the list
                            break

                    new_queue_order[static_index] = static_value.clone()

        # add the remaining items
        indices_needed = [index for index in range(item_count) if index not in list(new_queue_order.keys())]
        for index, displaced_item in enumerate(add_to_new_queue):
            new_queue_order[indices_needed[index]] = displaced_item.clone()

        self.directory_queue.clear()  # clears the list

        for key, value in sorted(new_queue_order.items()):
            self.directory_queue.addTopLevelItem(value)

        # reselect the items
        iterator = QtWidgets.QTreeWidgetItemIterator(self.directory_queue)
        while iterator.value():
            for selected_item in selected_items_copy:
                item = iterator.value()
                if item.data(0, 0) == selected_item.data(0, 0):
                    item.setSelected(True)
                    break
            iterator += 1
        self.reordering_queue = False

    def takeTopLevel(self, item_count):
        item_count = int(item_count)
        self.directory_queue.takeTopLevelItem(item_count)
        self.top_level_taken = True

    def setChild(self, child_count):
        self.child_session = self.directory_item.child(int(child_count))
        self.child_set = True

    def takeChild(self, child_count):
        self.child_session = self.directory_item.takeChild(int(child_count))
        self.child_taken = True
        # return child_session

    def takeChildData(self, child_count):
        self.child_session = self.directory_item.takeChild(int(child_count)).data(0, 0)
        self.child_data_taken = True

    def removeChild(self, QTreeWidgetItem):
        root = self.directory_queue.invisibleRootItem()
        (QTreeWidgetItem.parent() or root).removeChild(QTreeWidgetItem)
        self.child_removed = True

    def get_non_batch(self):
        if self.nonbatch_check.isChecked():
            self.nonbatch = 1
        else:
            self.nonbatch = 0

    def getMainWindowSettings(self):
        settings = {}

        if self.silent_cb.isChecked():
            settings['Silent'] = 1
        else:
            settings['Silent'] = 0

        if self.nonbatch_check.isChecked():
            settings['nonbatch'] = 1
            self.nonbatch = 1
        else:
            settings['nonbatch'] = 0
            self.nonbatch = 0

        settings['NumThreads'] = self.numThreads.text()

        settings['Cores'] = str(os.cpu_count())

        return settings


def disableParameters(main_window):
    main_window.numThreads.setEnabled(0)
    main_window.silent_cb.setEnabled(0)
    main_window.nonbatch_check.setEnabled(0)
    main_window.choose_dir.setEnabled(0)
    main_window.setbtn.setEnabled(0)
    main_window.current_directory.setEnabled(0)
    main_window.append_cut.setEnabled(0)


def enableParameters(main_window):
    main_window.numThreads.setEnabled(1)
    main_window.silent_cb.setEnabled(1)
    main_window.nonbatch_check.setEnabled(1)
    main_window.choose_dir.setEnabled(1)
    main_window.setbtn.setEnabled(1)
    main_window.current_directory.setEnabled(1)
    main_window.append_cut.setEnabled(1)


def getNextSetFiles(self):

    set_files = []

    if self.nonbatch == 0:
        directory = self.current_directory.text()
    elif self.nonbatch == 1:
        directory = os.path.dirname(self.current_directory.text())

    subdirectory = self.directory_item.data(0, 0)
    for i in range(self.directory_item.childCount()):
        session_item = self.directory_item.child(i)
        set_files.append(os.path.realpath(os.path.join(directory, subdirectory, session_item.data(0, 0))))

    return set_files


def getSetFileChildNumber(self, set_file):
    """
    This function will find the position within the Queue that the Session is located in.
    :param self:
    :param set_file:
    :return:
    """
    subdirectory = self.directory_item.data(0, 0)
    for i in range(self.directory_item.childCount()):
        session_item = self.directory_item.child(i)
        if self.nonbatch == 1:
            current_setfile = os.path.realpath(os.path.join(self.current_directory.text(), session_item.data(0, 0)))
        else:
            current_setfile = os.path.realpath(os.path.join(self.current_directory.text(), subdirectory,
                                                            session_item.data(0, 0)))

        if os.path.realpath(set_file) == os.path.realpath(current_setfile):
            return i

    return None


def runGUI(main_window, settings_window, directory):
    """This method is executed when you press 'Run' in the GUI."""
    # ------- making a function that runs the entire GUI ----------

    # overwrite with the latest settings file data

    disableParameters(main_window)

    main_settings = main_window.getMainWindowSettings()

    with open(main_window.settings_fname, 'r+') as f:  # opens settings file
        written_settings = json.load(f)  # loads settings

    for key, value in main_settings.items():
        written_settings[key] = value

    with open(main_window.settings_fname, 'w') as f:
        json.dump(written_settings, f)

    settings = {}

    # the advanced / basic settings have an Apply functionality that will save those settings, therefore we will not
    # include them in overwriting the settings above.
    basic_settings = settings_window.get_basic_settings()
    advanced_settings = settings_window.get_advanced_settings()

    settings.update(basic_settings)
    settings.update(advanced_settings)
    settings.update(main_settings)

    main_window.numThreads.setEnabled(0)

    # checks if the settings are appropriate to run analysis
    klusta_ready = check_klusta_ready(settings, directory, self=main_window,
                                      settings_filename=main_window.settings_fname,
                                      numThreads=settings['NumThreads'],
                                      numCores=settings['Cores'])

    if klusta_ready:
        main_window.LogAppend.myGUI_signal_str.emit(
            '[%s %s]: Analyzing the following directory: %s!' % (str(datetime.datetime.now().date()),
                                                                 str(datetime.datetime.now().time())[
                                                                 :8], directory))

        if main_window.nonbatch == 0:
            # message that shows how many files were found
            main_window.LogAppend.myGUI_signal_str.emit(
                '[%s %s]: Found %d sub-directories in the directory!' % (str(datetime.datetime.now().date()),
                                                                         str(datetime.datetime.now().time())[
                                                                         :8],
                                                                         main_window.directory_queue.topLevelItemCount()))

        else:
            directory = os.path.dirname(directory)

        if main_window.directory_queue.topLevelItemCount() == 0:
            if main_window.nonbatch == 1:
                main_window.choice = None
                main_window.LogError.myGUI_signal_str.emit('InvDirNonBatch')
                while main_window.choice is None:
                    time.sleep(0.2)
                main_window.stopBatch()
                return
            else:
                main_window.choice = None
                main_window.LogError.myGUI_signal_str.emit('InvDirBatch')
                while main_window.choice is None:
                    time.sleep(0.2)

                if main_window.choice == QtWidgets.QMessageBox.Abort:
                    main_window.stopBatch()
                    return

        # ----------- cycle through each file and find the tetrode files ------------------------------------------

        while main_window.batch_tint:
            # grabs the top item from the queue
            main_window.directory_item = main_window.directory_queue.topLevelItem(0)

            if not main_window.directory_item:
                continue
            else:
                # grab the subdirectory of the item object
                main_window.current_subdirectory = main_window.directory_item.data(0, 0)

                # check if the directory exists, if not, remove it
                if not os.path.exists(os.path.join(directory, main_window.current_subdirectory)):
                    # path does not exist, remove
                    main_window.top_level_taken = False
                    main_window.modifying_list = True
                    main_window.RemoveQueueItem.myGUI_signal_str.emit(str(0))
                    while not main_window.top_level_taken:
                        time.sleep(0.1)
                    main_window.modifying_list = False
                    continue

            # if there are sessions within the subdirectory, analyze them
            while main_window.directory_item.childCount() != 0:
                # set the current session
                main_window.current_session = main_window.directory_item.child(0).data(0, 0)

                sub_directory = main_window.directory_item.data(0, 0)

                directory_ready = False

                main_window.LogAppend.myGUI_signal_str.emit(
                    '[%s %s]: Checking if the following directory is ready to analyze: %s!' % (
                        str(datetime.datetime.now().date()),
                        str(datetime.datetime.now().time())[
                        :8], str(sub_directory)))

                while not directory_ready:
                    directory_ready = folder_ready(main_window, os.path.join(directory, sub_directory))

                try:
                    # runs the function that will perform the klusta'ing
                    if not os.path.exists(os.path.join(directory, sub_directory)):
                        main_window.top_level_taken = False
                        main_window.modifying_list = True
                        main_window.RemoveQueueItem.myGUI_signal_str.emit(str(0))
                        while not main_window.top_level_taken:
                            time.sleep(0.1)
                        main_window.modifying_list = False
                        continue
                    else:

                        msg = '[%s %s]: Now analyzing files in the %s folder!' % (
                            str(datetime.datetime.now().date()),
                            str(datetime.datetime.now().time())[
                            :8], sub_directory)

                        print_msg(main_window, msg)

                        main_window.current_subdirectory = os.path.basename(sub_directory)

                        set_files = getNextSetFiles(main_window)

                        # if not DebugSkipKlusta:
                        analyzed_files = klusta(set_files, settings, self=main_window, append=main_window.append_cut.text())

                        for file in set_files:
                            childNum = getSetFileChildNumber(main_window, file)

                            # removes session from list
                            main_window.child_data_taken = False
                            main_window.modifying_list = True
                            main_window.RemoveSessionData.myGUI_signal_str.emit(str(childNum))
                            while not main_window.child_data_taken:
                                time.sleep(0.1)
                            main_window.modifying_list = False

                except NotADirectoryError:
                    # if the file is not a directory it prints this message
                    main_window.LogAppend.myGUI_signal_str.emit(
                        '[%s %s]: %s is not a directory!' % (
                            str(datetime.datetime.now().date()),
                            str(datetime.datetime.now().time())[
                            :8], str(sub_directory)))
                    continue

            if main_window.directory_item.childCount() == 0:
                # deletes sub-directory if there are no sessions left
                main_window.top_level_taken = False
                main_window.modifying_list = True
                main_window.RemoveQueueItem.myGUI_signal_str.emit(str(0))
                while not main_window.top_level_taken:
                    time.sleep(0.1)
                main_window.modifying_list = False

                main_window.current_subdirectory = ''
                main_window.current_session = ''


def run():
    app = QtWidgets.QApplication(sys.argv)

    main_w = Window()  # calling the main window
    chooseDirectory_w = chooseDirectory()  # calling the Choose Directory Window
    settings_w = Settings_Window()  # calling the settings window
    smtp_setting_w = SmtpSettings()  # calling the smtp settings window
    add_exper = AddExpter()

    main_w.settingsWindow = settings_w

    add_exper.addbtn.clicked.connect(lambda: add_Expter(add_exper, smtp_setting_w))
    # syncs the current directory on the main window
    chooseDirectory_w.current_directory_name = main_w.current_directory_name

    main_w.raise_()  # making the main window on top

    add_exper.cancelbtn.clicked.connect(lambda: cancel_window(smtp_setting_w, add_exper))
    add_exper.backbtn.clicked.connect(lambda: raise_window(smtp_setting_w, add_exper))

    smtp_setting_w.addbtn.clicked.connect(lambda: raise_window(add_exper, smtp_setting_w))

    main_w.choose_dir.clicked.connect(lambda: raise_window(chooseDirectory_w, main_w))

    # brings the main window to the foreground
    chooseDirectory_w.backbtn.clicked.connect(lambda: raise_window(main_w, chooseDirectory_w))
    chooseDirectory_w.applybtn.clicked.connect(lambda: chooseDirectory_w.apply_dir(main_w))
    # brings the main window to the foreground

    main_w.setbtn.clicked.connect(lambda: raise_window(settings_w, main_w))

    main_w.smtpbtn.clicked.connect(lambda: raise_window(smtp_setting_w, main_w))

    smtp_setting_w.backbtn.clicked.connect(lambda: raise_window(main_w, smtp_setting_w))

    settings_w.backbtn.clicked.connect(lambda: raise_window(main_w, settings_w))

    settings_w.backbtn2.clicked.connect(lambda: raise_window(main_w, settings_w))

    # prompts the user to choose a directory
    chooseDirectory_w.dirbtn.clicked.connect(lambda: new_directory(chooseDirectory_w, main_w))

    sys.exit(app.exec_())  # prevents the window from immediately exiting out


if __name__ == "__main__":
    run()  # the command that calls run()
