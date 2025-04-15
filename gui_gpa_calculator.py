from customtkinter import *
from tkinter import messagebox

global grades
grades = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0
}


class Gpa_calculator(CTk):
    def __init__(self):
        super().__init__()
        self.title('GPA Calculator')
        self.geometry('700x500+200+100')
        self.minsize(600, 400)

        self.main_frame = CTkScrollableFrame(
            self,
            fg_color='black',
            scrollbar_button_color='#875cf5',
            scrollbar_fg_color='black',
            label_text='Welcome to GPA Calculator',
            label_fg_color='#875cf5',
            label_font=('Helvetica', 18),
            scrollbar_button_hover_color='#35235c',
            corner_radius=15,
            border_width=2,
            border_color='#875cf5'
        )
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.semesters = []

        self.create_widgets()

    def create_widgets(self):
        self.buttons_frame = CTkFrame(self.main_frame, fg_color='black')
        self.buttons_frame.pack(pady=5, fill=X)

        for i in range(3):
            self.buttons_frame.columnconfigure(i, weight=1)

        self.info_button = CTkButton(
            self.buttons_frame,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='About the Grades',
            hover_color='blue',
            corner_radius=15,
            command=self.info_func
        )
        self.info_button.grid(row=0, column=0, padx=10)

        self.add_semester_button = CTkButton(
            self.buttons_frame,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='Add Semester',
            hover_color='blue',
            corner_radius=15,
            command=self.add_semester
        )
        self.add_semester_button.grid(row=0, column=1, padx=10)

        self.change_grades_button = CTkButton(
            self.buttons_frame,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='Change Grades Points',
            hover_color='blue',
            corner_radius=15,
            command=self.change_grades
        )
        self.change_grades_button.grid(row=0, column=2, padx=10)


        self.overall_gpa_label = CTkLabel(
            self.main_frame,
            text='Overall GPA: 0.00',
            font=('Helvetica', 16)
        )
        self.overall_gpa_label.pack(pady=5)

   
        self.semester_frame = CTkFrame(self.main_frame, fg_color='black')
        self.semester_frame.pack(fill='both', expand=True)

    def add_semester(self):

        semester_frame = SemesterFrame(self.semester_frame, self.update_overall_gpa)
        semester_frame.pack(fill=X, pady=5)
        self.semesters.append(semester_frame)
        semester_frame.add_course()

    def update_overall_gpa(self):
        total_semester_gpa = 0
        count_semesters = 0
        for semester in self.semesters:
            qp, ch = semester.calculate_gpa()
            semester_gpa = qp / ch if ch > 0 else 0
            total_semester_gpa += semester_gpa
            count_semesters += 1

        overall_gpa = total_semester_gpa / count_semesters if count_semesters > 0 else 0
        self.overall_gpa_label.configure(text=f'Overall GPA: {overall_gpa:.2f}')
        return overall_gpa

    def change_grades(self):
        change_window = CTkToplevel(self)
        change_window.title('Change the Grades')
        change_window.geometry('300x500')

        change_frame = CTkFrame(change_window, fg_color='black')
        change_frame.pack(fill='both', expand=True, padx=5, pady=5)

        entries = {}
        for i, (grade, point) in enumerate(grades.items()):
            label = CTkLabel(change_frame, text=f'{grade}: ', fg_color='black')
            label.grid(row=i, column=0, pady=5, padx=5)

            entry = CTkEntry(
                change_frame,
                placeholder_text=f'{point}',
                corner_radius=15,
                border_width=2,
                border_color='#875cf5'
            )
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[grade] = entry

        def save_changes():
            global grades
            for grade, entry in entries.items():
                new_value = entry.get()
                if new_value:
                    try:
                        new_value = float(new_value)
                        grades[grade] = new_value
                    except ValueError:
                        messagebox.showerror('Invalid input', f'Please enter a valid value for {grade}')
                        return
            change_window.destroy()

        save_button = CTkButton(
            change_frame,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='Save Changes',
            hover_color='blue',
            corner_radius=15,
            command=save_changes
        )
        save_button.grid(row=len(grades), column=1, pady=10)
        change_window.grab_set()

    def info_func(self):
        grade_info = '\n'.join([f'* {grade} : {points:.1f}' for grade, points in grades.items()])
        messagebox.showinfo('About the Grades', f'Quality points are:\n\n{grade_info}')


