from Tkinter import *
from ttk import *

class SimpleTableInput(Frame):
    def __init__(self, parent, rows, columns):
        Frame.__init__(self, parent)

        self._entry = {}

        self.rows = len(rows)
        self.columns = len(columns)

        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows+1):
            for column in range(self.columns+1):
                if row == 0 and column ==0:
                    continue
                if row == 0 and column != 0:
                    Label(self, text=columns[column-1]).grid(row=row, column=column)
                elif column == 0 and row != 0:
                    Label(self, text=rows[row-1]).grid(row=row)
                else:
                    index = (row-1, column-1)
                    e = Entry(self, validate="key", validatecommand=vcmd)
                    e.grid(row=row, column=column, stick="nsew")
                    self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(self.rows, weight=1)

    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                value = self._entry[index].get()
                current_row.append(float(value))
            result.append(current_row)
        return result

    def set(self, row, column, value):
        index = (row, column)
        if index not in self._entry:
            return
        e = self._entry[index]
        text = str(value)
        e.delete(0, END)
        e.insert(0, text)
        pass

    def _validate(self, P):
        '''Perform input validation. 

        Allow only an empty value, or a value that can be converted to a float
        '''
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True