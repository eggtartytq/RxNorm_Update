import tkinter
from tkinter import filedialog
import pandas as pd
import settings


class SelectFiles:
    fileForm = pd.DataFrame(columns=['file', 'date', 'unzip_dir'])

    def get_target_files_with_gui(self):
        """
        select target files, and order by date
        :return:
        """
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        # call system file selecting dialog to select zip files
        folder_path = filedialog.askopenfiles()
        if len(folder_path) == 0:
            raise ValueError('Select at least one zip file of RxNORM release!')
        for i in range(0, len(folder_path)):
            self.fileForm.loc[i, 'file'] = folder_path[i].name
        self.get_date_and_sort()
        return self.fileForm

    def get_target_files_without_gui(self):
        self.fileForm.file = pd.read_csv(settings.FILE_PATH_CONFIG, header=None)
        self.fileForm.dropna(inplace=True, subset=["file"])
        self.get_date_and_sort()
        return self.fileForm

    def get_date_and_sort(self):
        for i in self.fileForm.index:
            filename = self.fileForm.loc[i, 'file']
            self.fileForm.loc[i, 'date'] = filename.split("_")[-1].split(".")[0]
        self.fileForm.sort_values('date', ascending=True, inplace=True)


if __name__ == "__main__":
    app = SelectFiles()
    print(app.get_target_files_with_gui())
    app = SelectFiles()
    print(app.get_target_files_without_gui())