class SemesterFrame(CTkFrame):
    def __init__(self, parent, overall_gpa_callback):
        super().__init__(parent, fg_color='black')
        self.overall_gpa_callback = overall_gpa_callback
        self.courses = [] 

        self.header_frame = CTkFrame(self, fg_color='black')
        self.header_frame.pack(fill=X, pady=5)
        self.delete_button = CTkButton(
            self.header_frame,
            fg_color='transparent',
            border_width=2,
            border_color='red',
            text='Delete Semester',
            hover_color='red',
            corner_radius=15,
            command=self.delete_semester
        )
        self.delete_button.pack(side=RIGHT, padx=10, pady=5)

        self.course_frame = CTkFrame(self, fg_color='black')
        self.course_frame.pack(fill=X, pady=5)

        self.add_course_button = CTkButton(
            self,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='Add Course',
            hover_color='blue',
            corner_radius=15,
            command=self.add_course
        )
        self.add_course_button.pack(pady=5)

        self.calculate_gpa_button = CTkButton(
            self,
            fg_color='transparent',
            border_width=2,
            border_color='blue',
            text='Calculate Semester GPA',
            hover_color='blue',
            corner_radius=15,
            command=self.update_gpa
        )
        self.calculate_gpa_button.pack(pady=5)

        self.gpa_label = CTkLabel(self, text='Total Credit Hours: 0 , Semester GPA: 0.00 , Overall GPA: 0.00')
        self.gpa_label.pack(pady=5)

    def delete_semester(self):
        self.pack_forget()
        self.destroy()

    def add_course(self):
        course_frame = CourseFrame(self.course_frame, self.update_gpa)
        course_frame.pack(fill=X, pady=3)
        self.courses.append(course_frame)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def update_gpa(self):
        quality_points, credit_hours = self.calculate_gpa()
        semester_gpa = quality_points / credit_hours if credit_hours > 0 else 0

        overall_gpa = self.overall_gpa_callback()
        self.gpa_label.configure(
            text=f'Total Credit Hours: {credit_hours} , Semester GPA: {semester_gpa:.2f} ,Overall GPA: {overall_gpa:.2f}'
        )

    def calculate_gpa(self):
        total_credit_hours = 0
        total_quality_points = 0
        for course in self.courses:
            qp, ch = course.get_course_data()
            total_credit_hours += ch
            total_quality_points += qp
        return total_quality_points, total_credit_hours


class CourseFrame(CTkFrame):
    def __init__(self, parent, update_gpa_callback):
        super().__init__(parent, fg_color='black')
        self.update_gpa_callback = update_gpa_callback

        self.rowconfigure(0, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=1)

        self.course_name_entry = CTkEntry(
            self,
            placeholder_text='Course Name (Optional)',
            corner_radius=15,
            border_width=2,
            border_color='#875cf5'
        )
        self.course_name_entry.grid(row=0, column=0, padx=5, pady=5)

        self.credit_hours_entry = CTkEntry(
            self,
            placeholder_text='Number of Credit Hours',
            corner_radius=15,
            border_width=2,
            border_color='#875cf5'
        )
        self.credit_hours_entry.grid(row=0, column=1, padx=5, pady=5)

        self.grade_box = CTkComboBox(
            self,
            values=list(grades.keys()),
            border_color='#875cf5',
            dropdown_hover_color='#35235c',
            button_color='#875cf5',
            button_hover_color='#35235c',
            corner_radius=10,
            state='readonly'
        )
        self.grade_box.grid(row=0, column=2, padx=5, pady=5)

        self.del_button = CTkButton(
            self,
            fg_color='transparent',
            border_color='red',
            border_width=2,
            hover_color='red',
            corner_radius=15,
            text='Delete',
            command=self.delete_course
        )
        self.del_button.grid(row=0, column=3, padx=5, pady=5)

    def delete_course(self):
        self.master.master.remove_course(self)
        self.pack_forget()
        self.destroy()
        self.update_gpa_callback()

    def get_course_data(self):
        try:
            hours = float(self.credit_hours_entry.get())
            grade = self.grade_box.get()
            grade_points = grades.get(grade, 0)
            quality_points = grade_points * hours
        except ValueError:
            hours = 0
            quality_points = 0
        return quality_points, hours


if __name__ == '__main__':
    root = Gpa_calculator()
    root.mainloop()
